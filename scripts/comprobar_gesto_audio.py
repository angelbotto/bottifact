"""Regresión de audio sin data-escritura-sonora: activación, hover, scroll silencioso y lápiz."""
import re
from comprobar_navegador import call,evaluate,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/biblioteca.html');call('exec','--command','set media light');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)');call('screenshot')
def click(name):
 snapshot=call('snapshot')['snapshot'];ref=re.search(r'button "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',snapshot).group(1);call('click','--element','@'+ref)
def open_sound():
 evaluate('scrollTo({top:0,behavior:"instant"});document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');call('screenshot')
def cards():
 evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector(".catalogo-indice a[href=\\"#receta-cards-trazadas\\"]").click();true');call('screenshot')
def move(index,dx=30):
 p=evaluate('(()=>{const r=document.querySelectorAll(".cards-trazadas > a")['+str(index)+'].getBoundingClientRect();return {x:r.left+'+str(dx)+',y:r.top+40};})()');call('mouse','move','--x',str(round(p['x'])),'--y',str(round(p['y'])))
evaluate('window.gestoEventos=[];document.addEventListener("pointermove",e=>gestoEventos.push({trusted:e.isTrusted,type:e.pointerType,x:e.clientX,y:e.clientY}));true')
cards();call('mouse','move','--x','10','--y','200');move(0);assert evaluate('NotaAudio.plays')==0 and not evaluate('NotaAudio.enabled')
open_sound();click('Sonidos apagados');assert evaluate('NotaAudio.enabled');cards();call('mouse','move','--x','10','--y','200');move(0);first=evaluate('NotaAudio.plays');assert first==1,first
move(0,45);assert evaluate('NotaAudio.plays')==first,'hover repetido dentro de la misma card'
evaluate('new Promise(r=>setTimeout(()=>r(true),180))');move(1);second=evaluate('NotaAudio.plays');assert second==first+1,second
evaluate('document.querySelectorAll(".cards-trazadas > a")[0].focus({preventScroll:true});true');call('mouse','wheel','--dy','100');call('screenshot');assert evaluate('NotaAudio.plays')==second,'scroll o foco sonoro'
evaluate('document.querySelector("#nota-decision").removeAttribute("data-escritura-sonora");document.querySelector(".catalogo-indice a[href=\\"#receta-manuscrita\\"]").click();true');call('screenshot');assert evaluate('NotaAudio.plays')==second,'escritura automática sonora'
click('Volver a escribir la nota');assert evaluate('NotaAudio.plays')==second+1,'falta lápiz explícito'
open_sound();click('Sonidos activados');r=evaluate('({enabled:NotaAudio.enabled,voices:NotaAudio.activeVoices,plays:NotaAudio.plays,events:gestoEventos})');assert not r['enabled'] and r['voices']==0 and any(e['trusted'] and e['type']=='mouse' for e in r['events']),r
r['method']='Orca click/mouse move/mouse wheel nativos. Apertura, foco y navegación preparados con DOM; no audición manual.';save('gesto-audio.json',r);print('Audio verificado: dos hover, un lápiz explícito, scroll/foco/entrada silenciosos y apagado.')
