#!/usr/bin/env python3
"""Compone una o varias páginas con los controles obligatorios. Sin instalaciones ni red."""
import argparse,json
from pathlib import Path
from contrato_artefacto import build

def main():
 p=argparse.ArgumentParser(description=__doc__);group=p.add_mutually_exclusive_group(required=True);group.add_argument('--contenido',type=Path);group.add_argument('--config',type=Path)
 p.add_argument('--titulo');p.add_argument('--descripcion',default='');p.add_argument('--salida',required=True,type=Path);args=p.parse_args()
 try:
  if args.config:
   config=json.loads(args.config.read_text());title=config['titulo'];description=config.get('descripcion','');pages=[{**page,'html':(args.config.parent/page['contenido']).read_text()} for page in config['paginas']]
  else:
   if not args.titulo:p.error('--titulo es obligatorio con --contenido')
   title=args.titulo;description=args.descripcion;pages=[{'id':'contenido','titulo':title,'html':args.contenido.read_text()}]
  sources=([args.config]+[args.config.parent/page['contenido'] for page in config['paginas']]) if args.config else [args.contenido]
  if args.salida.resolve() in [path.resolve() for path in sources]:raise ValueError('La salida no puede sobrescribir las fuentes de contenido.')
  result=build(title,pages,description)
  args.salida.parent.mkdir(parents=True,exist_ok=True);args.salida.write_text(result)
  print(str(args.salida)+': base estándar verificada; '+str(len(pages))+' página(s). Probar a 320/390 px y en navegador antes de compartir.')
 except (ValueError,KeyError,TypeError,OSError) as error:p.exit(1,str(error)+'\n')
if __name__=='__main__':main()
