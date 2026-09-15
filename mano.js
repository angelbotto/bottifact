/* Nota Tikin · alfabeto monolineal original, dibujado como trazos SVG.
   Minúsculas latinas, acentos, números y puntuación; otros glifos conservan texto.
   No usa fuentes remotas, temporizadores de escritura ni RAF. */
(()=>{'use strict';
 const NS='http://www.w3.org/2000/svg',instances=new WeakMap();
 const letters={
 a:[16,'M13 14 C5 9 1 17 4 23 C8 28 14 19 13 14 L13 25 Q15 27 17 23'],
 b:[16,'M4 25 Q2 8 6 3 Q10 0 7 12 L4 23 C8 11 17 12 15 20 Q12 29 4 24'],
 c:[15,'M14 14 C7 8 1 17 4 23 Q8 29 15 23'],
 d:[17,'M14 14 C7 9 1 17 4 24 Q11 29 14 16 L16 3 Q12 7 13 25 L17 24'],
 e:[15,'M4 19 Q17 19 13 13 C8 9 1 17 4 23 Q9 29 16 23'],
 f:[12,'M4 34 Q8 13 8 5 Q7 0 4 6 L4 28 Q4 38 1 32 M1 15 L13 14'],
 g:[17,'M14 14 C5 9 1 19 5 24 Q12 29 14 15 L13 29 C13 38 3 39 4 32 L15 27'],
 h:[17,'M4 26 Q3 8 7 3 Q10 1 8 9 L4 24 Q10 10 15 15 L14 25 Q15 28 18 24'],
 i:[9,'M5 14 L4 24 Q6 28 10 23 M6 7 L6.5 8'],
 j:[10,'M7 14 L6 30 Q4 39 1 33 M8 7 L8.5 8'],
 k:[16,'M4 26 L5 3 M15 13 L4 21 Q10 18 15 25 L18 23'],
 l:[10,'M5 3 Q11 0 7 12 Q1 26 7 26 L11 22'],
 m:[25,'M3 14 L3 26 Q7 10 12 15 L11 25 Q17 10 21 15 L21 25 Q23 28 26 23'],
 n:[17,'M3 14 L3 26 Q11 8 15 15 L14 25 Q16 27 18 23'],
 o:[16,'M11 13 C3 9 0 22 7 26 C16 30 19 12 11 13 Q12 18 18 17'],
 p:[17,'M4 14 L3 36 M4 23 Q8 9 14 15 C20 25 8 30 4 23'],
 q:[17,'M14 14 C5 9 1 19 5 24 Q12 29 14 14 L13 35 L18 29'],
 r:[14,'M3 14 L3 26 Q5 13 9 13 Q12 12 14 16'],
 s:[14,'M14 14 Q6 9 4 15 Q3 19 11 21 Q17 24 9 27 L2 24'],
 t:[12,'M7 6 L5 23 Q6 29 13 23 M1 14 L13 13'],
 u:[17,'M3 14 L3 22 Q4 31 14 15 L13 25 Q16 28 19 23'],
 v:[16,'M3 14 Q3 22 7 27 Q13 23 16 13'],
 w:[23,'M3 14 Q3 24 7 27 L13 15 Q12 25 17 27 L24 13'],
 x:[16,'M3 14 L15 26 M15 13 L3 26'],
 y:[16,'M3 14 Q2 30 13 19 L15 14 Q15 38 4 36 L3 32'],
 z:[16,'M3 15 Q10 11 15 14 L3 25 Q10 24 17 26'],
 '0':[17,'M9 6 C0 6 0 28 9 28 C19 28 19 6 9 6'],
 '1':[12,'M2 12 L8 6 L7 27 M2 27 L13 27'],
 '2':[16,'M2 11 Q10 1 15 9 Q20 15 2 27 L17 26'],
 '3':[16,'M2 8 Q20 0 12 15 Q22 27 3 27 M7 16 L12 15'],
 '4':[17,'M12 6 L2 20 L18 20 M13 6 L12 28'],
 '5':[16,'M16 6 L4 7 L3 17 Q18 11 16 23 Q13 30 2 26'],
 '6':[16,'M15 6 C2 3 0 29 10 27 C23 24 14 12 4 18'],
 '7':[16,'M2 7 L17 7 L7 28'],
 '8':[16,'M8 16 C-2 10 6 2 13 7 C20 13 1 16 2 23 C4 32 22 26 14 19 L8 16'],
 '9':[16,'M14 16 C2 22 0 5 10 6 Q21 6 11 28'],
 '.':[7,'M4 26 L4.5 26.5'],',':[7,'M5 25 L3 31'],':':[7,'M4 16 L4.5 16.5 M4 25 L4.5 25.5'],
 ';':[7,'M4 16 L4.5 16.5 M5 25 L3 31'],'-':[12,'M2 19 L12 18'],'?':[16,'M2 9 Q8 0 15 8 Q18 12 9 18 L8 21 M8 27 L8.5 27.5'],'!':[8,'M5 5 L4 20 M4 27 L4.5 27.5'],'¿':[16,'M8 6 L8.5 6.5 M8 12 L7 15 Q-2 22 5 28 Q12 33 16 24'],'¡':[8,'M4 7 L4.5 7.5 M4 14 L5 29']
 };
 const svg=(tag,attrs)=>{const e=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));return e;};
 function glyph(c){const parts=c.normalize('NFD'),g=letters[parts[0]];if(!g)return null;let d=g[1];for(const accent of [...parts].slice(1)){if(accent==='\u0301')d+=' M7 7 L11 3';else if(accent==='\u0303')d+=' M3 7 Q6 2 9 6 T15 5';else if(accent==='\u0308')d+=' M5 7 L5.5 7.5 M12 7 L12.5 7.5';else return null;}return [g[0],d];}
 class Mano{
  constructor(e){this.element=e;this.original=[...e.childNodes];this.text=e.textContent;this.paths=[];this.animations=[];this.played=false;this.visible=false;this.dead=false;this.epoch=0;this.abort=new AbortController();this.motion=matchMedia('(prefers-reduced-motion: reduce)');
   this.underline=e.hasAttribute('data-subrayar');
   if(!this.underline&&(this.text.length>240||[...this.text].some(c=>!(/\s/u.test(c))&&!glyph(c))))throw Error('Frase no compatible; se conserva el texto original.');
   if(!this.underline&&this.text.split(/\s+/u).some(word=>([...word].reduce((sum,c)=>sum+glyph(c)[0],5)/34)*parseFloat(getComputedStyle(e).fontSize)>160))throw Error('Palabra demasiado ancha; se conserva el texto.');
   if(this.underline){const s=svg('svg',{viewBox:'0 0 300 14',preserveAspectRatio:'none','aria-hidden':'true',class:'mano-subrayado'});s.append(svg('path',{d:'M3 9 Q98 3 172 8 T297 7'}));e.append(s);this.extra=s;}
   else {const visual=document.createElement('span');visual.className='mano-visual';visual.setAttribute('aria-hidden','true');
    this.text.split(/(\s+)/u).filter(Boolean).forEach(word=>{if(/^\s+$/u.test(word)){visual.append(document.createTextNode(word));return;}const gs=[...word].map(glyph),width=gs.reduce((s,g)=>s+g[0],0)+5,s=svg('svg',{viewBox:`0 0 ${width} 42`,class:'mano-palabra',width:(width/34)+'em',height:'1.24em'});let x=2;gs.forEach(g=>{s.append(svg('path',{d:g[1],transform:`translate(${x} 2)`}));x+=g[0];});visual.append(s);});
    const text=document.createElement('span');text.className='sr-only';text.textContent=this.text;e.replaceChildren(visual,text);this.extra=visual;
   }
   this.paths=[...this.extra.querySelectorAll('path')];this.lengths=this.paths.map(p=>p.getTotalLength());this.duration=Math.max(1400,Math.min(6500,this.text.length*45));if(this.underline)this.duration=650;
   e.classList.add('mano-lista');
   this.buttons=[...document.querySelectorAll('[data-mano-repetir]')].filter(b=>b.dataset.manoRepetir===e.id).map(b=>({b,text:b.dataset.manoEtiqueta||b.textContent}));this.sync();
   this.motion.addEventListener('change',()=>{if(this.motion.matches)this.finish();this.sync();},{signal:this.abort.signal});document.addEventListener('visibilitychange',()=>{if(document.hidden)this.finish();},{signal:this.abort.signal});
   this.observer=new IntersectionObserver(entries=>{this.visible=entries[0].intersectionRatio>=.3;if(this.visible&&!this.played&&!this.motion.matches)this.play();else if(!this.visible&&this.played)this.finish();},{threshold:[0,.3]});this.observer.observe(e);instances.set(e,this);
  }
  sync(){this.buttons.forEach(({b,text})=>{b.disabled=this.motion.matches;b.textContent=this.motion.matches?'Escritura completa · movimiento reducido':text;});}
  finish(){this.stopSound?.();this.stopSound=null;this.epoch++;this.animations.forEach(a=>a.cancel());this.animations=[];this.paths.forEach(p=>{p.style.strokeDasharray='none';p.style.strokeDashoffset='0';});}
  play(){if(this.dead)return;this.finish();if(!this.visible||this.motion.matches||document.hidden)return;this.played=true;this.stopSound=window.NotaAudio?.writing(this.element,this.duration);const epoch=this.epoch,total=this.lengths.reduce((a,b)=>a+b,0);let delay=0;this.paths.forEach((p,i)=>{const length=this.lengths[i],duration=this.duration*length/total;p.style.strokeDasharray=length;p.style.strokeDashoffset=length;this.animations.push(p.animate([{strokeDashoffset:length},{strokeDashoffset:0}],{duration,delay,fill:'forwards',easing:'linear'}));delay+=duration;});Promise.all(this.animations.map(a=>a.finished)).then(()=>{if(!this.dead&&epoch===this.epoch)this.finish();}).catch(()=>{});}
  destroy(){this.finish();this.dead=true;this.observer.disconnect();this.abort.abort();this.element.replaceChildren(...this.original);this.element.classList.remove('mano-lista');this.buttons.forEach(({b,text})=>{b.disabled=false;b.textContent=text;});instances.delete(this.element);}
 }
 function init(root=document){return [...(root.matches?.('[data-mano],[data-subrayar]')?[root]:[]),...root.querySelectorAll('[data-mano],[data-subrayar]')].map(e=>{if(instances.has(e))return instances.get(e);try{return new Mano(e);}catch{document.querySelectorAll('[data-mano-repetir]').forEach(b=>{if(b.dataset.manoRepetir===e.id){b.dataset.manoEtiqueta ||= b.textContent;b.disabled=true;b.textContent='Texto sin animación';}});return null;}});}
 document.addEventListener('click',e=>{const b=e.target.closest('[data-mano-repetir]');if(b)instances.get(document.getElementById(b.dataset.manoRepetir))?.play();});
 window.NotaMano={init,get:e=>instances.get(e)};init();
})();
