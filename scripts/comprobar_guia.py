"""Guía y nuevos temas con el navegador Orca. Medidas, no audición humana."""
import json,base64
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save,ROOT
from contrato_artefacto import THEMES
URL='http://127.0.0.1:8768/'
call('goto','--url',URL+'guia.html');call('exec','--command','set viewport 1440 960');evaluate('document.fonts.ready.then(()=>true)')
pages=evaluate('[...document.querySelectorAll("main > .pagina")].map(x=>x.id)')
assert len(pages)==13,pages
assert evaluate('document.querySelectorAll("[data-guia-componente]").length')==len(json.loads((ROOT/'registro.json').read_text())['componentes'])
rows=[];errors=[]
measurement=(ROOT/'scripts/medir_navegador.js').read_text().replace("closed.forEach(d=>d.open=true)","closed.splice(0,closed.length,...closed.filter(d=>!d.closest('.pagina')||d.closest('.pagina').classList.contains('viva')));closed.forEach(d=>d.open=true)")
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for page in pages:
  evaluate('document.querySelector(\'[data-ir="'+page+'"]\').click();true');call('screenshot')
  # Un frame de entrada por página. Cada paleta fuerza layout y espera sus observers;
  # agrupar nueve mediciones evita nueve transportes de captura sin cambiar las comprobaciones.
  batch=evaluate("""(async()=>{const results=[];for(const theme of """+json.dumps(THEMES[1:])+"""){
   const input=document.querySelector('[data-elegir-tema][value="'+theme+'"]');input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));
   await new Promise(r=>setTimeout(r,50));const d=await """+measurement.rstrip().rstrip(';')+""";
   const errors=[...d.errors,...d.svgTextOverflow,...d.contrasts.filter(c=>c.ratio<c.minimum)];
   if(d.documentWidth!==innerWidth)errors.push('Desborde: '+d.documentWidth);
   for(const r of d.regions)if(!(r.inside&&r.focus===0&&r.name&&(r.content<=r.width+1||r.end>0)))errors.push(r);
   results.push({viewport:[innerWidth,innerHeight],theme:d.theme,page:"""+json.dumps(page)+""",documentWidth:d.documentWidth,regions:d.regions.length,errors});
  }return results})()""")
  assert len(batch)==9,batch
  rows+=batch;errors+=[row for row in batch if row['errors']];save('guia-navegador.json',rows)
  print(w,page,'nueve temas;',len(errors),'fallos acumulados',flush=True)
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
