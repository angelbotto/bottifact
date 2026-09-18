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
