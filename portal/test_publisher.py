import contextlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from scripts import publish

class PublisherTests(unittest.TestCase):
 def test_cross_machine_document_identity_and_private_preferences(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);config=root/'portal.json';config.write_text(json.dumps({'server':'https://portal.test','token':'test-token'}));config.chmod(0o600)
   source=root/'report.html';source.write_text('<meta name="nota-documento" content="stable-report"><p>Contenido</p>');aid='a'*32
   calls=[]
   def request(base,token,path,data=None,method=None):
    calls.append((path,data,method))
    if path=='/api/session':return {'user':{'id':'owner','verified':True}}
    if path.startswith('/api/artifacts?'):return {'artifacts':[{'id':aid,'owner':'owner','document_id':'stable-report'}]}
    return {'id':aid,'version':'version-2','url':base+'/a/'+aid,'visibility':'private'}
   argv=['publish.py','--config',str(config),'publicar','--archivo',str(source),'--titulo','Informe']
   with patch('sys.argv',argv),patch.object(publish,'request',side_effect=request),contextlib.redirect_stdout(io.StringIO()):publish.main()
   self.assertEqual(calls[-1][0],'/api/artifacts/'+aid+'/versions');self.assertNotIn('visibility',calls[-1][1]);self.assertEqual((root/'publications.json').stat().st_mode&0o077,0)
   with patch('sys.argv',['publish.py','--config',str(config),'preferencias','--publicar-al-crear','si']),contextlib.redirect_stdout(io.StringIO()):publish.main()
   self.assertTrue(json.loads(config.read_text())['publish_on_create']);self.assertEqual(json.loads(config.read_text())['token'],'test-token')
   output=io.StringIO()
   with patch('sys.argv',['publish.py','--config',str(config),'estado']),patch.object(publish,'request',side_effect=request),contextlib.redirect_stdout(output):publish.main()
   self.assertTrue(json.loads(output.getvalue())['publish_on_create']);self.assertNotIn('test-token',output.getvalue())
 def test_ambiguous_document_needs_explicit_id(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp);config=root/'portal.json';config.write_text(json.dumps({'server':'https://portal.test','token':'test'}));config.chmod(0o600)
   source=root/'report.html';source.write_text('<meta name="nota-documento" content="stable-report">')
   with patch('sys.argv',['publish.py','--config',str(config),'publicar','--archivo',str(source),'--titulo','Informe']),patch.object(publish,'request',side_effect=[{'user':{'id':'owner'}},{'artifacts':[{'id':'a'*32,'owner':'owner','document_id':'stable-report'},{'id':'b'*32,'owner':'owner','document_id':'stable-report'}]}]),self.assertRaisesRegex(SystemExit,'varios artefactos'):publish.main()

if __name__=='__main__':unittest.main()

class ProvenanceTests(unittest.TestCase):
 def test_real_session_inference_does_not_mix_agents(self):
  from scripts.publish import source_defaults
  with patch.dict('os.environ',{'CODEX_THREAD_ID':'codex-real'},clear=True):
   self.assertEqual(source_defaults('',''),('Codex','codex-real'))
   self.assertEqual(source_defaults('Hermes',''),('Hermes',''))
   self.assertEqual(source_defaults('Codex','explicit'),('Codex','explicit'))
  with patch.dict('os.environ',{'CODEX_THREAD_ID':'a','HERMES_SESSION_ID':'b'},clear=True):
   self.assertEqual(source_defaults('',''),('',''))
   self.assertEqual(source_defaults('Hermes',''),('Hermes','b'))

class FeedbackCommandTests(unittest.TestCase):
 def test_cli_exports_permission_scoped_context_without_sending(self):
  with tempfile.TemporaryDirectory() as temporary:
   root=Path(temporary);config=root/'portal.json'
   config.write_text(json.dumps({'server':'https://portal.test','token':'fixture-token'}));config.chmod(0o600)
   response={'text':'Review context', 'items':[{'context':{'source':{'agent':'codex','session':'fixture-session'},'artifact':'a'*32,'version':'v1'},'text':'Review this quote'}]}
   output=io.StringIO()
   with patch('sys.argv',['publish.py','--config',str(config),'feedback','--artifact-id','a'*32,'--output',str(root/'handoff')]),patch.object(publish,'request',return_value=response) as request,contextlib.redirect_stdout(output):
    publish.main()
   self.assertEqual(request.call_args.args[2],'/api/review/export?artifact='+'a'*32+'&scope=open&kind=all')
   self.assertEqual(json.loads((root/'handoff/context.json').read_text())['items'],response['items'])
   self.assertFalse(json.loads(output.getvalue())['executed'])
   self.assertNotIn('fixture-token',output.getvalue())
