/* NotaPestanas: vistas locales de una misma pieza. Activación manual, sin red ni RAF. */
(() => {
  'use strict';
  const instances=new WeakMap();
  class Pestanas {
    constructor(root) {
      this.root=root;this.dead=false;this.abort=new AbortController();this.restore=[];
      this.nav=root.querySelector('[data-tabs-nav]');
      this.buttons=[...this.nav?.querySelectorAll('[data-tab]')||[]];
      this.panels=[...root.querySelectorAll(':scope > [data-tab-panel]')];
      if(!this.nav||this.buttons.length<2||this.buttons.length!==this.panels.length)throw new TypeError('Usa al menos dos botones y un panel por botón.');
      const ids=new Set();
      this.buttons.forEach((b,i)=>{
        if(!b.id||!b.dataset.tab||ids.has(b.dataset.tab)||this.panels[i].id!==b.dataset.tab||b.disabled)throw new TypeError('IDs únicos, botones habilitados y paneles en el mismo orden.');
        ids.add(b.dataset.tab);
      });
      const remember=(el,names)=>{const attrs=names.map(n=>[n,el.getAttribute(n)]);this.restore.push(()=>attrs.forEach(([n,v])=>v===null?el.removeAttribute(n):el.setAttribute(n,v)));};
      remember(root,['data-tabs-listas']);remember(this.nav,['role']);this.nav.setAttribute('role','tablist');
      this.buttons.forEach((b,i)=>{
        remember(b,['role','aria-controls','aria-selected','tabindex']);b.setAttribute('role','tab');b.setAttribute('aria-controls',this.panels[i].id);
        const p=this.panels[i];remember(p,['role','aria-labelledby','tabindex','hidden']);p.setAttribute('role','tabpanel');p.setAttribute('aria-labelledby',b.id);p.tabIndex=0;
        b.addEventListener('click',()=>this.select(i),{signal:this.abort.signal});
        b.addEventListener('keydown',e=>{
          const next={ArrowRight:(i+1)%this.buttons.length,ArrowLeft:(i-1+this.buttons.length)%this.buttons.length,Home:0,End:this.buttons.length-1}[e.key];
          if(next!==undefined){e.preventDefault();this.buttons.forEach((t,k)=>t.tabIndex=k===next?0:-1);this.buttons[next].focus();this.reveal(next);}
        },{signal:this.abort.signal});
      });
      root.dataset.tabsListas='';this.select(0);instances.set(root,this);
    }
    reveal(i) {
      const box=this.nav.closest('.pestanas-caja');if(!box)return;
      const a=this.buttons[i].getBoundingClientRect(),b=box.getBoundingClientRect();
      if(a.left<b.left)box.scrollLeft+=a.left-b.left-4;else if(a.right>b.right)box.scrollLeft+=a.right-b.right+4;
    }
    select(i) {
      if(this.dead)return;
      if(!Number.isInteger(i)||i<0||i>=this.buttons.length)throw new RangeError('Pestaña inexistente.');
      this.index=i;this.buttons.forEach((b,k)=>{b.setAttribute('aria-selected',String(k===i));b.tabIndex=k===i?0:-1;this.panels[k].hidden=k!==i;});
      this.reveal(i);this.root.dispatchEvent(new CustomEvent('nota:pestana',{bubbles:true,detail:{index:i,id:this.panels[i].id}}));
    }
    destroy() {if(this.dead)return;this.dead=true;this.abort.abort();this.restore.reverse().forEach(fn=>fn());instances.delete(this.root);}
  }
  function init(root=document) {
    return [...(root.matches?.('[data-pestanas]')?[root]:[]),...root.querySelectorAll('[data-pestanas]')].map(e=>{
      if(instances.has(e))return instances.get(e);e.querySelector('[data-error-pestanas]')?.remove();
      try{return new Pestanas(e);}catch(error){const p=document.createElement('p');p.dataset.errorPestanas='';p.textContent='Vistas disponibles como secciones: '+error.message;e.prepend(p);return null;}
    });
  }
  window.NotaPestanas={init,get:e=>instances.get(e)};init();
})();
