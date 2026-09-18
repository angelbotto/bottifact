"""Contrato visible de una y varias páginas, 36 combinaciones en Orca."""
import base64
from pathlib import Path
from check_browser import call,evaluate,save
records=[]
for path in ['examples/generated/standard.html','examples/generated/standard-chapters.html']:
 call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/'+path);evaluate('document.fonts.ready.then(()=>true)')
 for w,h in [(320,740),(390,844),(1440,960)]:
  call('exec','--command',f'set viewport {w} {h}')
  for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
   r=evaluate('''(async()=>{
    document.querySelector('[data-elegir-tema][value="THEME"]').click();scrollTo({top:0,behavior:'instant'});
    const menu=document.querySelector('[data-apariencia-menu]');menu.querySelector('summary').focus();menu.open=true;await new Promise(r=>setTimeout(r,50));
    const rect=e=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width}},panel=document.querySelector('.apariencia-panel');
    panel.scrollTop=0;const audio=rect(panel.querySelector('[data-audio-prueba]')),p=rect(panel),bar=rect(document.querySelector('.revision-barra'));
    const result={path:'PATH',theme:'THEME',width:innerWidth,documentWidth:document.documentElement.scrollWidth,panel:p,audio,bar,scrollable:getComputedStyle(panel).overflowY};menu.open=false;
    document.querySelector('.revision-barra [data-revision-lista]').click();result.dialog=rect(document.querySelector('[data-revision-panel]'));document.querySelector('[data-revision-panel]').close();return result;
   })()'''.replace('THEME',theme).replace('PATH',path))
   assert r['width']==w and r['documentWidth']==w,r
   for key in ['panel','audio','bar','dialog']:
    box=r[key];assert box['left']>=-1 and box['right']<=w+1 and box['top']>=0 and box['bottom']<=h+1,(key,r)
   assert r['scrollable']=='auto',r
   records.append(r)
  if w in [320,1440]:
   Path('tests/screenshots/'+path.removesuffix('.html')+'-'+str(w)+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 # Un comentario no cambia la altura del documento y exporta el contexto elegido.
 r=evaluate('''(()=>{scrollTo({top:0,behavior:'instant'});const before=document.documentElement.scrollHeight;document.querySelector('.revision-barra [data-revision-modo]').click();document.querySelector('#una-base p').click();const editor=document.querySelector('[data-revision-editor]');const opened=editor.open;document.querySelector('[data-revision-texto]').value='Aclarar cómo se actualizan documentos anteriores.';document.querySelector('[data-revision-guardar]').click();document.querySelector('.revision-barra [data-revision-lista]').click();const prompt=document.querySelector('[data-revision-prompt]').textContent,after=document.documentElement.scrollHeight;document.querySelector('[data-revision-panel]').close();return {opened,prompt,before,after,count:document.querySelector('.revision-barra [data-revision-lista]').textContent}})()''')
 assert r['opened'] and r['count']=='1' and 'Aclarar cómo' in r['prompt'] and 'una-base' in r['prompt'] and r['before']==r['after'],r
 records.append({'path':path,'comments':r})
 if 'capitulos' in path:
  r=evaluate('''(async()=>{document.querySelector('[data-ir=evidencia]').click();await new Promise(r=>setTimeout(r,80));const page=document.querySelector('.pagina.viva'),box=page.querySelector('.tabla-caja');box.scrollLeft=9999;return {page:page.id,current:document.querySelector('[data-ir=evidencia]').getAttribute('aria-current'),indices:[...document.querySelectorAll('.indice')].filter(e=>e.getClientRects().length).length,progress:document.querySelector('.regla').getAttribute('aria-valuenow'),tableWidth:box.clientWidth,tableContent:box.scrollWidth,tableEnd:box.scrollLeft}})()''');assert r['page']=='evidencia' and r['current']=='page' and r['indices']==1,r;records.append(r)
  for w,h in [(320,740),(390,844)]:
   call('exec','--command',f'set viewport {w} {h}')
   r=evaluate('(()=>{const b=document.querySelector(".pagina.viva .tabla-caja");b.scrollLeft=9999;return {width:innerWidth,documentWidth:document.documentElement.scrollWidth,table:b.clientWidth,content:b.scrollWidth,end:b.scrollLeft,overflow:getComputedStyle(b).overflowX}})()');assert r['documentWidth']==w and r['content']>r['table'] and r['end']>0 and r['overflow']=='auto',r;records.append(r)
save('estandar-navegador.json',{'method':'Orca viewport y eventos DOM; 36 combinaciones de pantalla/paleta. Comentarios creados sin cambio de altura y prompt comprobado; sin lector de pantalla ni clic físico de portapapeles.','records':records});print('Base estándar: 36 combinaciones, comentarios con contexto, capítulos y tablas móviles correctos.',flush=True)
