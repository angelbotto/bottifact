"""Prueba de nuevas piezas, marcos y prioridades en Orca; sin instalaciones."""
import json,base64,re
from pathlib import Path
from check_browser import call,evaluate,file,save
BASE='http://127.0.0.1:8768/examples/generated/priorities.html'
def fresh():call('goto','--url','about:blank');call('goto','--url',BASE);call('exec','--command','set viewport 1440 960');call('exec','--command','set media light');evaluate('document.fonts.ready.then(()=>true)')
fresh();r=file('tests_pieces_editorial.js');save('piezas-editoriales-interaccion.json',r);assert not r['failed'],r;print('Interacciones:',r,flush=True)
# Las capturas dan al navegador un frame presentado entre desplazamientos e IntersectionObserver.
def settle():call('screenshot');evaluate('new Promise(r=>setTimeout(()=>r(true),180))')
evaluate('document.querySelector("[data-aviso-animado]").scrollIntoView({block:"center",behavior:"instant"});true');settle()
r=evaluate('(()=>{const e=document.querySelector("[data-aviso-animado]"),a=NotaPiezasEditoriales.get(e);a.play();return {playing:a.animating,rect:e.getBoundingClientRect().toJSON(),motion:a.motion.matches}})()');assert r['playing'],r
call('screenshot');evaluate('scrollTo({top:0,behavior:"instant"});true');settle();assert not evaluate('NotaPiezasEditoriales.get(document.querySelector("[data-aviso-animado]")).animating')
evaluate('document.querySelector("[data-aviso-animado]").scrollIntoView({block:"center",behavior:"instant"});true');settle()
r=evaluate('(()=>{const e=document.querySelector("[data-aviso-animado]"),a=NotaPiezasEditoriales.get(e);a.play();Object.defineProperty(a.motion,"matches",{configurable:true,value:true});a.motion.dispatchEvent(new Event("change"));a.play();const stopped=!a.animating;delete a.motion.matches;a.destroy();const removed=!e.querySelector(".aviso-pulso");NotaPiezasEditoriales.init(e);return {stopped,removed,one:e.querySelectorAll(".aviso-pulso").length===1}})()');assert all(r.values()),r
save('piezas-editoriales-pulso.json',{'method':'Orca scroll, frames presentados y API de repetición. Reducción mediante evento MQL explícito.','result':r})
evaluate('document.querySelector("[data-galeria]").scrollIntoView({block:"center",behavior:"instant"});true');settle()
# Galería nativa: foco y desplazamiento local; Orca keypress no entrega keydown en esta sesión.
evaluate('document.querySelector("[data-galeria-pista]").focus();true')
evaluate('document.querySelector("[data-galeria-pista]").scrollBy({left:80,behavior:"instant"});true');settle()
assert evaluate('document.querySelector("[data-galeria-pista]").scrollLeft')>0
assert not evaluate('document.querySelector("[data-galeria] button")!==null')
evaluate('(()=>{const t=document.querySelector("[data-galeria-pista]");t.scrollTo({left:t.scrollWidth,behavior:"instant"});return true})()');settle()
r=evaluate('({left:document.querySelector("[data-galeria-pista]").scrollLeft,max:document.querySelector("[data-galeria-pista]").scrollWidth-document.querySelector("[data-galeria-pista]").clientWidth,status:document.querySelector("[data-galeria-estado]").textContent})');assert abs(r['left']-r['max'])<2,r
evaluate('document.querySelector("[data-galeria-pista]").scrollBy({left:-80,behavior:"instant"});true');settle();assert evaluate('document.querySelector("[data-galeria-pista]").scrollLeft')<r['max']-1
# Compatibilidad: los controles anteriores siguen siendo opcionales y funcionales.
r2=evaluate('''(()=>{const e=document.querySelector("[data-galeria]"),a=NotaPiezasEditoriales.get(e);a.destroy();e.insertAdjacentHTML("beforeend",'<button data-galeria-anterior>Anterior</button><button data-galeria-siguiente>Siguiente</button>');NotaPiezasEditoriales.init(e);const api=NotaPiezasEditoriales.get(e);Object.defineProperty(api.motion,"matches",{configurable:true,value:true});e.querySelector("[data-galeria-pista]").scrollLeft=0;e.querySelector("[data-galeria-siguiente]").click();const advanced=e.querySelector("[data-galeria-pista]").scrollLeft>0;api.destroy();e.querySelectorAll("button").forEach(b=>b.remove());NotaPiezasEditoriales.init(e);return {advanced}})()''');assert r2['advanced'],r2
save('piezas-editoriales-galeria.json',{'method':'Región enfocada; desplazamiento por scrollBy/scrollTo. Orca keypress no produjo keydown: no acredita teclado físico. Variante anterior con clic DOM y MQL reducido explícito.','end':r,'legacy':r2})
print('Pulso y galería: frames, entrada/salida, reducción, avance/final/regreso y ciclo correctos.',flush=True)
fresh();records=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  for page in ['prioridades','piezas']:
   evaluate('document.querySelector("[data-elegir-tema][value='+theme+']").click();document.querySelector("[data-ir='+page+']").click();true')
   d=file('measure_browser.js');d['page']=page
   assert d['documentWidth']==w and not d['errors'] and not d['svgTextOverflow'],d
   assert all(c['ratio']>=c['minimum'] for c in d['contrasts']),d['contrasts']
   for region in d['regions']:assert region['inside'] and region['focus']==0 and region['name'] and (region['content']<=region['width']+1 or region['end']>0 and region['overflow'] in ['auto','scroll']),region
   records.append(d)
  print(w,theme,'prioridades y piezas correctas',flush=True)
save('piezas-editoriales-pantallas.json',records)
# Clic nativo de copiar; permiso de portapapeles depende del navegador, fuente capturada para probar exactitud.
evaluate('document.querySelector("#codigo-lineas-ejemplo").scrollIntoView({block:"center",behavior:"instant"});window.copiaPrueba={};Object.defineProperty(navigator.clipboard,"writeText",{configurable:true,value:async text=>{copiaPrueba.text=text;}});document.addEventListener("click",e=>{if(e.target.closest("[data-copiar=codigo-lineas-fuente]"))copiaPrueba.trusted=e.isTrusted;});true')
ref=re.search(r'button "Copiar código Python"[^\n]*ref=(e\d+)',call('snapshot')['snapshot']).group(1);call('click','--element','@'+ref)
r=evaluate('({same:copiaPrueba.text===document.querySelector("#codigo-lineas-fuente").textContent,trusted:copiaPrueba.trusted,status:document.querySelector("#codigo-lineas-ejemplo .copia-estado").textContent})');assert r['same'] and r['trusted'] and 'copiado' in r['status'],r;save('piezas-editoriales-copia.json',{'method':'Clic nativo de Orca y writeText sustituido para capturar el texto, no lectura del portapapeles físico.','result':r})
for w,h,anchor in [(320,740,'galeria-ejemplo'),(390,844,'codigo-lineas-ejemplo'),(1440,960,'avisos-animados-ejemplo'),(1440,960,'actividad-editorial-ejemplo')]:
 call('exec','--command',f'set viewport {w} {h}');evaluate('document.querySelector("[data-elegir-tema][value=dark]").click();document.getElementById('+json.dumps(anchor)+').scrollIntoView({block:"center",behavior:"instant"});true');Path('tests/screenshots/'+anchor+'-'+str(w)+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
print('36 combinaciones, interacción, copia nativa con destino simulado y capturas listas.',flush=True)
