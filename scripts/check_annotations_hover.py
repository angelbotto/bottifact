#!/usr/bin/env python3
"""Repetición flotante y entrada por scroll en Orca. No acredita hardware táctil."""
import json
from check_browser import call, evaluate, save

URL='http://127.0.0.1:8768/tests/evidence/plan-evolution.html'
call('exec','--command','set media light')
call('exec','--command','set viewport 1440 960')
call('goto','--url',URL)
evaluate('''window.gestoEntradas=[];window.gestoAnimate=Element.prototype.animate;
Element.prototype.animate=function(...args){const e=this.closest('[data-mano],[data-subrayar]');if(e)gestoEntradas.push(e.id||e.dataset.subrayar);return gestoAnimate.apply(this,args);};true''')
initial=evaluate('''({right:NotaMano.get(document.getElementById('plan-nota-derecha')).played,
strike:NotaMano.get(document.querySelector('[data-subrayar=tachado]')).played})''')
assert not initial['right'] and not initial['strike'], initial
motion=[]
for selector in ['[data-subrayar=tachado]','#plan-nota-derecha']:
    amount=evaluate('Math.round(document.querySelector('+json.dumps(selector)+').getBoundingClientRect().top-innerHeight/2)')
    call('scroll','--direction','down','--amount',str(max(1,amount)))
    call('screenshot')  # Permite que el navegador entregue el IntersectionObserver real.
    row=evaluate('''(()=>{const e=document.querySelector(SELECTOR),s=NotaMano.get(e);return {selector:SELECTOR,played:s.played,visible:s.visible,scrollY,calls:gestoEntradas.filter(x=>x===(e.id||e.dataset.subrayar)).length};})()'''.replace('SELECTOR',json.dumps(selector)))
    assert row['played'] and row['calls']>0,row
    motion.append(row)
call('scroll','--direction','up','--amount','50000');call('screenshot')
assert evaluate('NotaMano.get(document.getElementById("plan-nota-derecha")).animations.length')==0

geometry=[]
for width,height in [(320,740),(390,844),(1440,960)]:
    call('exec','--command',f'set viewport {width} {height}')
    for theme in ['light','dark','sea']:
        evaluate('document.documentElement.dataset.theme='+json.dumps(theme)+';true')
        row=evaluate('''(()=>{const e=document.querySelector('.apunte-nota'),b=e.querySelector('button'),p=e.querySelector('.manuscrita'),before=e.getBoundingClientRect().height;
        b.style.display='none';const without=e.getBoundingClientRect().height;b.style.removeProperty('display');
        const boxes=[...document.querySelectorAll('.apunte-nota button')].map(b=>{const r=b.getBoundingClientRect();return {inside:r.left>=0&&r.right<=innerWidth,absolute:getComputedStyle(b).position==='absolute',name:!!b.getAttribute('aria-label')};});
        return {width:innerWidth,theme:document.documentElement.dataset.theme,before,without,margin:getComputedStyle(p).marginBottom,overflow:document.documentElement.scrollWidth>innerWidth,boxes};})()''')
        assert row['before']==row['without'] and row['margin']=='0px' and not row['overflow'],row
        assert all(b['inside'] and b['absolute'] and b['name'] for b in row['boxes']),row
        geometry.append(row)

# DOM focus comprueba que el botón invisible sigue siendo alcanzable y se revela.
evaluate('document.querySelector(".apunte-nota button").focus();true')
focus=evaluate('''(()=>{const b=document.querySelector('.apunte-nota button');return {active:document.activeElement===b,opacity:getComputedStyle(b).opacity,outline:getComputedStyle(b).outlineStyle};})()''')
assert focus['active'] and focus['opacity']=='1',focus
call('exec','--command','set media reduced-motion');call('screenshot')
reduced=evaluate('''[...document.querySelectorAll('[data-mano],[data-subrayar]')].map(e=>{const s=NotaMano.get(e);return {reduced:s.motion.matches,animations:s.animations.length,disabled:s.buttons.every(({b})=>b.disabled)};})''')
assert all(x['reduced'] and not x['animations'] and x['disabled'] for x in reduced),reduced
call('exec','--command','set media light')
save('apuntes-hover.json',{'initial':initial,'scroll':motion,'geometry':geometry,'focus':focus,'reduced':reduced,
 'limits':['Scroll por CLI y observadores reales; foco por DOM, no teclado físico.','Viewports emulados; no se acredita tacto físico ni audición humana.']})
print('Entrada por scroll, tachado, cancelación, foco y geometría: correctos.')
