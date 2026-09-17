import tempfile, unittest
from fastapi.testclient import TestClient
from portal.app import create_app, COOKIE

ORIGIN='https://portal.test'
def html(doc,text):return '<meta name="nota-documento" content="'+doc+'"><h1>Informe</h1><p>'+text+'</p><script>const excluded="palabrasecreta"</script>'

class LibraryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.app=create_app(self.tmp.name,origin=ORIGIN);self.store=self.app.state.store
  self.owner=self.client('owner@example.com');self.other=self.client('reader@example.com')
 def tearDown(self):self.tmp.cleanup()
 def client(self,email):
  c=TestClient(self.app,base_url=ORIGIN,headers={'Origin':ORIGIN});u=self.store.user(email,email);c.cookies.set(COOKIE,self.store.session(u['id']));return c
 def publish(self,title,text='Texto',doc='informe'):
  r=self.owner.post('/api/artifacts',json={'title':title,'space':'Tikin','html':html(doc,text)});self.assertEqual(r.status_code,200,r.text);return r.json()
 def test_content_search_diacritics_privacy_rename_and_revision(self):
  a=self.publish('Estado','Conciliación financiera: facturación extraordinaria.');path='/api/artifacts/'+a['id']
  for q in ['conciliacion','FACTURACION','finan','Estado','Tikin']:
   result=self.owner.get('/api/artifacts',params={'q':q}).json();self.assertEqual(result['total'],1);self.assertEqual(result['artifacts'][0]['id'],a['id'])
   self.assertEqual(self.other.get('/api/artifacts',params={'q':q}).json()['total'],0)
  for q in ['palabrasecreta','" OR - : *']:
   self.assertEqual(self.owner.get('/api/artifacts',params={'q':q}).status_code,200)
  self.assertEqual(self.owner.get('/api/artifacts?q=palabrasecreta').json()['total'],0)
  before=self.owner.get(path).json();self.assertEqual(self.other.patch(path,json={'title':'Mal','space':'Otro'}).status_code,404)
  self.assertEqual(self.owner.patch(path,json={'title':'Cierre trimestral','space':'Finanzas'}).status_code,200)
  after=self.owner.get(path).json();self.assertEqual(before['versions'],after['versions']);self.assertEqual(self.owner.get('/api/artifacts?q=trimestral').json()['total'],1)
  self.assertEqual(self.owner.get('/api/artifacts?q=Estado').json()['total'],0)
  revision=self.owner.post(path+'/versions',json={'title':'Cierre trimestral','space':'Finanzas','html':html('informe','Nuevas proyecciones')});self.assertEqual(revision.status_code,200)
  self.assertEqual(self.owner.get('/api/artifacts?q=conciliacion').json()['total'],0);self.assertEqual(self.owner.get('/api/artifacts?q=proyecciones').json()['total'],1)
 def test_cursor_continuity_filters_and_insert_before_cursor(self):
  ids=[self.publish('Reporte '+str(i).zfill(2),doc='doc-'+str(i))['id'] for i in range(19)]
  p={'sort':'title','limit':7,'space':'Tikin'};first=self.owner.get('/api/artifacts',params=p).json();self.assertEqual(len(first['artifacts']),7)
  added=self.publish('AAAA nuevo',doc='new')['id'];seen=[a['id'] for a in first['artifacts']];cursor=first['next_cursor']
  while cursor:
   r=self.owner.get('/api/artifacts',params={**p,'cursor':cursor}).json();seen.extend(a['id'] for a in r['artifacts']);cursor=r['next_cursor']
  self.assertEqual(set(seen),set(ids));self.assertEqual(len(seen),19);self.assertNotIn(added,seen)
  self.assertEqual(self.owner.get('/api/artifacts',params={**p,'cursor':first['next_cursor'],'q':'otro'}).status_code,422)
  self.assertEqual(self.owner.get('/api/artifacts?limit=0').status_code,422)
  self.assertEqual(self.other.get('/api/artifacts',params={**p,'cursor':first['next_cursor']}).json()['artifacts'],[])
 def test_shared_reader_sees_current_version_only_and_revocation_hides_search(self):
  a=self.publish('Historia','Dato histórico');path='/api/artifacts/'+a['id'];old=a['version']
  self.owner.post(path+'/versions',json={'title':'Historia','html':html('informe','Cifra actual')})
  self.owner.put(path+'/access',json={'visibility':'invited','comments':'reviewers','guests':False,'grants':[{'email':'reader@example.com','role':'viewer'}]})
  self.assertEqual(len(self.other.get(path).json()['versions']),1);self.assertEqual(len(self.owner.get(path).json()['versions']),2)
  self.assertEqual(self.other.get(path+'/render?version='+old).status_code,404)
  self.assertEqual(self.other.get('/api/artifacts?q=actual').json()['total'],1)
  self.owner.put(path+'/access',json={'visibility':'private','grants':[]})
  self.assertEqual(self.other.get('/api/artifacts?q=actual').json()['total'],0)
  self.assertEqual(self.other.get(path+'/preview').status_code,404)

if __name__=='__main__':unittest.main()
