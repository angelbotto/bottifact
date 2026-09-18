"""Matriz visual con Orca: servidor scripts/serve.py --puerto 8768. No requiere paquetes."""
import json,base64
from check_browser import ROOT,call,evaluate,save
from themes import FAMILIES
from contract_artifact import build,recipe
fixture=ROOT/'tests/evidence/temas-prueba.html'
fixture.write_text(build('Prueba de temas',[{'id':'contenido','titulo':'Temas','html':'<section id="prueba"><h2>Colores para leer.</h2><p>Una prueba de superficies, tablas y código.</p></section>'+recipe('barras')+recipe('codigo-lineas')+recipe('terminal')+recipe('explorador')}],theme='editorial',mode='system',document_id='nota-prueba-temas'))
url='http://127.0.0.1:8768/tests/evidence/temas-prueba.html'
try:
 call('goto','--url',url);call('exec','--command','set media light')
 evaluate('localStorage.removeItem("nota-apariencia-v2:/tests/evidence/temas-prueba.html");true')
 call('goto','--url',url)
 checks=[]
 for w,h in [(320,740),(390,844),(1440,960)]:
  call('exec','--command',f'set viewport {w} {h}')
  data=evaluate('''(async()=>{const rows=[],probe=document.createElement('span');document.body.append(probe);
function rgb(v){probe.style.color=v;return getComputedStyle(probe).color.match(/[\\d.]+/g).slice(0,3).map(Number)}
function lum(a){return a.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0)}
function ratio(a,b){const x=lum(rgb(a)),y=lum(rgb(b));return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
const menu=document.querySelector('[data-apariencia-menu]');menu.querySelector('summary').click();
for(const family of FAMILIES)for(const mode of ['light','dark']){
 menu.querySelector(`[data-elegir-tema][value="${family}"]`).click();menu.querySelector(`[data-elegir-modo][value="${mode}"]`).click();await new Promise(requestAnimationFrame);
 const c=getComputedStyle(document.documentElement),r=menu.querySelector('.apariencia-panel').getBoundingClientRect(),fails=[];
 for(const ink of ['tinta','tinta-2','tinta-3','naranja','verde','rojo','azul'])for(const bg of ['papel','panel','panel-2']){const n=ratio(c.getPropertyValue('--'+ink),c.getPropertyValue('--'+bg));if(n<4.5)fails.push({ink,bg,ratio:n});}
 const term=getComputedStyle(document.querySelector('.terminal'));const terminal=ratio(term.getPropertyValue('--term-tinta'),term.getPropertyValue('--term-papel'));
 const swatch=getComputedStyle(menu.querySelector(`[data-muestra-tema="${family}"]`)).backgroundColor;
 rows.push({family,mode,width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,menu:{left:r.left,right:r.right,top:r.top,bottom:r.bottom},fails,terminal,swatch,previewMatches:rgb(swatch).join(',')===rgb(c.getPropertyValue('--papel')).join(','),modeChecked:menu.querySelector('[data-elegir-modo]:checked').value,familyChecked:menu.querySelector('[data-elegir-tema]:checked').value});
}
menu.open=false;probe.remove();return rows})()'''.replace('FAMILIES',json.dumps(FAMILIES)))
  for r in data:
   assert r['width']==w and not r['overflow'],r
   assert r['menu']['left']>=0 and r['menu']['right']<=w+1 and r['menu']['top']>=0 and r['menu']['bottom']<=h+1,r
   assert not r['fails'] and r['terminal']>=4.5 and r['previewMatches'],r
   assert r['familyChecked']==r['family'] and r['modeChecked']==r['mode'],r
  checks+=data
  print(f'{w}px: {2*len(FAMILIES)} paletas, contraste de tres superficies, terminal y panel comprobados.',flush=True)
 # Cambiar el SO de verdad a través de media emulation, no un evento sintético del componente.
 evaluate("NotaTemas.set({family:'github',mode:'system'})")
 systems=[]
 for system in ['dark','light']:
  call('exec','--command','set media '+system);evaluate('new Promise(requestAnimationFrame)')
  value=evaluate('NotaTemas.get()');assert value['effective']==system and value['family']=='github' and value['mode']=='system',value;systems.append(value)
 evaluate("NotaTemas.set({family:'solarized',mode:'light'})");call('exec','--command','set media dark');evaluate('new Promise(requestAnimationFrame)');assert evaluate('NotaTemas.get().effective')=='light'
 call('goto','--url',url);assert evaluate('NotaTemas.get().family')=='solarized' and evaluate('NotaTemas.get().mode')=='light'
 # Búsqueda y categorías con catálogo sin duplicados de modo.
 filtered=evaluate('''(()=>{const m=document.querySelector('[data-apariencia-menu]');m.querySelector('summary').click();const input=m.querySelector('[data-buscar-tema]');input.value='catppuccin';input.dispatchEvent(new Event('input'));const count=m.querySelectorAll('[data-tema-familia]:not([hidden])').length;m.querySelector('[data-limpiar-temas]').click();const cat=m.querySelector('[data-familia-tema]');cat.value='editor';cat.dispatchEvent(new Event('change'));const editors=m.querySelectorAll('[data-tema-familia]:not([hidden])').length;const soundInThemes=m.querySelector('[data-preferencia-panel="temas"] [data-audio-global]')!==null;return {count,editors,soundInThemes}})()''')
 assert filtered=={'count':1,'editors':4,'soundInThemes':False},filtered
 save('temas-matriz.json',{'casos':checks,'sistema':systems,'filtros':filtered,'limites':['DOM y estilos calculados; no acredita lector de pantalla ni audición humana.']})
 print('Sistema, selección persistente, búsqueda y categorías correctos.',flush=True)
finally:
 fixture.unlink(missing_ok=True)
 call('exec','--command','set media light')
 call('goto','--url','http://127.0.0.1:8768/examples/generated/themes.html')
