"""Activación nativa y ciclo de sonido sincronizado con escritura visible."""
import re
from check_browser import call,evaluate,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/examples/generated/library.html');call('exec','--command','set media light');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)')
def click(name):
 snapshot=call('snapshot')['snapshot'];ref=re.search(r'button "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',snapshot).group(1);call('click','--element','@'+ref)
def sounds():
 evaluate('scrollTo({top:0,behavior:"instant"});document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');call('screenshot')
def note():
 evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector(\'.catalogo-indice a[href="#receta-manuscrita"]\').click();true')
def wait(ms):evaluate('new Promise(r=>setTimeout(()=>r(true),'+str(ms)+'))')
r=[]
assert not evaluate('NotaAudio.enabled') and evaluate('NotaAudio.plays')==0
sounds();click('Sonidos apagados');assert evaluate('NotaAudio.enabled')
note();wait(250);first=evaluate('({plays:NotaAudio.plays,voices:NotaAudio.activeVoices,animations:document.querySelector("#nota-decision").getAnimations({subtree:true}).length})');assert first['plays']==1 and first['voices']==1 and first['animations']>0,first;r.append({'entrada':first})
wait(850);assert evaluate('NotaAudio.activeVoices')==1,'el sonido no acompaña más de .65 s'
evaluate('scrollTo({top:0,behavior:"instant"});true');wait(180);assert evaluate('NotaAudio.activeVoices')==0,'salida no cancela';r.append({'salida':True})
note();wait(180);assert evaluate('NotaAudio.plays')==1,'entrada repetida';click('Volver a escribir la nota');assert evaluate('NotaAudio.plays')==2 and evaluate('NotaAudio.activeVoices')==1
m=evaluate('(()=>{const m=NotaMano.get(document.querySelector("#nota-decision"));Object.defineProperty(m.motion,"matches",{configurable:true,value:true});m.motion.dispatchEvent(new Event("change"));return {voices:NotaAudio.activeVoices,animations:m.animations.length,disabled:document.querySelector("[data-mano-repetir=nota-decision]").disabled}})()');assert m['voices']==0 and m['animations']==0 and m['disabled'],m;r.append({'reduce_MQL_explicito':m})
evaluate('(()=>{const m=NotaMano.get(document.querySelector("#nota-decision"));delete m.motion.matches;m.motion.dispatchEvent(new Event("change"));return true})()')
click('Volver a escribir la nota');assert evaluate('NotaAudio.activeVoices')==1
sounds();click('Sonidos activados');assert not evaluate('NotaAudio.enabled') and evaluate('NotaAudio.activeVoices')==0;r.append({'apagado':True})
# Tooltip nativo con puntero; no depende de title del navegador.
evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector(\'.catalogo-indice a[href="#receta-atencion"]\').click();true');wait(160)
p=evaluate('(()=>{const r=document.querySelector(".atencion-caja g").getBoundingClientRect();return {x:Math.round(r.left+100),y:Math.round(r.top+100)}})()');call('mouse','move','--x',str(p['x']),'--y',str(p['y']));t=evaluate('({hidden:document.querySelector(".atencion-tooltip").hidden,text:document.querySelector(".atencion-tooltip").textContent})');assert not t['hidden'] and '125 horas' in t['text'],t;r.append({'tooltip_puntero_nativo':t})
save('editorial-lapiz.json',{'method':'Clics y movimiento nativos de Orca; navegación preparada por DOM. Reducción mediante evento MQL explícito. No audición manual.','checks':r});print('Lápiz: entrada optativa, duración, salida, repetición, reduce, apagado y tooltip nativo verificados.')
