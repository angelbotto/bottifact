#!/usr/bin/env python3
"""Salida y movimiento de la segunda tanda. Orca; pypdf ya instalado."""
import argparse,base64,io
from check_browser import call,evaluate,save
from pypdf import PdfReader

p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8768/examples/generated/template.html');args=p.parse_args()
checks=[]
def check(name,ok):
 checks.append({'name':name,'ok':bool(ok)});save('segunda-salida.json',checks);assert ok,name

def settle(js=''):
 evaluate('(async()=>{'+js+';await new Promise(r=>setTimeout(r,150));return true;})()')
 call('screenshot')

call('exec','--command','set viewport 1639 939')
call('exec','--command','set media light')
call('goto','--url','about:blank')
call('goto','--url',args.url+'#segunda-tanda');settle()
check('Enlace inicial queda en destino tras construir gráficas y cargar fuentes',evaluate('Math.abs(document.getElementById("segunda-tanda").getBoundingClientRect().top-64)<2'))
settle('window.journey=NotaReportes.get(document.querySelector("[data-reporte=recorrido]")).globe;document.getElementById("recorrido-ejemplo").scrollIntoView({behavior:"instant"})')
check('Globo narrado arranca sin RAF',evaluate('journey.paused&&journey.frame===0'))
settle('journey.select(null);journey.resume()')
check('Globo narrado reanudado visible dibuja',evaluate('journey.visible&&journey.frame>0'))
call('exec','--command','set media reduced-motion');settle()
settle('journey.motion.dispatchEvent(new MediaQueryListEvent("change",{matches:journey.motion.matches,media:journey.motion.media}))')
check('Reduce cancela RAF y desactiva giro',evaluate('journey.motion.matches&&journey.frame===0&&journey.pauseButton.disabled'))
before=evaluate('journey.frames');settle()
check('No dibuja continuamente en reduce',evaluate('journey.frames')==before)
check('Controles y visor sin transiciones en reduce',evaluate('(()=>{const v=NotaVisores.get(document.querySelector("[data-visor]"));return [...document.querySelectorAll(".apariencia label,.pieza button"),...v.shadow.querySelectorAll("button")].every(e=>getComputedStyle(e).transitionDuration.split(",").every(t=>parseFloat(t)===0));})()'))
call('exec','--command','set media light');settle('journey.motion.dispatchEvent(new MediaQueryListEvent("change",{matches:false,media:journey.motion.media}));journey.resume();scrollTo({top:0,behavior:"instant"})')
check('Globo narrado fuera de pantalla cancela RAF',evaluate('!journey.visible&&journey.frame===0'))
settle('journey.pause()')
check('Foco programático llega al visor y controles; regla focus-visible presente',evaluate('(()=>{const es=[document.querySelector(".visor-caja"),document.querySelector("[data-comodidad]"),document.querySelector("[data-ancho-visor]")];return [...document.styleSheets].some(s=>[...s.cssRules].some(r=>r.selectorText?.includes(":focus-visible")&&r.style?.outline.includes("2px")))&&es.every(e=>{e.focus();return document.activeElement===e;});})()'))
settle('document.documentElement.dataset.theme="sea";document.documentElement.removeAttribute("data-lectura-comoda")')
closed=evaluate('[...document.querySelectorAll(".metodologia")].map(d=>d.open)')
pdf=call('pdf');reader=PdfReader(io.BytesIO(base64.b64decode(pdf['data'])))
content=' '.join((p.extract_text() or '') for p in reader.pages)
required=['Estados del ejemplo','Capacidad inicial','Resultado','Operaciones esperadas y observadas','Cómo leer esta evidencia','No incluye capacitación','60 h/mes','Bogotá','Madrid','Observación']
found={s:s.casefold() in content.casefold() for s in required}
save('segunda-impresion.json',{'method':'orca pdf; extracción pypdf','theme':'sea','pages':len(reader.pages),'required':found,'detailsRestored':closed==evaluate('[...document.querySelectorAll(".metodologia")].map(d=>d.open)')})
check('PDF conserva tablas, alternativa de visor, metodología y relato',all(found.values()))
check('Impresión restaura detalles',closed==evaluate('[...document.querySelectorAll(".metodologia")].map(d=>d.open)'))
save('segunda-salida-metodo.json',{'viewport':[1639,939],'motion':'Orca set media reduced-motion; MediaQueryListEvent explícito para listener, como en primera tanda','visibility':'Scroll real e IntersectionObserver, entrega de cuadros mediante screenshot','focus':'focus() y CSS calculado; no teclado físico ni lector de pantalla','pdf':'Orca PDF y texto extraído; no acredita impresión física','deepLink':'Después de fonts.ready y entrega de cuadro de navegador'})
print(checks)
