/* Puente de revisión de alcance limitado. Sin cookies, claves ni llamadas de red. */
(()=>{'use strict';
  const pending=new Map(),listeners=new Set();let latest=null;const retries=new Map();
  const send=(op,data={})=>new Promise((resolve,reject)=>{
    const id=crypto.randomUUID(),timer=setTimeout(()=>{pending.delete(id);reject(Error('No se pudo guardar. El texto permanece aquí; intenta de nuevo.'));},20000);
    pending.set(id,{resolve,reject,timer});parent.postMessage({bottifact:1,id,op,data},'*');
  });
  addEventListener('message',event=>{
    if(event.source!==parent||!event.data||event.data.bottifact!==1)return;
    const message=event.data;
    if(message.op==='capture-context'){
      const selection=getSelection(),node=selection?.anchorNode,el=node?.nodeType===1?node:node?.parentElement;
      const target=el?.closest('p,h1,h2,h3,h4,li,td,figure,pre')||document.querySelector('h1')||document.body;
      send('context',{reference:target.closest('[id]')?.id||'documento',tag:target.tagName,text:(target.textContent||'').trim().slice(0,4000),quote:(selection?.toString()||target.textContent||document.title).trim().slice(0,1200),page:document.title.slice(0,300),x:.5,y:.5}).catch(()=>{});return;
    }
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
  document.addEventListener('click',event=>{
    const a=event.target.closest?.('a');if(!a)return;
    const href=a.getAttribute('href')||'',base=href.split('#')[0].split('?')[0];
    const mapped=window.BottifactArchiveLinks?.[base]||window.BottifactArchiveLinks?.[base.replace(/^\.\//,'')];
    const path=mapped?(mapped+(href.includes('#')?('#'+href.split('#').slice(1).join('#')):'')):(a.hasAttribute('data-bottifact-link')?href:null);
    if(!path)return;event.preventDefault();send('navigate',{path}).catch(()=>{});
  },true);
  addEventListener('DOMContentLoaded',()=>send('ready',{pins:!!document.querySelector('script[data-nota-modulo="revision.js"]')}).then(value=>{latest=value;listeners.forEach(fn=>fn(value));}).catch(()=>{}),{once:true});
})();
