/* Sonido central: apagado al cargar, prueba explícita y salida comprobable. */
(()=>{
 'use strict';
 let enabled=false,context=null,master=null,analyser=null,voices=[],epoch=0,plays=0,volume=.65,activating=false;
 let message='Sonido apagado. Pulsa Probar sonido para escuchar una muestra.';
 const toggles=[...document.querySelectorAll('[data-audio-global],[data-sonido]')];
 if(!toggles.length)return;
 document.documentElement.dataset.audioCabecera='';
 const sync=()=>{
  toggles.forEach(b=>{
   b.setAttribute('aria-pressed',String(enabled));b.setAttribute('aria-busy',String(activating));
   const label=activating?'Cancelar activación':enabled?'Sonidos activados':'Sonidos apagados';
   b.querySelector('[data-audio-etiqueta]')?.replaceChildren(document.createTextNode(label));
   if(b.hasAttribute('data-sonido'))b.textContent=enabled?'Sonido activado':'Sonido apagado';
  });
  document.querySelectorAll('[data-audio-estado]').forEach(s=>s.textContent=message);
  document.querySelectorAll('[data-audio-volumen]').forEach(input=>input.value=String(Math.round(volume*100)));
  document.querySelectorAll('[data-audio-volumen-valor]').forEach(s=>s.textContent=Math.round(volume*100)+' %');
  document.querySelectorAll('[data-canal-sonido] [role="status"]').forEach(s=>s.textContent=enabled?'Sonido activado. Pulsa una acción para escucharla.':'Sonido apagado.');
 };
 const stop=()=>{voices.forEach(({node,gain})=>{try{node.stop();}catch{}node.disconnect();gain.disconnect();});voices=[];};
 function disable(reason='Sonido apagado. Pulsa Probar sonido para escuchar una muestra.'){
  enabled=false;activating=false;epoch++;stop();context?.suspend().catch(()=>{});message=reason;
  document.querySelectorAll('[data-canal-sonido]').forEach(e=>window.NotaSonido?.get(e)?.disable());sync();
 }
 async function activate(){
  const Audio=window.AudioContext||window.webkitAudioContext;
  if(!Audio){message='Este navegador no ofrece sonido Web Audio.';sync();return false;}
  const current=++epoch;activating=true;message='Activando sonido…';sync();let timer;
  try{
   if(!context||context.state==='closed'){
    context=new Audio();master=context.createGain();master.gain.value=volume;analyser=context.createAnalyser();analyser.fftSize=2048;
    master.connect(analyser);analyser.connect(context.destination);
    context.addEventListener('statechange',()=>{
     if(enabled&&context.state!=='running')disable('El navegador pausó el audio. Pulsa Probar sonido para reactivarlo.');
    });
   }
   await Promise.race([context.resume(),new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error('timeout')),3500);})]);
   if(current!==epoch||document.hidden)return false;
   if(context.state!=='running')throw Error('suspended');
   enabled=true;activating=false;message='Sonidos activados. Puedes probar el tono o la escritura.';sync();return true;
  }catch{if(current===epoch)disable('No se pudo activar el audio. Pulsa Probar sonido; revisa si esta pestaña está silenciada.');return false;}
  finally{clearTimeout(timer);}
 }
 function signal(kind,writingDuration){
  if(!enabled||!context||context.state!=='running'||document.hidden)return;
  if(kind==='hover'&&voices.some(v=>v.kind==='escritura'))return;
  stop();const now=context.currentTime,gain=context.createGain();let node,duration;
  if(kind==='escritura'){
   duration=writingDuration||.65;
   const buffer=context.createBuffer(1,Math.ceil(context.sampleRate*duration),context.sampleRate),data=buffer.getChannelData(0);let last=0,energy=0;
   for(let i=0;i<data.length;i++){last=.78*last+.22*(Math.random()*2-1);data[i]=last*(.35+.65*Math.sin(i/context.sampleRate*19)**4);energy+=data[i]**2;}
   const scale=.35/Math.max(.001,Math.sqrt(energy/data.length));
   for(let i=0;i<data.length;i++)data[i]=Math.max(-.9,Math.min(.9,data[i]*scale));
   node=context.createBufferSource();node.buffer=buffer;
   gain.gain.setValueAtTime(0,now);gain.gain.linearRampToValueAtTime(.18,now+.025);gain.gain.setValueAtTime(.14,now+duration-.07);gain.gain.linearRampToValueAtTime(0,now+duration);
  }else{
   duration=kind==='prueba'?.45:kind==='hover'?.06:.09;node=context.createOscillator();node.type='sine';
   node.frequency.setValueAtTime(kind==='confirmacion'?740:kind==='atencion'?390:540,now);
   if(kind==='prueba')node.frequency.exponentialRampToValueAtTime(720,now+duration);
   gain.gain.setValueAtTime(0,now);gain.gain.linearRampToValueAtTime(kind==='prueba'?.12:kind==='hover'?.012:.035,now+.008);gain.gain.exponentialRampToValueAtTime(.0001,now+duration);
  }
  node.connect(gain);gain.connect(master);const voice={node,gain,kind};voices.push(voice);
  const release=()=>{node.disconnect();gain.disconnect();voices=voices.filter(v=>v!==voice);};node.onended=release;
  node.start(now);node.stop(now+duration);plays++;
  return ()=>{try{node.stop();}catch{}release();};
 }
 document.addEventListener('click',async e=>{
  if(!e.isTrusted)return;const b=e.target.closest('button');if(!b||b.disabled)return;
  if(b.matches('[data-audio-prueba]')){
   if(!enabled||context?.state!=='running'){if(!await activate())return;}
   signal('prueba');message='Muestra reproducida al '+Math.round(volume*100)+' %. Si no la oyes, revisa el volumen y el silencio de la pestaña.';sync();return;
  }
  if(b.matches('[data-audio-global],[data-sonido]')){if(enabled||activating)disable();else await activate();return;}
  if(b.dataset.audio){
   const written=b.dataset.manoRepetir?document.getElementById(b.dataset.manoRepetir):b.closest('[data-escritura]');
   if(b.dataset.audio==='escritura'&&written?.hasAttribute('data-escritura-sonora'))return;
   const status=b.closest('[data-canal-sonido]')?.querySelector('[role="status"]');if(status)status.textContent=b.dataset.mensaje||b.textContent.trim();
   const local=b.closest('[data-canal-sonido]');if(local&&window.NotaSonido?.get(local)?.enabled)return;
   signal(b.dataset.audio);
  }
 });
 document.addEventListener('input',e=>{if(!e.target.matches('[data-audio-volumen]'))return;const n=Number(e.target.value);if(!Number.isFinite(n))return;volume=Math.max(0,Math.min(1,n/100));if(master)master.gain.setTargetAtTime(volume,context.currentTime,.015);sync();});
 let lastPointer=null,lastTarget=null,lastHover=-Infinity;
 document.addEventListener('pointermove',e=>{
  if(!e.isTrusted||e.pointerType!=='mouse')return;
  const moved=lastPointer&&Math.hypot(e.clientX-lastPointer.x,e.clientY-lastPointer.y)>1;
  lastPointer={x:e.clientX,y:e.clientY};const target=e.target.closest('[data-audio-hover]');if(!moved)return;
  if(target!==lastTarget&&target&&performance.now()-lastHover>=160&&enabled){signal('hover');lastHover=performance.now();}
  lastTarget=target;
 },{passive:true});
 document.addEventListener('visibilitychange',()=>{if(document.hidden)disable('Audio apagado al salir de la pestaña. Pulsa Probar sonido para volver a escucharlo.');});
 addEventListener('pagehide',()=>disable());
 window.NotaAudio={disable,writing(element,duration){
  const r=element.getBoundingClientRect();
  if(!element.hasAttribute('data-escritura-sonora')||!Number.isFinite(duration)||duration<100||duration>10000||r.bottom<=0||r.top>=innerHeight||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  return signal('escritura',duration/1000);
 },sampleLevel(){if(!analyser)return {peak:0,rms:0};const data=new Float32Array(analyser.fftSize);analyser.getFloatTimeDomainData(data);return {peak:Math.max(...data.map(Math.abs)),rms:Math.sqrt(data.reduce((sum,v)=>sum+v*v,0)/data.length)};},get state(){return context?.state||'uninitialized';},get volume(){return volume;},get enabled(){return enabled;},get activeVoices(){return voices.length;},get plays(){return plays;}};
 sync();
})();
