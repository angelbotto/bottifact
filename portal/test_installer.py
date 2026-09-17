import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('bottifact_updater',ROOT/'scripts/actualizar.py')
updater=importlib.util.module_from_spec(spec);spec.loader.exec_module(updater)

class InstallerTests(unittest.TestCase):
    def archive(self,version):
        files={'registro.json':b'{}','VERSION.json':json.dumps({'version':version}).encode(),'SKILL.md':b'---\nname: bottifact\ndescription: Test\n---\n'}
        for name in ['instalar.py','verificar_paquete.py']:files['scripts/'+name]=(ROOT/'scripts'/name).read_bytes()
        files['MANIFIESTO.json']=json.dumps({'formato':'bottifact-portable','version':version,'archivos':{k:hashlib.sha256(v).hexdigest() for k,v in files.items()}}).encode()
        out=io.BytesIO()
        with zipfile.ZipFile(out,'w') as z:
            for name,blob in files.items():z.writestr('bottifact/'+name,blob)
        return out.getvalue()

    def test_download_install_update_backup_and_git_guard(self):
        with tempfile.TemporaryDirectory() as temporary:
            dest=Path(temporary)/'stable/library'
            for version in ['first','second']:
                data=self.archive(version)
                def fetch(path,limit):return data if path.endswith('.zip') else (hashlib.sha256(data).hexdigest()+'  package.zip').encode()
                with patch.object(updater,'fetch',fetch),patch.object(sys,'argv',['install','--destino',str(dest),'--sin-enlaces']):updater.main()
                self.assertEqual(json.loads((dest/'VERSION.json').read_text())['version'],version)
            backups=list((Path(temporary)/'bottifact-respaldos').glob('library-*'))
            self.assertEqual(len(backups),1);self.assertEqual(json.loads((backups[0]/'VERSION.json').read_text())['version'],'first')
            (dest/'.git').mkdir()
            with patch.object(sys,'argv',['install','--destino',str(dest),'--sin-enlaces']):
                with self.assertRaises(ValueError):updater.main()

    def test_corrupt_and_traversal_packages_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            data=self.archive('test')
            with self.assertRaises(ValueError):updater.extract(data,'0'*64,Path(temporary))
            out=io.BytesIO()
            with zipfile.ZipFile(out,'w') as z:z.writestr('bottifact/../../escape','no')
            data=out.getvalue()
            with self.assertRaises(ValueError):updater.extract(data,hashlib.sha256(data).hexdigest(),Path(temporary))

if __name__=='__main__':unittest.main()
