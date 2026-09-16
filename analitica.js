/* Bottifact · analítica local. La tabla es la única fuente de cifras.
   Sin red, sin animación automática, SVG accesible y selección por teclado. */
(() => {
  'use strict';
  const instances=new WeakMap(),NS='http://www.w3.org/2000/svg',DAY=86400000;
  const fmt=n=>new Intl.NumberFormat('es-CO',Math.abs(n)>=1e6||(n!==0&&Math.abs(n)<.001)?{maximumSignificantDigits:4,notation:'scientific'}:{maximumSignificantDigits:6}).format(n);
  const el=(tag,text)=>{const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;};
  const svg=(tag,attrs={},text)=>{const e=document.createElementNS(NS,tag);for(const [k,v]of Object.entries(attrs))e.setAttribute(k,v);if(text!==undefined)e.textContent=text;return e;};
  const date=s=>{if(!/^\d{4}-\d{2}-\d{2}$/.test(s))throw Error('Fecha ISO requerida.');const n=Date.parse(s+'T00:00:00Z');if(!Number.isFinite(n)||new Date(n).toISOString().slice(0,10)!==s)throw Error('Fecha inválida.');return n;};
  const iso=n=>new Date(n).toISOString().slice(0,10);
  const positive=values=>{if(values.some(v=>v<0))throw Error('No se admiten cantidades negativas.');};
  function read(e){
    const type=e.dataset.analitica,counts={calendario:2,torta:2,areas:4,caja:6,velas:5,rutas:6,burbujas:4};
    const table=e.querySelector('table'),heads=[...(table?.tHead?.rows[0]?.cells||[])].map(c=>c.textContent.trim());
    if(!counts[type]||heads.length!==counts[type]||!table.tBodies[0])throw Error('Tipo o cabecera incorrectos.');
    const rows=[...table.tBodies[0].rows].map(r=>{
      if(r.cells.length!==heads.length)throw Error('Fila incompleta.');
      const label=r.cells[0].textContent.trim(),values=[...r.cells].slice(1).map(c=>{
        const raw=c.getAttribute('data-valor'),v=Number(raw);if(raw===null||!raw.trim()||!Number.isFinite(v)||Math.abs(v)>1e12)throw Error('Valor inválido o fuera de precisión.');return v;
      });return {label,values};
    });
    if(!rows.length||rows.length>(type==='calendario'?366:type==='areas'||type==='velas'?60:24))throw Error('Cantidad de registros fuera de límite.');
    if(new Set(rows.map(r=>r.label)).size!==rows.length)throw Error('Etiquetas duplicadas.');
    if(['calendario','areas','velas'].includes(type)){rows.forEach(r=>r.time=date(r.label));rows.sort((a,b)=>a.time-b.time);}
    if(['calendario','torta','areas'].includes(type))positive(rows.flatMap(r=>r.values));
    if(type==='torta'&&(rows.length>6||rows.reduce((s,r)=>s+r.values[0],0)<=0))throw Error('Torta: 1–6 categorías y total positivo.');
    if(type==='calendario'&&((rows.at(-1).time-rows[0].time)/DAY>365||rows.some(r=>!Number.isInteger(r.values[0]))))throw Error('Calendario: conteos enteros y hasta 366 días.');
    if(type==='areas'&&rows.length<2)throw Error('Áreas requieren al menos dos fechas.');
    if(type==='caja'&&rows.some(r=>r.values.some((v,i,a)=>i&&v<a[i-1])))throw Error('Orden esperado: mínimo ≤ Q1 ≤ mediana ≤ Q3 ≤ máximo.');
    if(type==='velas'&&rows.some(r=>{const[o,h,l,c]=r.values;return l>Math.min(o,c)||h<Math.max(o,c)||l>h;}))throw Error('OHLC: mínimo ≤ apertura/cierre ≤ máximo.');
    if(['rutas','burbujas'].includes(type)){
      if(!window.NotaGeografia)throw Error('Incluye geografia.js.');
      rows.forEach(r=>{const v=r.values;NotaGeografia.check(v[0],v[1]);if(type==='rutas')NotaGeografia.check(v[2],v[3]);positive([v.at(-1)]);});
    }
    return {type,heads,rows,title:table.caption?.textContent.trim()||'Gráfica',unit:e.dataset.unidad||heads.at(-1)};
  }
  class Chart {
    constructor(element){
      this.model=read(element);this.element=element;this.abort=new AbortController();this.parts=[];this.donut=true;this.selected=null;
      this.heading=el('h3',this.model.title);this.heading.className='grafica-titulo';
      this.stage=el('div');this.stage.className='grafica-caja analitica-caja';this.stage.tabIndex=0;this.stage.setAttribute('role','region');this.stage.setAttribute('aria-label',this.model.title+', gráfica desplazable');
      this.controls=el('div');this.controls.className='analitica-controles';
      this.status=el('p','Elige un registro para consultar sus valores.');this.status.className='analitica-estado';this.status.setAttribute('role','status');
      const label=el('label','Consultar registro ');this.select=el('select');this.select.setAttribute('aria-label','Registro de '+this.model.title);this.select.append(new Option('Todos los registros',''));
      this.model.rows.forEach((r,i)=>this.select.append(new Option(r.label,String(i))));label.append(this.select);this.controls.append(label);
      this.select.addEventListener('change',()=>this.choose(this.select.value===''?null:Number(this.select.value)),{signal:this.abort.signal});
      if(this.model.type==='torta'){
        this.toggle=el('button','Ver como torta');this.toggle.type='button';this.toggle.setAttribute('aria-pressed','false');
        this.toggle.addEventListener('click',()=>{this.donut=!this.donut;this.toggle.textContent=this.donut?'Ver como torta':'Ver como donut';this.toggle.setAttribute('aria-pressed',String(!this.donut));this.draw();},{signal:this.abort.signal});this.controls.append(this.toggle);
      }
      this.legend=el('ul');this.legend.className='analitica-leyenda';
      this.parts=[this.heading,this.controls,this.stage,this.legend,this.status];const before=element.firstChild;this.parts.forEach(p=>element.insertBefore(p,before));element.classList.add('nota-analitica');
      try{this.draw();}catch(error){this.parts.forEach(p=>p.remove());element.classList.remove('nota-analitica');this.abort.abort();throw error;}
      instances.set(element,this);
    }
    add(tag,attrs,text){const n=svg(tag,attrs,text);this.chart.append(n);return n;}
    text(x,y,text,anchor='start'){return this.add('text',{x,y,'text-anchor':anchor},text);}
    line(x1,y1,x2,y2,cls='grafica-rejilla'){return this.add('line',{x1,y1,x2,y2,class:cls});}
    color(i){return 'var(--grafica-'+(i%4+1)+')';}
    mark(n,i){n.dataset.registro=i;n.append(svg('title',{},this.describe(i)));return n;}
    describe(i){const r=this.model.rows[i];return r.label+' · '+r.values.map((v,k)=>this.model.heads[k+1]+': '+fmt(v)).join(' · ');}
    choose(i){this.selected=i;this.select.value=i===null?'':String(i);this.status.textContent=i===null?'Todos los registros.':this.describe(i);this.chart.querySelectorAll('[data-registro]').forEach(n=>n.classList.toggle('analitica-atenuada',i!==null&&Number(n.dataset.registro)!==i));}
    key(text,i){const li=el('li'),swatch=el('span');swatch.className='analitica-muestra';swatch.style.background=this.color(i);li.append(swatch,document.createTextNode(text));this.legend.append(li);}
    axis(min,max,label){
      if(min===max){const d=Math.abs(min)*.1||1;min-=d;max+=d;}
      const y=v=>310-(v-min)/(max-min)*250;this.domain=[min,max];
      for(let t=0;t<=4;t++){const v=min+(max-min)*t/4;this.line(84,y(v),660,y(v));this.text(72,y(v)+4,fmt(v),'end');}
      this.text(84,28,label);return y;
    }
    draw(){
      this.legend.replaceChildren();this.chart=svg('svg',{viewBox:'0 0 720 380',role:'img','aria-label':this.model.title+'. Valores completos en la tabla.'});this.chart.append(svg('title',{},this.model.title));this.stage.replaceChildren(this.chart);
      this[this.model.type]();this.choose(this.selected);
      this.chart.addEventListener('click',e=>{const mark=e.target.closest('[data-registro]');if(mark)this.choose(Number(mark.dataset.registro));});
    }
    calendario(){
      const {rows}=this.model,start=rows[0].time,end=rows.at(-1).time,max=Math.max(...rows.map(r=>r.values[0]));
      const offset=(new Date(start).getUTCDay()+6)%7,weeks=Math.ceil(((end-start)/DAY+1+offset)/7),size=Math.min(28,560/weeks),x0=84;
      this.chart.setAttribute('viewBox',`0 0 720 ${Math.max(285,size*7+100)}`);
      ['L','M','X','J','V','S','D'].forEach((d,i)=>this.text(64,66+i*size,d,'end'));
      const byDate=new Map(rows.map((r,i)=>[r.time,{r,i}]));this.max=max;
      let month=-1;
      for(let d=start;d<=end;d+=DAY){const index=(d-start)/DAY+offset,col=Math.floor(index/7),day=index%7,x=x0+col*size,y=50+day*size,entry=byDate.get(d),m=new Date(d).getUTCMonth();
        if(m!==month){this.text(x,32,new Intl.DateTimeFormat('es',{month:'short',timeZone:'UTC'}).format(d));month=m;}
        const v=entry?.r.values[0],level=v===undefined?null:v===0?0:Math.min(4,Math.ceil(v/Math.max(1,max)*4));
        const cell=this.add('rect',{x,y,width:size-3,height:size-3,rx:3,fill:`var(--calor-${level===null?'ausente':level})`,stroke:'var(--grafica-linea)','data-fecha':iso(d),'data-valor':v??'ausente'});
        if(entry)this.mark(cell,entry.i);else{cell.append(svg('title',{},iso(d)+': sin dato'));this.line(x+3,y+size-6,x+size-6,y+3,'analitica-ausente');}
      }
      const li=el('li',`0 · ${[1,2,3,4].map(i=>fmt(max*i/4)).join(' · ')} ${this.model.unit}. Intervalos (anterior, límite]; cero aparte. Diagonal: sin dato.`);this.legend.append(li);
      for(let i=0;i<=4;i++){const li=el('li'),s=el('span');s.className='analitica-muestra';s.style.background=`var(--calor-${i})`;li.append(s,document.createTextNode(i===0?'0':`≤ ${fmt(max*i/4)}`));this.legend.append(li);}
    }
    torta(){
      const {rows}=this.model,total=rows.reduce((s,r)=>s+r.values[0],0),cx=360,cy=185,r=140,inner=this.donut?86:0;let a=-Math.PI/2;this.total=total;
      rows.forEach((row,i)=>{const fraction=row.values[0]/total,b=a+fraction*Math.PI*2,p=t=>[cx+r*Math.cos(t),cy+r*Math.sin(t)],q=t=>[cx+inner*Math.cos(t),cy+inner*Math.sin(t)];
        if(fraction>0){let n;if(fraction===1)n=this.add('circle',{cx,cy,r:(r+inner)/2,fill:'none',stroke:this.color(i),'stroke-width':r-inner});else n=this.add('path',{d:`M${p(a)} A${r},${r} 0 ${fraction>.5?1:0},1 ${p(b)} L${q(b)} ${inner?`A${inner},${inner} 0 ${fraction>.5?1:0},0 ${q(a)}`:`L${cx},${cy}`} Z`,fill:this.color(i),stroke:'var(--grafica-papel)','stroke-width':2});this.mark(n,i);}
        this.key(`${i+1}. ${row.label} · ${fmt(row.values[0])} · ${fmt(fraction*100)} %`,i);a=b;
      });if(this.donut){this.text(cx,183,fmt(total),'middle');this.text(cx,205,this.model.unit,'middle');}else this.text(cx,360,'Total: '+fmt(total)+' '+this.model.unit,'middle');
    }
    areas(){
      const {rows,heads}=this.model,totals=rows.map(r=>r.values.reduce((s,v)=>s+v,0)),max=Math.max(...totals)||1,y=this.axis(0,max,this.model.unit),x=t=>84+(t-rows[0].time)/(rows.at(-1).time-rows[0].time)*576;
      for(let k=2;k>=0;k--){const top=rows.map(r=>[x(r.time),y(r.values.slice(0,k+1).reduce((s,v)=>s+v,0))]),bottom=rows.map(r=>[x(r.time),y(r.values.slice(0,k).reduce((s,v)=>s+v,0))]).reverse();this.add('path',{d:'M'+[...top,...bottom].map(p=>p.join(',')).join(' L')+' Z',fill:this.color(k),'fill-opacity':.4,stroke:this.color(k)});}
      heads.slice(1).forEach((h,i)=>this.key(h,i));rows.forEach((r,i)=>{this.mark(this.add('circle',{cx:x(r.time),cy:y(totals[i]),r:4,fill:'var(--grafica-tinta)'}),i);if(i===0||i===rows.length-1||rows.length<=6){this.text(x(r.time),340,r.label.slice(5),'middle');this.text(x(r.time),y(totals[i])-10,fmt(totals[i]),'middle');}});this.text(360,369,'Fecha · distancia temporal real','middle');
    }
    caja(){
      const {rows}=this.model,min=Math.min(...rows.map(r=>r.values[0])),max=Math.max(...rows.map(r=>r.values[4])),low=min===max?min-1:min,high=min===max?max+1:max,x=v=>160+(v-low)/(high-low)*480;this.domain=[low,high];
      this.chart.setAttribute('viewBox',`0 0 720 ${100+rows.length*60}`);
      for(let t=0;t<=4;t++){const v=low+(high-low)*t/4;this.text(x(v),32,fmt(v),'middle');this.line(x(v),45,x(v),60+rows.length*60);}
      rows.forEach((r,i)=>{const [min,q1,med,q3,max]=r.values,y=75+i*60,g=this.add('g',{});this.mark(g,i);
        g.append(svg('line',{x1:x(min),y1:y,x2:x(max),y2:y,stroke:this.color(i),'stroke-width':2}),svg('rect',{x:x(q1),y:y-14,width:x(q3)-x(q1),height:28,fill:this.color(i),'fill-opacity':.25,stroke:this.color(i)}));
        [min,med,max].forEach((v,k)=>g.append(svg('line',{x1:x(v),x2:x(v),y1:y-(k===1?14:8),y2:y+(k===1?14:8),stroke:this.color(i),'stroke-width':2})));this.text(145,y+4,r.label,'end');
      });this.text(160,88+rows.length*60,this.model.unit+' · bigotes = mínimo y máximo');
    }
    velas(){
      const {rows}=this.model,min=Math.min(...rows.map(r=>r.values[2])),max=Math.max(...rows.map(r=>r.values[1])),y=this.axis(min,max,this.model.unit),span=rows.at(-1).time-rows[0].time,x=t=>span?112+(t-rows[0].time)/span*520:380;
      const gap=rows.length>1?Math.min(...rows.slice(1).map((r,i)=>x(r.time)-x(rows[i].time))):60,width=Math.max(1,Math.min(32,gap*.6));
      rows.forEach((r,i)=>{const[o,h,l,c]=r.values,g=this.add('g',{});this.mark(g,i);const color=this.color(c>=o?2:0);g.append(svg('line',{x1:x(r.time),x2:x(r.time),y1:y(h),y2:y(l),stroke:color,'stroke-width':2}),svg('rect',{x:x(r.time)-width/2,y:y(Math.max(o,c)),width,height:Math.abs(y(o)-y(c)),fill:c>=o?'var(--grafica-papel)':color,stroke:color,'stroke-width':2}));if(c===o)g.append(svg('line',{x1:x(r.time)-width/2,x2:x(r.time)+width/2,y1:y(c),y2:y(c),stroke:color,'stroke-width':2}));if(rows.length<=8||i===0||i===rows.length-1)this.text(x(r.time),338,r.label.slice(5),'middle');});
      this.key('Hueca: cierre ≥ apertura',2);this.key('Rellena: cierre < apertura',0);this.text(360,369,'Fecha · distancia temporal real','middle');
    }
    mapBase(){
      this.chart.setAttribute('viewBox','0 0 720 480');const project=([lon,lat])=>[180+(lon+80)*21,440-(lat+5)*21];
      for(const ring of NotaGeografia.colombia.coordinates)this.add('path',{d:'M'+ring.map(project).map(p=>p.join(',')).join(' L')+' Z',fill:'var(--calor-0)',stroke:'var(--escena-linea)','stroke-width':1.5});
      this.text(580,50,'N ↑','middle');this.text(100,470,'Colombia · coordenadas WGS84 · proyección equirectangular');return project;
    }
    rutas(){
      const project=this.mapBase(),max=Math.max(...this.model.rows.map(r=>r.values[4]))||1;this.max=max;
      const cities=new Map();
      this.model.rows.forEach((r,i)=>{const[a,b,c,d,v]=r.values,p=project([b,a]),q=project([d,c]),dx=q[0]-p[0],dy=q[1]-p[1],distance=Math.hypot(dx,dy)||1,bend=Math.min(22,distance*.2);
        if(v>0){const n=this.add('path',{d:`M${p} Q${(p[0]+q[0])/2-dy/distance*bend},${(p[1]+q[1])/2+dx/distance*bend} ${q}`,fill:'none',stroke:this.color(i),'stroke-width':v/max*8,'stroke-linecap':'round','stroke-linejoin':'round'});this.mark(n,i);}
        const names=r.label.split(/\s*→\s*/);[[p,names[0]],[q,names[1]]].forEach(([pt,name])=>{const key=pt.join(',');if(!cities.has(key))cities.set(key,{pt,name:name||'Ciudad '+(cities.size+1)});});this.key(`${i+1}. ${r.label} · ${fmt(v)} ${this.model.unit}`,i);
      });
      // Los nodos se dibujan al final: ninguna ruta posterior corta o repinta su centro.
      cities.forEach(({pt,name})=>{this.add('circle',{cx:pt[0],cy:pt[1],r:5,fill:'var(--grafica-papel)',stroke:'var(--grafica-tinta)','stroke-width':2});const label=this.text(pt[0]+11,pt[1]-9,name);label.setAttribute('paint-order','stroke');label.setAttribute('stroke','var(--grafica-papel)');label.setAttribute('stroke-width',4);label.setAttribute('stroke-linejoin','round');});
      this.text(100,25,`Grosor proporcional · máximo ${fmt(max)} ${this.model.unit}`);
    }
    burbujas(){
      const project=this.mapBase(),max=Math.max(...this.model.rows.map(r=>r.values[2]))||1;this.max=max;
      this.model.rows.forEach((r,i)=>{const[lat,lon,value]=r.values,p=project([lon,lat]),radius=Math.sqrt(value/max)*28;const n=this.add('circle',{cx:p[0],cy:p[1],r:radius,fill:this.color(i),'fill-opacity':.35,stroke:this.color(i),'stroke-width':value?2:0});this.mark(n,i);this.text(p[0]+radius+7,p[1]+4,String(i+1));this.key(`${i+1}. ${r.label} · ${fmt(value)} ${this.model.unit}`,i);});
      this.text(100,25,`Área proporcional al volumen · máximo ${fmt(max)} ${this.model.unit}`);
    }
    destroy(){this.abort.abort();this.parts.forEach(p=>p.remove());this.element.classList.remove('nota-analitica');instances.delete(this.element);}
  }
  function init(root=document){return [...(root.matches?.('[data-analitica]')?[root]:[]),...root.querySelectorAll('[data-analitica]')].map(e=>{if(instances.has(e))return instances.get(e);e.querySelector('[data-error-analitica]')?.remove();try{return new Chart(e);}catch(error){const p=el('p','No se pudo construir la gráfica: '+error.message);p.dataset.errorAnalitica='';p.className='grafica-error';e.prepend(p);return null;}});}
  window.NotaAnalitica={init,get:e=>instances.get(e)};init();
})();
