"""Geometría de controles reales y panel de revisión en ambos esquemas del sistema."""
import json,base64,uuid
from comprobar_navegador import ROOT,call,evaluate,save
from contrato_artefacto import build
fixture=ROOT/'auditoria/colaboracion-ui-prueba.html'
fixture.write_text(build('Prueba UI',[{'id':'contenido','titulo':'Prueba','html':(ROOT/'ejemplos/colaborativo-contenido.html').read_text()}],document_id='prueba-ui-'+uuid.uuid4().hex,theme='linear-light',style='sobrio'))
try:
 call('goto','--url','http://127.0.0.1:8768/auditoria/colaboracion-ui-prueba.html');call('screenshot')
 evaluate('''(()=>{document.querySelector('.revision-barra [data-revision-modo]').click();document.getElementById('cita-revision').click();const t=document.querySelector('[data-revision-texto]');t.value='¿Podemos enlazar la evidencia de esta decisión?';t.dispatchEvent(new Event('input'));document.querySelector('[data-revision-guardar]').click();return true})()''')
 records=[]
 for scheme in ['light','dark']:
  call('exec','--command','set media '+scheme)
  for w,h in [(320,740),(390,844),(1440,960)]:
   call('exec','--command',f'set viewport {w} {h}')
   for theme in ['linear-light','linear-dark']:
    call('exec','--command',f'set viewport {w} {h}')
    evaluate('document.querySelector(\'[data-elegir-tema][value="'+theme+'"]\').click();true')
    r=evaluate('''(()=>{const m=document.querySelector('[data-apariencia-menu]');m.open=true;const p=m.querySelector('.apariencia-panel'),r=p.getBoundingClientRect();return {theme:document.documentElement.dataset.theme,dark:m.dataset.oscuro,paper:getComputedStyle(document.documentElement).getPropertyValue('--papel').trim(),width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,box:{x:r.left,y:r.top,right:r.right,bottom:r.bottom}}})()''')
    assert r['dark']==str(theme=='linear-dark').lower() and r['paper']==('#ffffff' if theme=='linear-light' else '#101114') and not r['overflow'],r
    # Wait a frame without screenshot: Orca captures can reset the viewport to the host size.
    evaluate('new Promise(requestAnimationFrame)');evaluate('document.querySelector("[data-apariencia-menu]").open=false;document.querySelector(".revision-barra [data-revision-lista]").click();true');evaluate('new Promise(requestAnimationFrame)')
    panel=evaluate('''(()=>{const p=document.querySelector('[data-revision-panel]'),r=p.getBoundingClientRect();return {width:innerWidth,height:innerHeight,left:r.left,right:r.right,top:r.top,bottom:r.bottom,overflow:p.scrollWidth>p.clientWidth}})()''')
    assert panel['width']==w and panel['left']>=0 and panel['right']<=panel['width']+1 and panel['top']>=0 and panel['bottom']<=panel['height']+1 and not panel['overflow'],panel
    records.append({'system':scheme,'theme':theme,'menu':r,'panel':panel})
    if scheme=='light' and w==1440:
     (ROOT/'auditoria/capturas'/f'colaboracion-panel-{theme}-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
    evaluate('document.querySelector("[data-revision-cerrar]").click();true')
 save('colaboracion-ui.json',records)
 evaluate('''(()=>{const p='nota-revision-v2:'+encodeURIComponent(document.querySelector('meta[name="nota-documento"]').content)+':';Object.keys(localStorage).filter(k=>k.startsWith(p)).forEach(k=>localStorage.removeItem(k));return true})()''')
 print('Dos temas, tres anchos y ambos esquemas del sistema: selección e interfaz de revisión correctas.')
finally:
 fixture.unlink(missing_ok=True)
 call('exec','--command','set media light')
 call('goto','--url','http://127.0.0.1:8768/colaborativo.html')
