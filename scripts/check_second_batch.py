#!/usr/bin/env python3
"""Verificación reproducible de la segunda tanda mediante Orca, sin instalar paquetes."""
from pathlib import Path
import argparse, json, datetime
from check_browser import call, evaluate, file, save

ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8768/examples/generated/template.html');args=p.parse_args()
 call('goto','--url',args.url)
 evaluate('document.fonts.ready.then(()=>true)')
 tests=file('tests_second_batch.js');save('segunda-componentes.json',tests)
 print(f"Segunda tanda: {tests['passed']} pasan, {tests['failed']} fallan",flush=True)
 assert not tests['failed'],tests
 call('goto','--url',args.url)
 old=file('tests_components.js');save('segunda-base.json',old)
 print(f"Base: {old['passed']} pasan, {old['failed']} fallan",flush=True)
 assert not old['failed'],old
 call('goto','--url',args.url)
 records=[]
 for width,height in [(320,740),(390,844),(1639,939)]:
  call('exec','--command',f'set viewport {width} {height}')
  for theme in ['light','dark','sea']:
   for comfortable in [False,True]:
    evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.documentElement.toggleAttribute("data-lectura-comoda",'+str(comfortable).lower()+');true')
    data=file('measure_browser.js')
    extra=evaluate('''(() => {
      const region=document.querySelector('.visor-caja');const prev=region.scrollLeft;region.scrollLeft=region.scrollWidth;
      const end=region.scrollLeft;region.scrollLeft=prev;
      const r=region.getBoundingClientRect();
      const controls=[...document.querySelectorAll('.apariencia,.pieza .acciones,.escenario-form')].map(e=>({name:e.className,width:e.clientWidth,scroll:e.scrollWidth}));
      const errors=[...document.querySelectorAll('[data-error-reporte],[data-error-visor]')].map(e=>e.textContent);
      const body=getComputedStyle(document.body);
      return {comfortable:document.documentElement.hasAttribute('data-lectura-comoda'),font:body.fontSize,lineHeight:body.lineHeight,controls,errors,
        viewer:{width:region.clientWidth,content:region.scrollWidth,end,inside:r.left>=0&&r.right<=innerWidth,focus:region.tabIndex,name:region.getAttribute('aria-label')}};
    })()''')
    data.update(extra);records.append(data);save('segunda-navegador.json',records)
    assert data['documentWidth']==width,(theme,width,'desbordamiento del documento')
    assert not data['errors'] and not data['svgTextOverflow'],data
    assert all(c['ratio']>=c['minimum'] for c in data['contrasts']),data['contrasts']
    assert all(c['scroll']<=c['width']+1 for c in data['controls']),data['controls']
    for region in data['regions']:
     assert region['inside'] and region['focus']==0 and region['name'],region
     if region['content']>region['width']+1:assert region['end']>0 and region['overflow'] in ['auto','scroll'],region
    v=data['viewer'];assert v['inside'] and v['focus']==0 and v['name'],v
    if v['content']>v['width']+1:assert v['end']>0,v
    print(f'{width} × {height}, {theme}, cómoda={comfortable}: sin cortes, escala y contraste base correctos',flush=True)
 save('segunda-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':args.url,'browser':evaluate('navigator.userAgent'),'combinations':len(records),'physicalKeyboard':False,'hardwarePhone':False})
