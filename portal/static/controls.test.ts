import {beforeEach, describe, expect, it, vi} from 'vitest';
import {readFileSync} from 'node:fs';
const script=(name:string)=>window.eval(readFileSync(new URL(name,import.meta.url),'utf8'));
declare global {interface Window {BottifactKnowledge:any;BottifactLibraryControls:any;}}
beforeEach(()=>{document.body.replaceChildren();script('./knowledge.js');script('./library-controls.js');});
describe('administrator knowledge exploration',()=>{
 const data={total:2,truncated:false,nodes:[{id:'a',title:'Artifact A',space:'Acme',category:'Product'},{id:'b',title:'Artifact B',space:'Other',category:'Product'}],network:{nodes:[{id:'a',artifact:'a',title:'Artifact A',kind:'artifact'},{id:'b',artifact:'b',title:'Artifact B',kind:'artifact'},{id:'s',title:'Acme',kind:'space',count:1},{id:'t',title:'Planning <script>',kind:'topic',count:2}],edges:[{source:'a',target:'s',reason:'Assigned company'},{source:'a',target:'t',reason:'Manual topic'},{source:'b',target:'t',reason:'Manual topic'}]}};
 it('explores company membership and explains links without opening a document',()=>{
  const root=document.createElement('div');document.body.append(root);const peek=vi.fn();const graph=window.BottifactKnowledge.graph(root,data,peek);
  (root.querySelector('[data-node="s"]') as HTMLElement).dispatchEvent(new MouseEvent('click'));
  expect(root.querySelector('.atlas-detail')?.textContent||root.textContent).toContain('Assigned company');expect(peek).not.toHaveBeenCalled();
  const explore=[...root.querySelectorAll('button')].find(b=>b.textContent==='Explorar conexiones')!;explore.click();
  expect(root.querySelectorAll('[data-node]')).toHaveLength(2);
  const scope=[...root.querySelectorAll('label')].find(l=>l.textContent?.startsWith('Alcance'))!.querySelector('select')!;scope.value='2';scope.dispatchEvent(new Event('change'));
  expect(root.querySelectorAll('[data-node]')).toHaveLength(3);
  const back=[...root.querySelectorAll('button')].find(b=>b.textContent==='← Volver')!;back.click();
  expect(root.querySelectorAll('[data-node]')).toHaveLength(4);
  expect(root.querySelector('script')).toBeNull();graph.destroy();
 });
 it('searches the whole loaded graph from a neighborhood, exposes exact labels safely',()=>{
  const root=document.createElement('div');document.body.append(root);const graph=window.BottifactKnowledge.graph(root,data,vi.fn());
  const search=root.querySelector('input[type=search]') as HTMLInputElement;search.value='Planning';search.dispatchEvent(new Event('input'));
  const result=root.querySelector('.atlas-search-results button') as HTMLButtonElement;expect(result.textContent).toContain('Planning <script>');result.click();
  expect(root.querySelectorAll('[data-node]')).toHaveLength(3);expect(root.querySelector('script')).toBeNull();graph.destroy();
 });
});
describe('searchable filter menu',()=>{
 it('filters accents, selects the native value and announces the chosen facet',()=>{
  document.body.innerHTML='<section><label>Company<select><option value="">All</option><option value="a">Ácme</option><option value="b">Other</option></select></label></section>';
  const root=document.querySelector('section')!,select=root.querySelector('select')!,change=vi.fn();select.addEventListener('change',change);window.BottifactLibraryControls.init(root);
  const search=root.querySelector('input')!;search.value='acme';search.dispatchEvent(new Event('input'));expect(root.querySelectorAll('button')).toHaveLength(1);
  root.querySelector('button')!.click();expect(select.value).toBe('a');expect(change).toHaveBeenCalledOnce();expect(root.querySelector('summary')?.getAttribute('aria-label')).toBe('Company: Ácme');
 });
});
