/* Ayudas del catálogo. La búsqueda filtra el índice, conserva las piezas en la página. */
(() => {
  'use strict';
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
