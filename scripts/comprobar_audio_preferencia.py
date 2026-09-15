"""Cancelación durante la activación y pausa sin olvidar la preferencia."""
import re
from comprobar_navegador import call,evaluate,save
URL='http://127.0.0.1:8768/estandar.html'
def click(name,role='button'):
 s=call('snapshot')['snapshot'];ref=re.search(r'\b'+role+' "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',s)[1];call('click','--element','@'+ref)
def open_menu():evaluate('document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true')
call('goto','--url',URL);evaluate('localStorage.setItem("nota-audio-preferencia","true");true');call('goto','--url',URL);call('exec','--command','set viewport 1440 960');open_menu()
# Slow the promise, preserving the real AudioContext and real native gesture.
evaluate('const resumeAudioOriginal=AudioContext.prototype.resume;AudioContext.prototype.resume=function(){const result=resumeAudioOriginal.call(this);return Promise.all([result,new Promise(r=>setTimeout(r,2500))]);};true')
click('Letras','tab');click('Sonidos activados')
cancelled=evaluate('new Promise(r=>setTimeout(()=>r({preferred:NotaAudio.preferred,enabled:NotaAudio.enabled,voices:NotaAudio.activeVoices,plays:NotaAudio.plays,busy:document.querySelector("[data-audio-global]").getAttribute("aria-busy")}),2600))')
assert cancelled==dict(preferred=False,enabled=False,voices=0,plays=0,busy='false'),cancelled
evaluate('AudioContext.prototype.resume=resumeAudioOriginal;true');click('Sonidos apagados');assert evaluate('new Promise(r=>setTimeout(()=>r(NotaAudio.enabled),200))')
evaluate('dispatchEvent(new Event("pagehide"));true')
paused=evaluate('({preferred:NotaAudio.preferred,enabled:NotaAudio.enabled,voices:NotaAudio.activeVoices,stored:localStorage.getItem("nota-audio-preferencia")})')
assert paused==dict(preferred=True,enabled=False,voices=0,stored='true'),paused
click('Temas','tab');resumed=evaluate('new Promise(r=>setTimeout(()=>r(NotaAudio.enabled),200))');assert resumed
evaluate('NotaAudio.disable();localStorage.removeItem("nota-audio-preferencia");true')
save('audio-preferencia.json',{'cancelledActivation':cancelled,'paused':paused,'resumedAfterTrustedClick':resumed,'method':'Clics nativos Orca; promesa resume demorada 2500 ms y pagehide simulado. Contexto real. No audición humana.'})
print('Silencio cancela una activación pendiente; salir de página pausa sin olvidar la preferencia.',flush=True)
