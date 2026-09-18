"""Índice por capítulo y regla: seguimiento, alcance y espacio reservado en Orca."""
import json,base64,datetime
from pathlib import Path
from check_browser import call,evaluate,file,save
URL='http://127.0.0.1:8768/examples/generated/library.html'
def settle():call('screenshot')
call('goto','--url','about:blank');call('goto','--url',URL);call('exec','--command','set media reduced-motion');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)');settle()
r=evaluate('''(()=>{const results=[],assert=(v,m)=>{if(!v)throw Error(m)},test=(name,fn)=>{try{fn();results.push({name,ok:true})}catch(e){results.push({name,ok:false,error:e.message})}},ruler=document.querySelector('.regla'),go=id=>document.querySelector('[data-ir='+id+']').click(),refresh=()=>dispatchEvent(new Event('scroll'));
 test('Un índice por capítulo y una regla',()=>{assert(document.querySelectorAll('.pagina > .indice').length===9,'índices');assert(document.querySelectorAll('.regla').length===1,'reglas');for(const a of document.querySelectorAll('.pagina .indice a'))assert(a.closest('.pagina').contains(document.getElementById(a.hash.slice(1))),'destino fuera de capítulo');});
 test('Sección actual y anteriores avanzan al desplazar',()=>{go('graficas');document.getElementById('receta-calor').scrollIntoView({behavior:'instant',block:'start'});refresh();assert(document.querySelector('.pagina.viva .indice [aria-current]').hash==='#receta-calor','actual');assert(document.querySelectorAll('.pagina.viva .aqui-visto').length===5,'anteriores');});
 test('Home/End alcanzan 0 y 100 del capítulo',()=>{ruler.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true}));refresh();assert(ruler.getAttribute('aria-valuenow')==='0','Home');ruler.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));refresh();assert(ruler.getAttribute('aria-valuenow')==='100','End');assert(Math.abs(document.querySelector('.pagina.viva').getBoundingClientRect().bottom-innerHeight)<2,'incluye paginación o pie');});
 test('Cambio de capítulo reinicia regla y limpia marcas ocultas',()=>{go('tablas');refresh();assert(ruler.getAttribute('aria-valuenow')==='0','no reinicia');assert(ruler.getAttribute('aria-controls')==='tablas','capítulo');assert(!document.querySelector('.pagina[hidden] .indice [aria-current]'),'marca oculta');});
 test('Enlace de índice mantiene hash y foco del destino',()=>{document.querySelector('.pagina.viva .indice a[href="#receta-sparkline"]').click();refresh();assert(location.hash==='#receta-sparkline'&&document.activeElement.id==='receta-sparkline','enlace');assert(document.querySelector('.pagina.viva .indice [aria-current]').hash==='#receta-sparkline','marca');});
 return {results,failed:results.filter(r=>!r.ok).length};})()''');save('lectura-interaccion.json',r);assert not r['failed'],r;print(r,flush=True)
records=[]
for w,h in [(320,740),(390,844),(1199,900),(1200,900),(1440,960),(1639,939)]:
 call('exec','--command',f'set viewport {w} {h}');settle()
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  r=evaluate('''(()=>{document.documentElement.dataset.theme=THEME;return [...document.querySelectorAll('.barra [data-ir]')].map(b=>{b.click();dispatchEvent(new Event('scroll'));const p=document.querySelector('.pagina.viva'),index=p.querySelector('.indice'),ruler=document.querySelector('.regla'),a=index.getBoundingClientRect(),r=ruler.getBoundingClientRect(),wide=[...p.querySelectorAll(':scope > .ancho,:scope > .amplio')].map(e=>e.getBoundingClientRect());return {page:p.id,w:innerWidth,h:innerHeight,theme:THEME,documentWidth:document.documentElement.scrollWidth,indexFixed:getComputedStyle(index).position==='fixed',indexInside:a.left>=0&&a.right<=innerWidth,indexFocusable:index.tabIndex===0,rulerInside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,orientation:ruler.getAttribute('aria-orientation'),noOverlap:innerWidth<1200||wide.every(f=>a.right+16<=f.left&&f.right+16<=r.left),percent:Number(ruler.getAttribute('aria-valuenow'))};});})()'''.replace('THEME',json.dumps(theme)))
  for row in r:
   assert row['documentWidth']==w and row['indexInside'] and row['indexFocusable'] and row['rulerInside'] and row['noOverlap'],row
   assert row['indexFixed']==(w>=1200) and row['orientation']==('vertical' if w>=1200 else 'horizontal'),row
  records.extend(r)
 print(w,'seis paletas y nueve capítulos sin solapamientos',flush=True)
save('lectura-pantallas.json',records)
# En móvil, clic horizontal (no coordenada vertical) y regla accesible por teclado.
call('exec','--command','set viewport 390 844');evaluate('document.querySelector("[data-ir=graficas]").click();true');settle()
r=evaluate('''(()=>{const e=document.querySelector('.regla'),r=e.getBoundingClientRect();e.dispatchEvent(new MouseEvent('click',{bubbles:true,clientX:r.left+r.width/2,clientY:r.top+2}));dispatchEvent(new Event('scroll'));return {value:Number(e.getAttribute('aria-valuenow')),orientation:e.getAttribute('aria-orientation')};})()''');assert 49<=r['value']<=51 and r['orientation']=='horizontal',r;save('lectura-movil.json',r)
# Legado: el seguimiento y la regla anteriores siguen pasando sus contratos.
call('goto','--url','http://127.0.0.1:8768/examples/generated/template.html');checks=file('tests_components.js');save('lectura-regresion.json',checks);assert not checks['failed'],checks
call('exec','--command','set media light');call('goto','--url',URL+'#receta-calor');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>{document.querySelector("[data-elegir-tema][value=light]").click();document.getElementById("receta-calor").scrollIntoView({behavior:"instant",block:"start"});return true;})');settle();Path('tests/screenshots/lectura-1440.png').write_bytes(base64.b64decode(call('screenshot')['data']))
call('exec','--command','set viewport 390 844');evaluate('document.querySelector("[data-ir=graficas]").click();scrollTo({top:0,behavior:"instant"});true');settle();Path('tests/screenshots/lectura-390.png').write_bytes(base64.b64decode(call('screenshot')['data']))
save('lectura-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'combinaciones':len(records),'method':'Orca viewport, DOM, scroll y teclado sintético; preferencia reducida emulada para comprobar actualizaciones sin animación. No lector de pantalla ni hardware móvil.'})
print('Lectura guiada verificada',flush=True)
