"""Regresiones de tooltip, navegación y piezas editoriales con Orca."""
import base64,json,argparse
from pathlib import Path
from comprobar_navegador import call,evaluate,save
parser=argparse.ArgumentParser();parser.add_argument('--mapa',action='store_true');args=parser.parse_args()
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/biblioteca.html');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)')
checks=evaluate('''(async()=>{const results=[],assert=(b,m)=>{if(!b)throw Error(m)},wait=ms=>new Promise(r=>setTimeout(r,ms)),test=async(name,f)=>{try{await f();results.push({name,ok:true})}catch(e){results.push({name,ok:false,error:e.message})}},go=id=>document.querySelector('.catalogo-indice a[href="#receta-'+id+'"]').click();
 await test('Inventario vigente, ocho piezas nuevas y navegación con nueve destinos',()=>{assert(document.querySelectorAll('.receta-copia code').length===Number(document.querySelector('.pie-colofon span').textContent.match(/[0-9]+/)[0]),'recetas');assert(document.querySelectorAll('.barra [data-ir]').length===9,'capítulos');assert(document.querySelectorAll('.barra .nav-separador').length===8,'separadores');});
 go('atencion');await wait(160);const e=document.querySelector('[data-atencion]'),map=NotaAtencion.get(e),b=map.controls.querySelector('button');
 await test('tooltip muestra valor, proporción, total y contexto de la tabla',()=>{b.click();const t=map.tooltip;assert(!t.hidden&&t.textContent.includes('125 horas')&&t.textContent.includes('212 horas')&&t.textContent.includes('cuatro semanas ficticias'),'detalle');assert(b.getAttribute('aria-describedby')===t.id,'relación');assert(map.chart.querySelectorAll('foreignObject').length>=3,'etiquetas grandes sustituidas por redondeo');assert(!t.querySelector('img,script'),'texto seguro');});
 await test('Escape descarta tooltip sin reabrirlo en el mismo objetivo',()=>{document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}));map.showTip(0,b);assert(map.tooltip.hidden,'escape');});
 await test('foco y permanencia sobre tooltip',async()=>{map.dismissed=null;b.focus({preventScroll:true});b.dispatchEvent(new FocusEvent('focusin',{bubbles:true}));assert(!map.tooltip.hidden,'foco');await wait(250);map.showTip(0,b);map.deferHide();map.tooltip.dispatchEvent(new PointerEvent('pointerenter'));await wait(220);assert(!map.tooltip.hidden,'hover persistente');document.dispatchEvent(new Event('scroll'));assert(!map.tooltip.hidden,'foco tras desplazamiento');map.showTip(0,map.chart.querySelector('g'));document.dispatchEvent(new Event('scroll'));assert(map.tooltip.hidden,'scroll de puntero');});
 await test('destroy retira tooltip y permite reiniciar sin duplicar',()=>{const id=map.tooltip.id;map.destroy();assert(!document.getElementById(id)&&e.querySelector('table'),'limpieza');NotaAtencion.init(e);NotaAtencion.init(e);assert(e.querySelectorAll('.atencion-caja').length===1,'instancia');});
 await test('borrador valida vacío y copia exactamente texto con contexto',async()=>{go('invitacion');const e=document.querySelector('[data-invitacion]'),m=NotaInvitacion.get(e),b=e.querySelector('button'),input=e.querySelector('textarea');b.click();assert(!input.validity.valid,'vacío');input.value='Una idea <script>literal</script> para revisar';input.dispatchEvent(new Event('input'));const original=navigator.clipboard.writeText;let copied;try{navigator.clipboard.writeText=async text=>{copied=text};b.click();await wait(40);assert(copied.includes(input.value)&&copied.includes('#invitacion-idea')&&copied.includes(document.title),'copia con contexto');assert(!e.querySelector('script'),'sin inyección');}finally{navigator.clipboard.writeText=original;}m.destroy();NotaInvitacion.init(e);assert(NotaInvitacion.get(e)!==m,'reinicio');});
 await test('listas conservan voces y estados semánticos',()=>{assert(document.querySelectorAll('.lista-estados .sr-only').length===4,'estados');assert(document.querySelectorAll('.conversacion strong').length===4,'voces');assert(document.querySelectorAll('.estanteria > li').length===3,'estantería');});
 return {results,failed:results.filter(r=>!r.ok).length};})()''');save('editorial-interaccion.json',checks);print(checks,flush=True);assert not checks['failed'],checks
