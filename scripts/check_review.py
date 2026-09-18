"""Controles, copia, comentarios, importación y escritura de esta ampliación."""
import sys,json,base64
from pathlib import Path
from check_browser import call,evaluate,file,save
BASE='http://127.0.0.1:8768'
def fresh(hash=''):call('goto','--url','about:blank');call('goto','--url',BASE+'/examples/generated/library.html'+hash);evaluate('document.fonts.ready.then(()=>true)')
def settle():evaluate('new Promise(r=>setTimeout(()=>r(true),150))');call('screenshot')
fresh();call('exec','--command','set viewport 390 844');r=file('tests_review.js');save('revision-interaccion.json',r);assert not r['failed'],r
fresh();records=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  r=evaluate('''(()=>{document.querySelector('[data-elegir-tema][value="THEME"]').click();document.querySelector('[data-ir=configuracion]').click();
   const term=document.querySelector('.terminal'),header=term.querySelector('.cab'),b=header.querySelector('button'),hb=header.getBoundingClientRect(),bb=b.getBoundingClientRect();
   document.querySelector('.revision-barra [data-revision-lista]').click();const dialog=document.querySelector('[data-revision-panel]'),d=dialog.getBoundingClientRect();
   const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d'),lum=color=>{ctx.fillStyle=color;ctx.fillRect(0,0,1,1);const rgb=[...ctx.getImageData(0,0,1,1).data].slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return rgb.reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);};
   const ratio=(a,b)=>(Math.max(lum(a),lum(b))+.05)/(Math.min(lum(a),lum(b))+.05),root=getComputedStyle(document.documentElement),panel=root.getPropertyValue('--panel');
   const contrasts=['--naranja','--verde','--azul'].map(token=>({token,ratio:ratio(root.getPropertyValue(token),panel)}));contrasts.push({token:'terminal tenue',ratio:ratio(getComputedStyle(header).color,getComputedStyle(term).backgroundColor)});
   const bar=document.querySelector('.revision-barra').getBoundingClientRect();dialog.close();
   const result={viewport:[innerWidth,innerHeight],theme:'THEME',buttonGap:hb.right-bb.right,buttonHeight:bb.height,dialog:{left:d.left,right:d.right,top:d.top,bottom:d.bottom},bar:{left:bar.left,right:bar.right,bottom:bar.bottom},contrasts,documentWidth:document.documentElement.scrollWidth};return result;
  })()'''.replace('THEME',theme))
  assert r['documentWidth']==w and r['buttonHeight']>=44 and 16<=r['buttonGap']<=20,r
  assert r['dialog']['left']>=0 and r['dialog']['right']<=w and r['dialog']['top']>=0 and r['dialog']['bottom']<=h,r
  assert r['bar']['left']>=0 and r['bar']['right']<=w and r['bar']['bottom']<=h,r
  assert all(c['ratio']>=4.5 for c in r['contrasts']),r
  records.append(r)
save('revision-pantallas.json',records)
# Comparar todo el HTML coloreado con el registro, sin red desde el artefacto.
registry=json.loads(Path('packages/core/registry/registry.json').read_text())
for item in registry['componentes']:
 assert evaluate('document.getElementById('+json.dumps('biblioteca-codigo-'+item['id'])+').textContent')==item['html'],item['id']
# La escritura debe esperar al viewport, ejecutarse una vez y respetar reduce.
fresh();call('exec','--command','set viewport 1440 960');call('exec','--command','set media light');settle()
r=evaluate('window.writing=NotaEscritura.get(document.querySelector("[data-escritura]"));({played:writing.played,animations:writing.animations.length})');assert not r['played'] and r['animations']==0,r
evaluate('document.querySelector("[data-ir=configuracion]").click();scrollTo({top:document.querySelector(".escritura-caja").getBoundingClientRect().top+scrollY-90,behavior:"instant"});true');settle()
visible=evaluate('({played:writing.played,visible:writing.visible,animations:writing.animations.length,audio:NotaSonido.get(writing.element).enabled})');assert visible['played'] and visible['visible'] and visible['animations']>0 and not visible['audio'],visible
call('exec','--command','set media reduced-motion');evaluate('writing.motion.dispatchEvent(new MediaQueryListEvent("change",{matches:writing.motion.matches,media:writing.motion.media}));true');settle();assert evaluate('writing.animations.length')==0
save('revision-escritura.json',{'before':r,'visible':visible,'reducedAnimations':0,'metodo':'Orca viewport/scroll real; media emulada y evento MQL explícito. Sin gesto de audio.'});call('exec','--command','set media light')
# Capturas para inspección.
fresh('#receta-archivo');call('exec','--command','set viewport 1024 900');settle();evaluate('document.querySelector("[data-elegir-tema][value=light]").click();document.querySelector("[data-papel-tramado]").click();const c=document.querySelector("#biblioteca-codigo-archivo").closest("details");c.open=true;c.scrollIntoView({behavior:"instant"});true');settle();Path('tests/screenshots/revision-codigo.png').write_bytes(base64.b64decode(call('screenshot')['data']))
print('Revisión: ocho interacciones, 18 combinaciones, 71 fuentes intactas y escritura al entrar/reduce correctas')
