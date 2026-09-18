"""Geometría de los ajustes de /work; usa el navegador compartido de Orca."""
import json,base64
from pathlib import Path
from check_browser import call,evaluate,save
call('goto','--url','about:blank');call('goto','--url','http://127.0.0.1:8768/examples/generated/priorities.html')
records=[]
for w,h in [(320,740),(390,844),(1440,960)]:
 call('exec','--command',f'set viewport {w} {h}')
 for theme in ['light','dark','sea','oliva','arcilla','ciruela']:
  evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';document.querySelector("[data-ir=piezas]").click();true')
  r=evaluate('''(()=>{const a=document.querySelector('[data-actividad]'),d=document.getElementById(a.dataset.actividadTabla),ar=a.getBoundingClientRect(),dr=d.getBoundingClientRect(),c=getComputedStyle(a),line=document.querySelector('.cronologia-vertical'),lc=getComputedStyle(line,'::before'),lis=[...line.children],last=lis.at(-1).getBoundingClientRect(),lr=line.getBoundingClientRect(),g=document.querySelector('.galeria-pista'),f=g.querySelector('figure'),fr=f.getBoundingClientRect(),caption=f.querySelector('figcaption'),cr=caption.getBoundingClientRect();return {viewport:innerWidth,theme:document.documentElement.dataset.theme,overflow:document.documentElement.scrollWidth>innerWidth,dataOutside:!a.contains(d),dataGap:dr.top-ar.bottom,innerPadding:parseFloat(c.paddingLeft)-parseFloat(getComputedStyle(a.querySelector('.marco-lineas'),'::after').left),timeline:{start:parseFloat(lc.top),height:parseFloat(lc.height),lastDot:last.top-lr.top+14,background:lc.backgroundImage,segments:lis.map(x=>getComputedStyle(x,'::before').content),textMasks:lis.map(x=>getComputedStyle(x).maskImage)},gallery:{height:fr.height,radius:getComputedStyle(f).borderRadius,shadow:getComputedStyle(f).boxShadow,captionInside:cr.top>=fr.top&&cr.bottom<=fr.bottom+1&&cr.width<=fr.width,region:g.clientWidth,content:g.scrollWidth,focus:g.tabIndex}}})()''')
  assert not r['overflow'] and r['dataOutside'] and r['dataGap']>=0 and r['innerPadding']>=19,r
  t=r['timeline'];assert t['start']+t['height']>=t['lastDot'] and all(x=='none' for x in t['segments']+t['textMasks']),r
  assert r['gallery']['captionInside'] and r['gallery']['focus']==0,r
  records.append(r)
 for anchor in ['trayectoria-ejemplo','actividad-editorial-ejemplo','galeria-ejemplo']:
  evaluate('document.documentElement.dataset.theme="dark";document.getElementById('+json.dumps(anchor)+').scrollIntoView({block:"center",behavior:"instant"});true')
  Path(f'tests/screenshots/ajustes-{anchor}-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 evaluate('document.querySelector("[data-ir=prioridades]").click();document.getElementById("apuntes-prioridades").scrollIntoView({block:"center",behavior:"instant"});true');call('screenshot');evaluate('new Promise(r=>setTimeout(()=>r(true),1800))')
 Path(f'tests/screenshots/ajustes-apuntes-{w}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
 assert not evaluate('document.documentElement.scrollWidth>innerWidth')
save('ajustes-work-pantallas.json',records);print('18 combinaciones de geometría; apuntes a 320/390/1440; capturas guardadas.')
