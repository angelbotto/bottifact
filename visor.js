/* NotaVisor · prototipos locales con ancho real y Shadow DOM.
   El HTML de template es de confianza. Sin iframes, red ni ejecución de scripts. */
(() => {
  'use strict';
  const instances=new WeakMap();
  class NotaVisor {
    constructor(root) {
      this.root=root;this.abort=new AbortController();this.dead=false;
      const template=root.querySelector('template[data-prototipo]');
      this.status=root.querySelector('[data-visor-estado]');this.box=root.querySelector('.visor-caja');
      this.source=root.querySelector('.visor-fuente');this.buttons=[...root.querySelectorAll('[data-ancho-visor]')];
      if(!template||!this.status||!this.box||!this.source||!this.buttons.length)throw new TypeError('Faltan template, alternativa o controles del visor.');
      this.template=template;this.initialTemplate=template;this.originalStatus=this.status.textContent;
      this.originalPressed=this.buttons.map(b=>b.getAttribute('aria-pressed'));
      this.originalSource=this.source.hasAttribute('data-oculta');
      if(template.content.querySelector('script') || [...template.content.querySelectorAll('*')].some(e=>[...e.attributes].some(a=>/^on/i.test(a.name)))) throw new TypeError('Usa HTML declarativo sin scripts ni manejadores inline.');
      this.host=document.createElement('div');this.host.className='visor-lienzo';this.box.append(this.host);
      this.shadow=this.host.attachShadow({mode:'open'});
      this.width=390;
      this.on(root,'click',e=>{
        const size=e.target.closest('[data-ancho-visor]');
        if(size&&root.contains(size))this.setWidth(size.dataset.anchoVisor);
        if(e.target.closest('[data-reiniciar-visor]')){this.template=this.initialTemplate;this.reset();}
        if(e.target.closest('[data-cargar-html]')){const input=root.querySelector('[data-html-visor]'),state=root.querySelector('[data-importar-estado]');try{this.loadHTML(input.value);state.textContent='HTML cargado. Cambia entre Móvil y Escritorio para revisarlo.';}catch(error){state.textContent=error.message;}}
      });
      this.on(this.shadow,'click',e=>{
        const button=e.target.closest('[data-demo-ir]');if(!button)return;
        const panels=[...this.shadow.querySelectorAll('[data-demo-pagina]')];
        const target=panels.find(p=>p.dataset.demoPagina===button.dataset.demoIr);if(!target)return;
        panels.forEach(p=>p.hidden=p!==target);
        this.shadow.querySelectorAll('[data-demo-ir]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.demoIr===target.dataset.demoPagina)));
        const heading=target.querySelector('h1,h2,h3');if(heading){heading.tabIndex=-1;heading.focus();}
      });
      this.resize=new ResizeObserver(()=>this.measure());this.resize.observe(this.box);
      this.reset();this.setWidth('390');this.source.setAttribute('data-oculta','');instances.set(root,this);
    }
    on(node,type,fn) {node.addEventListener(type,fn,{signal:this.abort.signal});}
    reset() {
      if(this.dead)return;
      this.shadow.replaceChildren(this.template.content.cloneNode(true));
      // Contrato declarativo: no ejecutar JS copiado desde una muestra.
      this.shadow.querySelectorAll('script').forEach(s=>s.remove());
      const base=document.createElement('style');
      base.textContent=':host{display:block;container-type:inline-size;color:var(--pieza-tinta);font:16px/1.6 var(--sans)}*,*::before,*::after{box-sizing:border-box} [hidden]{display:none!important} :focus-visible{outline:2px dashed var(--foco);outline-offset:3px} @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}';
      this.shadow.prepend(base);this.measure();
    }
    loadHTML(source) {
      if(this.dead)return;
      if(typeof source!=='string'||!source.trim()||source.length>100000)throw new TypeError('Pega entre 1 y 100.000 caracteres de HTML local.');
      const template=document.createElement('template');template.innerHTML=source;
      if(template.content.querySelector('script,iframe,object,embed,link,base,meta,template'))throw new TypeError('El visor admite HTML declarativo sin scripts, iframes ni recursos externos.');
      for(const node of template.content.querySelectorAll('*'))for(const a of node.attributes){
        if(/^on/i.test(a.name)||['srcdoc','action','formaction','srcset'].includes(a.name))throw new TypeError('Retira scripts, envíos y recursos externos del HTML.');
        if(['href','src','poster','xlink:href'].includes(a.name)&&!a.value.startsWith('#')&&!/^data:image\/(png|jpeg|webp|gif);base64,/i.test(a.value))throw new TypeError('Usa enlaces internos e imágenes raster incrustadas como data: URI.');
      }
      const styles=[...template.content.querySelectorAll('style')].map(e=>e.textContent).concat([...template.content.querySelectorAll('[style]')].map(e=>e.getAttribute('style'))).join(' ');
      if(/@import|url\s*\(/i.test(styles))throw new TypeError('Retira @import y url() del CSS pegado; usa los tokens del documento.');
      this.template=template;this.reset();
    }
    setWidth(raw) {
      const n=raw==='auto'?null:Number(raw);
      if(n!==null&&![320,390,768,1024].includes(n))throw new TypeError('Anchos disponibles: 320, 390, 768, 1024 o auto.');
      this.width=n;this.host.style.width=n===null?'100%':n+'px';
      this.buttons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.anchoVisor===String(raw))));this.measure();
    }
    measure() {
      if(this.dead)return;
      const w=Math.round(this.host.getBoundingClientRect().width);
      this.status.textContent='Vista de '+w+' px CSS'+(this.width===null?' · ajustada al espacio disponible.':'.')+' '+(this.box.scrollWidth>this.box.clientWidth?'Desplaza la región para ver todo el ancho.':'');
    }
    destroy() {
      if(this.dead)return;this.dead=true;this.abort.abort();this.resize.disconnect();this.host.remove();
      this.status.textContent=this.originalStatus;this.source.toggleAttribute('data-oculta',this.originalSource);
      this.buttons.forEach((b,i)=>{if(this.originalPressed[i]===null)b.removeAttribute('aria-pressed');else b.setAttribute('aria-pressed',this.originalPressed[i]);});
      instances.delete(this.root);
    }
  }
  function init(root=document) {
    return [...(root.matches?.('[data-visor]')?[root]:[]),...root.querySelectorAll('[data-visor]')].map(e=>{
      if(instances.has(e))return instances.get(e);
      e.querySelector('[data-error-visor]')?.remove();
      try{return new NotaVisor(e);}catch(error){const p=document.createElement('p');p.dataset.errorVisor='';p.textContent='Visor no disponible: '+error.message;e.prepend(p);e.querySelector('.visor-fuente')?.removeAttribute('data-oculta');return null;}
    });
  }
  window.NotaVisores={init,get:e=>instances.get(e)};init();
})();
