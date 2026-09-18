#!/usr/bin/env python3
"""Compone una o varias páginas con los controles obligatorios. Sin instalaciones ni red."""
import argparse,json
from pathlib import Path
from contract_artifact import build,THEMES,STYLES,MODES
from brands import BRANDS

def main():
 p=argparse.ArgumentParser(description=__doc__);group=p.add_mutually_exclusive_group(required=True);group.add_argument('--content','--contenido',dest='contenido',type=Path);group.add_argument('--config',type=Path)
 p.add_argument('--theme','--tema',dest='tema',choices=THEMES);p.add_argument('--mode','--modo',dest='modo',choices=MODES);p.add_argument('--typography','--estilo',dest='estilo',choices=STYLES)
 p.add_argument('--brand','--marca',dest='marca',choices=[*BRANDS,'bottifact'],help='Identidad y logo del documento; por defecto se infiere de un tema de marca.')
 p.add_argument('--document-id','--documento-id',dest='documento_id');p.add_argument('--title','--titulo',dest='titulo');p.add_argument('--description','--descripcion',dest='descripcion',default='');p.add_argument('--output','--salida',dest='salida',required=True,type=Path);args=p.parse_args()
 try:
  if args.config:
   config=json.loads(args.config.read_text());title=config['titulo'];description=config.get('descripcion','');pages=[{**page,'html':(args.config.parent/page['contenido']).read_text()} for page in config['paginas']]
  else:
   if not args.titulo:p.error('--titulo es obligatorio con --contenido')
   title=args.titulo;description=args.descripcion;pages=[{'id':'contenido','titulo':title,'html':args.contenido.read_text()}]
  sources=([args.config]+[args.config.parent/page['contenido'] for page in config['paginas']]) if args.config else [args.contenido]
  if args.salida.resolve() in [path.resolve() for path in sources]:raise ValueError('La salida no puede sobrescribir las fuentes de contenido.')
  result=build(title,pages,description,mode=args.modo or (config.get('modo') if args.config else None),theme=args.tema or (config.get('tema') if args.config else None),style=args.estilo or (config.get('estilo') if args.config else None),document_id=args.documento_id or (config.get('documento_id') if args.config else None),marca=args.marca or (config.get('marca') if args.config else None))
  args.salida.parent.mkdir(parents=True,exist_ok=True);args.salida.write_text(result)
  print(str(args.salida)+': base estándar verificada; '+str(len(pages))+' página(s). Probar a 320/390 px y en navegador antes de compartir.')
 except (ValueError,KeyError,TypeError,OSError) as error:p.exit(1,str(error)+'\n')
if __name__=='__main__':main()
