"""Regresión del marco anidado y lectura del memo ejecutivo con datos del catálogo."""
import json
from comprobar_navegador import call, evaluate, save

call('goto', '--url', 'http://127.0.0.1:8768/ejecutivo.html')
regression = evaluate('''(()=>{
 const fixture=document.createElement('section');fixture.className='ancho';
 fixture.innerHTML='<div class="cards-trazadas cards-abiertas marco-difuso"><a href="#memo"><h3>Marco de prueba</h3><p>Contenido legible</p></a><figure class="ancho"><p>Figura interior</p></figure></div>';
 document.querySelector('#memo').append(fixture);
 NotaPiezasEditoriales.init(fixture);NotaPiezasEditoriales.init(fixture);
 const inner=fixture.querySelector('.marco-difuso'),r={frames:fixture.querySelectorAll('.marco-lineas').length,before:getComputedStyle(inner,'::before').content,after:getComputedStyle(inner,'::after').content,padding:getComputedStyle(inner).padding,mask:getComputedStyle(inner).maskImage};fixture.remove();return r;
})()''')
assert regression == {'frames': 1, 'before': 'none', 'after': 'none', 'padding': '0px', 'mask': 'none'}, regression
measurements = []
for mode in ['light', 'dark']:
    evaluate('NotaTemas.set({family:"editorial",mode:'+json.dumps(mode)+'});true')
    for width, height in [(320, 740), (390, 844), (1440, 940)]:
        call('exec', '--command', f'set viewport {width} {height}')
        evaluate('new Promise(requestAnimationFrame)')
        result = evaluate('''(()=>({width:innerWidth,documentWidth:document.documentElement.scrollWidth,frames:document.querySelector('#balance').querySelectorAll('.marco-lineas').length,notes:document.querySelectorAll('#memo [data-escritura-sonora]').length,left:document.querySelectorAll('#memo .apunte.izquierda').length,right:document.querySelectorAll('#memo .apunte:not(.izquierda)').length,charts:[...document.querySelectorAll('#memo [data-grafica],#memo [data-analitica]')].map(e=>({id:e.id,svg:!!e.querySelector('svg'),total:[...e.querySelectorAll('td[data-valor]')].reduce((s,e)=>s+Number(e.dataset.valor),0)}))}))()''')
        assert result['width'] == width and result['documentWidth'] <= width + 1, result
        assert result['frames'] == 1 and result['notes'] == 6 and result['left'] == result['right'] == 3, result
        assert len(result['charts']) == 2 and all(c['svg'] and c['total'] == 82 for c in result['charts']), result
        result['mode'] = mode
        measurements.append(result)
toggle = evaluate('''(()=>{const e=document.querySelector('#ejecutivo-composicion'),b=[...e.querySelectorAll('button')].find(b=>b.textContent==='Ver como torta');b.click();const switched=b.textContent==='Ver como donut';b.click();return {switched,restored:b.textContent==='Ver como torta'}})()''')
assert toggle['switched'] and toggle['restored'], toggle
save('voz-ejecutiva-composicion.json', {'regression': regression, 'measurements': measurements, 'toggle': toggle, 'limits': ['Comprobación DOM de las notas, no audición humana.', 'La instalación del skill no acredita calidad editorial de cada agente.']})
call('exec', '--command', 'set viewport 1440 940')
print('Marco único, 6 notas, 2 gráficas con total 82 y torta/donut: correctos en claro/oscuro y 3 anchos.')
