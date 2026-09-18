#!/usr/bin/env python3
"""Instala una copia portable verificada. Un destino existente requiere --actualizar."""
import argparse,shutil,tempfile,datetime,os
from pathlib import Path
from verify_package import verify

def install(source,destination,update=False):
 source=source.resolve();destination=Path(os.path.abspath(destination.expanduser()))
 # No se puede mover/respaldar una carpeta que contiene la fuente o sus padres.
 if source==destination or source.is_relative_to(destination) or destination.is_relative_to(source):raise ValueError('El destino debe estar fuera de la carpeta del paquete.')
 manifest=verify(source)
 existing=destination.exists() or destination.is_symlink()
 if existing and not update:raise ValueError('El destino ya existe. Para conservar una copia anterior y actualizar, añade --actualizar.')
 destination.parent.mkdir(parents=True,exist_ok=True)
 stage=Path(tempfile.mkdtemp(prefix='.bottifact-instalacion-',dir=destination.parent));backup=None
 try:
  for name in [*manifest['archivos'],*[n for n in ['manifest.json','MANIFIESTO.json'] if (source/n).exists()]]:
   target=stage/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source/name,target)
  verify(stage)
  if existing:
   # Fuera de skills para que los agentes no descubran dos versiones de la misma biblioteca.
   backups=destination.parent.parent/'bottifact-respaldos';backups.mkdir(parents=True,exist_ok=True)
   backup=backups/(destination.name+'-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
   destination.rename(backup)
  try:stage.rename(destination)
  except BaseException:
   if backup:backup.rename(destination)
   raise
 finally:
  if stage.exists():shutil.rmtree(stage)
 return destination,backup
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--destination','--destino',dest='destino',type=Path,required=True);p.add_argument('--update','--actualizar',dest='actualizar',action='store_true');args=p.parse_args()
 try:
  dest,backup=install(Path(__file__).resolve().parents[1],args.destino,args.actualizar)
  print('Instalado y verificado: '+str(dest))
  if backup:print('Versión anterior conservada: '+str(backup))
  print('Abre una conversación nueva y pide usar bottifact. La carga del agente se comprueba en este equipo.')
 except (ValueError,KeyError,OSError) as e:p.exit(1,str(e)+'\n')
