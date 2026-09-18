/* Bottifact · attention map: partición binaria con área exactamente proporcional.
   Sin datos remotos ni animación automática; detalle completo fuera de las celdas pequeñas. */
(()=>{'use strict';const NS='http://www.w3.org/2000/svg',instances=new WeakMap();let serial=0;
 const svg=(tag,attrs,text)=>{const n=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>n.setAttribute(k,v));if(text!==undefined)n.textContent=text;return n;};
 const fmt=n=>new Intl.NumberFormat('es-CO',{maximumSignificantDigits:6}).format(n),pct=n=>new Intl.NumberFormat('es-CO',{maximumFractionDigits:1}).format(n);
 function partition(rows,x=0,y=0,w=1000,h=380){if(rows.length===1)return [{...rows[0],x,y,w,h}];const sum=rows.reduce((a,r)=>a+r.value,0);let acc=0,index=0;while(index<rows.length-1&&acc<sum/2){acc+=rows[index++].value;}const fraction=acc/sum,a=rows.slice(0,index),b=rows.slice(index);return w>=h?[...partition(a,x,y,w*fraction,h),...partition(b,x+w*fraction,y,w*(1-fraction),h)]:[...partition(a,x,y,w,h*fraction),...partition(b,x,y+h*fraction,w,h*(1-fraction))];}
 class Map{
  constructor(e){this.element=e;this.abort=new AbortController();const table=e.querySelector('table');if(!table?.tBodies[0]||table.tHead?.rows[0]?.cells.length!==2)throw Error('Falta tabla de áreas.');this.rows=[...table.tBodies[0].rows].map((r,i)=>{const raw=r.cells[1]?.getAttribute('data-valor'),value=Number(raw);if(raw===null||!raw?.trim()||!Number.isFinite(value)||value<0||value>1e9)throw Error('Cantidad no negativa y finita requerida.');return {name:r.cells[0].textContent.trim(),value,index:i,context:r.querySelector('[data-contexto]')?.textContent.trim()||r.dataset.contexto||''};});this.total=this.rows.reduce((s,r)=>s+r.value,0);if(this.rows.some(r=>!r.name)||!this.total||this.rows.length>40||new Set(this.rows.map(r=>r.name)).size!==this.rows.length)throw Error('1–40 nombres únicos y total positivo.');
   this.tiles=partition(this.rows.filter(r=>r.value>0).sort((a,b)=>b.value-a.value));this.parts=[];const title=document.createElement('h3');title.className='grafica-titulo';title.textContent=table.caption?.textContent||'Attention map';
   this.stage=document.createElement('div');this.stage.className='grafica-caja atencion-caja';this.stage.tabIndex=0;this.stage.setAttribute('role','region');this.stage.setAttribute('aria-label','Mapa de áreas desplazable; valores completos en la tabla');this.chart=svg('svg',{viewBox:'0 0 1000 380',role:'img','aria-label':title.textContent+'. Cada área representa su parte del total.'});this.stage.append(this.chart);
   this.status=document.createElement('p');this.status.className='atencion-estado';this.status.setAttribute('role','status');this.status.textContent='Total: '+fmt(this.total)+' '+(e.dataset.unidad||'unidades')+'. Selecciona una categoría para consultar su proporción.';
   this.controls=document.createElement('div');this.controls.className='atencion-leyenda';this.controls.setAttribute('role','group');this.controls.setAttribute('aria-label','Consultar categorías del mapa');
   this.rows.forEach(r=>{const b=document.createElement('button');b.type='button';b.dataset.categoria=r.index;b.dataset.audioHover='';b.textContent=(r.index+1)+'. '+r.name+' · '+fmt(r.value);b.setAttribute('aria-pressed','false');this.controls.append(b);});
   this.tiles.forEach(r=>{const g=svg('g',{'data-categoria':r.index,'data-audio-hover':''}),rect=svg('rect',{x:r.x,y:r.y,width:r.w,height:r.h,class:'atencion-area'});g.append(rect);
    if(r.w>=160&&r.h>=80&&r.name.length<=22){const f=svg('foreignObject',{x:r.x+16,y:r.y+14,width:r.w-32,height:r.h-28}),div=document.createElementNS('http://www.w3.org/1999/xhtml','div');div.className='atencion-etiqueta';const strong=document.createElement('strong'),small=document.createElement('span');strong.textContent=(r.index+1)+'. '+r.name;small.textContent=fmt(r.value)+' '+(e.dataset.unidad||'unidades');div.append(strong,small);f.append(div);g.append(f);}else if(r.w>=30&&r.h>=30)g.append(svg('text',{x:r.x+10,y:r.y+22},String(r.index+1)));this.chart.append(g);});
   this.tooltip=document.createElement('div');this.tooltip.className='atencion-tooltip';this.tooltip.id='atencion-detalle-'+(++serial);this.tooltip.setAttribute('role','tooltip');this.tooltip.hidden=true;document.body.append(this.tooltip);
   const signal=this.abort.signal;
   const target=event=>event.target.closest('[data-categoria]');
   e.addEventListener('pointermove',event=>{if(event.pointerType==='touch')return;const t=target(event);if(t){clearTimeout(this.hideTimer);this.showTip(+t.dataset.categoria,t,event.clientX,event.clientY);}}, {signal});
   e.addEventListener('pointerleave',()=>this.deferHide(),{signal});
   e.addEventListener('focusin',event=>{const t=target(event);if(t)this.showTip(+t.dataset.categoria,t);},{signal});
   e.addEventListener('focusout',()=>this.deferHide(),{signal});
   this.tooltip.addEventListener('pointerenter',()=>clearTimeout(this.hideTimer),{signal});
   this.tooltip.addEventListener('pointerleave',()=>this.deferHide(),{signal});
   document.addEventListener('keydown',event=>{if(event.key==='Escape'){this.dismissed=this.tipTarget;this.hideTip();}},{signal});
   document.addEventListener('pointerdown',event=>{if(!e.contains(event.target)&&!this.tooltip.contains(event.target))this.hideTip();},{signal});
   document.addEventListener('scroll',event=>{if(this.tooltip.contains(event.target))return;if(this.tipTarget===document.activeElement)this.showTip(+this.tipTarget.dataset.categoria,this.tipTarget);else this.hideTip();},{signal,capture:true,passive:true});
   document.addEventListener('nota:pagina',()=>this.hideTip(),{signal});
   addEventListener('resize',()=>this.hideTip(),{signal});
   this.parts=[title,this.stage,this.controls,this.status];e.prepend(...this.parts);e.classList.add('nota-atencion');this.fitLabels();this.resize=new ResizeObserver(()=>this.fitLabels());this.resize.observe(this.stage);document.fonts?.ready.then(()=>{if(!this.dead)this.fitLabels();});e.addEventListener('click',event=>{const target=event.target.closest('[data-categoria]');if(!target)return;this.dismissed=null;this.select(+target.dataset.categoria);this.showTip(+target.dataset.categoria,target);},{signal:this.abort.signal});instances.set(e,this);
  }
  detail(row){return fmt(row.value)+' '+(this.element.dataset.unidad||'unidades')+' · '+pct(row.value/this.total*100)+' % de '+fmt(this.total)+' '+(this.element.dataset.unidad||'unidades')+'.';}
  showTip(index,target,x,y){
   if(this.dismissed===target)return;this.dismissed=null;const row=this.rows[index];if(!row)return;
   clearTimeout(this.hideTimer);this.tipTarget?.removeAttribute('aria-describedby');this.tipTarget=target;
   const title=document.createElement('strong'),value=document.createElement('span'),context=document.createElement('span');title.textContent=row.name;value.textContent=this.detail(row);context.textContent=row.context;
   this.tooltip.replaceChildren(title,value,...(row.context?[context]:[]));this.tooltip.hidden=false;
   target.setAttribute('aria-describedby',this.tooltip.id);
   const r=target.getBoundingClientRect(),tip=this.tooltip.getBoundingClientRect();
   const px=x??r.left,py=y??r.bottom;
   this.tooltip.style.left=Math.max(8,Math.min(innerWidth-tip.width-8,px+12))+'px';
   this.tooltip.style.top=Math.max(8,Math.min(innerHeight-tip.height-8,py+12))+'px';
  }
  hideTip(){clearTimeout(this.hideTimer);this.tooltip.hidden=true;this.tipTarget?.removeAttribute('aria-describedby');this.tipTarget=null;}
  deferHide(){clearTimeout(this.hideTimer);this.hideTimer=setTimeout(()=>{this.dismissed=null;this.hideTip();},180);}
  fitLabels(){this.chart.querySelectorAll('foreignObject').forEach(f=>{const d=f.firstChild;if(d.scrollHeight>+f.getAttribute('height')+1||d.scrollWidth>+f.getAttribute('width')+1){const g=f.parentElement,index=+g.dataset.categoria,r=this.tiles.find(t=>t.index===index);f.remove();g.append(svg('text',{x:r.x+10,y:r.y+22},String(index+1)));}});}
  select(index){const row=this.rows[index];if(!row)return;this.status.textContent=row.name+': '+fmt(row.value)+' '+(this.element.dataset.unidad||'unidades')+' · '+pct(row.value/this.total*100)+' % del total.';this.controls.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.categoria===index)));this.chart.querySelectorAll('g').forEach(g=>g.classList.toggle('atencion-elegida',+g.dataset.categoria===index));}
  destroy(){this.dead=true;this.hideTip();this.tooltip.remove();this.resize.disconnect();this.abort.abort();this.parts.forEach(p=>p.remove());this.element.classList.remove('nota-atencion');instances.delete(this.element);}
 }
 function init(root=document){return [...(root.matches?.('[data-atencion]')?[root]:[]),...root.querySelectorAll('[data-atencion]')].map(e=>{if(instances.has(e))return instances.get(e);e.querySelector('[data-error-atencion]')?.remove();try{return new Map(e);}catch(error){const p=document.createElement('p');p.className='grafica-error';p.dataset.errorAtencion='';p.textContent='No se pudo construir el mapa: '+error.message;e.prepend(p);return null;}});}
 window.NotaAtencion={init,get:e=>instances.get(e),partition};init();
})();
