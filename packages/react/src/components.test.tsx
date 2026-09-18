import React, { StrictMode } from 'react';
import version from '../../../VERSION.json' with { type: 'json' };
import { afterEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { Artifact, Callout, CardGrid, DataTable, MarginNote, RecipePreview } from './index.js';
import { createRecipeDocument, getRecipe, recipes } from '@bottifact/core';
import { getThemeTokens, themeFamilies } from '@bottifact/core/themes';

afterEach(() => { cleanup(); vi.restoreAllMocks(); vi.unstubAllGlobals(); });
function media() {
  const listeners = new Set<() => void>();
  const query = { matches: true, media: '', onchange: null, addEventListener: (_: string, fn: () => void) => listeners.add(fn), removeEventListener: (_: string, fn: () => void) => listeners.delete(fn), addListener: () => {}, removeListener: () => {}, dispatchEvent: () => true };
  vi.stubGlobal('matchMedia', () => query);
  return listeners;
}

describe('portable components', () => {
  it('keeps theme state scoped and cleans subscriptions under StrictMode', () => {
    const listeners = media();
    const previous = document.documentElement.dataset.theme;
    const view = render(<StrictMode><Artifact theme="linear"><p>Reading</p></Artifact></StrictMode>);
    expect(screen.getByRole('article').dataset.colorMode).toBe('dark');
    expect(document.documentElement.dataset.theme).toBe(previous);
    expect(listeners.size).toBe(1);
    view.unmount(); expect(listeners.size).toBe(0);
  });
  it('sorts numbers numerically, filters, and preserves the input rows', () => {
    const rows = [{ id: 'a', city: 'West', amount: 20 }, { id: 'b', city: 'East', amount: 3 }];
    render(<DataTable rows={rows} rowKey={row => row.id} caption="Illustrative totals" columns={[{ id: 'city', header: 'City', value: row => row.city }, { id: 'amount', header: 'Amount', value: row => row.amount }]} />);
    fireEvent.click(screen.getByRole('button', { name: /Amount/ }));
    const body = screen.getByRole('table').querySelector('tbody')!;
    expect(within(body).getAllByRole('row')[0].textContent).toBe('East3');
    expect(rows[0].id).toBe('a');
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'missing' } });
    expect(screen.getByText('No matching rows.')).toBeTruthy();
    expect(screen.getByRole('status').textContent).toBe('0 of 2 rows');
  });
  it('escapes supplied text and refuses executable card links', () => {
    render(<><Callout title="Example">{'<script>bad()</script>'}</Callout><CardGrid items={[{ id: 'x', title: 'Example', description: 'Text', href: 'javascript:bad()' }]} /></>);
    expect(document.querySelector('script')).toBeNull();
    expect(screen.queryByRole('link')).toBeNull();
  });
  it('disconnects the visibility observer when a margin note unmounts', () => {
    media(); vi.stubGlobal('matchMedia', () => ({ matches: false }));
    const disconnect = vi.fn();
    vi.stubGlobal('IntersectionObserver', class { observe() {} disconnect = disconnect; });
    const view = render(<StrictMode><MarginNote note="Review the denominator"><p>Evidence</p></MarginNote></StrictMode>);
    view.unmount(); expect(disconnect).toHaveBeenCalledTimes(2);
  });
  it('loads a complete recipe into an isolated frame and handles invalid IDs', async () => {
    const view = render(<RecipePreview id="bar-chart" theme="blueprint" mode="dark" />);
    const frame = await screen.findByTitle('Bottifact component: bar-chart');
    expect(frame.getAttribute('sandbox')).not.toContain('allow-same-origin');
    expect(frame.getAttribute('srcdoc')).toContain('data-grafica');
    view.rerender(<RecipePreview id={'unknown' as never} />);
    expect((await screen.findByRole('alert')).textContent).toContain('could not be loaded');
  });
  it('exposes all recipes and both modes of every theme from the same source', async () => {
    expect(recipes).toHaveLength(version.componentes);
    expect(themeFamilies).toHaveLength(version.temas.length);
    for (const theme of themeFamilies) for (const mode of ['light', 'dark'] as const) expect(getThemeTokens(theme.id, mode).papel).toMatch(/^(#|hsl\()/);
    expect(getRecipe('barras').id).toBe('bar-chart');
    await expect(createRecipeDocument('bar-chart', { theme: 'invalid' as never })).rejects.toThrow();
  });
});

describe('table workbench',()=>{
 it('keeps row selection across sorting and filters and inspects the stable row',()=>{
 const rows=[{id:'a',city:'Bogotá',amount:10},{id:'b',city:'Cali',amount:2}];
 render(<DataTable rows={rows} rowKey={r=>r.id} caption="Deliveries" selectable inspectable columns={[{id:'city',header:'City',value:r=>r.city},{id:'amount',header:'Amount',type:'number',value:r=>r.amount}]}/>);
 fireEvent.click(screen.getByLabelText('Select row a'));fireEvent.click(screen.getByRole('button',{name:/Amount/}));expect((screen.getByLabelText('Select row a') as HTMLInputElement).checked).toBe(true);
 fireEvent.change(screen.getByRole('searchbox'),{target:{value:'Cali'}});expect(screen.getByText(/1 selected in the supplied dataset/).textContent).toContain('1 hidden');
 fireEvent.click(screen.getByLabelText('Inspect row b'));expect(screen.getByRole('dialog').textContent).toContain('Record: b');
 });
});

it('uses a mobile record layout without losing stable cell references or selection',()=>{
  media();
  render(<DataTable rows={[{id:'r1',name:'Route',amount:42}]} rowKey={r=>r.id} caption="Mobile records" selectable columns={[{id:'name',header:'Name',value:r=>r.name},{id:'amount',header:'Amount',value:r=>r.amount}]}/>);
  const cell=document.querySelector('[data-cell-id="r1:amount"]');
  expect(document.querySelector('.bf-table-section')?.getAttribute('data-layout')).toBe('cards');
  fireEvent.click(screen.getByLabelText('Select row r1'));
  fireEvent.click(screen.getByRole('button',{name:'Table',exact:true}));
  expect(document.querySelector('[data-cell-id="r1:amount"]')).toBe(cell);
  expect((screen.getByLabelText('Select row r1') as HTMLInputElement).checked).toBe(true);
  fireEvent.click(screen.getByRole('button',{name:'Cards',exact:true}));
  expect(document.querySelectorAll('[data-cell-id="r1:amount"]')).toHaveLength(1);
});
it('switches grouped board and list views without losing record selection',()=>{
 render(<DataTable caption="Test records" rows={[{id:'1',status:'Open',amount:4},{id:'2',status:'Closed',amount:6}]} rowKey={r=>r.id} selectable columns={[{id:'id',header:'ID',value:r=>r.id},{id:'status',header:'Status',value:r=>r.status},{id:'amount',header:'Amount',type:'number',value:r=>r.amount}]}/>);
 fireEvent.click(screen.getByLabelText('Select row 1'));
 fireEvent.click(screen.getByRole('button',{name:'Board',exact:true}));
 expect(document.querySelector('[data-layout=board]')).not.toBeNull();
 expect(document.querySelectorAll('tbody')).toHaveLength(2);
 fireEvent.click(screen.getByRole('button',{name:'List',exact:true}));
 expect((screen.getByLabelText('Select row 1') as HTMLInputElement).checked).toBe(true);
 expect(screen.getByText('4')).toBeDefined();
});
