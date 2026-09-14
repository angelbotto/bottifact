/* Resaltado HTML local. Construye nodos de texto; nunca interpreta el código copiable. */
(()=>{'use strict';
 function init(root=document){root.querySelectorAll('.receta-copia code,[data-lenguaje="html"]').forEach(code=>{
  if(code.dataset.coloreado)return;const source=code.textContent;if(!source.trim().startsWith('<'))return;
  const frag=document.createDocumentFragment(),add=(s,cls)=>{if(!cls){frag.append(document.createTextNode(s));return;}const span=document.createElement('span');span.className=cls;span.textContent=s;frag.append(span);};
  const re=/<!--[\s\S]*?-->|<\/?[A-Za-z][^>]*>/g;let end=0;
  for(const match of source.matchAll(re)){add(source.slice(end,match.index));const token=match[0];if(token.startsWith('<!--'))add(token,'com');else{
   const parts=/(<\/?[\w:-]+)|("[^"]*"|'[^']*')|([\w:-]+)(?=\s*=)/g;let pos=0;
   for(const p of token.matchAll(parts)){add(token.slice(pos,p.index));add(p[0],p[1]?'kw':p[2]?'str':'codigo-atributo');pos=p.index+p[0].length;}add(token.slice(pos));
  }end=match.index+token.length;}add(source.slice(end));code.replaceChildren(frag);code.dataset.coloreado='';
 });}
 window.NotaCodigo={init};init();
})();
