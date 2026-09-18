/* Ayudas del catálogo. La búsqueda filtra el índice, conserva las piezas en la página. */
(() => {
  'use strict';
  // Las gráficas anteriores al destino se insertan después del salto nativo.
  // Reubicar sólo la navegación inicial, sin interferir con un lector que ya actuó.
  const hash=location.hash,abort=new AbortController();let touched=false;
  if(hash) {
    for(const type of ['wheel','touchstart','pointerdown','keydown'])window.addEventListener(type,()=>{touched=true;},{passive:true,signal:abort.signal});
    document.fonts.ready.then(()=>{
      abort.abort();if(touched||location.hash!==hash)return;
      let id;try{id=decodeURIComponent(hash.slice(1));}catch{return;}
      document.getElementById(id)?.scrollIntoView({behavior:'instant'});
    });
  }
  const normal=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es');
  document.querySelectorAll('[data-buscador-recetas]').forEach(root=>{
    const input=root.querySelector('input'),list=root.querySelector('.catalogo-indice'),status=root.querySelector('[role="status"]');
    if(!input||!list||!status)return;
    const items=[...list.children];
    const update=()=>{const words=normal(input.value).trim().split(/\s+/);let count=0;
      items.forEach(li=>{li.hidden=!words.every(w=>normal(li.textContent+' '+(li.dataset.claves||'')).includes(w));if(!li.hidden)count++;});
      status.textContent=count?'Encuentra '+count+' de '+items.length+' recetas.':'Sin coincidencias. Prueba con tabla, artículo, globo o prototipo.';
    };
    input.addEventListener('input',update);update();
  });
})();
