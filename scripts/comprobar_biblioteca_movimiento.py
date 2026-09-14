"""Visibilidad y movimiento de una escena dentro de la nueva edición."""
from comprobar_navegador import call,evaluate,save
call('goto','--url','http://127.0.0.1:8768/biblioteca.html#receta-xyz')
call('exec','--command','set viewport 1440 960')
call('exec','--command','set media light')
def settle():evaluate('new Promise(r=>setTimeout(()=>r(true),150))');call('screenshot')
evaluate('document.fonts.ready.then(()=>true)');settle()
evaluate('window.escenaBiblioteca=NotaEscena.get(document.querySelector("[data-escena=xyz]"));scrollTo({top:document.querySelector("[data-escena=xyz]").getBoundingClientRect().top+scrollY-40,behavior:"instant"});escenaBiblioteca.resume();true');settle()
active=evaluate('({visible:escenaBiblioteca.visible,frame:escenaBiblioteca.frame,frames:escenaBiblioteca.frames})');assert active['visible'] and active['frame']>0,active
evaluate('document.querySelector("[data-ir=portada]").click();scrollTo({top:0,behavior:"instant"});true');settle()
hidden=evaluate('({visible:escenaBiblioteca.visible,frame:escenaBiblioteca.frame})');assert not hidden['visible'] and hidden['frame']==0,hidden
evaluate('document.querySelector(".catalogo-indice a[href$=xyz]").click();scrollTo({top:document.querySelector("[data-escena=xyz]").getBoundingClientRect().top+scrollY-40,behavior:"instant"});true');settle()
call('exec','--command','set media reduced-motion');settle()
evaluate('escenaBiblioteca.motion.dispatchEvent(new MediaQueryListEvent("change",{matches:escenaBiblioteca.motion.matches,media:escenaBiblioteca.motion.media}));true');settle()
reduced=evaluate('({matches:escenaBiblioteca.motion.matches,frame:escenaBiblioteca.frame,frames:escenaBiblioteca.frames,disabled:escenaBiblioteca.pauseButton.disabled})');settle();assert reduced['matches'] and reduced['frame']==0 and reduced['disabled'] and evaluate('escenaBiblioteca.frames')==reduced['frames'],reduced
save('biblioteca-movimiento.json',{'active':active,'hidden':hidden,'reduced':reduced,'metodo':'Orca set media, scroll y screenshots para observers; MediaQueryListEvent explícito para listener de reduce. No es cambio físico de preferencia del SO.'})
call('exec','--command','set media light')
print('Escena: RAF activo visible, cancelado al ocultar capítulo y con movimiento reducido')
