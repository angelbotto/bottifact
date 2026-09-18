#!/usr/bin/env python3
"""Pruebas optativas con el navegador de Orca. Iniciar scripts/serve.py antes.
No instala dependencias. Usa sólo el CLI público y guarda evidencia en tests/evidence/.
"""
from pathlib import Path
import argparse, json, subprocess, datetime

ROOT=Path(__file__).resolve().parents[1]
def call(*args):
 p=subprocess.run(['orca',*args,'--json'],capture_output=True,text=True,check=False)
 result=json.loads(p.stdout)
 if not result.get('ok'):raise RuntimeError(result.get('error'))
 return result['result']
def evaluate(expression):
 raw=call('eval','--expression',expression)['result']
 try:return json.loads(raw)
 except (json.JSONDecodeError,TypeError):return raw
def file(name):return evaluate((ROOT/'scripts'/name).read_text())
def save(name,value):(ROOT/'tests/evidence'/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8766/examples/generated/template.html');args=parser.parse_args()
 call('goto','--url',args.url)
 checks=file('tests_components.js');save('componentes.json',checks)
 print(f"Componentes: {checks['passed']} pasan, {checks['failed']} fallan",flush=True)
 assert not checks['failed'],checks
 audio=file('tests_audio.js');save('audio.json',audio)
 assert all(r['ok'] for r in audio.get('results',[])),audio
 print('Audio offline: '+str(audio),flush=True)
 # Recarga para descartar todas las modificaciones de las pruebas unitarias.
 call('goto','--url',args.url)
 measurements=[]
 for width,height in [(320,740),(390,844),(1639,939)]:
  call('exec','--command',f'set viewport {width} {height}')
  for theme in ['light','dark','sea']:
   evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
   data=file('measure_browser.js');measurements.append(data);save('navegador.json',measurements)
   assert data['documentWidth']==width,(theme,width,'desbordamiento')
   assert not data['errors'] and not data['svgTextOverflow'],data
   for region in data['regions']:
    assert region['inside'] and region['focus']==0 and region['name'],region
    if region['content']>region['width']+1:assert region['end']>0 and region['overflow'] in ['auto','scroll'],region
   assert all(c['ratio']>=c['minimum'] for c in data['contrasts']),data['contrasts']
   print(f'{width} × {height}, {theme}: anchos, desplazamiento, rótulos y contraste correctos',flush=True)
 save('ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':args.url,'browser':evaluate('navigator.userAgent'),'static':'python3 scripts/validate.py se ejecuta por separado','limitations':['No acredita audición manual ni gesto físico de activación del audio.','Context loss se ensaya con eventos sintéticos; fallback sin Three sí construye una instancia sin la dependencia.','Foco comprobado por DOM/CSS; no equivale a una sesión con lector de pantalla.']})
