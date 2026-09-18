"""Panel escalable, combinaciones y preferencia de audio; navegador Orca local.
Clics de audio nativos. Teclas de pestañas sintéticas: no equivalen a teclado físico.
"""
import re,json,base64
from check_browser import call,evaluate,save,ROOT
URL='http://127.0.0.1:8768/examples/generated/liftit.html'
def open_menu():
 evaluate('scrollTo({top:0,behavior:"instant"});document.querySelector("[data-apariencia-menu] summary").focus();document.querySelector("[data-apariencia-menu]").open=true;true')
def click(name,role='button'):
 snap=call('snapshot')['snapshot'];m=re.search(r'\b'+role+' "'+re.escape(name)+r'"[^\n]*ref=(e\d+)',snap)
 assert m,(name,snap[:1200]);call('click','--element','@'+m[1])
def fresh(reset=False):
 call('goto','--url',URL)
 if reset:
  evaluate('localStorage.removeItem("nota-audio-preferencia");true');call('goto','--url',URL)
 call('exec','--command','set viewport 390 844');evaluate('document.fonts.ready.then(()=>true)')
fresh(True)
initial=evaluate('({preferred:NotaAudio.preferred,enabled:NotaAudio.enabled,state:NotaAudio.state,plays:NotaAudio.plays})')
assert initial==dict(preferred=True,enabled=False,state='uninitialized',plays=0),initial
# Programmatic interaction must not start sound. First actual tab click unlocks without a startup beep.
open_menu();evaluate('document.querySelector("[data-preferencia-tab=temas]").click();true')
assert evaluate('NotaAudio.state')=='uninitialized'
click('Letras','tab');unlocked=evaluate('new Promise(r=>setTimeout(()=>r({preferred:NotaAudio.preferred,enabled:NotaAudio.enabled,state:NotaAudio.state,plays:NotaAudio.plays}),500))')
assert unlocked==dict(preferred=True,enabled=True,state='running',plays=0),unlocked
click('Sonidos activados');assert not evaluate('NotaAudio.preferred||NotaAudio.enabled||NotaAudio.activeVoices')
click('Temas','tab');assert not evaluate('NotaAudio.enabled')
fresh();assert not evaluate('NotaAudio.preferred||NotaAudio.enabled')
open_menu();click('Letras','tab');assert not evaluate('NotaAudio.enabled')
muted={'persists':True,'laterClickDoesNotEnable':True}
# CSS/DOM geometry, all nine palettes, tabs and narrow viewports.
measurements=[]
for width,height in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {width} {height}');open_menu()
 rows=evaluate('''(async()=>{const rows=[],menu=document.querySelector('[data-apariencia-menu]'),panel=menu.querySelector('.apariencia-panel');
 for(const theme of ['light','dark','sea','oliva','arcilla','ciruela','liftit','blueprint','hacker']){
 const input=menu.querySelector('[data-elegir-tema][value="'+theme+'"]');input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));
 for(const tab of menu.querySelectorAll('[data-preferencia-tab]')){
 tab.click();await new Promise(r=>setTimeout(r,25));const r=panel.getBoundingClientRect(),regions=[...panel.querySelectorAll('[role=region]')].filter(x=>x.getClientRects().length).map(x=>{x.scrollTop=x.scrollHeight;return {name:x.getAttribute('aria-label'),focus:x.tabIndex,scroll:x.scrollTop,height:x.clientHeight,content:x.scrollHeight,width:x.clientWidth,contentWidth:x.scrollWidth,overflow:getComputedStyle(x).overflowY}});
 rows.push({theme,tab:tab.dataset.preferenciaTab,viewport:innerWidth,width:document.documentElement.scrollWidth,rect:{left:r.left,right:r.right,top:r.top,bottom:r.bottom},regions,toggleVisible:(()=>{const b=menu.querySelector('[data-audio-global]').getBoundingClientRect();return b.top>=r.top&&b.bottom<=r.bottom&&b.bottom<=innerHeight})()});
 }}return rows;})()''')
 for row in rows:
  assert row['width']==width and row['rect']['left']>=0 and row['rect']['right']<=width+.1 and row['rect']['bottom']<=height+.1,row
  assert row['toggleVisible'],row
  for region in row['regions']:
   assert region['name'] and region['focus']==0 and region['contentWidth']<=region['width']+1,region
   if region['content']>region['height']+1:assert region['scroll']>0 and region['overflow']=='auto',region
 measurements+=rows
 print(width,'px: 27 combinaciones de panel correctas',flush=True)
