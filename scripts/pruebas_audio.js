(async () => {
  // Prueba unitaria del manejador y síntesis REAL offline. No simula permiso de audio
  // ni demuestra un clic físico: isTrusted es un objeto de prueba explícito.
  const results=[],NativeAudio=window.AudioContext,Offline=window.OfflineAudioContext||window.webkitOfflineAudioContext;
  if(!Offline)return {skipped:'OfflineAudioContext no disponible'};
  const source=document.querySelector('[data-canal-sonido]');
  for(const [kind,duration] of [['accion',.125],['confirmacion',.125],['atencion',.19]]){
    const f=source.cloneNode(true);f.removeAttribute('id');let handler,context;
    const listen=f.addEventListener.bind(f);f.addEventListener=(type,fn,options)=>{if(type==='click')handler=fn;listen(type,fn,options);};
    window.AudioContext=function(){context=new Offline(1,24000,48000);context.resume=async()=>{};context.suspend=async()=>{};context.close=async()=>{};return context;};
    document.querySelector('main').append(f);
    let e;
    try{
      e=new NotaSonido(f);const toggle=f.querySelector('[data-audio-activar]'),button=f.querySelector('[data-audio="'+kind+'"]');
      await handler({isTrusted:true,target:button});if(e.audio||e.plays)throw new Error('Sonó estando apagado');
      await handler({isTrusted:true,target:toggle});if(!e.enabled||e.plays)throw new Error('Activar emite sonido');
      await handler({isTrusted:true,target:button});const audio=await context.startRendering(),samples=audio.getChannelData(0);
      let peak=0,last=-1,energy=0;for(let i=0;i<samples.length;i++){const v=Math.abs(samples[i]);peak=Math.max(peak,v);energy+=v*v;if(v>1e-5)last=i;}
      if(peak>.026||peak<.018||last/48000>duration+.002||last/48000<duration-.02)throw new Error('Envolvente o duración incorrecta');
      results.push({kind,ok:true,sampleRate:48000,peak,rms:Math.sqrt(energy/samples.length),lastAudible:last/48000,maximumDuration:duration,plays:e.plays});
      e.disable();if(e.voices.length||e.enabled)throw new Error('Voces no canceladas');
    }catch(error){results.push({kind,ok:false,error:error.message});}
    finally{e?.destroy();f.remove();window.AudioContext=NativeAudio;}
  }
  // Una promesa tardía de resume no puede reproducir tras apagar.
  const f=source.cloneNode(true);let handler,resolve;const listen=f.addEventListener.bind(f);
  f.addEventListener=(type,fn,options)=>{if(type==='click')handler=fn;listen(type,fn,options);};
  window.AudioContext=function(){return {resume:()=>new Promise(r=>resolve=r),suspend:async()=>{},close:async()=>{},createOscillator(){throw new Error('No debe crear voces tras apagar');}};};
  try{
    const e=new NotaSonido(f),pending=handler({isTrusted:true,target:f.querySelector('[data-audio-activar]')});
    e.disable();resolve();await pending;results.push({kind:'resume cancelado',ok:!e.enabled&&e.plays===0&&e.voices.length===0});e.destroy();
  }finally{window.AudioContext=NativeAudio;}
  return {method:'Web Audio OfflineAudioContext; manejador con evento unitario, sin audición manual',results};
})()
