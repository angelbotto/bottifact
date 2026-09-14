/* Tabla exploradora: búsqueda, filtro, orden y grupos explícitos. Sin datos remotos. */
(()=>{'use strict';const instances=new WeakMap(),normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
 function init(root=document){return [...(root.matches?.('[data-explorador]')?[root]:[]),...root.querySelectorAll('[data-explorador]')].map(el=>{
  if(instances.has(el))return instances.get(el);const form=el.querySelector('form'),table=el.querySelector('table'),status=el.querySelector('[data-explorador-estado]'),initial=table?.tBodies[0],rows=[...(initial?.rows||[])];
  if(!form||!status||!rows.length||rows.some(r=>r.cells.length!==4||!Number.isFinite(Number(r.cells[3].dataset.valor))))return null;
  const abort=new AbortController(),headers=[...table.tHead.rows[0].cells],originalSort=headers.map(h=>h.getAttribute('aria-sort')),before=status.textContent;
  let column=0,direction=1;const parts=[];
  function update(){parts.splice(0).forEach(p=>p.remove());initial.remove();
   const words=normal(form.elements.buscar.value).trim().split(/\s+/),state=form.elements.estado.value,group=form.elements.grupo.value;
   const visible=rows.filter(r=>(!state||r.cells[2].textContent.trim()===state)&&words.every(w=>normal(r.textContent).includes(w)));
   visible.sort((a,b)=>column<0?rows.indexOf(a)-rows.indexOf(b):direction*(column===3?Number(a.cells[3].dataset.valor)-Number(b.cells[3].dataset.valor):a.cells[column].textContent.localeCompare(b.cells[column].textContent,'es',{numeric:true,sensitivity:'base'}))||rows.indexOf(a)-rows.indexOf(b));
   const groups=new Map();visible.forEach(r=>{const key=group?r.cells[Number(group)].textContent.trim():'';if(!groups.has(key))groups.set(key,[]);groups.get(key).push(r);});
   if(!visible.length){const body=document.createElement('tbody'),row=body.insertRow(),cell=row.insertCell();cell.colSpan=4;cell.textContent='No hay filas que coincidan. Limpia los filtros para volver a empezar.';table.append(body);parts.push(body);}
   for(const [name,items] of [...groups].sort(([a],[b])=>a.localeCompare(b,'es'))){const body=document.createElement('tbody');if(group){const tr=body.insertRow(),th=document.createElement('th');th.scope='rowgroup';th.colSpan=4;th.className='tabla-grupo';th.textContent=name+' · '+items.length+' registros';tr.append(th);}items.forEach(r=>body.append(r));table.append(body);parts.push(body);}
   const total=visible.reduce((s,r)=>s+Number(r.cells[3].dataset.valor),0);
   status.textContent=visible.length+' de '+rows.length+' registros · '+total.toLocaleString('es-CO')+' COP en la vista actual.';
   headers.forEach((h,i)=>{h.setAttribute('aria-sort',i===column?(direction===1?'ascending':'descending'):'none');const hint=h.querySelector('[data-indicador-orden]');if(hint)hint.textContent=i===column?(direction===1?'↑':'↓'):'↕';});
   const hidden=[...form.querySelectorAll('[data-columna]:not(:checked)')].map(e=>Number(e.dataset.columna));headers.forEach((h,i)=>h.hidden=hidden.includes(i));rows.forEach(r=>[...r.cells].forEach((c,i)=>c.hidden=hidden.includes(i)));table.querySelectorAll('.tabla-grupo').forEach(th=>th.colSpan=4-hidden.length);const count=form.querySelector('[data-filtros-cuenta]');if(count)count.textContent=state?'1 · ':'';
  }
  form.addEventListener('input',update,{signal:abort.signal});form.addEventListener('change',update,{signal:abort.signal});form.addEventListener('submit',e=>e.preventDefault(),{signal:abort.signal});
  form.addEventListener('reset',()=>queueMicrotask(()=>{if(abort.signal.aborted)return;column=0;direction=1;update();}),{signal:abort.signal});
  el.querySelectorAll('[data-orden-col]').forEach(b=>b.addEventListener('click',()=>{column=Number(b.dataset.direccion)===0?-1:Number(b.dataset.ordenCol);direction=Number(b.dataset.direccion)||1;update();},{signal:abort.signal}));
  headers.forEach((h,i)=>(h.querySelector('[data-orden-col]')?null:h.querySelector('button'))?.addEventListener('click',()=>{direction=column===i?-direction:1;column=i;update();},{signal:abort.signal}));
  const instance={update,destroy(){abort.abort();parts.forEach(p=>p.remove());rows.forEach(r=>initial.append(r));rows.forEach(r=>[...r.cells].forEach(c=>c.hidden=false));headers.forEach(h=>h.hidden=false);table.append(initial);headers.forEach((h,i)=>originalSort[i]===null?h.removeAttribute('aria-sort'):h.setAttribute('aria-sort',originalSort[i]));status.textContent=before;instances.delete(el);}};
  instances.set(el,instance);update();return instance;
 });}
 window.NotaExplorador={init,get:el=>instances.get(el)};init();
})();
