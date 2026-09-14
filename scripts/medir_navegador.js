(async () => {
  await document.fonts.ready;
  const closed=[...document.querySelectorAll('details:not([open])')];closed.forEach(d=>d.open=true);
  const css=getComputedStyle(document.documentElement),canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
  function rgb(color){ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);return [...ctx.getImageData(0,0,1,1).data].slice(0,3);}
  const lum=color=>rgb(color).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
  const value=token=>css.getPropertyValue(token).trim();
  const contrast=(a,b)=>{const x=lum(value(a)),y=lum(value(b));return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);};
  const contrasts=[...[0,1,2,3,4].map(i=>({pair:'calor-'+i,ratio:contrast('--calor-tinta','--calor-'+i),minimum:4.5})),
    ...[1,2,3,4].map(i=>({pair:'serie-'+i,ratio:contrast('--grafica-'+i,'--grafica-papel'),minimum:3})),
    {pair:'etiquetas',ratio:contrast('--grafica-tinta','--grafica-papel'),minimum:4.5},
    {pair:'escena',ratio:contrast('--escena-tinta','--grafica-papel'),minimum:4.5},
    {pair:'sonido',ratio:contrast('--sonido-activo','--sonido-papel'),minimum:4.5},
    {pair:'escritura',ratio:contrast('--escritura-trazo','--escritura-papel'),minimum:3}];
  const regions=[...document.querySelectorAll('.tabla-caja,.diagrama-caja,.grafica-caja,.escena-caja,.escritura-caja,pre,.barra')].filter(e=>e.getClientRects().length).map(e=>{
    const before=e.scrollLeft;e.scrollLeft=e.scrollWidth;const end=e.scrollLeft;e.scrollLeft=before;
    const r=e.getBoundingClientRect(),style=getComputedStyle(e);
    return {kind:e.className||e.tagName,width:e.clientWidth,content:e.scrollWidth,end,overflow:style.overflowX,focus:e.tabIndex,name:e.getAttribute('aria-label'),inside:r.left>=-.5&&r.right<=innerWidth+.5};
  });
  const svgTextOverflow=[];
  document.querySelectorAll('.grafica-caja svg').forEach(svg=>{const bounds=svg.viewBox.baseVal;svg.querySelectorAll('text').forEach(t=>{const b=t.getBBox();if(b.x<-.5||b.y<-.5||b.x+b.width>bounds.width+.5||b.y+b.height>bounds.height+.5)svgTextOverflow.push(t.textContent);});});
  const p=document.querySelector('.seccion p'),wide=document.querySelector('.hoja > .ancho'),wider=document.querySelector('.hoja > .amplio');
  const result={viewport:[innerWidth,innerHeight],theme:document.documentElement.dataset.theme||'system',documentWidth:document.documentElement.scrollWidth,regions,contrasts,svgTextOverflow,
    widths:[p,wide,wider].map(e=>e?.getBoundingClientRect().width),errors:[...document.querySelectorAll('[data-error-grafica],[data-error-escena]')].map(e=>e.textContent),
    resources:performance.getEntriesByType('resource').map(e=>({url:e.name,type:e.initiatorType})),reduced:matchMedia('(prefers-reduced-motion: reduce)').matches};
  closed.forEach(d=>d.open=false);return result;
})()
