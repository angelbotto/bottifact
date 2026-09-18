/* A bounded, local relationship explorer. Its tables are the source of truth. */
(() => {
  'use strict';
  const instances = new WeakMap();
  const normalize = s => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const make = (tag, text, cls) => { const el = document.createElement(tag); if (text != null) el.textContent = text; if (cls) el.className = cls; return el; };
  function init(root = document) {
    return [...(root.matches?.('[data-relationship-map]') ? [root] : []), ...root.querySelectorAll('[data-relationship-map]')].map(el => {
      if (instances.has(el)) return instances.get(el);
      const nodeRows = [...el.querySelectorAll('[data-map-nodes] tbody tr')], edgeRows = [...el.querySelectorAll('[data-map-edges] tbody tr')];
      const nodes = nodeRows.map(row => ({id: row.dataset.node, title: row.cells[0]?.textContent.trim(), type: row.cells[1]?.textContent.trim(), detail: row.cells[2]?.textContent.trim()}));
      const edges = edgeRows.map(row => ({source: row.dataset.source, target: row.dataset.target, type: row.cells[0]?.textContent.trim(), reason: row.cells[1]?.textContent.trim(), state: row.cells[2]?.textContent.trim()}));
      const byId = new Map(nodes.map(n => [n.id, n]));
      if (!nodes.length || nodes.length > 100 || edges.length > 250 || byId.size !== nodes.length || nodes.some(n => !n.id || !n.title || !n.type) || edges.some(e => !byId.has(e.source) || !byId.has(e.target) || !e.type || !e.reason || !['Declarada','Sugerida'].includes(e.state))) return null;
      const abort = new AbortController(), on = (target, type, fn) => target.addEventListener(type, fn, {signal: abort.signal});
      const ui = make('div', null, 'relationship-ui'), tools = make('div', null, 'relationship-tools');
      function selectControl(label, values) { const wrap = make('label', label), input = make('select'); for (const [value, text] of values) { const option = make('option', text); option.value = value; input.append(option); } wrap.append(input); tools.append(wrap); return input; }
      const findLabel = make('label', 'Encontrar una pieza'), search = make('input'); search.type = 'search'; search.placeholder = 'Nombre, tipo o contexto'; findLabel.append(search); tools.append(findLabel);
      const focus = selectControl('Punto de partida', nodes.map(n => [n.id, n.title]));
      const depth = selectControl('Alcance', [['1', 'Un salto'], ['2', 'Dos saltos'], ['all', 'Todo el mapa']]);
      const relation = selectControl('Relación', [['', 'Todas'], ...[...new Set(edges.map(e => e.type))].map(t => [t,t])]);
      const certainty = selectControl('Estado', [['', 'Declaradas y sugeridas'], ['Declarada','Sólo declaradas'], ['Sugerida','Sólo sugeridas']]);
      const status = make('p', null, 'procedencia'); status.setAttribute('role', 'status');
      const results = make('div', null, 'relationship-search'); results.setAttribute('aria-label','Resultados de búsqueda');
      const layout = make('div', null, 'relationship-layout'), viewport = make('div', null, 'relationship-viewport'); viewport.tabIndex = 0; viewport.setAttribute('role', 'region'); viewport.setAttribute('aria-label', 'Mapa desplazable; también disponible en la lista de conexiones');
      const stage = make('div', null, 'relationship-stage'), surface = make('div', null, 'relationship-surface'), inspector = make('aside', null, 'relationship-inspector');
      stage.append(surface); viewport.append(stage); layout.append(viewport, inspector);
      const toolbar = make('div', null, 'relationship-actions'); let current = nodes[0].id, history = [], zoom = 1, width = 0, height = 0;
      function button(text, fn) { const b = make('button', text); b.type = 'button'; on(b, 'click', fn); return b; }
      const back = button('← Volver', () => { if (history.length) { current = history.pop(); focus.value = current; update(); surface.querySelector('[aria-pressed="true"]')?.focus({preventScroll:true}); } });
      const fit = () => { zoom = Math.max(.35, Math.min(1, (viewport.clientWidth - 24) / width)); resize(); };
      toolbar.append(back, button('−', () => { zoom = Math.max(.35, zoom / 1.2); resize(); }), button('+', () => { zoom = Math.min(1.8, zoom * 1.2); resize(); }), button('Ajustar', fit), button('100 %', () => {zoom=1;resize();}));
      toolbar.children[1].setAttribute('aria-label','Alejar mapa');toolbar.children[2].setAttribute('aria-label','Acercar mapa');
      ui.append(tools, status, results, toolbar, layout); el.querySelector('h3')?.after(ui);
      function resize() { surface.style.transform = `scale(${zoom})`; stage.style.width = `${width*zoom}px`; stage.style.height = `${height*zoom}px`; }
      function choose(id) { if (id !== current) history.push(current); current=id; focus.value=id; update(); surface.querySelector('[aria-pressed="true"]')?.focus({preventScroll:true}); }
      // Render-time listeners are discarded on every update; persistent controls live until destroy.
      let renderAbort = new AbortController();
      function action(text, fn, cls) { const b=make('button',text,cls); b.type='button'; b.addEventListener('click',fn,{signal:renderAbort.signal}); return b; }
      function update() {
        renderAbort.abort(); renderAbort=new AbortController(); back.disabled=!history.length;
        const candidates=edges.filter(e=>(!relation.value||e.type===relation.value)&&(!certainty.value||e.state===certainty.value));
        let visible=new Set([current]), frontier=new Set([current]);
        if(depth.value==='all') visible=new Set(nodes.map(n=>n.id));
        else for(let i=0;i<Number(depth.value);i++){ const next=new Set(); for(const e of candidates){if(frontier.has(e.source))next.add(e.target);if(frontier.has(e.target))next.add(e.source);} for(const id of next)visible.add(id);frontier=next; }
        const shown=nodes.filter(n=>visible.has(n.id)), links=candidates.filter(e=>visible.has(e.source)&&visible.has(e.target));
        status.textContent=`${shown.length} de ${nodes.length} piezas · ${links.length} de ${edges.length} relaciones · ${depth.value==='all'?'mapa completo':'vecindad de '+byId.get(current).title}. Las flechas indican dirección; las líneas discontinuas son sugerencias.`;
        const words=normalize(search.value).trim().split(/\s+/).filter(Boolean), matches=nodes.filter(n=>words.every(w=>normalize(n.title+' '+n.type+' '+n.detail).includes(w)));
        results.replaceChildren();results.hidden=!words.length;
        if(words.length){results.append(make('p',matches.length+' resultados en todas las piezas'));for(const n of matches)results.append(action(n.title,()=>choose(n.id)));}
        const categories=[...new Set(nodes.map(n=>n.type))], columns=categories.filter(t=>shown.some(n=>n.type===t)), positions=new Map();
        const nodeHeight=Math.max(114,52+Math.ceil(Math.max(...shown.map(n=>n.title.length))/22)*23),rowStep=nodeHeight+42;
        let maxRows=1;columns.forEach((type,col)=>{const members=shown.filter(n=>n.type===type);maxRows=Math.max(maxRows,members.length);members.forEach((n,row)=>positions.set(n.id,{x:24+col*260,y:52+row*rowStep}));});
        width=Math.max(280,columns.length*260+24);height=maxRows*rowStep+72;surface.style.width=width+'px';surface.style.height=height+'px';surface.replaceChildren();
        const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.setAttribute('width',width);svg.setAttribute('height',height);svg.setAttribute('aria-hidden','true');svg.classList.add('relationship-lines');
        links.forEach(e=>{const a=positions.get(e.source),b=positions.get(e.target),path=document.createElementNS(ns,'path'),right=b.x>=a.x,same=b.x===a.x;const x1=a.x+(right?218:0),x2=b.x+(same?218:right?0:218),y1=a.y+nodeHeight/2,y2=b.y+nodeHeight/2;path.setAttribute('d',`M${x1} ${y1} C${x1+(right?35:-35)} ${y1},${x2+(right?-35:35)} ${y2},${x2} ${y2}`);const tip=document.createElementNS(ns,'path');const offset=right?-7:7;tip.setAttribute('d',`M${x2+offset} ${y2-4}L${x2} ${y2}L${x2+offset} ${y2+4}`);svg.append(tip);if(e.state==='Sugerida')path.setAttribute('stroke-dasharray','5 5');svg.append(path);});surface.append(svg);
        columns.forEach((type,col)=>{const label=make('p',type,'relationship-column');label.style.left=(24+col*260)+'px';surface.append(label);});
        shown.forEach(n=>{const pos=positions.get(n.id),b=action('',()=>choose(n.id),'relationship-node');b.setAttribute('aria-pressed',String(n.id===current));b.append(make('small',n.type),make('strong',n.title));b.style.minHeight=nodeHeight+'px';b.style.left=pos.x+'px';b.style.top=pos.y+'px';surface.append(b);});
        const node=byId.get(current);inspector.replaceChildren(make('p',node.type,'ceja'),make('h4',node.title),make('p',node.detail),make('h4','Conexiones explicadas'));
        const local=candidates.filter(e=>e.source===current||e.target===current);
        if(!local.length)inspector.append(make('p','Sin conexiones para estos filtros. Amplía la relación o el estado.'));
        local.forEach(e=>{const outgoing=e.source===current,other=byId.get(outgoing?e.target:e.source),box=make('div',null,'relationship-link');box.append(make('p',`${outgoing?'Sale hacia':'Llega desde'} ${other.title} · ${e.type}`),make('p',e.reason),make('small',e.state),action('Explorar '+other.title,()=>choose(other.id)));inspector.append(box);});
        const directory=make('details'),summary=make('summary','Lista equivalente · '+shown.length+' piezas');directory.append(summary);shown.forEach(n=>directory.append(action(n.title,()=>choose(n.id))));inspector.append(directory);resize();
      }
      on(search,'input',update);on(focus,'change',()=>choose(focus.value));for(const control of [depth,relation,certainty])on(control,'change',update);
      const api={get selected(){return current;},select(id){if(byId.has(id))choose(id);},destroy(){abort.abort();renderAbort.abort();ui.remove();instances.delete(el);}};
      instances.set(el,api);update();return api;
    });
  }
  window.BottifactRelationships={init,get:el=>instances.get(el),destroy:el=>instances.get(el)?.destroy()};init();
})();
