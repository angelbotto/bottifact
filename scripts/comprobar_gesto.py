"""Escritura, treemap y cards: geometría, visibilidad y preferencia reducida."""
import json,base64,datetime
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/biblioteca.html');call('exec','--command','set media light');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>{document.querySelectorAll("[data-mano],[data-subrayar]").forEach(e=>NotaMano.get(e)?.motion.dispatchEvent(new Event("change")));return true})');call('screenshot')
r=file('pruebas_gesto.js');save('gesto-interaccion.json',r);print(r,flush=True);assert not r['failed'],r
records=[]
for w,h in [(320,740),(390,844),(1000,900),(1200,900),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for key in ['manuscrita','apuntes','cards-trazadas','atencion']:
   evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector(".catalogo-indice a[href=\\"#receta-'+key+'\\"]").click();true')
   row=evaluate('''(()=>{const key=KEY,el=key==='manuscrita'?document.querySelector('.gesto-escrito'):key==='apuntes'?document.querySelector('.apuntes'):key==='cards-trazadas'?document.querySelector('.cards-trazadas'):document.querySelector('.nota-atencion'),r=el.getBoundingClientRect();return {w:innerWidth,theme:document.documentElement.dataset.theme,key,documentWidth:document.documentElement.scrollWidth,inside:r.left>=0&&r.right<=innerWidth,glyphs:[...el.querySelectorAll('.mano-palabra')].map(s=>({actual:s.getBoundingClientRect().width,expected:s.viewBox.baseVal.width/34*parseFloat(getComputedStyle(s).fontSize)})),notes:[...el.querySelectorAll('.apunte')].map(a=>{const b=a.querySelector('.apunte-cuerpo').getBoundingClientRect(),n=a.querySelector('.apunte-nota').getBoundingClientRect();return innerWidth<1000?n.top>=b.bottom:n.right<=b.left||n.left>=b.right;}),regions:[...el.querySelectorAll('.grafica-caja,.tabla-caja')].map(e=>({w:e.clientWidth,scroll:e.scrollWidth,focus:e.tabIndex===0,named:!!e.getAttribute('aria-label')}))};})()'''.replace('KEY',json.dumps(key)))
   assert row['documentWidth']==w and row['inside'] and all(row['notes']),row
   assert all(abs(g['actual']-g['expected'])<1 for g in row['glyphs']),row
   if w<=390:assert all(r['scroll']>r['w'] and r['focus'] and r['named'] for r in row['regions']),row
   records.append(row)
 print(w,'seis temas y cuatro piezas sin recorte ni compresión',flush=True)
save('gesto-pantallas.json',records)
call('exec','--command','set media reduced-motion');r=evaluate('''(()=>{document.querySelectorAll('[data-mano],[data-subrayar]').forEach(e=>{const s=NotaMano.get(e);s.motion.dispatchEvent(new Event('change'));s.play();});return [...document.querySelectorAll('[data-mano],[data-subrayar]')].map(e=>{const s=NotaMano.get(e);return {matches:s.motion.matches,animations:s.animations.length,buttons:s.buttons.every(({b})=>b.disabled)}});})()''');assert all(x['matches'] and x['animations']==0 and x['buttons'] for x in r),r;save('gesto-reduce.json',r)
call('exec','--command','set media light');evaluate('document.querySelectorAll("[data-mano],[data-subrayar]").forEach(e=>NotaMano.get(e).motion.dispatchEvent(new Event("change")));true')
for key in ['manuscrita','apuntes','cards-trazadas','atencion']:
 evaluate('document.querySelector("[data-elegir-tema][value=light]").click();document.querySelector(".catalogo-indice a[href=\\"#receta-'+key+'\\"]").click();document.querySelectorAll("[data-mano],[data-subrayar]").forEach(e=>NotaMano.get(e)?.finish());true');call('screenshot');Path('auditoria/capturas/gesto-'+key+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
save('gesto-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'combinaciones':len(records),'method':'Orca, DOM, clics sintéticos y preferencia reducida emulada con evento MQL explícito; sin lector de pantalla ni móvil físico.'})
print('Gesto verificado',flush=True)
