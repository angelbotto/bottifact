/* Revisión local de bloques. Sin red ni almacenamiento; prompt explícito y copiable. */
(()=>{'use strict';const instances=new WeakMap();
 function init(root=document){return [...(root.matches?.('[data-revision]')?[root]:[]),...root.querySelectorAll('[data-revision]')].map(el=>{
  if(instances.has(el))return instances.get(el);
  const editor=el.querySelector('[data-revision-editor]'),panel=el.querySelector('[data-revision-panel]'),input=el.querySelector('[data-revision-texto]'),context=el.querySelector('[data-revision-contexto]'),list=el.querySelector('[data-revision-notas]'),prompt=el.querySelector('[data-revision-prompt]'),status=el.querySelector('[data-revision-estado]');
  if(!editor||!panel||!input||!context||!list||!prompt||!status)return null;
  const abort=new AbortController(),notes=[],addedIDs=new Map(),originalStatus=status.textContent,originalPrompt=prompt.textContent;
  let mode=false,pending=null,editing=null,serial=0;const focusTargets=new Map();
  const bar=document.createElement('div');bar.className='revision-barra revision-ui';bar.setAttribute('role','group');bar.setAttribute('aria-label','Revisar este documento');
  const modeButton=el.querySelector('[data-revision-modo]').cloneNode(true),listButton=el.querySelector('[data-revision-lista]').cloneNode(true);bar.append(modeButton,listButton);document.body.append(bar,editor,panel);
  function listen(node,type,fn,options={}){node.addEventListener(type,fn,{...options,signal:abort.signal});}
  function setMode(value){
   focusTargets.forEach((old,node)=>old===null?node.removeAttribute('tabindex'):node.setAttribute('tabindex',old));focusTargets.clear();
   if(value)document.querySelectorAll('main .pagina.viva p,main .pagina.viva h1,main .pagina.viva h2,main .pagina.viva h3,main .pagina.viva figure,main:not(.multipagina) p,main:not(.multipagina) figure').forEach(node=>{if(node.closest('.receta-copia,[data-revision],.revision-ui')||!node.getClientRects().length)return;focusTargets.set(node,node.getAttribute('tabindex'));node.tabIndex=0;});
   mode=value;document.documentElement.toggleAttribute('data-revisando',mode);[modeButton,el.querySelector('[data-revision-modo]')].forEach(b=>{b.setAttribute('aria-pressed',String(mode));b.textContent=mode?'Elige un fragmento · Esc cancela':'Comentar documento';});status.textContent=mode?'Elige un párrafo, título, figura o card. Escape cancela.':notes.length+' comentarios locales. Copia antes de recargar.';}
  function make(tag,text){const node=document.createElement(tag);node.textContent=text;return node;}
  function render(){list.replaceChildren();notes.forEach((note,i)=>{
   note.marker.textContent=String(i+1);note.marker.setAttribute('aria-label','Editar comentario '+(i+1));
   const li=document.createElement('li'),quote=make('blockquote',note.quote),p=make('p',note.text),actions=document.createElement('div');actions.className='acciones';
   const link=make('a','Ver fragmento');link.href='#'+note.target.id;listen(link,'click',()=>panel.close());
   const edit=make('button','Editar'),remove=make('button','Borrar');edit.type=remove.type='button';listen(edit,'click',()=>{panel.close();open(note);});listen(remove,'click',()=>{note.marker.remove();notes.splice(notes.indexOf(note),1);render();panel.querySelector('[data-revision-cerrar]').focus();});
   actions.append(link,edit,remove);li.append(make('p',note.page+' · '+note.reference),quote,p,actions);list.append(li);
  });
  if(!notes.length)list.append(make('li','Todavía no hay comentarios. Cierra esta ventana y elige un fragmento.'));
  prompt.textContent=notes.length?'Aplica estos ajustes al artefacto «'+document.title+'». Conserva el contenido y comportamiento no señalados.\n\n'+notes.map((n,i)=>(i+1)+'. Capítulo: '+n.page+'\nReferencia: #'+n.reference+'\nFragmento: '+n.quote+'\nAjuste: '+n.text).join('\n\n'):'No hay comentarios todavía.';
  listButton.textContent='Ver comentarios · '+notes.length;status.textContent=notes.length+' comentarios locales. Copia antes de recargar.';
  }
  function open(note){editing=notes.includes(note)?note:null;pending=note;setMode(false);context.textContent=note.page+' · '+note.quote;input.value=editing?note.text:'';editor.querySelector('h2').textContent=editing?'Editar comentario':'Añadir comentario';editor.showModal();input.focus();}
  function choose(target,selection=''){
   if(!target||!target.closest('main')||target.closest('.revision-ui,.receta-copia,[data-revision]'))return;
   const page=target.closest('.pagina');let anchor=target;while(anchor&&(!anchor.id||addedIDs.has(anchor)))anchor=anchor.parentElement;const reference=anchor?.id||page?.id||'contenido';
   const quote=(selection||target.textContent).trim().replace(/\s+/g,' ').slice(0,1000);if(!quote)return;
   open({target,reference,page:page?.querySelector('h1')?.textContent||document.title,quote,text:''});
  }
  function toggle(){const selected=getSelection(),text=selected?.toString().trim(),node=selected?.anchorNode;
   if(text&&node){const element=node.nodeType===1?node:node.parentElement;const target=element.closest('p,h1,h2,h3,h4,figure,.card-editorial,li');if(target?.closest('main')&&!target.closest('.revision-ui,.receta-copia')){choose(target,text);return;}}
   setMode(!mode);
  }
  [modeButton,el.querySelector('[data-revision-modo]')].forEach(b=>listen(b,'click',toggle));
  [listButton,el.querySelector('[data-revision-lista]')].forEach(b=>listen(b,'click',()=>{setMode(false);render();panel.showModal();}));
  listen(document,'click',event=>{
   if(!mode||event.target.closest('.revision-ui,button,input,select,textarea,summary,a,.barra,.receta-copia'))return;
   let target=event.target.closest('figure,table,.card-editorial')||event.target.closest('p,h1,h2,h3,h4,.card-editorial,li');if(!target?.closest('main'))return;
   event.preventDefault();event.stopPropagation();choose(target);
  },{capture:true});
  listen(document,'nota:pagina',()=>{if(mode)setMode(false);});
  listen(document,'keydown',e=>{if(mode&&e.key==='Enter'&&focusTargets.has(e.target)){e.preventDefault();choose(e.target);return;}if(e.key==='Escape'&&mode){setMode(false);modeButton.focus();}});
  listen(editor.querySelector('form'),'submit',e=>e.preventDefault());
  listen(editor.querySelector('[data-revision-guardar]'),'click',()=>{
   if(!input.value.trim()){input.setCustomValidity('Escribe el ajuste que propones.');input.reportValidity();return;}input.setCustomValidity('');if(!input.reportValidity())return;
   pending.text=input.value.trim();
   if(!editing){const note=pending;if(!note.target.id){let id;do{id='nota-revision-bloque-'+(++serial);}while(document.getElementById(id));addedIDs.set(note.target,'');note.target.id=id;}
    const marker=make('button','');marker.type='button';marker.className='revision-marca';note.marker=marker;note.target.before(marker);notes.push(note);listen(marker,'click',()=>open(note));
   }render();editor.close();pending=null;editing=null;modeButton.focus();
  });
  listen(input,'input',()=>input.setCustomValidity(''));
  listen(editor.querySelector('[data-revision-cancelar]'),'click',()=>editor.close());listen(panel.querySelector('[data-revision-cerrar]'),'click',()=>panel.close());
  const instance={get comments(){return notes.map(({text,quote,page,reference})=>({text,quote,page,reference}));},destroy(){setMode(false);abort.abort();editor.close();panel.close();bar.remove();notes.forEach(n=>n.marker.remove());addedIDs.forEach((_,node)=>node.removeAttribute('id'));el.append(editor,panel);status.textContent=originalStatus;prompt.textContent=originalPrompt;list.replaceChildren();instances.delete(el);}};
  instances.set(el,instance);return instance;
 });}
 window.NotaRevision={init,get:el=>instances.get(el)};init();
})();
