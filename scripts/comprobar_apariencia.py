#!/usr/bin/env python3
"""Comprobar controles de apariencia en Orca. Sin instalación ni publicación."""
import argparse,base64,datetime
from pathlib import Path
from comprobar_navegador import call,evaluate,file,save
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8768/plantilla.html');args=p.parse_args()
call('goto','--url','about:blank');call('goto','--url',args.url)
r=file('pruebas_apariencia.js');save('apariencia-interaccion.json',r);print(r,flush=True);assert not r['failed']
records=[]
for width,height in [(320,740),(390,844),(1639,939)]:
 call('exec','--command',f'set viewport {width} {height}')
 for theme in ['light','dark','sea']:
  for style in ['editorial','sobrio','tecnico']:
   for extras in [False,True]:
    data=evaluate('''(()=>{
     const m=document.querySelector('[data-apariencia-menu]');scrollTo({top:0,behavior:'instant'});if(!m.open)m.querySelector('summary').click();
     m.querySelector('[data-elegir-tema][value="THEME"]').click();m.querySelector('[data-elegir-estilo][value="STYLE"]').click();
     for(const [key,attr] of [['data-comodidad','data-lectura-comoda'],['data-papel-tramado','data-trama']])if(document.documentElement.hasAttribute(attr)!==EXTRAS)m.querySelector('['+key+']').click();
     dispatchEvent(new Event('resize'));
     const p=m.querySelector('.apariencia-panel'),r=p.getBoundingClientRect(),before=p.scrollTop;p.scrollTop=p.scrollHeight;const end=p.scrollTop;p.scrollTop=before;
     const c=getComputedStyle(document.documentElement),canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
     const rgb=t=>{ctx.fillStyle=c.getPropertyValue(t);ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data].slice(0,3);};
     const lum=arr=>arr.map(x=>x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
     const ratio=(a,b)=>{a=lum(a);b=lum(b);return (Math.max(a,b)+.05)/(Math.min(a,b)+.05);};
     const contrasts=['--apariencia-tinta','--apariencia-secundaria'].flatMap(t=>['--apariencia-papel','--pieza-suave'].map(b=>({token:t,background:b,ratio:ratio(rgb(t),rgb(b))}))); 
     const paper=rgb('--papel'),line=rgb('--papel-trama'),mix=paper.map((n,i)=>n*.62+line[i]*.38);
     const textureContrast=Math.min(...['--tinta','--tinta-2'].map(t=>ratio(rgb(t),mix)));
     const headings=[...document.querySelectorAll('h1,h2,h3')].filter(e=>e.getClientRects().length).filter(e=>e.scrollWidth>e.clientWidth+1).map(e=>e.textContent);
     return {viewport:[innerWidth,innerHeight],theme:'THEME',style:'STYLE',extras:EXTRAS,documentWidth:document.documentElement.scrollWidth,headings,
      trigger:m.querySelector('summary').getBoundingClientRect().toJSON(),panel:{rect:r.toJSON(),client:p.clientHeight,scroll:p.scrollHeight,end,focus:p.tabIndex,name:p.getAttribute('aria-label'),overflow:getComputedStyle(p).overflowY},contrasts,textureContrast};
    })()'''.replace('THEME',theme).replace('STYLE',style).replace('EXTRAS',str(extras).lower()))
    records.append(data);save('apariencia-pantallas.json',records)
    assert data['viewport']==[width,height],data['viewport']
    assert data['documentWidth']==width and not data['headings'],(width,theme,style,data['headings'])
    r=data['panel']['rect'];assert r['left']>=0 and r['right']<=width and r['top']>=0 and r['bottom']<=height,(width,r)
    assert r['top']>=data['trigger']['bottom'] or r['bottom']<=data['trigger']['top'],'Panel tapa disparador'
    assert all(c['ratio']>=4.5 for c in data['contrasts']) and data['textureContrast']>=4.5,data
    if data['panel']['scroll']>data['panel']['client']+1:assert data['panel']['end']>0,data
  print(width,theme,'estilos y extras correctos',flush=True)
 # Captura al final de cada viewport: Sea, Técnico y extras activos.
 Path(f'auditoria/capturas/apariencia-{width}.png').write_bytes(base64.b64decode(call('screenshot')['data']))
# Preferencias guardadas no afectan notas anteriores que no incluyen estos controles.
call('goto','--url',args.url.replace('plantilla.html','multipagina.html'))
legacy=evaluate('({style:document.documentElement.dataset.estilo||null,texture:document.documentElement.hasAttribute("data-trama"),comfortable:document.documentElement.hasAttribute("data-lectura-comoda"),font:getComputedStyle(document.body).fontSize})')
assert legacy=={'style':None,'texture':False,'comfortable':False,'font':'16px'},legacy
save('apariencia-ejecucion.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':args.url,'browser':evaluate('navigator.userAgent'),'combinations':len(records),'legacy':legacy,'limits':['Escape/pointer/focusin ensayados con eventos explícitos; focus() actualiza activeElement pero el host no entregó eventos de foco. No teclado físico/lector de pantalla.','La trama se evalúa con el peor color compuesto al 38%; la marca real es menor por antialiasing.','No prueba de hardware móvil ni zoom 200%.']})
# Restaurar el catálogo y verificar que la ampliación anterior sigue operativa.
call('goto','--url',args.url)
evaluate('(()=>{const m=document.querySelector("[data-apariencia-menu]");m.querySelector("summary").click();m.querySelector("[data-elegir-estilo][value=editorial]").click();m.querySelector("[data-elegir-tema][value=light]").click();for(const [key,attr] of [["data-comodidad","data-lectura-comoda"],["data-papel-tramado","data-trama"]])if(document.documentElement.hasAttribute(attr))m.querySelector("["+key+"]").click();m.open=false;return true;})()')
r=file('pruebas_segunda_tanda.js');save('apariencia-regresion.json',r);print('Regresión',r['passed'],r['failed'],flush=True);assert not r['failed']
