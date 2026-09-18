"""Integración de flota: observer real, contraste y recetas anchas en la guía."""
import json,base64
from check_browser import call,evaluate,save,ROOT
call('goto','--url','http://127.0.0.1:8768/examples/generated/liftit.html');call('exec','--command','set viewport 1440 960');call('screenshot')
evaluate('window.fleet=NotaFlota.get(document.querySelector("[data-flota]"));fleet.stage.scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot')
lifecycle={}
fleet_state='({frames:fleet.frames,visible:fleet.visible,frame:fleet.frame,playing:fleet.playing})'
evaluate('fleet.play.click();true');call('screenshot');state=evaluate(fleet_state);lifecycle['running']=state['visible'] and state['frames']>0 and state['playing']
evaluate("document.querySelector('footer').scrollIntoView({block:'end',behavior:'instant'});true");call('screenshot');state=evaluate(fleet_state);before=state['frames'];after=evaluate('new Promise(r=>setTimeout(()=>r(fleet.frames),150))');lifecycle['outside']=not state['visible'] and not state['frame'] and before==after
evaluate('fleet.stage.scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot');state=evaluate(fleet_state);lifecycle['resume']=state['visible'] and state['frames']>before and bool(state['frame'])
evaluate('fleet.play.click();true');state=evaluate(fleet_state);lifecycle['pause']=not state['frame'] and not state['playing']
assert all(lifecycle.values()),lifecycle
contrasts=evaluate('''(async()=>{const rows=[];for(const theme of ['light','dark','sea','oliva','arcilla','ciruela','liftit','blueprint','hacker']){document.documentElement.dataset.theme=theme;await new Promise(r=>setTimeout(r,35));const css=getComputedStyle(fleet.element),ctx=document.createElement('canvas').getContext('2d'),col=x=>{ctx.clearRect(0,0,1,1);ctx.fillStyle=css.getPropertyValue(x).trim();ctx.fillRect(0,0,1,1);const [r,g,b]=ctx.getImageData(0,0,1,1).data;return new THREE.Color().setRGB(r/255,g/255,b/255,THREE.SRGBColorSpace)},lum=c=>.2126*c.r+.7152*c.g+.0722*c.b,ratio=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05);rows.push({theme,routes:[1,2,3,4].flatMap(n=>['--flota-territorio','--flota-oceano'].map(bg=>ratio(col('--grafica-'+n),col(bg)))),point:ratio(col('--flota-punto'),col('--flota-territorio')),labels:ratio(col('--tinta'),col('--papel')),mutation:fleet.earth.material.color.equals(col('--flota-oceano'))});}return rows})()''')
for row in contrasts:assert min(row['routes'])>=3 and row['point']>=3 and row['labels']>=4.5 and row['mutation'],row
routes=evaluate('''(()=>fleet.model.data.map(row=>{fleet.select(row.id);const s=fleet.surface.getBoundingClientRect(),curve=fleet.routes[fleet.model.data.indexOf(row)].curve,points=[curve.getPoint(0),curve.getPoint(1)].map(p=>fleet.point(p));return {id:row.id,endpoints:points.every(p=>p.x>=0&&p.x<=s.width&&p.y>=0&&p.y<=s.height),names:fleet.cityLabels.filter(x=>!x.el.hidden).length===2,pinPixels:fleet.pins[0].scale.x*.0048/fleet.camera.top*s.height};}))()''')
assert all(r['endpoints'] and r['names'] and abs(r['pinPixels']-10)<.001 for r in routes),routes
queue=evaluate('''(()=>{const e=document.querySelector('#cola-novedades-ejemplo'),form=e.querySelector('form');form.elements.estado.value='Con novedad';form.elements.grupo.value='1';form.dispatchEvent(new Event('change'));const out={row:e.querySelectorAll('tbody tr:has(td[data-valor])').length===1,id:e.querySelector('tbody tr:has(td[data-valor])').textContent.includes('LFT-034'),orders:e.querySelector('[data-explorador-estado]').textContent.includes('12 pedidos')};form.reset();return out})()''');assert all(queue.values()),queue
measurement=(ROOT/'scripts/measure_browser.js').read_text().replace("closed.forEach(d=>d.open=true)","closed.splice(0,closed.length,...closed.filter(d=>!d.closest('.pagina')||d.closest('.pagina').classList.contains('viva')));closed.forEach(d=>d.open=true)")
records=[]
for page in ['liftit','guia']:
 call('goto','--url','http://127.0.0.1:8768/'+page+'.html');call('screenshot')
 if page=='guia':assert evaluate('document.querySelector("#guia-logistica").textContent.includes("Logística")')
 for width,height in [(320,740),(390,844),(1440,960)]:
  call('exec','--command',f'set viewport {width} {height}')
  for chapter in (['documento'] if page=='liftit' else ['piezas-reportes','piezas-tablas','piezas-expresion','componer']):
   if page=='guia':evaluate('document.querySelector(\'[data-ir="'+chapter+'"]\').click();true')
   call('screenshot')
   batch=evaluate('''(async()=>{const rows=[];for(const theme of ['light','dark','sea','oliva','arcilla','ciruela','liftit','blueprint','hacker']){document.documentElement.dataset.theme=theme;await new Promise(r=>setTimeout(r,35));const m=await '''+measurement.rstrip().rstrip(';')+''';rows.push({theme,documentWidth:m.documentWidth,errors:[...m.errors,...m.svgTextOverflow,...m.contrasts.filter(c=>c.ratio<c.minimum),...m.regions.filter(r=>!(r.inside&&r.focus===0&&r.name&&(r.content<=r.width+1||r.end>0)))]});}return rows})()''')
   for r in batch:assert r['documentWidth']==width and not r['errors'],(page,chapter,width,r)
   records.append({'page':page,'chapter':chapter,'width':width,'checks':batch});print(page,chapter,width,'px: nueve paletas correctas',flush=True)
# Final visual captures after changing the terrain token and constant-size geometry.
call('goto','--url','http://127.0.0.1:8768/examples/generated/liftit.html');call('screenshot')
for width,height in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {width} {height}')
 for mode in ['world','region','route']:
  evaluate('(()=>{document.documentElement.dataset.theme="liftit";const f=NotaFlota.get(document.querySelector("[data-flota]"));f.buttons.'+mode+'.click();f.stage.scrollIntoView({block:"center",behavior:"instant"});return true})()');call('screenshot');(ROOT/'tests/screenshots'/f'flota-{mode}-{width}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
save('flota-integracion.json',{'lifecycleRealScroll':lifecycle,'contrasts':contrasts,'routes':routes,'queue':queue,'layouts':records})
print('Observer real, contraste, tres rutas, novedades y 135 vistas de integración correctos.',flush=True)
