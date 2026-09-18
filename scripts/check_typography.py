"""Toda la guía con las seis combinaciones a 320 y 390 px. Sólo navegador Orca local."""
import json
from check_browser import call,evaluate,save,ROOT
call('goto','--url','http://127.0.0.1:8768/examples/generated/guide.html');evaluate('document.fonts.ready.then(()=>true)')
pages=evaluate('[...document.querySelectorAll("main > .pagina")].map(x=>x.id)')
measurement=(ROOT/'scripts/measure_browser.js').read_text().replace("closed.forEach(d=>d.open=true)","closed.splice(0,closed.length,...closed.filter(d=>!d.closest('.pagina')||d.closest('.pagina').classList.contains('viva')));closed.forEach(d=>d.open=true)")
rows=[]
for width,height in [(320,740),(390,844)]:
 call('exec','--command',f'set viewport {width} {height}')
 for page in pages:
  evaluate('document.querySelector(\'[data-ir="'+page+'"]\').click();true');call('screenshot')
  batch=evaluate('''(async()=>{const rows=[];for(const style of ['editorial','sobrio','tecnico','libro','revista','bitacora']){const input=document.querySelector('[data-elegir-estilo][value="'+style+'"]');input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));await document.fonts.ready;await new Promise(r=>setTimeout(r,30));const d=await '''+measurement.rstrip().rstrip(';')+''';const errors=[...d.errors,...d.svgTextOverflow];if(d.documentWidth!==innerWidth)errors.push('Desborde: '+d.documentWidth);for(const r of d.regions)if(!(r.inside&&r.focus===0&&r.name&&(r.content<=r.width+1||r.end>0)))errors.push(r);rows.push({style,viewport:innerWidth,page:'''+json.dumps(page)+''',errors});}return rows})()''')
  rows+=batch;save('tipografia-guia.json',rows);assert all(not r['errors'] for r in batch),batch
  print(width,page,': seis estilos correctos',flush=True)
evaluate('localStorage.removeItem("nota-estilo");true')
print(len(rows),'combinaciones de tipografía y página correctas.',flush=True)
