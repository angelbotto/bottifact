"""Pines, menús, visor y audio central en el navegador público de Orca."""
import re,json,base64,datetime
from pathlib import Path
from check_browser import call,evaluate,file,save
BASE='http://127.0.0.1:8768/examples/generated/library.html'
def fresh():
 call('goto','--url','about:blank');call('goto','--url',BASE)
 evaluate('document.fonts.ready.then(()=>true)')
def settle():
 evaluate('new Promise(r=>setTimeout(()=>r(true),100))');call('screenshot')
def click_named(name):
 s=call('snapshot')['snapshot'];ref=re.search(r'button "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',s).group(1)
 call('click','--element','@'+ref)
def capture(name):Path('tests/screenshots/'+name+'.png').write_bytes(base64.b64decode(call('screenshot')['data']))
fresh();call('exec','--command','set viewport 390 844');settle()
r=file('tests_polish.js');save('pulido-interaccion.json',r);assert not r['failed'],r;print('Ocho contratos de interacción correctos',flush=True)
# Cada menú conserva su contenido, foco y desplazamiento local dentro del viewport.
fresh();records=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
  for page,selector in [('tablas','[data-explorador]'),('prototipos','[data-visor]')]:
   evaluate('document.querySelector("[data-ir='+page+']").click();document.querySelector('+json.dumps(selector)+').scrollIntoView({behavior:"instant",block:"start"});true')
   for index in range(evaluate('document.querySelectorAll('+json.dumps(selector+' .control-menu')+').length')):
    evaluate('document.querySelectorAll('+json.dumps(selector+' .control-menu')+')['+str(index)+'].querySelector("summary").scrollIntoView({behavior:"instant",block:"center"});true');settle()
    r=evaluate('''(async()=>{const m=document.querySelectorAll(SELECTOR)[INDEX];m.open=true;await new Promise(r=>setTimeout(r,60));const p=m.querySelector('.control-panel'),r=p.getBoundingClientRect(),s=getComputedStyle(p);const out={width:innerWidth,height:innerHeight,theme:document.documentElement.dataset.theme,menu:p.getAttribute('aria-label'),left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:s.overflow,tabIndex:p.tabIndex,documentWidth:document.documentElement.scrollWidth};m.querySelector('summary').focus({preventScroll:true});document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));out.escape=!m.open&&document.activeElement===m.querySelector('summary');return out;})()'''.replace('SELECTOR',json.dumps(selector+' .control-menu')).replace('INDEX',str(index)))
    assert r['left']>=0 and r['right']<=w+.1 and r['top']>=0 and r['bottom']<=h+.1 and r['documentWidth']==w,r
    assert r['overflow']=='auto' and r['tabIndex']==0 and r['escape'],r
    records.append(r)
  print(w,theme,'menús de tabla y visor correctos',flush=True)
save('pulido-menus.json',records)
# Léxico: los símbolos de un lenguaje no consumen código de otro; texto exactamente igual.
r=evaluate(r'''(()=>{const tests=[['css','.nota { color: #ffeeaa; padding: 12px; }'],['javascript','const n = 12; // comentario\nconst ok = true;'],['shell','echo --version 42 # comentario'],['sql','SELECT total FROM datos -- comentario\nWHERE total > 10'],['json','{"activo": true, "total": 12}']];return tests.map(([lang,source])=>{const wrap=document.createElement('div'),code=document.createElement('code');code.dataset.lenguaje=lang;code.textContent=source;wrap.append(code);NotaCodigo.init(wrap);return {lang,same:code.textContent===source,tokens:code.querySelectorAll('span').length,comments:[...code.querySelectorAll('.com')].map(e=>e.textContent)};});})()''')
assert all(t['same'] and t['tokens']>=2 for t in r),r
save('pulido-codigo.json',r)
# Audio: preparación DOM del disclosure y foco. Activación/repetición son clics nativos de Orca.
fresh();call('exec','--command','set viewport 1024 900');settle()
evaluate('window.audioClicks=[];document.addEventListener("click",e=>{if(e.target.closest("[data-audio-global],[data-escribir]"))audioClicks.push({trusted:e.isTrusted,action:e.target.closest("button").textContent.trim()})},true);document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');settle()
click_named('Sonidos apagados');assert evaluate('NotaAudio.enabled')
evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector("[data-ir=configuracion]").click();document.querySelector("[data-escritura]").scrollIntoView({behavior:"instant",block:"center"});true');settle()
assert evaluate('NotaAudio.plays')==0,'scroll emitió sonido'
click_named('Repetir escritura')
evaluate('new Promise(r=>setTimeout(()=>r(true),750))')
r=evaluate('({enabled:NotaAudio.enabled,plays:NotaAudio.plays,voices:NotaAudio.activeVoices,clicks:audioClicks})');assert r['enabled'] and r['plays']==1 and r['voices']==0 and all(c['trusted'] for c in r['clicks']),r
# El mismo interruptor apaga; no se recuerda tras recargar.
evaluate('scrollTo({top:0,behavior:"instant"});document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');settle();click_named('Sonidos activados');assert not evaluate('NotaAudio.enabled')
r['off']=True;r['method']='Orca click nativo (isTrusted); apertura/foco del disclosure preparados con DOM. No acredita audición manual.';save('pulido-audio.json',r);print('Audio: gesto real, scroll silencioso, lápiz y apagado correctos',flush=True)
# Capturas de las interacciones finales para inspección visual.
fresh();call('exec','--command','set viewport 1024 900');evaluate('document.querySelector("[data-elegir-tema][value=light]").click();document.querySelector("[data-ir=tablas]").click();document.querySelector("[data-explorador]").scrollIntoView({behavior:"instant",block:"center"});true');settle();capture('pulido-tabla')
evaluate('document.querySelector("[data-ir=prototipos]").click();document.querySelector("[data-visor]").scrollIntoView({behavior:"instant",block:"start"});true');settle();capture('pulido-visor')
call('exec','--command','set viewport 390 844');evaluate('document.querySelector("[data-ir=portada]").click();getSelection().removeAllRanges();document.querySelector(".revision-barra [data-revision-modo]").click();const p=document.querySelector(".pagina.viva .bajada"),r=p.getBoundingClientRect();p.dispatchEvent(new MouseEvent("click",{bubbles:true,clientX:r.left+r.width*.4,clientY:r.top+20}));document.querySelector("[data-revision-texto]").value="Demos más aire a esta introducción.";true');settle();capture('pulido-burbuja-390')
save('pulido-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'menus':len(records),'viewport':[320,390,1440],'limitations':['No audición manual ni lector de pantalla.','Pruebas de interacción DOM excepto los clics de audio indicados.']})
