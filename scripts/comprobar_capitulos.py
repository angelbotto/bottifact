#!/usr/bin/env python3
"""Paletas y edición multipágina en Orca, sin instalar paquetes."""
import argparse,base64,io,json,datetime
from pathlib import Path
from pypdf import PdfReader
from comprobar_navegador import call,evaluate,file,save
p=argparse.ArgumentParser();p.add_argument('--base',default='http://127.0.0.1:8768');args=p.parse_args();base=args.base.rstrip('/')
def fresh(path):call('goto','--url','about:blank');call('goto','--url',base+'/'+path)
def settle():evaluate('new Promise(r=>setTimeout(()=>r(true),150))');call('screenshot')
def snapshot(name):Path('auditoria/capturas/'+name+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
fresh('informe.html');call('exec','--command','set viewport 1639 939');settle()
header=evaluate('({scrollY,top:document.querySelector(".edicion-cabecera").getBoundingClientRect().top})');assert header['scrollY']==0,header
r=file('pruebas_capitulos.js');save('capitulos-interaccion.json',r);print(r,flush=True);assert not r['failed']
# Hash después de una carga nueva, no navegación sólo dentro del DOM existente.
fresh('informe.html#prototipo');settle();assert evaluate('document.querySelector(".pagina.viva").id')=='prototipo'
records=[]
for width,height in [(320,740),(390,844),(1639,939)]:
 call('exec','--command',f'set viewport {width} {height}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for page in ['resumen','evidencia','prototipo','siguientes']:
   evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector("[data-ir='+page+']").click();scrollTo({top:0,behavior:"instant"});true')
   data=evaluate('''(()=>{
    const active=document.querySelector('.pagina.viva'),text=active.querySelector('.bajada').getBoundingClientRect(),figure=active.querySelector('.ancho,.amplio')?.getBoundingClientRect();
    const boxes=[...document.querySelectorAll('.barra,.tabla-caja,.grafica-caja,.pestanas-caja,.visor-caja')].filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect(),before=e.scrollLeft;e.scrollLeft=e.scrollWidth;const end=e.scrollLeft;e.scrollLeft=before;return {class:e.className,width:e.clientWidth,content:e.scrollWidth,end,inside:r.left>=-.5&&r.right<=innerWidth+.5,focus:e.tabIndex,name:e.getAttribute('aria-label')};});
    const m=document.querySelector('[data-apariencia-menu]');if(!m.open)m.querySelector('summary').click();dispatchEvent(new Event('resize'));const p=m.querySelector('.apariencia-panel'),r=p.getBoundingClientRect();p.scrollTop=p.scrollHeight;const end=p.scrollTop;m.open=false;
    return {viewport:[innerWidth,innerHeight],theme:document.documentElement.dataset.theme,page:active.id,documentWidth:document.documentElement.scrollWidth,text:text.width,figure:figure?.width,center:figure?Math.abs(text.left+text.width/2-figure.left-figure.width/2):null,boxes,
     menu:{inside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,end,scroll:p.scrollHeight},errors:[...document.querySelectorAll('[data-error-grafica],[data-error-reporte],[data-error-visor],[data-error-pestanas]')].map(e=>e.textContent)};
   })()''')
   records.append(data);save('capitulos-pantallas.json',records)
   assert data['documentWidth']==width and not data['errors'],data
   assert all(b['inside'] and b['focus']==0 and b['name'] and (b['content']<=b['width']+1 or b['end']>0) for b in data['boxes']),data
   assert data['menu']['inside'],data
   if data.get('figure') is not None:assert data['figure']>=data['text'] and data['center']<1,data
  print(width,theme,'4 capítulos sin cortes',flush=True)
# Capturas de las tres paletas nuevas y del capítulo de evidencia.
for name,theme,page,w,h in [('informe-oliva','oliva','resumen',1639,939),('informe-arcilla','arcilla','evidencia',390,844),('informe-ciruela','ciruela','prototipo',1639,939)]:
 call('exec','--command',f'set viewport {w} {h}');evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector("[data-ir='+page+']").click();scrollTo({top:0,behavior:"instant"});true');snapshot(name)
# Contraste de todos los componentes del catálogo, con esquema del SO claro y oscuro.
fresh('plantilla.html');contrasts=[]
for media in ['light','dark']:
 call('exec','--command','set media '+media)
 for width,height in [(320,740),(390,844),(1639,939)]:
  call('exec','--command',f'set viewport {width} {height}')
  for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
   evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true');data=file('medir_navegador.js')
   assert data['documentWidth']==width and not data['errors'] and not data['svgTextOverflow'],data
   assert all(c['ratio']>=c['minimum'] for c in data['contrasts']),data['contrasts']
   contrasts.append({'media':media,'viewport':data['viewport'],'theme':theme,'documentWidth':data['documentWidth'],'contrasts':data['contrasts'],'svgTextOverflow':data['svgTextOverflow']});save('capitulos-paletas.json',contrasts)
 print('Contrastes y ancho, preferencia de sistema',media,'correctos',flush=True)
# No sobrescribir evidencia anterior: el mismo paquete de regresiones sobre el servidor nuevo.
r=file('pruebas_segunda_tanda.js');save('capitulos-regresion.json',r);assert not r['failed'],r
import pruebas_regresiones as legacy
legacy.call=lambda *a:call(*(x.replace('http://127.0.0.1:8766',base) for x in a))
legacy.save=lambda name,value:save('capitulos-base.json',value)
old=legacy.run();print(len(old),'regresiones de base pasan',flush=True)
fresh('informe.html#prototipo');call('exec','--command','set media reduced-motion');call('screenshot')
assert evaluate('[...document.querySelectorAll(".barra button,.pestanas-nav button")].every(e=>getComputedStyle(e).transitionDuration.split(",").every(t=>parseFloat(t)===0))')
pdf=call('pdf');reader=PdfReader(io.BytesIO(base64.b64decode(pdf['data'])))
text=' '.join(p.extract_text() or '' for p in reader.pages)
required=['Confirmar sin repetir','Qué sabemos','Recorrer la propuesta','La siguiente prueba','Qué necesitamos observar','Qué no se puede concluir','Estados del ejemplo']
found={s:s in text for s in required};assert all(found.values()),found
save('capitulos-salida.json',{'pages':len(reader.pages),'activeAtPrint':'prototipo','required':found,'restored':evaluate('document.querySelector(".pagina.viva").id')=='prototipo','reducedTransitions':True})
save('capitulos-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base':base,'browser':evaluate('navigator.userAgent'),'pageCombinations':len(records),'paletteCombinations':len(contrasts),'initialHeader':header,'limitations':['Foco y teclado probados por DOM y eventos explícitos; no teclado físico/lector de pantalla.','Viewport emulado, no hardware móvil. PDF extraído con pypdf; no impresión física.']})
call('exec','--command','set media light')
print('Edición, paletas, base y PDF correctos',flush=True)
