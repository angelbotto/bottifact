#!/usr/bin/env python3
"""Contratos de datos, interacción local, geometría y temas de las ocho piezas."""
import json,base64
from check_browser import call,evaluate,file,save,ROOT
URL='http://127.0.0.1:8768/examples/generated/evidence.html'
call('goto','--url',URL);call('exec','--command','set viewport 1440 960');call('screenshot')
tests=file('tests_evidence.js');save('evidencia-pruebas.json',tests)
assert not tests['failed'],tests
print(str(tests['passed'])+' comprobaciones de datos, interacción y ciclo de vida correctas.',flush=True)
call('goto','--url',URL)
measurements=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela','liftit','blueprint','hacker']:
  evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
  row=evaluate('''(()=>{const roots=[...document.querySelectorAll('[data-evidencia]')];const texts=[];
   roots.forEach(e=>e.querySelectorAll('.evidencia-visor svg').forEach(s=>{const v=s.viewBox.baseVal;for(const t of s.querySelectorAll('text')){const b=t.getBBox();if(b.x < -1||b.y < -1||b.x+b.width>v.width+1||b.y+b.height>v.height+1)texts.push({type:e.dataset.evidencia,text:t.textContent,b:{x:b.x,y:b.y,w:b.width,h:b.height},v:{w:v.width,h:v.height}});}}));
   return {viewport:[innerWidth,innerHeight],theme:document.documentElement.dataset.theme,overflow:document.documentElement.scrollWidth>innerWidth,texts,regions:roots.flatMap(e=>[...e.querySelectorAll('.evidencia-visor,.tabla-caja')].map(c=>{const before=c.scrollLeft;c.scrollLeft=c.scrollWidth;const end=c.scrollLeft;c.scrollLeft=before;return {kind:e.dataset.evidencia,width:c.clientWidth,content:c.scrollWidth,end,focus:c.tabIndex===0,named:!!c.getAttribute('aria-label'),overflow:getComputedStyle(c).overflowX};}))};})()''')
  assert not row['overflow'] and not row['texts'],row
  assert all(r['focus'] and r['named'] and (r['content']<=r['width']+1 or (r['end']>0 and r['overflow']=='auto')) for r in row['regions']),row
  measurements.append(row)
 print(str(w)+' px: nueve temas, texto SVG dentro y desplazamiento local.',flush=True)
save('evidencia-geometria.json',measurements)
call('exec','--command','set viewport 1440 960');evaluate('document.documentElement.dataset.theme="dark";true')
for kind in ['sankey','cohortes','sensibilidad','gantt','embudo','incertidumbre','imagen','relato']:
 evaluate('document.querySelector(\'[data-evidencia="'+kind+'"]\').scrollIntoView({block:"start",behavior:"instant"});scrollBy(0,-100);true')
 shot=call('screenshot');(ROOT/'tests/screenshots'/('evidencia-'+kind+'.png')).write_bytes(base64.b64decode(shot['data']))
call('exec','--command','set media reduced-motion');call('screenshot')
reduce=evaluate('({matches:matchMedia("(prefers-reduced-motion:reduce)").matches,animations:[...document.querySelectorAll("[data-evidencia]")].reduce((n,e)=>n+e.getAnimations({subtree:true}).length,0)})')
assert reduce['matches'] and reduce['animations']==0,reduce
save('evidencia-movimiento.json',reduce);call('exec','--command','set media light')
print('Movimiento reducido sin animaciones de las piezas nuevas.',flush=True)
