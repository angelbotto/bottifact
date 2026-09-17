import unittest
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from portal.app import create_app, COOKIE
from portal.search import extract_text

class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.app=create_app(Path(self.tmp.name),origin='https://portal.test');self.store=self.app.state.store
        self.owner=self.client('owner@example.com');self.other=self.client('other@example.com')
    def tearDown(self):self.tmp.cleanup()
    def client(self,email):
        c=TestClient(self.app,base_url='https://portal.test',headers={'Origin':'https://portal.test'});u=self.store.user(email,email);c.cookies.set(COOKIE,self.store.session(u['id']));return c
    def publish(self,c,title='Flota y rutas',body='Entregas y despacho de logística',**kw):
        r=c.post('/api/artifacts',json={'title':title,'html':'<meta name="nota-documento" content="test"><main><h1>'+title+'</h1><p>'+body+'</p></main>',**kw});self.assertEqual(r.status_code,200,r.text);return r.json()
    def test_graph_never_exposes_private_nodes_drafts_notes_or_provenance_to_readers(self):
        a=self.publish(self.owner,source={'agent':'Codex','session':'session-secret','device':'MacBook personal'})
        b=self.publish(self.owner,title='Despacho y rutas')
        self.publish(self.other,title='Flota privada ajena')
        data=self.owner.get('/api/artifacts?graph=1').json();self.assertEqual(len(data['nodes']),2);self.assertEqual(len(data['edges']),1)
        path='/api/artifacts/'+a['id'];self.owner.put(path+'/access',json={'visibility':'invited','grants':[{'email':'other@example.com','role':'viewer'}]})
        self.owner.post(path+'/versions',json={'title':'Presupuesto confidencial','html':'<meta name="nota-documento" content="test"><p>Finanzas ingresos margen secreto</p>','mode':'draft'})
        data=self.other.get('/api/artifacts?graph=1').json();self.assertNotIn(b['id'],str(data));self.assertNotIn('session-secret',str(data));self.assertNotIn('MacBook personal',str(data));self.assertNotIn('confidencial',str(data))
        self.assertNotIn('session-secret',str(self.other.get(path).json()))
        self.assertEqual(self.other.get('/api/artifacts?q=session-secret').json()['total'],0)
        self.assertEqual(self.owner.get('/api/artifacts?q=MacBook').json()['total'],1)
    def test_classification_is_explained_and_manual_override_survives_revisions(self):
        a=self.publish(self.owner);path='/api/artifacts/'+a['id'];data=self.owner.get(path).json()
        self.assertEqual(data['category'],'Operaciones');self.assertIn('logística',data['auto_tags']);self.assertTrue(data['classification'][0]['evidence'])
        r=self.owner.patch(path+'/organization',json={'category':'Mi dirección','automatic':False,'tags':['prioridad'],'collections':['Semana 3']});self.assertEqual(r.status_code,200)
        self.owner.post(path+'/versions',json={'title':'Finanzas','html':'<meta name="nota-documento" content="test"><p>Ingresos margen costos</p>'})
        data=self.owner.get(path).json();self.assertEqual(data['category'],'Mi dirección');self.assertEqual(data['auto_tags'],[]);self.assertEqual(data['tags'],['prioridad'])
        self.assertEqual(self.owner.get('/api/artifacts?category=Mi%20direcci%C3%B3n&tag=prioridad').json()['total'],1)
        self.assertEqual(self.owner.get('/api/artifacts?q=Semana').json()['total'],1)
        self.assertNotEqual(self.other.patch(path+'/organization',json={'category':'Robo'}).status_code,200)
        self.owner.patch(path+'/organization',json={'category':'','automatic':True});self.assertEqual(self.owner.get(path).json()['category'],'Finanzas')
    def test_search_excludes_chrome_and_ranks_title(self):
        self.assertEqual(extract_text('<title>ruido</title><header>menú</header><div class="apariencia-panel"><div>Tu espacio</div><label>Sonido</label></div><main><p>Contenido</p><br><p>Final</p></main>'),'Contenido Final')
        a=self.publish(self.owner,'Flota','Texto de prueba');self.publish(self.owner,'Otro documento','Una flota secundaria')
        rows=self.owner.get('/api/artifacts?q=flota&sort=relevance&limit=1').json();self.assertEqual(rows['artifacts'][0]['id'],a['id'])
        self.assertIsNotNone(rows['next_cursor'])
        changed=self.owner.get('/api/artifacts',params={'q':'flota','sort':'relevance','limit':1,'category':'Finanzas','cursor':rows['next_cursor']});self.assertEqual(changed.status_code,422)
    def test_version_device_is_preserved_in_feedback_prompt(self):
        a=self.publish(self.owner,source={'agent':'Hermes','session':'sess-123','device':'MacBook'})
        self.owner.post('/api/artifacts/'+a['id']+'/review',json={'id':'note','kind':'create','entry_type':'note','version':a['version'],'text':'Revisar','anchor':{'reference':'x','text':'Entregas','quote':'Entregas','page':'Flota','x':.5,'y':.5}})
        text=self.owner.get('/api/review/export').json()['text'];self.assertIn('Dispositivo de creación: MacBook',text);self.assertIn('sess-123',text)
