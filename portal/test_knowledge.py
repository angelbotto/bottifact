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
    def test_membership_network_explains_company_and_topics_without_private_leaks(self):
        a=self.publish(self.owner,title='Liftit operations',space='Liftit')
        b=self.publish(self.owner,title='Financial brief',space='Tikin',body='Finanzas ingresos margen')
        secret=self.publish(self.other,title='Private company',space='Secret company')
        self.owner.patch('/api/artifacts/'+a['id']+'/organization',json={'tags':['planificación'],'collections':['Q4']})
        self.owner.patch('/api/artifacts/'+b['id']+'/organization',json={'tags':['planificación'],'collections':[]})
        network=self.owner.get('/api/artifacts?graph=1').json()['network']
        kinds={n['kind'] for n in network['nodes']};self.assertEqual(kinds,{'artifact','space','topic','collection'})
        topic=next(n for n in network['nodes'] if n['title']=='planificación');self.assertEqual(topic['count'],2)
        self.assertEqual(len([e for e in network['edges'] if e['target']==topic['id']]),2)
        self.assertTrue(all(e['reason'] for e in network['edges']))
        self.assertNotIn('Secret company',str(network));self.assertNotIn(secret['id'],str(network))
        filtered=self.owner.get('/api/artifacts?graph=1&space=Liftit').json()['network'];self.assertNotIn(b['id'],str(filtered))
    def test_global_sort_directions_and_cursor_scope(self):
        for title,space in [('Alpha','Zeta'),('Beta','Alpha'),('Gamma','Beta')]:self.publish(self.owner,title=title,space=space)
        for sort in ('title','space','category','agent','recent','comments'):
            first=self.owner.get('/api/artifacts',params={'sort':sort,'direction':'desc','limit':1}).json()
            seen=[first['artifacts'][0]['id']];cursor=first['next_cursor']
            while cursor:
                result=self.owner.get('/api/artifacts',params={'sort':sort,'direction':'desc','limit':1,'cursor':cursor}).json();seen.extend(a['id'] for a in result['artifacts']);cursor=result['next_cursor']
            self.assertEqual(len(seen),3);self.assertEqual(len(set(seen)),3)
        result=self.owner.get('/api/artifacts?sort=title&direction=desc').json();self.assertEqual([a['title'] for a in result['artifacts']],['Gamma','Beta','Alpha'])
        first=self.owner.get('/api/artifacts?sort=title&direction=desc&limit=1').json()
        self.assertEqual(self.owner.get('/api/artifacts',params={'sort':'title','direction':'asc','limit':1,'cursor':first['next_cursor']}).status_code,422)
    def test_agent_filter_does_not_expose_reader_origin(self):
        a=self.publish(self.owner,source={'agent':'Hermes','session':'private-session'})
        self.owner.put('/api/artifacts/'+a['id']+'/access',json={'visibility':'invited','grants':[{'email':'other@example.com','role':'viewer'}]})
        self.assertEqual(self.owner.get('/api/artifacts?agent=hermes').json()['total'],1)
        self.assertEqual(self.other.get('/api/artifacts?agent=Hermes').json()['total'],0)
        self.assertEqual(self.owner.get('/api/artifacts').json()['agents'],['Hermes'])
        self.assertEqual(self.other.get('/api/artifacts').json()['agents'],[])
