/* Sonido central: activación explícita; hover optativo sólo al mover el puntero. */
(()=>{'use strict';let enabled=false,context=null,voices=[],epoch=0,plays=0;const toggles=[...document.querySelectorAll('[data-audio-global],[data-sonido]')];
 if(!toggles.length)return;document.documentElement.dataset.audioCabecera='';
 const sync=()=>{document.querySelectorAll('[data-canal-sonido] [role="status"]').forEach(s=>s.textContent=enabled?'Sonido activado. Pulsa una acción para escucharla.':'Sonido apagado.');toggles.forEach(b=>{b.setAttribute('aria-pressed',String(enabled));b.querySelector('[data-audio-etiqueta]')?.replaceChildren(document.createTextNode(enabled?'Sonidos activados':'Sonidos apagados'));if(b.hasAttribute('data-sonido'))b.textContent=enabled?'Sonido activado':'Sonido apagado';});};
 const stop=()=>{voices.forEach(({node,gain})=>{try{node.stop();}catch{}node.disconnect();gain.disconnect();});voices=[];};
 function disable(){enabled=false;epoch++;stop();context?.suspend().catch(()=>{});document.querySelectorAll('[data-canal-sonido]').forEach(e=>window.NotaSonido?.get(e)?.disable());sync();}
 async function activate(){const Audio=window.AudioContext||window.webkitAudioContext;if(!Audio)return;const current=++epoch;try{context ||= new Audio();await context.resume();if(current!==epoch||document.hidden)return;enabled=true;sync();}catch{disable();}}
 function signal(kind,writingDuration){if(!enabled||!context||context.state!=='running'||document.hidden)return;if(kind==='hover'&&voices.some(v=>v.kind==='escritura'))return;stop();const now=context.currentTime,gain=context.createGain();let node,duration;
  if(kind==='escritura'){duration=writingDuration||.65;const buffer=context.createBuffer(1,Math.ceil(context.sampleRate*duration),context.sampleRate),data=buffer.getChannelData(0);let last=0;for(let i=0;i<data.length;i++){last=.85*last+.15*(Math.random()*2-1);data[i]=last*(.55+.45*Math.sin(i/context.sampleRate*19)**4);}node=context.createBufferSource();node.buffer=buffer;gain.gain.setValueAtTime(0,now);gain.gain.linearRampToValueAtTime(.10,now+.025);gain.gain.setValueAtTime(.075,now+duration-.07);gain.gain.linearRampToValueAtTime(0,now+duration);
  }else{duration=kind==='hover'?.06:.09;node=context.createOscillator();node.type='sine';node.frequency.setValueAtTime(kind==='confirmacion'?740:kind==='atencion'?390:540,now);gain.gain.setValueAtTime(0,now);gain.gain.linearRampToValueAtTime(kind==='hover'?.006:.018,now+.004);gain.gain.exponentialRampToValueAtTime(.0001,now+duration);}
  node.connect(gain);gain.connect(context.destination);const voice={node,gain,kind};voices.push(voice);node.onended=()=>{node.disconnect();gain.disconnect();voices=voices.filter(v=>v!==voice);};node.start(now);node.stop(now+duration);plays++;return ()=>{try{node.stop();}catch{}node.disconnect();gain.disconnect();voices=voices.filter(v=>v!==voice);};
 }
 document.addEventListener('click',async e=>{if(!e.isTrusted)return;const b=e.target.closest('button');if(!b||b.disabled)return;if(b.matches('[data-audio-global],[data-sonido]')){if(enabled)disable();else await activate();return;}if(b.dataset.audio){const written=b.dataset.manoRepetir?document.getElementById(b.dataset.manoRepetir):b.closest('[data-escritura]');if(b.dataset.audio==='escritura'&&written?.hasAttribute('data-escritura-sonora'))return;const status=b.closest('[data-canal-sonido]')?.querySelector('[role="status"]');if(status)status.textContent=b.dataset.mensaje||b.textContent.trim();const local=b.closest('[data-canal-sonido]');if(local&&window.NotaSonido?.get(local)?.enabled)return;signal(b.dataset.audio);}});
 let lastPointer=null,lastTarget=null,lastHover=-Infinity;
 document.addEventListener('pointermove',e=>{
  if(!e.isTrusted||e.pointerType!=='mouse')return;
  const moved=lastPointer&&Math.hypot(e.clientX-lastPointer.x,e.clientY-lastPointer.y)>1;
  lastPointer={x:e.clientX,y:e.clientY};const target=e.target.closest('[data-audio-hover]');
  if(!moved)return;
  if(target!==lastTarget&&target&&performance.now()-lastHover>=160&&enabled){signal('hover');lastHover=performance.now();}
  lastTarget=target;
 },{passive:true});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)disable();});addEventListener('pagehide',disable);
 window.NotaAudio={disable,writing(element,duration){const r=element.getBoundingClientRect();if(!element.hasAttribute('data-escritura-sonora')||!Number.isFinite(duration)||duration<100||duration>10000||r.bottom<=0||r.top>=innerHeight||matchMedia('(prefers-reduced-motion: reduce)').matches)return;return signal('escritura',duration/1000);},get enabled(){return enabled;},get activeVoices(){return voices.length;},get plays(){return plays;}};sync();
})();
