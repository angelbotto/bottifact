"""Capturas de revisión visual y comprobación final del ruler legado."""
from pathlib import Path
import base64
from check_browser import call,evaluate,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/examples/generated/library.html');call('exec','--command','set media reduced-motion');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)')
for key in ['calendario','torta','areas','caja','velas','mapa-rutas','mapa-burbujas','columnas-mapa','arcos-mapa','almacen']:
 evaluate('document.documentElement.dataset.theme="light";document.querySelector("a[href=\\"#receta-'+key+'\\"]").click();true');call('screenshot')
 Path('tests/screenshots/analitica-'+key+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
call('exec','--command','set viewport 1639 730');evaluate('document.documentElement.dataset.theme="dark";document.querySelector("[data-ir=graficas]").click();scrollTo({top:0,behavior:"instant"});dispatchEvent(new Event("scroll"));true');call('screenshot');Path('tests/screenshots/analitica-cabecera-1639.png').write_bytes(base64.b64decode(call('screenshot')['data']))
call('exec','--command','set viewport 390 844');evaluate('document.querySelector("a[href=\\"#receta-torta\\"]").click();true');call('screenshot');Path('tests/screenshots/analitica-torta-390.png').write_bytes(base64.b64decode(call('screenshot')['data']))
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/examples/generated/template.html');call('exec','--command','set viewport 1639 939');call('screenshot')
r=evaluate('''(()=>{const e=document.querySelector('.regla');return [0,24,100].map(n=>{e.style.setProperty('--lectura',n/100);e.querySelector('.val').textContent=n+'%';const a=e.getBoundingClientRect(),b=e.querySelector('.val').getBoundingClientRect(),c=e.querySelector('.cursor').getBoundingClientRect();return {value:n,inside:b.left>=a.left&&b.right<=a.right&&b.top>=a.top&&b.bottom<=a.bottom,separate:b.right+4<=c.left,colored:getComputedStyle(e.querySelector('.ticks'),'::after').clipPath!=='none'};});})()''');assert all(x['inside'] and x['separate'] and x['colored'] for x in r),r;save('analitica-regla-legado.json',r)
print('Doce capturas y regla heredada verificadas')
