#!/usr/bin/env python3
"""Paquete portable de este skill, sin historia, capturas ni otras instalaciones."""
from pathlib import Path
import hashlib,json,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1]

def package():
 # Lista por extensiones y carpetas explícitas. No empaqueta archivos privados desconocidos.
 files=[]
 for p in ROOT.iterdir():
  if p.is_file() and not p.is_symlink() and p.suffix in {'.md','.css','.js','.json','.html'}:files.append(p)
 for folder in ['scripts','ejemplos','assets','agents','licencias']:
  if not (ROOT/folder).exists():continue
  for p in (ROOT/folder).rglob('*'):
   if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and p.suffix in {'.py','.js','.cjs','.html','.json','.md','.yaml','.woff2','.mp3','.svg','.txt'}:files.append(p)
 # Procedencia y resultados textuales, sin imágenes de sesiones ni vídeos.
 for p in (ROOT/'auditoria').iterdir():
  if p.is_file() and p.suffix in {'.md','.json'}:files.append(p)
 files=sorted(set(files));blobs={str(p.relative_to(ROOT)):p.read_bytes() for p in files}
 blobs.pop('MANIFIESTO.json',None)
 version=json.loads(blobs['VERSION.json'])['version']
 manifest={'formato':'nota-tikin-portable','version':version,'archivos':{n:hashlib.sha256(b).hexdigest() for n,b in blobs.items()}}
 blobs['MANIFIESTO.json']=(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n').encode()
 out=ROOT/'descargas';out.mkdir(exist_ok=True);target=out/'nota-tikin-portable.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,b in sorted(blobs.items()):
   info=zipfile.ZipInfo('nota-tikin/'+n,date_time=(2026,9,15,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,b)
 sha=hashlib.sha256(target.read_bytes()).hexdigest();(out/'nota-tikin-portable.sha256').write_text(sha+'  '+target.name+'\n')
 print(str(target)+': '+str(len(files))+' archivos, '+str(target.stat().st_size)+' bytes; SHA-256 '+sha)
 return target
if __name__=='__main__':package()
