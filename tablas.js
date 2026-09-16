/* Bottifact · ordenación optativa y series embebidas. Tabla sigue siendo la fuente. */
(() => {
  'use strict';
  const instances=new WeakMap(), NS='http://www.w3.org/2000/svg';
  const numeric=raw=>raw!==null && raw.trim()!=='' && Number.isFinite(Number(raw)) ? Number(raw) : null;
  const svgNode=(tag,attrs)=>{const e=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));return e;};
  function init(root=document) {
    const tables=[...(root.matches?.('[data-tabla]')?[root]:[]),...root.querySelectorAll('table[data-tabla]')];
    return tables.map(table=>{
      if(instances.has(table))return instances.get(table);
      const abort=new AbortController(),parts=[],initial=[...(table.tBodies[0]?.rows||[])];
      const headers=[...(table.tHead?.rows[0]?.cells||[])],sorts=headers.map(h=>h.getAttribute('aria-sort'));
      let status;
      table.querySelectorAll('[data-sparkline]').forEach(cell=>{
        const points=[...cell.querySelectorAll('[data-valor]')].map(e=>numeric(e.getAttribute('data-valor')));
        if(!points.length||points.every(p=>p===null))return;
        const valid=points.filter(p=>p!==null);
        // Exige un dominio compartido, evitando comparar minigráficas autoescaladas entre filas.
        const min=numeric(table.getAttribute('data-min')),max=numeric(table.getAttribute('data-max'));
        if(min===null||max===null||max<=min||valid.some(v=>v<min||v>max))return;
        const svg=svgNode('svg',{viewBox:'0 0 160 44',class:'sparkline','aria-hidden':'true'});
        let d='',pen=false,last;
        points.forEach((v,i)=>{if(v===null){pen=false;return;}const x=4+(points.length===1?76:i/(points.length-1)*152),y=40-(v-min)/(max-min)*36;d+=(pen?'L':'M')+x+' '+y;pen=true;last=[x,y];});
        svg.append(svgNode('path',{d}));if(last)svg.append(svgNode('circle',{cx:last[0],cy:last[1],r:2.5}));
        cell.prepend(svg);parts.push(svg);
      });
      headers.forEach((header,index)=>{
        const button=header.querySelector('[data-ordenar]');if(!button)return;
        header.setAttribute('aria-sort','none');
        button.addEventListener('click',()=>{
          const ascending=header.getAttribute('aria-sort')!=='ascending';
          const rows=[...(table.tBodies[0]?.rows||[])];
          const type=button.dataset.ordenar;
          const key=row=>type==='numero'?numeric(row.cells[index].getAttribute('data-valor')):row.cells[index].textContent.trim();
          rows.sort((a,b)=>{
            const x=key(a),y=key(b);
            // Ausencias al final en ambos sentidos; iguales mantienen orden estable.
            if(x===null)return y===null?0:1;if(y===null)return -1;
            const diff=type==='numero'?x-y:String(x).localeCompare(String(y),'es',{numeric:true,sensitivity:'base'});
            return ascending?diff:-diff;
          });
          rows.forEach(row=>table.tBodies[0].append(row));
          headers.forEach(h=>h.setAttribute('aria-sort',h===header?(ascending?'ascending':'descending'):'none'));
          if(!status){status=document.createElement('p');status.className='copia-estado';status.setAttribute('role','status');table.closest('.tabla-caja').after(status);parts.push(status);}
          status.textContent='Ordenado por '+button.textContent.trim()+', '+(ascending?'ascendente':'descendente')+'.';
        },{signal:abort.signal});
      });
      const instance={destroy(){abort.abort();parts.forEach(e=>e.remove());initial.forEach(r=>table.tBodies[0].append(r));headers.forEach((h,i)=>{if(sorts[i]===null)h.removeAttribute('aria-sort');else h.setAttribute('aria-sort',sorts[i]);});instances.delete(table);}};
      instances.set(table,instance);return instance;
    });
  }
  window.NotaTablas={init,get:el=>instances.get(el)};init();
})();