# Search handles accents, empty results, category intersection, reset and a future larger catalog.
open_menu()
filtered=evaluate('''(()=>{const m=document.querySelector('[data-apariencia-menu]');m.querySelector('[data-preferencia-tab=temas]').click();const s=m.querySelector('[data-buscar-tema]'),f=m.querySelector('[data-familia-tema]');const change=()=>s.dispatchEvent(new Event('input',{bubbles:true}));const visible=()=>[...m.querySelectorAll('[data-tema-familia]:not([hidden]) input')].map(x=>x.value);s.value='calido';change();const accent=visible();f.value='tecnico';f.dispatchEvent(new Event('change',{bubbles:true}));const empty=visible(),status=m.querySelector('[data-temas-resultados]').textContent;m.querySelector('[data-limpiar-temas]').click();const reset=visible();
 const grid=m.querySelector('.apariencia-colores'),original=grid.querySelector('label');for(let i=0;i<40;i++){const label=original.cloneNode(true);label.querySelector('input').value='future-'+i;label.querySelector('input').checked=false;grid.append(label)}change();grid.scrollTop=grid.scrollHeight;const future={count:visible().length,scroll:grid.scrollTop,height:grid.clientHeight,content:grid.scrollHeight};return {accent,empty,status,reset:reset.length,future};})()''')
assert filtered['accent']==['light','dark'] and not filtered['empty'] and filtered['reset']==10 and filtered['future']['count']==50 and filtered['future']['scroll']>0,filtered
# Keyboard semantics and Escape return; events synthetic and explicitly reported.
keyboard=evaluate('''(()=>{const m=document.querySelector('[data-apariencia-menu]'),t=m.querySelector('[data-preferencia-tab=temas]');t.focus();t.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));const right=document.activeElement.dataset.preferenciaTab;document.activeElement.dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true}));const end=document.activeElement.dataset.preferenciaTab;document.activeElement.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));return {right,end,closed:!m.open,focus:document.activeElement===m.querySelector('summary')};})()''')
assert keyboard==dict(right='letras',end='sonido',closed=True,focus=True),keyboard
# Reload removes synthetic extra labels. All type choices, including real font loading.
fresh();open_menu();types=[]
for width,height in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {width} {height}')
 for style in ['editorial','sobrio','tecnico','libro','revista','bitacora']:
  result=evaluate('''(async()=>{const m=document.querySelector('[data-apariencia-menu]');m.querySelector('[data-preferencia-tab=letras]').click();const input=m.querySelector('[data-elegir-estilo][value="'''+style+'''"]');input.checked=true;input.dispatchEvent(new Event('change',{bubbles:true}));await document.fonts.ready;const body=document.querySelector('main section p')||document.querySelector('.bajada');return {style:document.documentElement.dataset.estilo||'editorial',width:document.documentElement.scrollWidth,viewport:innerWidth,title:getComputedStyle(document.querySelector('h1')).fontFamily,body:getComputedStyle(body).fontFamily,literata:document.fonts.check('16px Literata'),loaded:[...document.fonts].filter(f=>f.family==='Literata'&&f.status==='loaded').length};})()''')
  assert result['width']==width,result
  if style in ['libro','revista','bitacora']:assert result['loaded']>0 and 'Literata' in result['body'],result
  types.append(result)
# Verify mute-first click also avoids creating an AudioContext, not merely output.
fresh(True);open_menu();click('Sonidos activados');firstMute=evaluate('({preferred:NotaAudio.preferred,state:NotaAudio.state,plays:NotaAudio.plays})')
assert firstMute==dict(preferred=False,state='uninitialized',plays=0),firstMute
# Leave previews in their authored default, without overwriting the user's preferences on Tailscale origin.
evaluate('localStorage.removeItem("nota-audio-preferencia");localStorage.removeItem("nota-tema:"+location.pathname);localStorage.removeItem("nota-estilo:"+location.pathname);true')
fresh();open_menu()
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}');open_menu();(ROOT/'tests/screenshots'/f'apariencia-temas-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 click('Letras','tab');(ROOT/'tests/screenshots'/f'apariencia-letras-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']));evaluate('document.querySelector("[data-preferencia-tab=temas]").click();true')
save('apariencia-verificacion.json',{'panel':measurements,'types':types,'search':filtered,'keyboardSynthetic':keyboard,'audio':{'initial':initial,'firstTrustedClick':unlocked,'muted':muted,'firstClickMute':firstMute},'limitations':['Teclas simuladas por eventos DOM, no teclado físico ni lector de pantalla.','AudioContext y ausencia de señal de inicio; señal audible medida por otra prueba.','No prueba en el MacBook del usuario.']})
print('81 paneles, 18 combinaciones tipográficas, 50 temas de prueba, búsqueda y audio inicial/silencio persistido: correctos.',flush=True)