records=[]
for width,height in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {width} {height}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for key in (['atencion'] if args.mapa else ['atencion','cards-trazadas','estanteria','invitacion','lista-estados','lista-proyectos','conversacion','navegacion','pie-editorial','marco']):
   evaluate('document.querySelector("[data-elegir-tema][value='+theme+']").click();document.querySelector(\'.catalogo-indice a[href="#receta-'+key+'"]\').click();true')
   r=evaluate('''(()=>{const e=document.querySelector('.pagina.viva'),nav=document.querySelector('.navegacion-scroll');let tip=null;if(e.id==='graficas'){const m=NotaAtencion.get(document.querySelector('[data-atencion]'));m.controls.lastElementChild.click();const b=m.tooltip.getBoundingClientRect();tip={left:b.left,right:b.right,top:b.top,bottom:b.bottom,hidden:m.tooltip.hidden};}return {width:innerWidth,document:document.documentElement.scrollWidth,nav:{width:nav.clientWidth,scroll:nav.scrollWidth,name:nav.getAttribute('aria-label'),focus:nav.tabIndex},tip,cover:[...e.querySelectorAll('.estante-portada')].map(n=>({width:n.clientWidth,scroll:n.scrollWidth})),frames:[...e.querySelectorAll('.marco-difuso')].map(n=>{const r=n.getBoundingClientRect();return {left:r.left,right:r.right,mask:getComputedStyle(n,':before').maskImage}})}})()''')
   assert r['width']==r['document']==width,(width,theme,key,r)
   assert r['nav']['name'] and r['nav']['focus']==0,r
   assert all(c['scroll']<=c['width']+1 for c in r['cover']),r
   assert all(f['left']>=0 and f['right']<=width+.5 and f['mask']!='none' for f in r['frames']),r
   if r['tip']:assert not r['tip']['hidden'] and r['tip']['left']>=0 and r['tip']['right']<=width and r['tip']['top']>=0 and r['tip']['bottom']<=height,r
   records.append({'width':width,'theme':theme,'piece':key,**r})
  print(width,theme,'piezas, marcos y tooltip dentro del viewport',flush=True)
 save('editorial-mapa-pantallas.json' if args.mapa else 'editorial-pantallas.json',records)
evaluate('document.querySelector("[data-invitacion] textarea").value="";document.querySelector("[data-invitacion] [role=status]").textContent="Borrador local; copia antes de cerrar.";true')
# Selección de capítulos fuera del área visible en móvil, foco y menú de apariencia.
call('exec','--command','set viewport 320 740')
r=evaluate('''(()=>{document.querySelector('[data-ir=configuracion]').click();const e=document.querySelector('[data-ir=configuracion]'),n=document.querySelector('.navegacion-scroll'),r=e.getBoundingClientRect(),c=n.getBoundingClientRect();return {left:r.left,right:r.right,boxLeft:c.left,boxRight:c.right,scroll:n.scrollLeft,current:e.getAttribute('aria-current')}})()''');assert r['left']>=r['boxLeft']-1 and r['right']<=r['boxRight']+1 and r['current']=='page',r;save('editorial-navegacion.json',r)
for key in ['cards-trazadas','atencion','estanteria','invitacion','lista-estados','pie-editorial']:
 call('exec','--command','set viewport 1440 960');evaluate('document.querySelector("[data-elegir-tema][value=dark]").click();document.querySelector(\'.catalogo-indice a[href="#receta-'+key+'"]\').click();true');evaluate('new Promise(r=>setTimeout(()=>r(true),220))')
 if key=='atencion':evaluate('(()=>{const m=NotaAtencion.get(document.querySelector("[data-atencion]")),g=m.chart.querySelector("g"),r=g.getBoundingClientRect();m.showTip(0,g,r.left+250,r.top+160);return true})()')
 call('screenshot');Path('auditoria/capturas/editorial-'+key+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
print('Editorial: contratos y '+str(len(records))+' combinaciones verificadas.',flush=True)
