"""Guía y nuevos temas con el navegador Orca. Medidas, no audición humana."""
import json,base64
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save,ROOT
from contrato_artefacto import THEMES
URL='http://127.0.0.1:8768/'
call('goto','--url',URL+'guia.html');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)')
pages=evaluate('[...document.querySelectorAll("main > .pagina")].map(x=>x.id)')
assert len(pages)==13,pages
assert evaluate('document.querySelectorAll("[data-guia-componente]").length')==71
rows=[];errors=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in THEMES[1:]:
  evaluate('(()=>{const input=document.querySelector(\'[data-elegir-tema][value="'+theme+'"]\');input.checked=true;input.dispatchEvent(new Event("change",{bubbles:true}));return true})()')
  for page in pages:
   evaluate('document.querySelector(\'[data-ir="'+page+'"]\').click();true');call('screenshot')
   d=evaluate((ROOT/'scripts/medir_navegador.js').read_text().replace("closed.forEach(d=>d.open=true)","closed.splice(0,closed.length,...closed.filter(d=>!d.closest('.pagina')||d.closest('.pagina').classList.contains('viva')));closed.forEach(d=>d.open=true)"))
   issues=[]
   if d['documentWidth']!=w:issues.append('Desborde de documento: '+str(d['documentWidth']))
   issues+=d['errors']+d['svgTextOverflow']
   issues+=[c for c in d['contrasts'] if c['ratio']<c['minimum']]
   for r in d['regions']:
    if not(r['inside'] and r['focus']==0 and r['name'] and (r['content']<=r['width']+1 or r['end']>0)):issues.append(r)
   row={'viewport':[w,h],'theme':theme,'page':page,'documentWidth':d['documentWidth'],'regions':len(d['regions']),'errors':issues};rows.append(row)
   if issues:errors.append(row)
  save('guia-navegador.json',rows)
  print(w,theme,len(pages),'páginas;',len(errors),'fallos acumulados',flush=True)
# Presets por archivo y persistencia aislada de la preferencia global.
for name,style in [('liftit','sobrio'),('blueprint','tecnico'),('hacker','tecnico')]:
 call('goto','--url',URL+name+'.html');evaluate('localStorage.removeItem("nota-tema:"+location.pathname);localStorage.removeItem("nota-estilo:"+location.pathname);true');call('reload');call('exec','--command','set viewport 1440 960');call('screenshot')
 assert evaluate('document.documentElement.dataset.theme')==name
 assert evaluate('document.documentElement.dataset.estilo')==style
 for w,h in [(320,740),(390,844),(1440,960)]:
  call('exec','--command',f'set viewport {w} {h}');call('screenshot');d=evaluate((ROOT/'scripts/medir_navegador.js').read_text().replace("closed.forEach(d=>d.open=true)","closed.splice(0,closed.length,...closed.filter(d=>!d.closest('.pagina')||d.closest('.pagina').classList.contains('viva')));closed.forEach(d=>d.open=true)"))
  issue=d['errors']+d['svgTextOverflow']+[c for c in d['contrasts'] if c['ratio']<c['minimum']]
  assert d['documentWidth']==w and not issue,(name,w,issue)
  evaluate('scrollTo(0,0);true');(ROOT/'auditoria/capturas'/f'guia-tema-{name}-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 evaluate('(()=>{const x=document.querySelector(\'[data-elegir-tema][value="sea"]\');x.checked=true;x.dispatchEvent(new Event("change",{bubbles:true}));return true})()');call('reload');assert evaluate('document.documentElement.dataset.theme')=='sea'
 evaluate('localStorage.removeItem("nota-tema:"+location.pathname);true');call('reload')
save('guia-presets.json',{'default':True,'style':True,'reload_preference':True,'viewports':[320,390,1440]})
assert not errors,errors
print(str(len(rows))+' combinaciones de guía y nueve vistas de los presets sin errores.',flush=True)
