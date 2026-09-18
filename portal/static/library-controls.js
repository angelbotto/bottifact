/* Searchable facets and column preferences; native selects remain the state source. */
window.BottifactLibraryControls=(()=>{
 const make=(tag,text,cls)=>{const e=document.createElement(tag);if(text!=null)e.textContent=text;if(cls)e.className=cls;return e;};
 function init(root){
  document.addEventListener('pointerdown',event=>{for(const menu of root.querySelectorAll('details[open]'))if(!menu.contains(event.target))menu.open=false;});
  for(const select of root.querySelectorAll('select')){
   if(select.dataset.enhanced)continue;select.dataset.enhanced='true';
   const label=select.closest('label'),name=label.firstChild.textContent.trim(),menu=make('details',null,'facet-menu'),summary=make('summary'),panel=make('div',null,'facet-panel'),search=make('input'),options=make('div',null,'facet-options');
   search.type='search';search.placeholder='Buscar '+name.toLocaleLowerCase();search.setAttribute('aria-label','Buscar opciones de '+name);panel.append(search,options);menu.append(summary,panel);select.hidden=true;label.append(menu);
   function render(){summary.textContent=select.selectedOptions[0]?.textContent||'Elegir';summary.setAttribute('aria-label',name+': '+summary.textContent);options.replaceChildren();const words=search.value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().trim();let count=0;
    for(const option of select.options){if(words&&!option.textContent.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().includes(words))continue;count++;const b=make('button',option.textContent);b.type='button';b.dataset.facetValue=option.value;b.setAttribute('aria-pressed',String(option.selected));b.addEventListener('click',()=>{select.value=option.value;select.dispatchEvent(new Event('change',{bubbles:true}));menu.open=false;summary.focus();render();});options.append(b);}if(!count)options.append(make('p','Sin coincidencias.'));
   }
   search.addEventListener('input',render);select.addEventListener('change',render);select.addEventListener('bottifact-sync',render);menu.addEventListener('toggle',()=>{if(menu.open){for(const other of root.querySelectorAll('details[open]'))if(other!==menu)other.open=false;search.value='';render();search.focus();}});menu.addEventListener('keydown',e=>{if(e.key==='Escape'){e.preventDefault();menu.open=false;summary.focus();}if(e.key==='ArrowDown'&&e.target===search){e.preventDefault();options.querySelector('button')?.focus();}});
   new MutationObserver(render).observe(select,{childList:true,subtree:true});render();
  }
 }
 return {init};
})();
