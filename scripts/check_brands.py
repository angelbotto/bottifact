"""Logos incrustados, identidad estable y lectura móvil; navegador Orca en :8768."""
from check_browser import call, evaluate, save

checks = []
try:
    for brand in ['liftit', 'tikin', 'catabum']:
        call('goto', '--url', 'http://127.0.0.1:8768/'+brand+'.html')
        for width, height in [(320, 740), (390, 844), (1440, 960)]:
            call('exec', '--command', f'set viewport {width} {height}')
            for mode in ['light', 'dark']:
                evaluate("NotaTemas.set({family:'"+brand+"',mode:'"+mode+"'});true")
                evaluate('new Promise(requestAnimationFrame)')
                row = evaluate('''(async()=>{
                    const firma=document.querySelector('.firma-editorial'),
                        logos=[...firma.querySelectorAll('img')];
                    await Promise.all(logos.map(img=>img.decode()));
                    const visible=logos.filter(img=>getComputedStyle(img).display!=='none'),
                        r=firma.getBoundingClientRect(),m=document.querySelector('.marca-firma');
                    return {width:innerWidth,overflow:document.documentElement.scrollWidth>innerWidth,
                        brand:m.dataset.marca,label:firma.getAttribute('aria-label'),
                        theme:NotaTemas.get(),visible:visible.length,
                        tone:visible[0]?.className,loaded:logos.every(img=>img.naturalWidth>0),
                        inside:r.left>=0&&r.right<=innerWidth,
                        review:!!document.querySelector('[data-revision]')};
                })()''')
                assert row['width']==width and not row['overflow'] and row['inside'], row
                assert row['brand']==brand and row['visible']==1 and row['loaded'], row
                assert 'marca-logo-'+mode in row['tone'] and row['review'], row
                checks.append(row)
        # La apariencia del lector no puede sustituir la firma del documento.
        evaluate("NotaTemas.set({family:'blueprint',mode:'dark'});true")
        assert evaluate("document.querySelector('.firma-editorial [data-marca]').dataset.marca")==brand
        evaluate("NotaTemas.set({family:'"+brand+"',mode:'system'});true")
        for mode in ['light','dark']:
            call('exec','--command','set media '+mode)
            # Emular media y entregar su evento change ocurren en frames distintos.
            state=evaluate("(async()=>{const end=performance.now()+2000;while(NotaTemas.get().effective!=='"+mode+"'&&performance.now()<end)await new Promise(requestAnimationFrame);return NotaTemas.get()})()")
            assert state['effective']==mode, state
            assert evaluate("getComputedStyle(document.querySelector('.firma-editorial .marca-logo-"+mode+"')).display")!='none'
        print(brand+': logo, identidad estable, 3 anchos y modos claro/oscuro/sistema correctos.',flush=True)
    save('marcas-matriz.json', {'casos':checks,'alcance':'DOM y estilos calculados. No acredita ejecución del modelo ni audición humana.'})
finally:
    call('exec','--command','set media light')
    call('goto','--url','http://127.0.0.1:8768/examples/generated/brands.html')
