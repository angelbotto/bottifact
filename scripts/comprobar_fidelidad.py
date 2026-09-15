"""Fuentes reales, cancelación, arrastre de galería y medidas en seis paletas con Orca."""
import json,base64
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/biblioteca.html');call('exec','--command','set viewport 1440 960');call('exec','--command','set media light');evaluate('document.fonts.ready.then(()=>true)')
def frame():call('screenshot')
def link(name):evaluate('document.querySelector(\'.catalogo-indice a[href="#receta-'+name+'"]\').click();true');frame()
r=evaluate('(()=>{const a=NotaMano.get(document.getElementById("nota-decision"));return {font:a.font,played:a.played,paths:a.paths.length,characters:a.characters.length}})()');assert r['font'] and not r['played'] and r['paths']==0 and r['characters']>20,r
link('manuscrita')
r=evaluate('(()=>{const a=NotaMano.get(document.getElementById("nota-decision"));return {playing:a.animations.length>0,visible:a.visible,opacity:a.characters.map(x=>+getComputedStyle(x).opacity),duration:a.duration,fonts:getComputedStyle(a.element).fontFamily,sound:NotaAudio.enabled}})()');assert r['playing'] and r['visible'] and not r['sound'] and 'Reenie Beanie' in r['fonts'],r
before=sum(r['opacity']);evaluate('new Promise(r=>setTimeout(()=>r(true),180))');after=evaluate('NotaMano.get(document.getElementById("nota-decision")).characters.reduce((s,x)=>s+(+getComputedStyle(x).opacity),0)');assert after>before
link('galeria');assert evaluate('NotaMano.get(document.getElementById("nota-decision")).animations.length')==0
link('manuscrita');assert evaluate('NotaMano.get(document.getElementById("nota-decision")).animations.length')==0
r=evaluate('(()=>{const e=document.getElementById("nota-decision"),a=NotaMano.get(e);a.play();Object.defineProperty(a.motion,"matches",{configurable:true,value:true});a.motion.dispatchEvent(new Event("change"));const result={cancelled:a.animations.length===0,complete:a.characters.every(x=>+getComputedStyle(x).opacity===1),buttons:a.buttons.every(({b})=>b.disabled)};delete a.motion.matches;const original=a.text;a.destroy();result.restored=e.textContent===original&&!e.querySelector(".mano-fuente");NotaMano.init(e);return result})()');assert all(r.values()),r
save('fidelidad-escritura.json',{'entry':True,'progress':True,'exit':True,'one_entry':True,'reduced_and_destroy':r,'method':'Frames de Orca; reducción por evento MQL explícito, sin lector de pantalla.'})
link('galeria');evaluate('document.querySelector(".galeria-pista").scrollLeft=0;window.dragEvents=[];document.querySelector(".galeria-pista").addEventListener("pointerdown",e=>dragEvents.push({trusted:e.isTrusted,type:e.pointerType}));true');frame()
p=evaluate('(()=>{const t=document.querySelector(".galeria-pista"),r=t.getBoundingClientRect();return {x:r.left+Math.min(400,r.width-30),y:r.top+80}})()')
call('mouse','move','--x',str(round(p['x'])),'--y',str(round(p['y'])));call('mouse','down','--button','left');call('mouse','move','--x',str(round(p['x']-180)),'--y',str(round(p['y'])));call('mouse','up','--button','left');frame()
r=evaluate('(()=>{const t=document.querySelector(".galeria-pista");return {left:t.scrollLeft,cursor:getComputedStyle(t).cursor,released:!t.classList.contains("arrastrando"),events:dragEvents,headings:document.querySelector("[data-galeria]").querySelectorAll("h3,.procedencia").length}})()');assert r['left']>100 and r['released'] and r['headings']==0 and any(x['trusted'] for x in r['events']),r;save('fidelidad-arrastre.json',r)
rows=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
  for name in ['apuntes','manuscrita','galeria']:
   link(name);evaluate('document.querySelectorAll("[data-mano],[data-subrayar]").forEach(e=>NotaMano.get(e)?.finish());true')
   d=file('medir_navegador.js');assert d['documentWidth']==w and not d['errors'] and not d['svgTextOverflow'],d
   assert all(c['ratio']>=c['minimum'] for c in d['contrasts']),d['contrasts']
   for region in d['regions']:assert region['inside'] and region['focus']==0 and region['name'] and (region['content']<=region['width']+1 or region['end']>0),region
   rows.append({'viewport':[w,h],'theme':theme,'recipe':name,'documentWidth':d['documentWidth']})
  print(w,theme,'fuente/apuntes/galería sin recorte',flush=True)
 for name in ['apuntes','manuscrita','galeria']:
  link(name);evaluate('document.documentElement.dataset.theme="dark";document.querySelectorAll("[data-mano],[data-subrayar]").forEach(e=>NotaMano.get(e)?.finish());true')
  if name=='galeria':evaluate('document.querySelector(".galeria-pista").scrollLeft=0;true')
  Path(f'auditoria/capturas/fidelidad-{name}-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
save('fidelidad-pantallas.json',rows)
print('54 combinaciones, entrada/repetición/cancelación y arrastre nativo correctos.')
