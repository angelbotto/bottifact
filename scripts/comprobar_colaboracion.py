"""Pruebas de revisión y tabla en un documento aislado del demo del usuario."""
import json,base64,uuid
from comprobar_navegador import ROOT,call,evaluate,save
from contrato_artefacto import build
fixture=ROOT/'auditoria/colaborativo-prueba.html'
identity='prueba-colab-'+uuid.uuid4().hex
fixture.write_text(build('Prueba de revisión',[{'id':'contenido','titulo':'Prueba','html':(ROOT/'ejemplos/colaborativo-contenido.html').read_text()}],theme='linear-light',style='sobrio',document_id=identity))
try:
 call('goto','--url','http://127.0.0.1:8768/auditoria/colaborativo-prueba.html');call('screenshot')
 r=evaluate('''(()=>{const tests=[],ok=(name,value)=>{tests.push({name,ok:!!value});if(!value)throw Error(name);};
 const root=document.querySelector('[data-explorador]'),table=NotaExplorador.get(root),form=root.querySelector('form');ok('36 filas disponibles y 10 montadas',table.visible.length===36&&root.querySelectorAll('tbody tr').length===10);
 root.querySelector('.explorador-seleccion').click();root.querySelector('[aria-label="Página siguiente de tabla"]').click();ok('Selección persiste entre páginas',table.selected.length===1&&root.querySelector('.explorador-paginacion span').textContent.includes('2 de 4'));ok('CSV selección exacta',table.exportCSV().split('\\r\\n').length===2);
 root.querySelectorAll('.explorador-utilidades button')[0].click();
 const fc=root.querySelector('[aria-label="Columna a filtrar"]');fc.value='3';fc.dispatchEvent(new Event('change',{bubbles:true}));const min=root.querySelector('[aria-label="Valor mínimo"]');min.value='300000';min.dispatchEvent(new Event('input',{bubbles:true}));ok('Filtro numérico 7 filas',table.visible.length===7);
 fc.value='4';fc.dispatchEvent(new Event('change',{bubbles:true}));min.value='2026-09-25';min.dispatchEvent(new Event('input',{bubbles:true}));ok('Filtro fecha 4 filas',table.visible.length===4);
 fc.value='';fc.dispatchEvent(new Event('change',{bubbles:true}));form.elements.grupo.value='1';form.elements.grupo.dispatchEvent(new Event('change',{bubbles:true}));const group=root.querySelector('.tabla-grupo button');group.click();ok('Grupo plegable',group.getAttribute('aria-expanded')==='true'&&!!root.querySelector('tbody tr[hidden]'));
 form.elements.grupo.value='';form.elements.grupo.dispatchEvent(new Event('change',{bubbles:true}));dispatchEvent(new Event('beforeprint'));ok('Impresión conserva las 36 filas',root.querySelectorAll('tbody tr').length===36);dispatchEvent(new Event('afterprint'));ok('Después de imprimir recupera página',root.querySelectorAll('tbody tr').length===10);
 const rev=document.querySelector('[data-revision]');document.querySelector('.revision-barra [data-revision-modo]').click();document.getElementById('cita-revision').click();const input=document.querySelector('[data-revision-texto]');input.value='Revisar el alcance de esta decisión.';input.dispatchEvent(new Event('input',{bubbles:true}));document.querySelector('[data-revision-guardar]').click();ok('Comentario creado',NotaRevision.get(rev).comments.length===1);
 document.querySelector('.revision-barra [data-revision-lista]').click();const reply=document.querySelector('.revision-responder input');reply.value='Añadí la evidencia.';document.querySelector('.revision-responder button').click();ok('Respuesta conservada',NotaRevision.get(rev).comments[0].replies.length===1);
 const action=text=>[...document.querySelectorAll('.revision-hilo button')].find(b=>b.textContent===text);action('Resolver').click();ok('Resolver excluye del prompt',NotaRevision.get(rev).comments[0].resolved&&!document.querySelector('[data-revision-prompt]').textContent.includes('Revisar el alcance'));
 const filter=document.querySelector('.revision-utilidades select');filter.value='resolved';filter.dispatchEvent(new Event('change',{bubbles:true}));action('Reabrir').click();ok('Reabrir conserva hilo',!NotaRevision.get(rev).comments[0].resolved);document.querySelector('[data-revision-cerrar]').click();return tests;})()''')
 save('colaboracion-interacciones.json',r);print('Interacciones de tabla y comentarios correctas.',flush=True)
 call('reload');call('screenshot')
 r=evaluate('''(()=>{const r=NotaRevision.get(document.querySelector('[data-revision]')),data=r.exportData();return {count:r.comments.length,replies:r.comments[0]?.replies.length,events:data.events.length,pin:!!document.querySelector('.revision-marca'),id:document.querySelector('meta[name="nota-documento"]').content,roundtrip:r.importData(JSON.parse(JSON.stringify(data)))};})()''')
 assert r['count']==1 and r['replies']==1 and r['pin'] and r['roundtrip']==0,r
 save('colaboracion-recarga.json',r)
 # Text changes must not silently anchor a saved comment to a different paragraph.
 r=evaluate('''(()=>{const el=document.querySelector('[data-revision]'),old=NotaRevision.get(el);old.destroy();document.getElementById('cita-revision').textContent='El contenido cambió por completo.';const next=NotaRevision.init()[0];document.querySelector('.revision-barra [data-revision-lista]').click();return {retained:next.comments.length,orphan:document.querySelector('[data-revision-notas]').textContent.includes('El bloque cambió')};})()''');assert r['retained']==1 and r['orphan'],r;save('colaboracion-ancla.json',r)
 print('Recarga, importación idempotente y ancla modificada correctas.',flush=True)
 # Clean only this test document's storage.
 evaluate('''(()=>{const p='nota-revision-v2:'+encodeURIComponent(document.querySelector('meta[name="nota-documento"]').content)+':';Object.keys(localStorage).filter(k=>k.startsWith(p)).forEach(k=>localStorage.removeItem(k));return true})()''')
finally:
 fixture.unlink(missing_ok=True)
call('goto','--url','http://127.0.0.1:8768/colaborativo.html')
geometry=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['linear-light','linear-dark']:
  evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
  r=evaluate('''(()=>{const s=getComputedStyle(document.documentElement),hex=x=>x.match(/[\\d.]+/g)?.map(Number),rgb=c=>{const e=document.createElement('span');e.style.color=c;document.body.append(e);const r=hex(getComputedStyle(e).color);e.remove();return r;},lum=c=>rgb(c).slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((n,x,i)=>n+x*[.2126,.7152,.0722][i],0);const ratios=['--papel','--panel','--panel-2'].flatMap(bg=>['--tinta','--tinta-2','--tinta-3'].map(fg=>{const a=lum(s.getPropertyValue(bg)),b=lum(s.getPropertyValue(fg));return {bg,fg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)}}));return {width:innerWidth,theme:document.documentElement.dataset.theme,overflow:document.documentElement.scrollWidth>innerWidth,ratios};})()''')
  assert not r['overflow'] and all(x['ratio']>=4.5 for x in r['ratios']),r;geometry.append(r)
 save('colaboracion-geometria.json',geometry)
print('Linear Light/Dark: contraste textual y geometría a 320, 390 y 1440 px correctos.',flush=True)
call('exec','--command','set viewport 1440 960')
for theme in ['linear-light','linear-dark']:
 evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector("[data-explorador]").scrollIntoView({block:"center",behavior:"instant"});true')
 shot=call('screenshot');(ROOT/'auditoria/capturas'/('colaboracion-'+theme+'.png')).write_bytes(base64.b64decode(shot['data']))
