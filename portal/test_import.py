import json, os, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
from portal.app import create_app, COOKIE
from portal.import_archive import import_archive

class ImportTests(unittest.TestCase):
    def test_private_idempotent_import_preserves_links_attachments_and_hides_old_bookmark(self):
        with tempfile.TemporaryDirectory() as tmp, patch.dict(os.environ,{'BOTTIFACT_ADMIN_EMAILS':'owner@example.com'}):
            root=Path(tmp);app=create_app(str(root/'data'),origin='https://portal.test');store=app.state.store
            owner=store.user('owner@example.com','Owner');c=TestClient(app,base_url='https://portal.test');c.cookies.set(COOKIE,store.session(owner['id']))
            (root/'a.html').write_text('<!doctype html><html><head><title>Reporte</title></head><body><h1>Informe</h1><a href="b.html#dato">Detalle</a><a href="datos.csv">CSV</a></body></html>')
            (root/'b.html').write_text('<h1 id="dato">Detalle</h1>');(root/'datos.csv').write_text('total\n12')
            entries=[{'source':'archive:a','file':str(root/'a.html'),'title':'Informe','space':'Prueba','legacy_url':'https://old.test/a/','attachments':{'datos.csv':str(root/'datos.csv')}},{'source':'archive:b','file':str(root/'b.html'),'title':'Detalle','space':'Prueba'}]
            with store.db() as db:db.execute('INSERT INTO bookmarks VALUES(?,?,?,?,?,?)',('old',owner['id'],'Anterior','https://old.test/a/','Prueba',0))
            results=import_archive(store,entries);aid,bid=[r['id'] for r in results]
            self.assertTrue(all(r['status']=='imported' for r in results))
            again=import_archive(store,entries);self.assertTrue(all(r['status']=='existing' for r in again))
            listed=c.get('/api/artifacts').json()['artifacts'];self.assertEqual(len(listed),2);self.assertTrue(all(a['visibility']=='private' for a in listed));self.assertTrue(all(not a.get('external') for a in listed))
            content=c.get('/api/artifacts/'+aid+'/render').text
            self.assertIn('/a/'+bid+'#dato',content);self.assertIn('window.BottifactArchiveLinks',content)
            path='/api/artifacts/'+aid+'/attachments/'+results[0]['version']+'/datos.csv'
            self.assertIn(path,content);self.assertEqual(c.get(path).text,'total\n12')
            anonymous=TestClient(app,base_url='https://portal.test');self.assertEqual(anonymous.get(path).status_code,404)
            with store.db() as db:self.assertEqual(db.execute('SELECT count(*) FROM versions').fetchone()[0],2)
            (root/'a.html').write_text('<h1>Revisión</h1>');updated=import_archive(store,entries)
            self.assertEqual(updated[0]['id'],aid);self.assertNotEqual(updated[0]['version'],results[0]['version'])
            self.assertEqual(c.get(path).status_code,200)

if __name__=='__main__':unittest.main()
