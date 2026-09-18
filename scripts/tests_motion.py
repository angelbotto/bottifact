"""Ciclo real de visibilidad, RAF y Web Animations en el navegador de Orca."""
from check_browser import call,evaluate,save

def run():
 results=[]
 def check(name,value):
  results.append({'name':name,'ok':bool(value)})
  save('movimiento.json',results)
  assert value,name
 def settle(js):
  evaluate('(async()=>{'+js+';await new Promise(r=>setTimeout(r,120));return true;})()')
  # El host en segundo plano entrega observers/MQL al producir un cuadro visual.
  # Capturar fuerza ese cuadro; no se inventan eventos de visibilidad o preferencia.
  call('screenshot')
 def go(selector):settle('const el=document.querySelector('+repr(selector)+');scrollTo({top:el.getBoundingClientRect().top+scrollY-40,behavior:"instant"})')
 def media(value):
  call('exec','--command','set media '+value);settle('')
  # El modo CSS/matches es real emulado. El host entrega change de forma intermitente:
  # el contrato de cancelación del listener se ensaya con un evento unitario explícito.
  evaluate('for(const e of [window.globo,window.escenaPrueba,window.escrituraPrueba])if(e&&!e.dead)e.motion.dispatchEvent(new MediaQueryListEvent("change",{matches:e.motion.matches,media:e.motion.media}));true')
 call('exec','--command','set media light')
 call('exec','--command','set viewport 1639 939')
 go('#globo-rutas')
 settle('globo.resume()')
 check('Globo visible tiene RAF',evaluate('globo.visible && globo.frame>0'))
 before=evaluate('globo.frames');settle('');check('Globo dibuja durante giro',evaluate('globo.frames')>before)
 media('reduced-motion');settle('')
 check('Preferencia reduce cancela RAF de globo activo',evaluate('globo.motion.matches && globo.frame===0 && globo.pauseButton.disabled'))
 before=evaluate('globo.frames');settle('');check('Globo reducido no sigue dibujando',evaluate('globo.frames')==before)
 media('light');settle('scrollTo({top:0,behavior:"instant"})')
 before=evaluate('globo.frames');settle('');check('Globo fuera de pantalla se detiene',evaluate('!globo.visible && globo.frame===0 && globo.frames==='+str(before)))

 go('#xyz-ejemplo');settle('window.escenaPrueba=NotaEscena.get(document.querySelector("#xyz-ejemplo"));escenaPrueba.resume()')
 check('Escena visible tiene RAF',evaluate('escenaPrueba.visible && escenaPrueba.frame>0'))
 before=evaluate('escenaPrueba.frames');settle('');check('Escena gira por tiempo',evaluate('escenaPrueba.frames')>before)
 media('reduced-motion');settle('')
 check('Preferencia reduce cancela RAF de escena activa',evaluate('escenaPrueba.frame===0 && escenaPrueba.pauseButton.disabled'))
 before=evaluate('escenaPrueba.frames');settle('');check('Escena reducida no dibuja continuamente',evaluate('escenaPrueba.frames')==before)
 media('light');settle('escenaPrueba.resume();scrollTo({top:0,behavior:"instant"})')
 before=evaluate('escenaPrueba.frames');settle('');check('Escena fuera de pantalla sin RAF',evaluate('!escenaPrueba.visible && escenaPrueba.frame===0 && escenaPrueba.frames==='+str(before)))
 evaluate('escenaPrueba.pause();true')

 go('[data-escritura]')
 settle('window.escrituraPrueba=NotaEscritura.get(document.querySelector("[data-escritura]"));escrituraPrueba.duration=10000;escrituraPrueba.play()')
 check('Escritura usa animaciones de paths',evaluate('escrituraPrueba.animations.length===escrituraPrueba.paths.length && escrituraPrueba.animations.length>0'))
 check('Los trazos son secuenciales y el último termina a 10 s',evaluate('Math.abs(escrituraPrueba.animations.at(-1).effect.getComputedTiming().endTime-10000)<.01'))
 media('reduced-motion');settle('')
 check('Reducir cancela WAAPI y completa los trazos',evaluate('escrituraPrueba.animations.length===0 && escrituraPrueba.paths.every(p=>getComputedStyle(p).strokeDashoffset==="0px"||getComputedStyle(p).strokeDashoffset==="0")'))
 check('Reducir cancela transiciones CSS',evaluate('[...document.querySelectorAll("button,.portada,a")].every(e=>getComputedStyle(e).transitionDuration.split(",").every(t=>parseFloat(t)===0))'))
 evaluate('escrituraPrueba.play();true');check('play respeta reduce',evaluate('escrituraPrueba.animations.length===0'))
 media('light');go('[data-escritura]');settle('escrituraPrueba.play();scrollTo({top:0,behavior:"instant"})')
 check('Salir de pantalla cancela escritura',evaluate('escrituraPrueba.animations.length===0'))
 go('[data-escritura]');settle('escrituraPrueba.play()');evaluate('escrituraPrueba.destroy();true')
 check('destroy cancela animaciones y libera instancia',evaluate('escrituraPrueba.animations.length===0 && !NotaEscritura.get(escrituraPrueba.element)'))
 evaluate('NotaEscritura.init(escrituraPrueba.element);true')
 save('movimiento-metodo.json',{'viewport':[1639,939],'media':'orca exec set media reduced-motion; CSS y matches emulados','cambio':'MediaQueryListEvent explícito para los listeners: el host entregó change de forma intermitente','visibilidad':'Scroll real y cuadros screenshot para entregar IntersectionObserver','no_afirma':'Cambio físico de preferencia del sistema operativo'})
 return results

if __name__=='__main__':print(run())
