#!/usr/bin/env python3
"""Inventario compacto o una receta completa; no carga todos los HTML al agente."""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--id');args=p.parse_args()
items=json.loads((Path(__file__).resolve().parents[1]/'packages/core/registry/registry.json').read_text())['componentes']
if args.id:
 aliases=json.loads((Path(__file__).resolve().parents[1]/'packages/core/registry/component-aliases.json').read_text())
 found=next((r for r in items if r['id']==args.id or aliases.get(r['id'])==args.id),None)
 if not found:p.error('Componente desconocido: '+args.id)
 print(json.dumps(found,ensure_ascii=False,indent=2))
else:
 for r in items:print(r['capitulo']+' | '+r['id']+' | '+r['nombre']+' | '+', '.join(r['dependencias']))
