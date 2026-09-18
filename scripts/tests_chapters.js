(async()=>{
 const results=[],assert=(x,m)=>{if(!x)throw new Error(m);};
 const test=async(name,fn)=>{try{await fn();results.push({name,ok:true});}catch(e){results.push({name,ok:false,error:e.message});}};
 const wait=()=>new Promise(r=>setTimeout(r,80));
 const go=id=>document.querySelector(`[data-ir="${id}"]`).click();
 await test('Cuatro capítulos, una sola página visible y salto al capítulo activo',()=>{
  const pages=[...document.querySelectorAll('.pagina')];assert(pages.length===4,'Páginas');
  for(const p of pages){go(p.id);assert(pages.filter(e=>!e.hidden).length===1&&!p.hidden,'Visibilidad');assert(document.querySelector('.barra [aria-current="page"]').dataset.ir===p.id,'Navegación');assert(document.querySelector('.salto').hash==='#'+p.id,'Salto a contenido oculto');}
 });
 await test('Anterior y siguiente respetan extremos',()=>{
  go('resumen');assert(document.querySelector('[data-nav=prev]').disabled,'Prev inicial');document.querySelector('[data-nav=next]').click();assert(location.hash==='#evidencia','Next');go('siguientes');assert(document.querySelector('[data-nav=next]').disabled,'Next final');
 });
 await test('Historial retrocede y avanza entre capítulos',async()=>{
  go('resumen');go('evidencia');go('prototipo');history.back();await wait();assert(document.querySelector('.pagina.viva').id==='evidencia','Atrás');history.forward();await wait();assert(document.querySelector('.pagina.viva').id==='prototipo','Adelante');
 });
 await test('Pestañas: roles, selección y paneles sincronizados',()=>{
  go('evidencia');const e=document.querySelector('[data-pestanas]'),t=NotaPestanas.get(e);
  assert(t&&t===NotaPestanas.init(e)[0],'Instancia');assert(t.nav.getAttribute('role')==='tablist','Tablist');
  t.buttons.forEach((b,i)=>{b.click();assert(t.index===i,'Selección');assert(t.panels.filter(p=>!p.hidden).length===1&&!t.panels[i].hidden,'Panel');assert(b.getAttribute('aria-selected')==='true'&&b.tabIndex===0,'Tab');assert(t.panels[i].getAttribute('aria-labelledby')===b.id,'Nombre');});
 });
 await test('Flechas mueven foco sin activar; Inicio/Fin y clic activan a demanda',()=>{
  const t=NotaPestanas.get(document.querySelector('[data-pestanas]'));t.select(0);t.buttons[0].focus();t.buttons[0].dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true,cancelable:true}));
  assert(document.activeElement===t.buttons[2]&&t.index===0,'Flecha o activación automática');t.buttons[2].click();assert(t.index===2,'Activación');t.buttons[2].dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true,cancelable:true}));assert(document.activeElement===t.buttons[0],'Home');t.buttons[0].dispatchEvent(new KeyboardEvent('keydown',{key:'End',bubbles:true,cancelable:true}));assert(document.activeElement===t.buttons[2],'End');t.select(0);
 });
 await test('destroy restaura secciones; reintento inválido no altera el contenido',()=>{
  const source=document.querySelector('[data-pestanas]');
  // Recuperar el HTML original por medio de destroy y restaurar la instancia viva.
  const live=NotaPestanas.get(source);live.destroy();const original=source.innerHTML;
  const a=NotaPestanas.init(source)[0];a.select(2);a.destroy();a.destroy();assert(source.innerHTML===original,'No restauró HTML');
  const b=source.querySelector('[data-tab]'),old=b.dataset.tab;b.dataset.tab='no-existe';assert(NotaPestanas.init(source)[0]===null,'ID inexistente aceptado');assert([...source.querySelectorAll('[data-tab-panel]')].every(p=>!p.hidden),'Ocultó fallback');
  b.dataset.tab=old;assert(NotaPestanas.init(source)[0]&&!source.querySelector('[data-error-pestanas]'),'Reintento');
 });
 await test('Visor se activa en un capítulo inicialmente oculto',async()=>{
  go('prototipo');await wait();const v=NotaVisores.get(document.querySelector('[data-visor]'));v.setWidth('390');assert(v.host.getBoundingClientRect().width===390,'Ancho real');v.shadow.querySelector('[data-demo-ir]').click();assert(v.shadow.querySelector('[data-demo-pagina]:not([hidden])'),'Estado');v.reset();
 });
 await test('Las seis paletas se eligen y el icono coincide con su luminosidad',()=>{
  const m=document.querySelector('[data-apariencia-menu]');for(const name of ['light','dark','sea','oliva','arcilla','ciruela']){
   m.querySelector(`[data-elegir-tema][value="${name}"]`).click();assert(document.documentElement.dataset.theme===name,'Tema');assert(m.dataset.oscuro===String(['dark','sea','ciruela'].includes(name)),'Icono');
  }
 });
 go('resumen');return {results,passed:results.filter(r=>r.ok).length,failed:results.filter(r=>!r.ok).length};
})()
