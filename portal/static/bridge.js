/* Puente de revisión de alcance limitado. Sin cookies, claves ni llamadas de red. */
(()=>{'use strict';
  const pending=new Map(),listeners=new Set();let latest=null;const retries=new Map();
  const send=(op,data={})=>new Promise((resolve,reject)=>{
    const id=crypto.randomUUID(),timer=setTimeout(()=>{pending.delete(id);reject(Error('No se pudo guardar en el NAS. El texto permanece aquí; intenta de nuevo.'));},20000);
    pending.set(id,{resolve,reject,timer});parent.postMessage({bottifact:1,id,op,data},'*');
  });
  addEventListener('message',event=>{
    if(event.source!==parent||!event.data||event.data.bottifact!==1)return;
    const message=event.data;
    if(message.op==='snapshot'){latest=message.data;listeners.forEach(fn=>fn(latest));return;}
    const request=pending.get(message.id);if(!request)return;
    clearTimeout(request.timer);pending.delete(message.id);
    if(message.error)request.reject(Error(message.error));else request.resolve(message.data);
  });
  window.BottifactReviewBridge={
    commit:async data=>{const key=JSON.stringify(data),id=retries.get(key)||crypto.randomUUID();retries.set(key,id);const result=await send('commit',{...data,id});retries.delete(key);latest=result;listeners.forEach(fn=>fn(result));return result;},
    subscribe:fn=>{listeners.add(fn);if(latest)fn(latest);return()=>listeners.delete(fn);},
    identify:()=>send('identify').catch(()=>{}),
  };
  addEventListener('DOMContentLoaded',()=>send('ready').then(value=>{latest=value;listeners.forEach(fn=>fn(value));}).catch(()=>{}),{once:true});
})();
