#!/usr/bin/env python3
"""Salida impresa y CSS de movimiento del control, usando Orca y pypdf existente."""
import sys,base64,io
from pypdf import PdfReader
from check_browser import call,evaluate,save
url=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8768/examples/generated/template.html'
call('goto','--url','about:blank');call('goto','--url',url)
call('exec','--command','set viewport 320 568')
evaluate('(()=>{const m=document.querySelector("[data-apariencia-menu]");m.querySelector("summary").click();m.querySelector("[data-elegir-tema][value=sea]").click();m.querySelector("[data-elegir-estilo][value=tecnico]").click();if(!document.documentElement.hasAttribute("data-trama"))m.querySelector("[data-papel-tramado]").click();return true;})()')
small=evaluate('(()=>{const p=document.querySelector(".apariencia-panel"),r=p.getBoundingClientRect();p.scrollTop=p.scrollHeight;return {viewport:[innerWidth,innerHeight],top:r.top,bottom:r.bottom,scroll:p.scrollHeight,client:p.clientHeight,end:p.scrollTop};})()')
assert small['viewport']==[320,568] and small['bottom']<=568 and small['end']>0,small
call('exec','--command','set media reduced-motion');call('screenshot')
reduce=evaluate('matchMedia("(prefers-reduced-motion:reduce)").matches&&[...document.querySelectorAll(".apariencia-menu summary,.apariencia-menu button,.apariencia-panel")].every(e=>getComputedStyle(e).transitionDuration.split(",").every(t=>parseFloat(t)===0))')
assert reduce
pdf=call('pdf');reader=PdfReader(io.BytesIO(base64.b64decode(pdf['data'])))
text=' '.join(p.extract_text() or '' for p in reader.pages)
checks={'title':'Una llave pequeña' in text,'table':'Operaciones esperadas y observadas' in text,'viewer':'Estados del ejemplo' in text,'controlsHidden':'Tu forma de leer' not in text}
assert all(checks.values()),checks
# CSS de impresión es legible desde CSSOM, sin alterar la preferencia persistida.
texture=evaluate('[...document.styleSheets].some(s=>[...s.cssRules].some(r=>r.conditionText==="print"&&r.cssText.includes(":root[data-trama] body")&&r.cssText.includes("background-image: none")))')
assert texture
save('apariencia-salida.json',{'url':url,'smallWindow':small,'reducedCSS':reduce,'pdf':{'pages':len(reader.pages),'theme':'sea','style':'tecnico','checks':checks},'textureRemovedPrintRule':texture,'method':'Orca media emulada; CSS computado; PDF texto extraído con pypdf. No impresión física.'})
call('exec','--command','set media light')
print('Ventana baja, CSS reducido y PDF:',checks)
