(async()=>{
 const results=[],assert=(x,m)=>{if(!x)throw new Error(m);};
 const test=async(name,fn)=>{try{await fn();results.push({name,ok:true});}catch(e){results.push({name,ok:false,error:e.message});}};
 const menus=[...document.querySelectorAll('[data-apariencia-menu]')],root=document.documentElement;
 const settle=()=>new Promise(r=>setTimeout(r,40));
 const choose=(key,value)=>{const m=menus[0];if(!m.open)m.querySelector('summary').click();m.querySelector(`[${key}][value="${value}"]`).click();};
 await test('Cuatro controles: cabecera y tres variantes copiables, IDs únicos',()=>{
  assert(menus.length===4,'Cantidad de controles');const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);assert(new Set(ids).size===ids.length,'IDs duplicados');
  menus.forEach(m=>assert(document.getElementById(m.querySelector('summary').getAttribute('aria-controls'))===m.querySelector('.apariencia-panel'),'Control sin panel'));
 });
 await test('Pulsar abre/cierra; sólo queda un panel abierto',async()=>{
  menus[0].querySelector('summary').click();assert(menus[0].open,'No abrió');menus[0].querySelector('summary').click();assert(!menus[0].open,'No cerró');
  menus[1].scrollIntoView({behavior:'instant'});menus[1].querySelector('summary').click();menus[2].querySelector('summary').click();await settle();assert(menus.filter(m=>m.open).length===1&&menus[2].open,'Dos paneles abiertos');
 });
 await test('Escape cierra y devuelve foco al disparador',()=>{
  menus[2].querySelector('input').focus();document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true}));assert(!menus[2].open&&document.activeElement===menus[2].querySelector('summary'),'Escape o foco');
 });
 await test('Contratos focusin y pointerdown cierran sin robar foco',async()=>{
  const m=menus[2];m.querySelector('summary').click();const outside=document.querySelector('a');outside.focus();outside.dispatchEvent(new FocusEvent('focusin',{bubbles:true}));await settle();assert(!m.open&&document.activeElement===outside,'Salida con foco');
  m.scrollIntoView({behavior:'instant'});m.querySelector('summary').click();document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));assert(!m.open,'No cerró fuera');
 });
 await test('Temas sincronizados, muestras nombradas e iconos efectivos',()=>{
  menus[0].scrollIntoView({behavior:'instant'});
  for(const value of ['light','dark','sea','system']){
   choose('data-elegir-tema',value);assert((root.dataset.theme||'system')===value,'Paleta');
   const dark=value==='dark'||value==='sea'||(value==='system'&&matchMedia('(prefers-color-scheme:dark)').matches);
   menus.forEach(m=>{assert(m.dataset.oscuro===String(dark),'Icono');assert(m.querySelector('[data-elegir-tema]:checked').value===value,'Sincronización');
    assert(getComputedStyle(m.querySelector(dark?'.icono-luna':'.icono-sol')).display!=='none','Icono oculto');});
  }
 });
 await test('Estilo de títulos cambia familia sin cambiar cuerpo ni datos',()=>{
  const body=getComputedStyle(document.body).fontFamily;
  for(const [value,family] of [['sobrio','Geist'],['tecnico','Geist Mono'],['editorial','Instrument Serif']]){
   choose('data-elegir-estilo',value);assert(getComputedStyle(document.querySelector('h1')).fontFamily.includes(family),'Familia incorrecta');
   assert(getComputedStyle(document.body).fontFamily===body,'Modificó párrafos');menus.forEach(m=>assert(m.querySelector('[data-elegir-estilo]:checked').value===value,'Estilos no sincronizados'));
  }
  assert(!root.hasAttribute('data-estilo'),'Editorial no restaura origen');
 });
 await test('Lectura cómoda y trama independientes, reversibles y sincronizadas',()=>{
  for(const [key,attr] of [['data-comodidad','data-lectura-comoda'],['data-papel-tramado','data-trama']]){
   const b=menus[0].querySelector(`[${key}]`);if(root.hasAttribute(attr))b.click();b.click();assert(root.hasAttribute(attr),'No activa');
   menus.forEach(m=>assert(m.querySelector(`[${key}]`).getAttribute('aria-pressed')==='true','No sincroniza'));b.click();assert(!root.hasAttribute(attr),'No restaura');
  }
 });
 await test('Panel desplazable tiene nombre, foco y no es un menú de comandos',()=>menus.forEach(m=>{
  const p=m.querySelector('.apariencia-panel');assert(p.tabIndex===0&&p.getAttribute('aria-label')&&p.getAttribute('role')==='region','Semántica');assert(!m.querySelector('[role="menu"],[role="switch"]'),'Rol incorrecto');
 })) ;
 choose('data-elegir-tema','light');choose('data-elegir-estilo','editorial');menus.forEach(m=>m.open=false);
 return {results,passed:results.filter(r=>r.ok).length,failed:results.filter(r=>!r.ok).length};
})()
