/* Bottifact · piezas de reportes. Tablas como fuente, sin red ni animaciones.
   Incluir tras globo.js si se usa recorrido. init/get/destroy por contenedor. */
(() => {
  'use strict';
  const instances = new WeakMap();
  const fmt = n => new Intl.NumberFormat('es-CO', {maximumSignificantDigits: 12, notation: n !== 0 && Math.abs(n) < .001 ? 'scientific' : 'standard'}).format(n);
  const tickFmt = n => new Intl.NumberFormat('es-CO', {maximumSignificantDigits: 4, notation: Math.abs(n) >= 10000 || (n !== 0 && Math.abs(n) < .01) ? 'scientific' : 'standard'}).format(n);
  const el = (tag, cls, text) => {
    const node = document.createElement(tag); if(cls) node.className = cls;
    if(text !== undefined) node.textContent = text; return node;
  };
  const svg = (tag, attrs = {}, text) => {
    const node = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.entries(attrs).forEach(([k,v]) => node.setAttribute(k, String(v)));
    if(text !== undefined) node.textContent = text; return node;
  };
  function finite(raw, missing = false) {
    if(raw === null || raw.trim() === '') { if(missing) return null; throw new TypeError('Falta un valor.'); }
    const n = Number(raw);
    if(!Number.isFinite(n) || Math.abs(n) > 1e9) throw new TypeError('Se admiten valores finitos de hasta mil millones en magnitud.');
    return n;
  }
  function domain(values) {
    const lo = Math.min(0,...values), hi = Math.max(0,...values);
    return lo === hi ? [0,1] : [lo,hi];
  }
  const scale = (d,a,b) => v => a + (v-d[0])/(d[1]-d[0])*(b-a);
  function tableData(root, min, max) {
    const table = root.querySelector('table');
    const heads = [...(table?.tHead?.rows[0]?.cells || [])].map(c => c.textContent.trim());
    const rows = [...(table?.tBodies[0]?.rows || [])];
    if(heads.length < min || heads.length > max || !rows.length || rows.length > 60) throw new TypeError('Revisa cabeceras; se admiten de 1 a 60 filas.');
    if(rows.some(r => r.cells.length !== heads.length)) throw new TypeError('Las filas deben tener las mismas columnas.');
    return {table, heads, rows};
  }
  function region(title, width, height) {
    const box = el('div','grafica-caja'); box.tabIndex = 0; box.setAttribute('role','region');
    box.setAttribute('aria-label',title+'. Dibujo desplazable; tabla completa a continuación.');
    const drawing = svg('svg',{viewBox:`0 0 ${width} ${height}`,width,height,role:'img','aria-label':title});
    drawing.append(svg('title',{},title)); box.append(drawing); return [box,drawing];
  }
  function text(root,x,y,value,attrs={}) { const t = svg('text',{x,y,...attrs},value); root.append(t); return t; }
  const linesOf = (value,size) => value.match(new RegExp('.{1,'+size+'}(?:\\s|$)|.{1,'+size+'}', 'g')) || [''];
  function wrapped(root,x,y,value,size=22) {
    const lines = linesOf(value,size);
    const t = text(root,x,y,''); lines.forEach((line,i)=>t.append(svg('tspan',{x,dy:i?18:0},line.trim())));
    return lines.length;
  }
  class Reporte {
    constructor(root) {
      this.root=root; this.parts=[]; this.restore=[]; this.abort=new AbortController(); this.dead=false;
      try {
        switch(root.dataset.reporte) {
          case 'cascada': this.waterfall(); break;
          case 'multiples': this.multiples(); break;
          case 'conciliacion': this.reconcile(); break;
          case 'escenario': this.scenario(); break;
          case 'recorrido': this.journey(); break;
          default: throw new TypeError('Tipo de reporte desconocido.');
        }
        instances.set(root,this);
      } catch(error) {this.destroy();throw error;}
    }
    add(node,before=this.root.querySelector('.tabla-caja')) {this.root.insertBefore(node,before);this.parts.push(node);return node;}
    change(node,value) {if(!node)throw new TypeError('Falta una celda de resultado.');const children=[...node.childNodes];this.restore.push(()=>node.replaceChildren(...children));node.textContent=value;}
    on(node,type,fn) {node.addEventListener(type,fn,{signal:this.abort.signal});}
    waterfall() {
      const {table,rows}=tableData(this.root,3,3);
      let total=0;
      const data=rows.map(r=>{
        const value=finite(r.cells[1].getAttribute('data-valor'));
        const from=total; total+=value;
        if(Math.abs(total)>1e9)throw new TypeError('El acumulado excede mil millones.');
        return {row:r,label:r.cells[0].textContent.trim(),value,from,to:total};
      });
      const d=domain(data.flatMap(r=>[r.from,r.to]));
      const layout=data.map(r=>Math.max(64,linesOf(r.label,20).length*18+22));
      const width=860,height=layout.reduce((a,b)=>a+b,0)+160;
      const [box,s]=region(table.caption?.textContent||'Cascada',width,height);
      s.dataset.xMin=d[0];s.dataset.xMax=d[1];const x=scale(d,300,680),bottom=height-52;
      for(let i=0;i<=4;i++) {
        const tick=d[0]+(d[1]-d[0])*i/4;
        s.append(svg('line',{x1:x(tick),x2:x(tick),y1:40,y2:bottom,class:'grafica-rejilla','data-tick-x':tick}));
        text(s,x(tick),bottom+30,tickFmt(tick),{'text-anchor':'middle'});
      }
      s.append(svg('line',{x1:x(0),x2:x(0),y1:40,y2:bottom,class:'grafica-eje'}));
      let y=56;
      data.forEach((r,i)=>{
        wrapped(s,12,y+17,r.label,20);
        const bar=svg('rect',{x:Math.min(x(r.from),x(r.to)),y,width:Math.abs(x(r.to)-x(r.from)),height:28,
          class:r.value<0?'cascada-baja':'cascada-sube','data-from':r.from,'data-to':r.to});
        bar.append(svg('title',{},r.label+': '+fmt(r.value)+'; acumulado '+fmt(r.to)));s.append(bar);
        text(s,700,y+18,(r.value>0?'+':'')+fmt(r.value));
        if(i<data.length-1)s.append(svg('path',{d:`M${x(r.to)} ${y+28}V${y+layout[i]}`,class:'cascada-enlace'}));
        y+=layout[i];
      });
      text(s,12,y+18,'Resultado');text(s,700,y+18,fmt(total));
      s.append(svg('rect',{x:Math.min(x(0),x(total)),y,width:Math.abs(x(total)-x(0)),height:28,class:'cascada-total','data-total':total}));
      this.add(box);
      data.forEach(r=>this.change(r.row.cells[2],fmt(r.to)));
      if(table.tFoot)this.change(table.tFoot.rows[0].cells[2],fmt(total));
    }
    multiples() {
      const {table,rows,heads}=tableData(this.root,2,5);
      if(rows.length<2)throw new TypeError('Los múltiples necesitan al menos dos períodos.');
      const labels=rows.map(r=>r.cells[0].textContent.trim());
      const values=rows.map(r=>[...r.cells].slice(1).map(c=>finite(c.getAttribute('data-valor'),true)));
      const d=domain(values.flat().filter(v=>v!==null));
      const group=el('div','multiples-rejilla');
      heads.slice(1).forEach((head,index)=>{
        const panel=el('div');panel.append(el('h4','',head));
        const [box,s]=region(head+' · '+(table.caption?.textContent||'Serie'),360,290);
        s.dataset.yMin=d[0];s.dataset.yMax=d[1];const x=scale([0,rows.length-1],80,290),y=scale(d,185,25);
        [0,.5,1].forEach(f=>{const tick=d[0]+(d[1]-d[0])*f;
          text(s,68,y(tick)+4,tickFmt(tick),{'text-anchor':'end'});
          s.append(svg('line',{x1:80,x2:290,y1:y(tick),y2:y(tick),class:'grafica-rejilla','data-tick-y':tick}));});
        let path='',pen=false;
        values.forEach((row,i)=>{
          const v=row[index];if(v===null){pen=false;return;}
          path+=(pen?'L':'M')+x(i)+' '+y(v);pen=true;
          const p=svg('circle',{cx:x(i),cy:y(v),r:4,class:'grafica-punto serie-0','data-value':v});p.append(svg('title',{},labels[i]+': '+fmt(v)));s.append(p);
        });
        s.prepend(svg('path',{d:path,class:'grafica-trazo serie-0'}));
        // Los extremos se identifican por índice; la tabla nombra todos los períodos.
        text(s,80,220,'1',{'text-anchor':'middle'});text(s,290,220,String(rows.length),{'text-anchor':'middle'});
        text(s,185,258,'Período de la tabla',{'text-anchor':'middle'});
        panel.append(box);group.append(panel);
      });
      this.add(group);
    }
    reconcile() {
      const {table,rows}=tableData(this.root,5,5);
      const data=rows.map(row=>{
        const a=finite(row.cells[1].getAttribute('data-valor')), b=finite(row.cells[2].getAttribute('data-valor'),true);
        if(!Number.isSafeInteger(a)||a<0||(b!==null&&(!Number.isSafeInteger(b)||b<0))) throw new TypeError('Conciliación requiere conteos enteros no negativos.');
        return {row,a,b};
      });
      let expected=0,observed=0,complete=true;
      data.forEach(({row,a,b})=>{expected+=a; if(b===null)complete=false;else observed+=b;
        this.change(row.cells[3],b===null?'Sin dato':(b-a>0?'+':'')+fmt(b-a));});
      if(table.tFoot) {
        const cells=table.tFoot.rows[0].cells;
        this.change(cells[1],fmt(expected));this.change(cells[2],complete?fmt(observed):'Incompleto');
        this.change(cells[3],complete?fmt(observed-expected):'Sin comparación');
      }
    }
    scenario() {
      const form=this.root.querySelector('form');
      const fields=['volumen','antes','despues'].map(n=>form?.elements.namedItem(n));
      const result=this.root.querySelector('[data-resultado]');const detail=this.root.querySelector('[data-formula]');
      if(fields.some(f=>!f)||!result||!detail)throw new TypeError('Faltan campos o resultados del escenario.');
      this.change(result,result.textContent);this.change(detail,detail.textContent);
      const update=()=>{
        if(fields.some(f=>!f.validity.valid||f.value==='')) {result.textContent='Completa los tres valores dentro de sus límites.';detail.textContent='No hay una estimación válida.';return;}
        const [volume,before,after]=fields.map(f=>Number(f.value));
        const hours=volume*(before-after)/60;
        result.textContent=fmt(Math.abs(hours))+' h/mes '+(hours>=0?'liberadas':'adicionales');
        detail.textContent=`${fmt(volume)} operaciones × (${fmt(before)} − ${fmt(after)}) min ÷ 60 = ${fmt(hours)} h/mes. Es capacidad estimada, no ahorro monetario ni una predicción.`;
      };
      this.on(form,'submit',e=>e.preventDefault());this.on(form,'input',update);
      this.on(form,'reset',()=>queueMicrotask(()=>{if(!this.dead)update();}));update();
    }
    journey() {
      const stage=this.root.querySelector('[data-recorrido-globo]');
      const steps=[...this.root.querySelectorAll('[data-ruta]')];
      const status=this.root.querySelector('[data-recorrido-estado]');
      const prev=this.root.querySelector('[data-paso="prev"]'),next=this.root.querySelector('[data-paso="next"]');
      if(!stage||!steps.length||!status||!prev||!next||!window.NotaGlobo)throw new TypeError('El recorrido necesita pasos, controles y NotaGlobo.');
      const points=new Map(),ids=new Set();
      const arcs=steps.map(step=>{
        const places=[...step.querySelectorAll('[data-lugar]')];const id=step.dataset.ruta;
        if(!id||ids.has(id)||places.length!==2)throw new TypeError('Cada paso necesita una ruta única y dos lugares.');ids.add(id);
        places.forEach(place=>{
          const p={id:place.dataset.lugar,label:place.textContent.trim(),lat:finite(place.getAttribute('data-lat')),lon:finite(place.getAttribute('data-lon'))};
          if(!p.id || Math.abs(p.lat)>90 || Math.abs(p.lon)>180)throw new TypeError('Coordenada geográfica inválida.');
          if(points.has(p.id)&&JSON.stringify(points.get(p.id))!==JSON.stringify(p))throw new TypeError('Coordenadas o nombre inconsistentes para el mismo lugar.');
          points.set(p.id,p);
        });
        return {id,from:places[0].dataset.lugar,to:places[1].dataset.lugar,label:places.map(p=>p.textContent.trim()).join(' → '),detail:step.querySelector('p')?.textContent.trim()||''};
      });
      this.globe=new NotaGlobo(stage,{points:[...points.values()],arcs});this.globe.pause();
      this.change(status,status.textContent);const prior=[prev.disabled,next.disabled];
      this.restore.push(()=>{prev.disabled=prior[0];next.disabled=prior[1];});
      steps.forEach(step=>{const current=step.getAttribute('aria-current');this.restore.push(()=>{if(current===null)step.removeAttribute('aria-current');else step.setAttribute('aria-current',current);});});
      let index=0;
      const go=i=>{
        index=Math.max(0,Math.min(steps.length-1,i));this.globe.select(arcs[index].id);
        steps.forEach((step,k)=>{if(k===index)step.setAttribute('aria-current','step');else step.removeAttribute('aria-current');});
        prev.disabled=index===0;next.disabled=index===steps.length-1;
        status.textContent=`Etapa ${index+1} de ${steps.length}: ${arcs[index].label}. ${arcs[index].detail}`;
      };
      this.on(prev,'click',()=>go(index-1));this.on(next,'click',()=>go(index+1));
      // La lista nativa del globo y los botones del relato comparten la etapa.
      this.on(stage,'click',event=>{
        const button=event.target.closest('[data-route]');if(!button)return;
        const i=arcs.findIndex(arc=>arc.id===button.dataset.route);if(i>=0)go(i);
      });
      go(0);
    }
    destroy() {
      if(this.dead)return;this.dead=true;this.abort.abort();this.globe?.destroy();
      this.parts.forEach(p=>p.remove());this.restore.reverse().forEach(fn=>fn());instances.delete(this.root);
    }
  }
  function init(root=document) {
    return [...(root.matches?.('[data-reporte]')?[root]:[]),...root.querySelectorAll('[data-reporte]')].map(e=>{
      if(instances.has(e))return instances.get(e);
      e.querySelector('[data-error-reporte]')?.remove();
      try {return new Reporte(e);}catch(error){const p=el('p','nota-vacio','No se pudo preparar esta pieza: '+error.message+' El contenido original sigue disponible.');p.dataset.errorReporte='';e.prepend(p);return null;}
    });
  }
  window.NotaReportes={init,get:e=>instances.get(e)};init();
})();
