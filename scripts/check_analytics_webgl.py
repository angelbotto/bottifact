"""Ciclo de vida de las tres escenas nuevas, con IO y media emulada en Orca."""
from check_browser import call,evaluate,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/examples/generated/library.html');call('exec','--command','set viewport 1440 960')
def settle():evaluate('new Promise(r=>setTimeout(()=>r(true),150))');call('screenshot')
records=[]
for kind,key in [('columnas','columnas-mapa'),('arcos','arcos-mapa'),('almacen','almacen')]:
 call('exec','--command','set media light')
 evaluate(f'document.querySelector("a[href=\\"#receta-{key}\\"]").click();window.nuevaEscena=NotaEscena.get(document.querySelector("[data-escena={kind}]"));nuevaEscena.motion.dispatchEvent(new Event("change"));nuevaEscena.stage.scrollIntoView({{behavior:"instant",block:"center"}});true');settle()
 evaluate('nuevaEscena.resume();true');settle()
 active=evaluate('({visible:nuevaEscena.visible,frame:nuevaEscena.frame,frames:nuevaEscena.frames})');assert active['visible'] and active['frame']>0,active
 evaluate('document.querySelector("[data-ir=portada]").click();true');settle()
 hidden=evaluate('({visible:nuevaEscena.visible,frame:nuevaEscena.frame,frames:nuevaEscena.frames})');settle();assert not hidden['visible'] and hidden['frame']==0 and hidden['frames']==evaluate('nuevaEscena.frames'),hidden
 evaluate(f'document.querySelector("a[href=\\"#receta-{key}\\"]").click();nuevaEscena.stage.scrollIntoView({{behavior:"instant",block:"center"}});true');settle()
 call('exec','--command','set media reduced-motion');evaluate('nuevaEscena.motion.dispatchEvent(new Event("change"));true');settle()
 reduced=evaluate('({matches:nuevaEscena.motion.matches,frame:nuevaEscena.frame,frames:nuevaEscena.frames,disabled:nuevaEscena.pauseButton.disabled})');settle();assert reduced['matches'] and reduced['frame']==0 and reduced['disabled'] and reduced['frames']==evaluate('nuevaEscena.frames'),reduced
 # Retirar la instancia real y reconstruir sobre la tabla intacta.
 destroyed=evaluate('(()=>{const s=nuevaEscena,e=s.element,t=e.querySelector("table").outerHTML;s.destroy();const result={frame:s.frame,resources:s.resources.size,unregistered:!NotaEscena.get(e),table:e.querySelector("table").outerHTML===t};NotaEscena.init(e);return result;})()');assert destroyed=={'frame':0,'resources':0,'unregistered':True,'table':True},destroyed
 fallback=evaluate(f'''(()=>{{const source=document.querySelector('[data-escena={kind}]'),e=document.createElement('figure');e.dataset.escena='{kind}';e.append(source.querySelector('.tabla-caja').cloneNode(true));document.body.append(e);const three=window.THREE;let s;try{{window.THREE=undefined;s=NotaEscena.init(e)[0];}}finally{{window.THREE=three;}}const result={{renderer:!!s.renderer,table:!!e.querySelector('table'),error:!s.error.hidden,hidden:s.stage.hidden}};s.destroy();e.remove();return result;}})()''');assert fallback=={'renderer':False,'table':True,'error':True,'hidden':True},fallback
 records.append({'type':kind,'active':active,'hidden':hidden,'reduced':reduced,'destroy':destroyed,'withoutThree':fallback});print(kind,'visible, fuera de pantalla, reduce, destroy y sin Three correctos',flush=True)
save('analitica-webgl.json',{'records':records,'method':'Orca y WebGL real. IO por scroll/cambio de capítulo. Reduce emulado con evento MQL explícito. Fallback simulando dependencia Three ausente; no fallo físico de GPU.'})
call('exec','--command','set media light')
