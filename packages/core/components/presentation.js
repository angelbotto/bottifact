/* Dedicated slide navigation. Articles and decks are authored as separate deliverables. */
(() => {
  'use strict';
  const main = document.querySelector('main[data-presentation]');
  if (!main || main.dataset.presentationReady) return;
  main.dataset.presentationReady = '';
  const pages = [...main.querySelectorAll(':scope > .pagina')];
  if (!pages.length) return;
  const root = document.documentElement;
  let index = Math.max(0, pages.findIndex(p => !p.hidden));
  const make = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  const tools = make('nav', '', 'presentation-tools');
  tools.setAttribute('aria-label', 'Controles de presentación');
  const previous = make('button'), next = make('button'), overview = make('button'), fullscreen = make('button');
  function decorate(button, label, icon, iconOnly = false) {
    button.type = 'button';button.setAttribute('aria-label', label);button.title = label;
    if (iconOnly) button.replaceChildren(window.BottifactUI?.icon(icon) || make('span', label));
    else window.BottifactUI?.decorate(button, icon);
  }
  decorate(previous, 'Diapositiva anterior', 'back', true);
  decorate(next, 'Diapositiva siguiente', 'arrow', true);
  decorate(fullscreen, 'Pantalla completa', 'expand', true);
  overview.type = 'button';overview.setAttribute('aria-haspopup','dialog');
  const count = make('span', '', 'presentation-count');count.setAttribute('aria-live','polite');
  tools.append(previous, overview, next, fullscreen, count);main.before(tools);
  fullscreen.hidden = !document.fullscreenEnabled;
  const dialog = make('dialog', '', 'presentation-overview');
  const heading = make('h2', 'Diapositivas');heading.id = 'presentation-overview-title';dialog.setAttribute('aria-labelledby',heading.id);
  const close = make('button', 'Cerrar');close.type = 'button';
  const grid = make('div', '', 'presentation-slide-index');
  const choices = pages.map((page, i) => {
    const button = make('button');button.type = 'button';
    button.append(make('span', String(i+1).padStart(2,'0'), 'presentation-slide-number'), make('strong', page.querySelector('h1')?.textContent || 'Diapositiva '+(i+1)), make('span', (page.querySelector('p:not(.ceja)')?.textContent || '').slice(0,160)));
    button.addEventListener('click', () => {dialog.close();go(i);});grid.append(button);return button;
  });
  dialog.append(heading, close, grid);document.body.append(dialog);
  function sync() {
    root.dataset.presentationView = 'slides';
    pages.forEach((page,i) => page.hidden = i !== index);
    previous.disabled = index === 0;next.disabled = index === pages.length-1;
    overview.textContent = (index+1)+' / '+pages.length;
    overview.setAttribute('aria-label', 'Ver las '+pages.length+' diapositivas. Actual: '+(index+1));
    count.textContent = 'Diapositiva '+(index+1)+' de '+pages.length;
    choices.forEach((b,i) => {if(i===index)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');});
  }
  function go(i) {
    if (i < 0 || i >= pages.length) return;
    document.querySelector('.barra [data-ir="'+CSS.escape(pages[i].id)+'"]')?.click();
  }
  previous.addEventListener('click',()=>go(index-1));next.addEventListener('click',()=>go(index+1));
  overview.addEventListener('click',()=>{dialog.showModal();choices[index]?.focus();});
  close.addEventListener('click',()=>{dialog.close();overview.focus();});
  dialog.addEventListener('cancel',()=>overview.focus());
  fullscreen.addEventListener('click',async()=>{
    try{if(document.fullscreenElement)await document.exitFullscreen();else await root.requestFullscreen();}
    catch{count.textContent='Pantalla completa no disponible en este visor.';}
  });
  document.addEventListener('nota:pagina',event=>{const i=pages.findIndex(p=>p.id===event.detail.id);if(i>=0){index=i;sync();}});
  document.addEventListener('keydown',event=>{
    if(event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey || root.hasAttribute('data-revisando') || document.querySelector('dialog[open]') || event.target.closest('input,textarea,select,button,a,summary,[contenteditable],.bottifact-toolbar,[role="slider"],[role="grid"],pre,[data-explorador]'))return;
    const destination={ArrowRight:index+1,PageDown:index+1,ArrowLeft:index-1,PageUp:index-1,Home:0,End:pages.length-1}[event.key];
    if(destination!==undefined){event.preventDefault();go(destination);}
  });
  // Navigation preserves the original slide nodes and comment anchors.
  sync();
})();
