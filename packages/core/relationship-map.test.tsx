import { beforeEach, afterEach, describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
const source = readFileSync('packages/core/components/relationship-map.js', 'utf8');
const fixture = readFileSync('packages/core/recipes/relationship-map/example.html', 'utf8');
const api = () => (window as any).BottifactRelationships;
const host = () => document.querySelector('[data-relationship-map]')!;
const control = (label: string) => [...document.querySelectorAll('label')].find(e => e.firstChild?.textContent === label)!.querySelector('select')!;
const choose = (label: string, value: string) => {const el=control(label);el.value=value;el.dispatchEvent(new Event('change'));};
beforeEach(() => {document.body.innerHTML=fixture;window.eval(source);});
afterEach(() => {api()?.destroy(host());document.body.replaceChildren();});
describe('relationship explorer', () => {
 it('shows a bounded neighborhood with explicit directions and preserves its source', () => {
  expect(document.querySelectorAll('.relationship-node')).toHaveLength(2);
  api().get(host()).select('report');
  expect(document.querySelectorAll('.relationship-node')).toHaveLength(4);
  expect(document.querySelector('.relationship-inspector')!.textContent).toContain('Llega desde Evaluar capacidad');
  expect(document.querySelectorAll('[data-map-nodes] tbody tr')).toHaveLength(6);
 });
 it('searches outside the visible neighborhood and supports return navigation', () => {
  const search=document.querySelector('input')!;search.value='restricciones';search.dispatchEvent(new Event('input'));
  const result=document.querySelector('.relationship-search button') as HTMLButtonElement;expect(result.textContent).toBe('Registro de restricciones');result.click();
  expect(api().get(host()).selected).toBe('source');
  (document.querySelector('.relationship-actions button') as HTMLButtonElement).click();
  expect(api().get(host()).selected).toBe('project');
 });
 it('filters suggestions before expanding neighborhoods and handles zero connections', () => {
  api().get(host()).select('source');expect(document.querySelectorAll('.relationship-node')).toHaveLength(2);
  choose('Estado','Declarada');expect(document.querySelectorAll('.relationship-node')).toHaveLength(1);
  expect(document.querySelector('.relationship-inspector')!.textContent).toContain('Sin conexiones');
  choose('Alcance','all');expect(document.querySelectorAll('.relationship-node')).toHaveLength(6);
 });
 it('supports two-hop navigation, destroy and idempotent remount', () => {
  choose('Alcance','2');expect(document.querySelectorAll('.relationship-node')).toHaveLength(3);
  api().init();expect(document.querySelectorAll('.relationship-ui')).toHaveLength(1);
  api().destroy(host());expect(document.querySelector('.relationship-ui')).toBeNull();
  expect(document.querySelectorAll('[data-map-edges] tbody tr')).toHaveLength(5);
  api().init();expect(document.querySelectorAll('.relationship-ui')).toHaveLength(1);
 });
 it('leaves invalid source tables readable without mounting a partial graph', () => {
  api().destroy(host());document.querySelector('[data-map-edges] tbody tr')!.setAttribute('data-target','missing');api().init();
  expect(document.querySelector('.relationship-ui')).toBeNull();expect(document.querySelector('[data-map-nodes]')).not.toBeNull();
 });
 it('renders imported strings as text and does not create executable markup', () => {
  api().destroy(host());document.querySelector('[data-map-nodes] th[scope=row]')!.textContent='<img src=x onerror=alert(1)>';api().init();
  expect(document.querySelector('.relationship-ui img')).toBeNull();expect(document.querySelector('.relationship-node strong')!.textContent).toContain('<img');
 });
});
