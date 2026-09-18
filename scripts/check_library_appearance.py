import sys,json
sys.path.insert(0,'scripts')
from check_browser import call,evaluate,save
call('goto','--url','http://127.0.0.1:8768/examples/generated/library.html#configuracion')
checks=[]
for w,h in [(320,740),(390,844)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  r=evaluate('''(()=>{const theme=THEME,m=document.querySelector('[data-apariencia-menu]');m.querySelector('[data-elegir-tema][value="'+theme+'"]').click();scrollTo({top:0,behavior:'instant'});m.open=true;dispatchEvent(new Event('resize'));const p=m.querySelector('.apariencia-panel').getBoundingClientRect();const r={theme:document.documentElement.dataset.theme,icon:m.dataset.oscuro,inside:p.left>=0&&p.right<=innerWidth&&p.top>=0&&p.bottom<=innerHeight,width:document.documentElement.scrollWidth,viewport:innerWidth};m.open=false;return r;})()'''.replace('THEME',json.dumps(theme)))
  assert r['theme']==theme and r['icon']==str(theme in ['dark','sea','ciruela']).lower() and r['inside'] and r['width']==w,r
  checks.append(r)
r=evaluate('''(()=>{const f=document.querySelector('[data-config-editorial] form');f.elements.disposicion.value='lista';f.dispatchEvent(new Event('change'));document.querySelector('[data-config-editorial] a').click();return {page:document.querySelector('.pagina.viva').id,hash:location.hash,columns:getComputedStyle(document.querySelector('[data-publicaciones]')).gridTemplateColumns};})()''');assert r['page']=='publicaciones' and r['hash']=='#archivo-ejemplo',r
save('biblioteca-apariencia.json',{'combinaciones':checks,'configuracion_enlace':r})
print('12 comprobaciones de apariencia + enlace del configurador correctos')
