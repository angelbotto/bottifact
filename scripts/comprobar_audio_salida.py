"""Clic nativo y señal Web Audio medida después del volumen maestro; no audición humana."""
import re
from comprobar_navegador import call,evaluate,save

def fresh():
 call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/estandar.html');call('exec','--command','set viewport 1440 960')
 evaluate('document.fonts.ready.then(()=>true)')
def click(name):
 ref=re.search(r'button "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',call('snapshot')['snapshot']).group(1);call('click','--element','@'+ref)
def menu():
 evaluate('scrollTo({top:0,behavior:"instant"});document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true')
def arm(selector):
 evaluate('''(()=>{window.audioSamples=[];document.addEventListener('click',function collect(e){if(!e.target.closest('''+repr(selector)+'''))return;document.removeEventListener('click',collect);window.audioTrusted=e.isTrusted;let n=0;const timer=setInterval(()=>{audioSamples.push(NotaAudio.sampleLevel());if(++n===30)clearInterval(timer);},20);});return true})()''')
def samples():
 evaluate('new Promise(r=>setTimeout(()=>r(true),700))');return evaluate('({trusted:audioTrusted,state:NotaAudio.state,enabled:NotaAudio.enabled,plays:NotaAudio.plays,peak:Math.max(...audioSamples.map(s=>s.peak)),rms:Math.max(...audioSamples.map(s=>s.rms))})')
fresh();assert not evaluate('NotaAudio.enabled') and evaluate('NotaAudio.plays')==0
menu();arm('[data-audio-prueba]');click('Probar sonido');tone=samples();assert tone['trusted'] and tone['state']=='running' and tone['rms']>.005 and tone['peak']<1,tone
# El MP3 conserva dinámica natural: se comprueba señal, no un RMS mínimo que obligue a amplificarlo.
# Entrada automática de lápiz ya habilitado; repetir con gesto nativo para medir sin carreras.
evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector("#nota-estandar-gesto").scrollIntoView({block:"center",behavior:"instant"});true')
arm('[data-mano-repetir]');click('Repetir la nota');pencil=samples();assert pencil['trusted'] and pencil['rms']>.0001 and pencil['peak']<1,pencil
menu();evaluate('(()=>{const v=document.querySelector("[data-audio-volumen]");v.value=0;v.dispatchEvent(new Event("input",{bubbles:true}));return true})()');arm('[data-audio-prueba]');click('Probar sonido');zero=samples();zero['settledPeak']=evaluate('Math.max(...audioSamples.slice(10).map(s=>s.peak))');assert zero['settledPeak']<.00001,zero
click('Sonidos activados');assert not evaluate('NotaAudio.enabled') and evaluate('NotaAudio.activeVoices')==0
# Error explícito del navegador: no presentar un estado activado falso.
fresh();evaluate('window.AudioContext=class{constructor(){throw Error("denied")}};true');menu();click('Probar sonido');blocked=evaluate('({enabled:NotaAudio.enabled,status:document.querySelector("[data-audio-estado]").textContent})');assert not blocked['enabled'] and 'No se pudo' in blocked['status'],blocked
save('audio-salida.json',{'method':'Orca click nativo; AnalyserNode después de gain maestro, 30 muestras cada 20 ms. Error con constructor simulado. No audición manual ni prueba de salida del MacBook.','tone':tone,'pencil':pencil,'zero':zero,'blocked':blocked})
print('Señal comprobada:',tone,pencil,zero,blocked,flush=True)
