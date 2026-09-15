#!/usr/bin/env python3
"""Verificación optativa de biblioteca en Orca; no instala paquetes."""
import argparse,json,datetime,base64,io
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save
p=argparse.ArgumentParser();p.add_argument('--base',default='http://127.0.0.1:8768');base=p.parse_args().base.rstrip('/')
def fresh(path):call('goto','--url','about:blank');call('goto','--url',base+'/'+path)
def settle():evaluate('new Promise(r=>setTimeout(()=>r(true),120))');call('screenshot')
fresh('biblioteca.html');call('exec','--command','set viewport 390 844');settle()
checks=evaluate('''(async()=>{
 const results=[],assert=(x,m)=>{if(!x)throw Error(m)},test=async(name,fn)=>{try{await fn();results.push({name,ok:true})}catch(e){results.push({name,ok:false,error:e.message})}},wait=()=>new Promise(r=>setTimeout(r,100));
 await test('71 recetas y nueve capítulos',()=>{assert(document.querySelectorAll('.pagina').length===9,'capítulos');assert(document.querySelectorAll('.receta-copia code').length===71,'recetas');});
 await test('búsqueda de recetas y salto entre capítulos',()=>{const input=document.querySelector('#biblioteca-buscar');input.value='distribución';input.dispatchEvent(new Event('input'));const shown=[...document.querySelectorAll('.catalogo-indice li')].filter(e=>!e.hidden);assert(shown.length===1,'búsqueda acentuada');shown[0].querySelector('a').click();assert(document.querySelector('.pagina.viva').id==='graficas','capítulo');assert(location.hash==='#receta-distribucion','URL');assert(document.activeElement.id==='receta-distribucion','foco');});
 await test('Atrás y Adelante con receta profunda',async()=>{document.querySelector('[data-ir=publicaciones]').click();history.back();await wait();assert(document.querySelector('.pagina.viva').id==='graficas'&&location.hash==='#receta-distribucion','atrás');history.forward();await wait();assert(document.querySelector('.pagina.viva').id==='publicaciones','adelante');});
 const archive=document.querySelector('[data-archivo]'),form=archive.querySelector('form'),visible=()=>[...archive.querySelectorAll('[data-publicacion]')].filter(e=>!e.hidden);
 await test('archivo combina texto sin acentos y tema',()=>{form.elements.buscar.value='hipotesis';form.dispatchEvent(new Event('input'));assert(visible().length===1,'texto');form.elements.tema.value='Producto';form.dispatchEvent(new Event('change'));assert(visible().length===0&&!archive.querySelector('[data-archivo-vacio]').hidden,'vacío');});
 await test('reset y ciclo destroy/init del archivo',async()=>{form.reset();await wait();assert(visible().length===3,'reset');NotaEditorial.get(archive).destroy();assert(!NotaEditorial.get(archive),'destroy');NotaEditorial.init();NotaEditorial.init();assert(!!NotaEditorial.get(archive),'init idempotente');});
 const config=document.querySelector('[data-config-editorial]'),cf=config.querySelector('form');
 await test('configuración cambia CSS y JSON de forma coherente',()=>{cf.elements.disposicion.value='lista';cf.elements.extractos.checked=false;cf.dispatchEvent(new Event('change'));const c=JSON.parse(config.querySelector('code').textContent);assert(c.disposicion==='lista'&&!c.extractos&&c.metadatos,'JSON');assert(getComputedStyle(archive.querySelector('[data-extracto]')).display==='none','extracto');assert(document.documentElement.hasAttribute('data-editorial-lista'),'lista');});
 await test('configuración se restaura y destruye',async()=>{cf.reset();await wait();assert(!document.documentElement.hasAttribute('data-editorial-lista'),'reset');NotaEditorial.get(config).destroy();assert(!NotaEditorial.get(config),'destroy');NotaEditorial.init();assert(NotaEditorial.get(config),'init');});
 await test('sin sonido activado durante navegación',()=>{assert([...document.querySelectorAll('[data-sonido]')].every(b=>b.getAttribute('aria-pressed')==='false'),'sonido');});
 return {results,failed:results.filter(r=>!r.ok).length};
})()''');save('biblioteca-interaccion.json',checks);print(checks,flush=True);assert not checks['failed'],checks
fresh('biblioteca.html#receta-calor');settle();deep=evaluate('({page:document.querySelector(".pagina.viva").id,hash:location.hash,top:document.getElementById("receta-calor").getBoundingClientRect().top})');assert deep['page']=='graficas' and deep['hash']=='#receta-calor' and 45<=deep['top']<=150,deep
pages=['portada','publicaciones','lectura','reportes','graficas','tablas','prototipos','expresion','configuracion'];records=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for page in pages:
   evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector("[data-ir='+page+']").click();scrollTo({top:0,behavior:"instant"});true')
   data=file('medir_navegador.js');data['page']=page
   assert data['viewport']==[w,h] and data['documentWidth']==w,(page,theme,w,data['documentWidth'])
   assert not data['errors'] and not data['svgTextOverflow'],data
   assert all(c['ratio']>=c['minimum'] for c in data['contrasts']),data['contrasts']
   assert all(b['inside'] and b['focus']==0 and b['name'] and (b['content']<=b['width']+1 or b['end']>0 and b['overflow'] in ['auto','scroll']) for b in data['regions']),data
   records.append(data)
  save('biblioteca-pantallas.json',records);print(w,theme,'nueve capítulos: ancho, regiones, rótulos y contraste',flush=True)
# Regresiones de los documentos existentes tras cambiar el módulo optativo.
fresh('informe.html');r=file('pruebas_capitulos.js');save('biblioteca-regresion-capitulos.json',r);assert not r['failed'],r
fresh('plantilla.html');r=file('pruebas_segunda_tanda.js');save('biblioteca-regresion-catalogo.json',r);assert not r['failed'],r
fresh('biblioteca.html#prototipos');call('exec','--command','set viewport 1440 960');settle()
from pypdf import PdfReader
pdf=base64.b64decode(call('pdf')['data']);reader=PdfReader(io.BytesIO(pdf));text='\n'.join(p.extract_text() for p in reader.pages)
for title in ['El cuaderno abierto','Qué cambió en el documento','Lo que podría salir mal','Tres momentos de una confirmación']:
 assert title in text,(title,'ausente en PDF')
assert evaluate('document.querySelector(".pagina.viva").id')=='prototipos'
save('biblioteca-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':base+'/biblioteca.html','browser':evaluate('navigator.userAgent'),'combinaciones':len(records),'deep':deep,'pdf_paginas':len(reader.pages),'limitaciones':['Eventos DOM y foco programático, no prueba de teclado físico ni lector de pantalla.','No audición manual de audio ni medición de hardware móvil.','No ejecuta Ghost ni GScan.']})
for w,h,page,theme,name in [(390,844,'portada','oliva','biblioteca-390'),(1440,960,'publicaciones','arcilla','biblioteca-archivo'),(1440,960,'portada','light','biblioteca-inicio')]:
 call('exec','--command',f'set viewport {w} {h}');evaluate('document.querySelector("[data-elegir-tema][value='+theme+']").click();document.querySelector("[data-ir='+page+']").click();scrollTo({top:0,behavior:"instant"});true');settle();Path('auditoria/capturas/'+name+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
print('Biblioteca verificada: 162 combinaciones, interacciones, dos regresiones y PDF',flush=True)
