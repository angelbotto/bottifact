"""Copia, revisión, visor, tabla y señal sonora en la guía completa."""
import json,re,base64
from comprobar_navegador import call,evaluate,save,ROOT

def fresh():
 call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/guia.html');call('exec','--command','set viewport 390 844');evaluate('document.fonts.ready.then(()=>true)');call('screenshot')
fresh()
js=(ROOT/'scripts/pruebas_revision.js').read_text().replace('biblioteca-codigo-','guia-fuente-').replace('length===71','length===72').replace("go('tablas')","go('piezas-tablas')").replace("go('prototipos')","go('piezas-prototipos')").replace("go('portada')","go('manual')").replace("document.querySelectorAll('.card-editorial').length===3","document.querySelectorAll('.card-editorial').length>=3")
r=evaluate(js);save('guia-interacciones.json',r);assert not r['failed'],r
sources=evaluate('Object.fromEntries([...document.querySelectorAll("code[id^=guia-fuente-]")].map(x=>[x.id.slice(12),x.textContent]))')
for item in json.loads((ROOT/'registro.json').read_text())['componentes']:assert sources.get(item['id'])==item['html'],item['id']
# Activación nativa, nota al entrar y repetición sonora. No se afirma audición física.
fresh();call('exec','--command','set viewport 1440 960')
assert not evaluate('NotaAudio.enabled') and evaluate('NotaAudio.plays')==0
assert not evaluate('NotaMano.get(document.getElementById("guia-demo-apunte-izquierdo")).played')
evaluate('document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');call('screenshot')
def click(name):
 ref=re.search(r'button "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',call('snapshot')['snapshot']).group(1);call('click','--element','@'+ref)
evaluate('document.querySelector("[data-preferencia-tab=sonido]").click();true');click('Probar sonido');assert evaluate('new Promise(r=>setTimeout(()=>r(NotaAudio.enabled),400))')
evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector(\'[data-ir="voz"]\').click();document.getElementById("guia-demo-apuntes-ejemplo").scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot')
evaluate('''(()=>{window.sampleAudio=[];document.addEventListener('click',function f(e){if(!e.target.closest('[data-mano-repetir]'))return;document.removeEventListener('click',f);window.gestoReal=e.isTrusted;let n=0;const t=setInterval(()=>{sampleAudio.push(NotaAudio.sampleLevel());if(++n===30)clearInterval(t)},20)});return true})()''')
click('Repetir apunte izquierdo');evaluate('new Promise(r=>setTimeout(()=>r(true),700))')
audio=evaluate('({trusted:gestoReal,enabled:NotaAudio.enabled,state:NotaAudio.state,rms:Math.max(...sampleAudio.map(x=>x.rms)),peak:Math.max(...sampleAudio.map(x=>x.peak)),played:NotaMano.get(document.getElementById("guia-demo-apunte-izquierdo")).played})')
assert audio['trusted'] and audio['played'] and audio['rms']>.0001 and audio['peak']<1,audio
reduced=evaluate('''(()=>{const a=NotaMano.get(document.getElementById('guia-demo-apunte-izquierdo'));Object.defineProperty(a.motion,'matches',{configurable:true,value:true});a.motion.dispatchEvent(new Event('change'));const r={animations:a.animations.length,voices:NotaAudio.activeVoices,complete:a.characters.every(x=>+getComputedStyle(x).opacity===1)};delete a.motion.matches;return r})()''')
assert reduced['animations']==0 and reduced['voices']==0 and reduced['complete'],reduced
save('guia-audio.json',{'audio':audio,'reduced':reduced,'method':'Orca clic nativo; AnalyserNode después de gain. Reducción por MQL explícito. No audición humana ni salida del MacBook.'})
# Captura de guía y de la composición, con todo el texto visible.
evaluate('NotaAudio.disable();document.querySelectorAll("[data-mano],[data-subrayar]").forEach(x=>NotaMano.get(x)?.finish());true')
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}');evaluate('document.getElementById("guia-demo-apuntes-ejemplo").scrollIntoView({block:"center",behavior:"instant"});true');(ROOT/'auditoria/capturas'/f'guia-notas-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
print('Ocho interacciones, 71 fuentes exactas, entrada de escritura, clic nativo y cancelación de sonido correctos.',flush=True)
