"""Gráficas nuevas y regresión de laterales; navegador Orca, sin dependencias."""
import json,base64,datetime
from pathlib import Path
from check_browser import call,evaluate,file,save
URL='http://127.0.0.1:8768/examples/generated/library.html'
def settle():call('screenshot')
def fresh():call('goto','--url','about:blank');call('goto','--url',URL)
fresh();call('exec','--command','set media reduced-motion');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>{document.querySelectorAll("[data-analitica] details").forEach(d=>d.open=true);return true})');settle()
r=file('tests_analytics.js');save('analitica-interaccion.json',r);print(r,flush=True);assert not r['failed'],r
records=[]
for w,h in [(320,740),(390,844),(1200,700),(1440,960),(2048,730),(2560,900)]:
 call('exec','--command',f'set viewport {w} {h}');settle()
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for page in ['graficas','expresion']:
   evaluate(f'document.documentElement.dataset.theme={json.dumps(theme)};document.querySelector("[data-ir={page}]").click();scrollTo({{top:0,behavior:"instant"}});dispatchEvent(new Event("scroll"));true')
   row=evaluate('''(()=>{const bar=document.querySelector('.barra').getBoundingClientRect(),index=document.querySelector('.pagina.viva .indice').getBoundingClientRect(),ruler=document.querySelector('.regla'),r=ruler.getBoundingClientRect(),value=ruler.querySelector('.val').getBoundingClientRect(),cursor=ruler.querySelector('.cursor').getBoundingClientRect();return {w:innerWidth,h:innerHeight,page:document.querySelector('.pagina.viva').id,theme:document.documentElement.dataset.theme,documentWidth:document.documentElement.scrollWidth,belowHeader:innerWidth<1200||(index.top>=bar.bottom+20&&r.top>=bar.bottom+20),rulerInside:r.top>=0&&r.bottom<=innerHeight,indexInside:index.bottom<=innerHeight,valueInside:value.left>=r.left&&value.right<=r.right&&value.top>=r.top&&value.bottom<=r.bottom,valueSeparate:innerWidth<1200||value.right+4<=cursor.left,regions:[...document.querySelectorAll('.pagina.viva .analitica-caja,.pagina.viva .escena-caja,.pagina.viva .tabla-caja')].map(e=>({width:e.clientWidth,scroll:e.scrollWidth,named:!!e.getAttribute('aria-label'),focus:e.tabIndex===0}))};})()''')
   assert row['documentWidth']==w and row['belowHeader'] and row['rulerInside'] and row['valueInside'] and row['valueSeparate'],row
   if w>=1200:assert row['indexInside'],row
   for region in row['regions']:
    assert region['named'] and region['focus'],region
    if w<=390:assert region['scroll']>region['width'],region
   records.append(row)
 print(w,'cabecera, laterales y regiones: seis paletas, dos capítulos',flush=True)
save('analitica-pantallas.json',records)
# Progreso intermedio/final: porcentaje completo y tick relleno acotado.
call('exec','--command','set viewport 2048 730');evaluate('document.querySelector("[data-ir=graficas]").click();true');settle()
for value in [0,24,100]:
 r=evaluate('''(()=>{const e=document.querySelector('.regla');e.setAttribute('aria-valuenow',VALUE);e.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));dispatchEvent(new Event('scroll'));const v=e.querySelector('.val').getBoundingClientRect(),c=e.querySelector('.cursor').getBoundingClientRect();return {value:+e.getAttribute('aria-valuenow'),separate:v.right+4<=c.left,clip:getComputedStyle(e.querySelector('.ticks'),'::after').clipPath};})()'''.replace('VALUE',str(max(-1,value-1))))
 assert r['value']==value and r['separate'] and r['clip']!='none',r
save('analitica-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cases':len(records),'interacciones':len(file('tests_analytics.js')['results']),'method':'Orca: viewport, DOM, coordenadas SVG/Three, clics/teclado sintéticos; sin lector de pantalla ni dispositivo móvil físico.'})
print('Analítica verificada',flush=True)
