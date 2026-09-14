/* NOTA TIKIN · archivos y configuración editorial local. Sin red ni persistencia. */
(() => {
  'use strict';
  const instances=new WeakMap(),normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es');
  function init(root=document){
    root.querySelectorAll('[data-archivo]').forEach(el=>{
      if(instances.has(el))return;
      const form=el.querySelector('form'),status=el.querySelector('[data-archivo-estado]'),empty=el.querySelector('[data-archivo-vacio]'),items=[...el.querySelectorAll('[data-publicacion]')];
      if(!form?.elements.buscar||!form.elements.tema||!status||!empty)return;
      const abort=new AbortController(),original=items.map(e=>e.hidden),originalStatus=status.textContent,emptyHidden=empty.hidden;
      const update=()=>{const words=normal(form.elements.buscar.value).trim().split(/\s+/),tema=form.elements.tema.value;let count=0;
        items.forEach(e=>{e.hidden=!!(tema&&e.dataset.tema!==tema)||!words.every(w=>normal(e.textContent).includes(w));if(!e.hidden)count++;});
        empty.hidden=count>0;status.textContent=count+' de '+items.length+' publicaciones.';
      };
      form.addEventListener('input',update,{signal:abort.signal});form.addEventListener('change',update,{signal:abort.signal});
      form.addEventListener('submit',e=>e.preventDefault(),{signal:abort.signal});
      form.addEventListener('reset',()=>queueMicrotask(()=>{if(!abort.signal.aborted)update();}),{signal:abort.signal});
      instances.set(el,{update,destroy(){abort.abort();items.forEach((e,i)=>e.hidden=original[i]);status.textContent=originalStatus;empty.hidden=emptyHidden;instances.delete(el);}});update();
    });
    root.querySelectorAll('[data-config-editorial]').forEach(el=>{
      if(instances.has(el))return;const form=el.querySelector('form'),code=el.querySelector('[data-config-json]'),status=el.querySelector('[data-config-estado]');
      if(!form?.elements.disposicion||!code||!status)return;
      const abort=new AbortController(),html=document.documentElement,attrs=['data-editorial-lista','data-editorial-sin-extractos','data-editorial-sin-meta'],before=attrs.map(a=>html.getAttribute(a)),beforeCode=code.textContent,beforeStatus=status.textContent;
      const update=()=>{const config={version:1,disposicion:form.elements.disposicion.value,extractos:form.elements.extractos.checked,metadatos:form.elements.metadatos.checked};
        html.toggleAttribute(attrs[0],config.disposicion==='lista');html.toggleAttribute(attrs[1],!config.extractos);html.toggleAttribute(attrs[2],!config.metadatos);
        code.textContent=JSON.stringify(config,null,2);status.textContent=(config.disposicion==='lista'?'Lista de lectura':'Rejilla editorial')+(config.extractos?' con extractos':' sin extractos')+(config.metadatos?' y metadatos.':' y sin metadatos.');
      };
      form.addEventListener('change',update,{signal:abort.signal});form.addEventListener('submit',e=>e.preventDefault(),{signal:abort.signal});form.addEventListener('reset',()=>queueMicrotask(()=>{if(!abort.signal.aborted)update();}),{signal:abort.signal});
      instances.set(el,{update,destroy(){abort.abort();attrs.forEach((a,i)=>before[i]===null?html.removeAttribute(a):html.setAttribute(a,before[i]));code.textContent=beforeCode;status.textContent=beforeStatus;instances.delete(el);}});update();
    });
  }
  window.NotaEditorial={init,get:el=>instances.get(el)};init();
})();
