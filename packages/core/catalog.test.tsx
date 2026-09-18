import { afterEach, describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
const source=readFileSync('packages/core/components/catalog.js','utf8');
afterEach(()=>document.body.replaceChildren());
describe('catalog discovery',()=>{
 it('combines text, family and intent, then restores all recipes',()=>{
  document.body.innerHTML=`<section data-buscador-recetas><input><select data-catalog-category><option value=""></option><option>charts</option></select><select data-catalog-intent><option value=""></option><option>knowledge</option></select><button data-catalog-reset>Reset</button><p role="status"></p><ul class="catalogo-indice"><li data-category="charts" data-intents="knowledge" data-claves="relación">Mapa</li><li data-category="reports" data-intents="knowledge">Evidencia</li><li data-category="charts" data-intents="operations">Rutas</li></ul></section>`;
  window.eval(source);
  const input=document.querySelector('input')!;input.value='relacion';input.dispatchEvent(new Event('input'));
  expect([...document.querySelectorAll('li')].filter(e=>!e.hidden)).toHaveLength(1);
  input.value='';input.dispatchEvent(new Event('input'));
  for(const [selector,value] of [['[data-catalog-category]','charts'],['[data-catalog-intent]','knowledge']]){const s=document.querySelector(selector) as HTMLSelectElement;s.value=value;s.dispatchEvent(new Event('change'));}
  expect([...document.querySelectorAll('li')].filter(e=>!e.hidden).map(e=>e.textContent)).toEqual(['Mapa']);
  (document.querySelector('button') as HTMLButtonElement).click();expect([...document.querySelectorAll('li')].filter(e=>!e.hidden)).toHaveLength(3);expect(document.activeElement).toBe(input);
 });
});
