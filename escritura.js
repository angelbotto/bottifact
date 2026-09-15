/* Nota Tikin · escribir paths SVG en orden, con longitud real y texto equivalente.
   Sin RAF. Las animaciones Web Animations se cancelan al reducir movimiento. */
(() => {
  'use strict';
  const instances=new WeakMap();
  class NotaEscritura {
    constructor(element){
      if(instances.has(element))throw new TypeError('Ya existe una escritura en este contenedor.');
      const paths=[...element.querySelectorAll('path[data-trazo]')];
      if(!paths.length||!element.querySelector('[data-texto-escritura]'))throw new TypeError('Se necesitan paths y texto equivalente.');
      this.element=element;this.paths=paths;this.dead=false;this.visible=false;this.played=false;this.animations=[];this.epoch=0;
      this.duration=Number(element.dataset.duracion||2400);
      if(!Number.isFinite(this.duration)||this.duration<100||this.duration>10000)throw new TypeError('Duración entre 100 y 10000 ms.');
      this.lengths=paths.map(p=>p.getTotalLength());
      if(this.lengths.some(n=>!Number.isFinite(n)||n<=0))throw new TypeError('Cada path debe tener longitud positiva.');
      this.original=paths.map(p=>[p.style.strokeDasharray,p.style.strokeDashoffset]);
      this.status=element.querySelector('[role="status"]');
      this.motion=matchMedia('(prefers-reduced-motion: reduce)');this.abort=new AbortController();
      element.addEventListener('click',e=>{
        if(e.target.closest('[data-escribir]'))this.play();
        if(e.target.closest('[data-finalizar]'))this.finish();
      },{signal:this.abort.signal});
      this.motion.addEventListener('change',()=>{if(this.motion.matches)this.finish();this.sync();},{signal:this.abort.signal});
      document.addEventListener('visibilitychange',()=>{if(document.hidden)this.finish();},{signal:this.abort.signal});
      this.intersection=new IntersectionObserver(entries=>{this.visible=entries[0].isIntersecting&&entries[0].intersectionRatio>=.3;if(!this.visible)this.finish();else if(element.hasAttribute('data-al-ver')&&!this.played&&!this.motion.matches){this.played=true;this.play();}},{threshold:[0,.3]});this.intersection.observe(element.querySelector('.escritura-caja')||element);
      this.sync();instances.set(element,this);
    }
    sync(){const button=this.element.querySelector('[data-escribir]');if(button){button.disabled=this.motion.matches;button.textContent=this.motion.matches?'Trazo completo (movimiento reducido)':'Repetir escritura';}}
    cancel(){this.stopSound?.();this.stopSound=null;this.epoch++;this.animations.forEach(a=>a.cancel());this.animations=[];}
    finish(){this.cancel();this.paths.forEach(p=>{p.style.strokeDasharray='none';p.style.strokeDashoffset='0';});if(this.status)this.status.textContent='Trazo completo.';}
    play(){
      if(this.dead)return;this.finish();
      if(this.motion.matches||document.hidden||!this.visible||!this.paths[0].animate)return;
      const rect=this.element.getBoundingClientRect();if(rect.bottom<=0||rect.top>=innerHeight)return;
      this.stopSound=window.NotaAudio?.writing(this.element,this.duration);
      const epoch=this.epoch,total=this.lengths.reduce((a,b)=>a+b,0);let delay=0;
      this.paths.forEach((path,i)=>{
        const length=this.lengths[i],duration=this.duration*length/total;
        path.style.strokeDasharray=String(length);path.style.strokeDashoffset=String(length);
        const animation=path.animate([{strokeDashoffset:length},{strokeDashoffset:0}],{duration,delay,easing:'linear',fill:'forwards'});
        this.animations.push(animation);delay+=duration;
      });
      if(this.status)this.status.textContent='Escribiendo. La frase completa permanece debajo.';
      Promise.all(this.animations.map(a=>a.finished)).then(()=>{if(!this.dead&&this.epoch===epoch)this.finish();}).catch(()=>{});
    }
    destroy(){if(this.dead)return;this.finish();this.dead=true;this.abort.abort();this.intersection.disconnect();this.paths.forEach((p,i)=>{[p.style.strokeDasharray,p.style.strokeDashoffset]=this.original[i];});instances.delete(this.element);}
  }
  function init(root=document){return [...(root.matches?.('[data-escritura]')?[root]:[]),...root.querySelectorAll('[data-escritura]')].map(e=>instances.get(e)||new NotaEscritura(e));}
  window.NotaEscritura=NotaEscritura;NotaEscritura.init=init;NotaEscritura.get=e=>instances.get(e);init();
})();
