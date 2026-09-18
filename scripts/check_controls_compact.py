"""Controles discretos: geometría, accesibilidad, copia y edición en Orca."""
import json,base64
from check_browser import call,evaluate,ROOT,save
call('goto','--url','http://127.0.0.1:8768/examples/generated/guide.html');call('screenshot')
rows=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 evaluate('document.querySelector("[data-ir=voz]").click();true');call('screenshot')
 replay=evaluate('''(()=>[...document.querySelectorAll('[data-mano-repetir]')].filter(e=>e.getClientRects().length).map(e=>({icon:!!e.querySelector('svg'),name:e.getAttribute('aria-label'),width:e.getBoundingClientRect().width,text:e.textContent})))()''')
 assert replay and all(x['icon'] and x['name'] and x['width']<=44 and not x['text'].strip() for x in replay),replay
 evaluate('document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true');call('screenshot')
 panel=evaluate('''(()=>{const menu=document.querySelector('[data-apariencia-menu]'),r=menu.querySelector('.apariencia-panel').getBoundingClientRect();const out={inside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,width:r.width,panels:[]};for(const tab of menu.querySelectorAll('[data-preferencia-tab]')){tab.click();const button=menu.querySelector('[data-audio-global]');out.panels.push({name:tab.dataset.preferenciaTab,sound:!!button.getClientRects().length});}menu.querySelector('[data-preferencia-tab=temas]').click();return out})()''')
 assert panel['inside'] and panel['width']==min(560,w-24),panel
 assert all(p['sound']==(p['name']=='sonido') for p in panel['panels']),panel
 (ROOT/'tests/screenshots'/f'compacto-temas-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 # Each palette preserves the three panels and local scrolling; no document overflow.
 theme=evaluate('''(()=>{const menu=document.querySelector('[data-apariencia-menu]'),out=[];for(const t of ['light','dark','sea','oliva','arcilla','ciruela','liftit','blueprint','hacker']){menu.querySelector('[data-elegir-tema][value='+t+']').click();const p=menu.querySelector('.apariencia-panel'),r=p.getBoundingClientRect(),grid=menu.querySelector('.apariencia-colores');grid.scrollTop=grid.scrollHeight;out.push({theme:t,inside:r.left>=0&&r.right<=innerWidth&&r.bottom<=innerHeight,width:document.documentElement.scrollWidth,scroll:grid.scrollHeight<=grid.clientHeight+1||grid.scrollTop>0});}menu.open=false;return out})()''')
 assert all(t['inside'] and t['width']==w and t['scroll'] for t in theme),theme
 evaluate('document.querySelector("[data-ir=piezas-prototipos]").click();document.querySelector(".visor-herramientas").scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot')
 visor=evaluate('''(()=>{const root=document.querySelector('[data-visor]'),v=NotaVisores.get(root),out={sizes:[]};for(const raw of ['390','768','1024']){const b=root.querySelector('[data-ancho-visor="'+raw+'"]');b.click();out.sizes.push({width:parseFloat(v.host.style.width),expected:+raw,icon:!!b.querySelector('svg'),name:b.getAttribute('aria-label')});}v.setAspect('16/9');root.querySelector('[data-girar-visor]').click();out.rotated=v.rotated&&parseFloat(v.host.style.width)===576;if(!v.fit)root.querySelector('[data-ajustar-visor]').click();out.fit=v.wrapper.getBoundingClientRect().width<=v.box.clientWidth+1;out.inside=document.documentElement.scrollWidth===innerWidth;return out})()''')
 assert all(x['width']==x['expected'] and x['icon'] and x['name'] for x in visor['sizes']) and visor['rotated'] and visor['fit'] and visor['inside'],visor
 (ROOT/'tests/screenshots'/f'compacto-visor-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 evaluate('(()=>{document.querySelector("[data-ir=manual]").click();document.querySelector(".revision-barra [data-revision-modo]").click();const t=document.querySelector(".pagina.viva .bajada");t.focus();t.dispatchEvent(new KeyboardEvent("keydown",{key:"Enter",bubbles:true}));return true})()');call('screenshot')
 comment=evaluate('''(()=>{const e=document.querySelector('[data-revision-editor]'),input=e.querySelector('textarea'),r=e.getBoundingClientRect(),out={shortHeight:r.height,inside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,contextClosed:!e.querySelector('details').open,buttons:[...e.querySelectorAll('button')].every(b=>b.querySelector('svg')&&b.getAttribute('aria-label'))};input.value='Dar más aire a esta explicación.';input.dispatchEvent(new Event('input'));out.send=!e.querySelector('[data-revision-guardar]').disabled;return out})()''')
 assert comment['shortHeight']<=140 and all(comment[k] for k in ['inside','contextClosed','buttons','send']),comment
 (ROOT/'tests/screenshots'/f'compacto-comentario-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 large=evaluate('''(()=>{const e=document.querySelector('[data-revision-editor]'),input=e.querySelector('textarea');input.value='Contexto detallado. '.repeat(160);input.dispatchEvent(new Event('input'));const r=e.getBoundingClientRect();return {height:input.getBoundingClientRect().height,scroll:input.scrollHeight>input.clientHeight,inside:r.top>=0&&r.bottom<=innerHeight}})()''');assert large['height']<=160 and large['scroll'] and large['inside'],large
 evaluate('document.querySelector("[data-revision-cancelar]").click();true')
 rows.append({'width':w,'replay':replay,'appearance':panel,'themes':theme,'visor':visor,'comment':comment,'longComment':large});print(w,'px: apuntes, temas, visor y comentarios correctos',flush=True)
call('goto','--url','http://127.0.0.1:8768/examples/generated/hacker.html');call('screenshot')
copy=evaluate('''(async()=>{const write=navigator.clipboard.writeText,out=[];try{for(const b of document.querySelectorAll('.codigo [data-copiar],.terminal [data-copiar]')){let copied;navigator.clipboard.writeText=async text=>{copied=text};const source=document.getElementById(b.dataset.copiar).textContent;b.click();await new Promise(r=>setTimeout(r,10));out.push({name:b.getAttribute('aria-label'),icon:!!b.querySelector('svg'),text:b.textContent,exact:copied===source});}}finally{navigator.clipboard.writeText=write}return out})()''');assert all(x['icon'] and x['name'] and not x['text'] and x['exact'] for x in copy),copy
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}');evaluate('document.querySelector(".codigo-sin-titulo").scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot');(ROOT/'tests/screenshots'/f'compacto-codigo-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
save('controles-compactos.json',{'layouts':rows,'copy':copy,'limits':['Viewports emulados con Orca. Sin prueba física de MacBook o lector de pantalla.','Copia comprobada interceptando clipboard.writeText, sin alterar el portapapeles del usuario.']})
print('Controles compactos y copia exacta correctos.',flush=True)
