import React, { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Artifact, Callout, CardGrid, DataTable, MarginNote, Timeline, RecipePreview, recipes, themeFamilies, type RecipeId, type ThemeFamily, type ThemeMode } from '@bottifact/react';
import '@bottifact/react/styles.css';
import './showcase.css';

const rows = [{ id: 'a', stream: 'Documentation', state: 'Ready', count: 12 }, { id: 'b', stream: 'Components', state: 'In review', count: 8 }, { id: 'c', stream: 'Experiments', state: 'Planned', count: 3 }];
function App() {
  const [theme, setTheme] = useState<ThemeFamily>('editorial');
  const [mode, setMode] = useState<ThemeMode>('dark');
  const [recipe, setRecipe] = useState<RecipeId>('margin-notes');
  return <><nav className="lab-toolbar" aria-label="Component lab"><a href="#intro">bottifact <small>/ component lab</small></a><div><label>Theme<select value={theme} onChange={event => setTheme(event.target.value as ThemeFamily)}>{themeFamilies.map(family => <option key={family.id} value={family.id}>{family.name}</option>)}</select></label><label>Mode<select value={mode} onChange={event => setMode(event.target.value as ThemeMode)}><option>light</option><option>dark</option><option>system</option></select></label></div></nav>
    <Artifact theme={theme} mode={mode} id="intro">
      <header className="lab-intro"><p className="bf-meta">OPEN SOURCE / REACT + HTML</p><h1>From evidence<br/>to a decision.</h1><p>Components for documents that deserve a second read.<br/>This lab contains synthetic examples only.</p></header>
      <MarginNote note="What would change our mind?" side="right"><h2>Make the reasoning visible.</h2><p>A useful artifact connects a claim to its evidence and leaves space for a thoughtful question in the margin.</p></MarginNote>
      <CardGrid items={[{ id: 'one', title: 'Compose with intent', description: 'Typed React primitives and a catalog of 88 existing recipes.', meta: '01 / COMPONENTS' }, { id: 'two', title: 'Discuss in context', description: 'Keep the quote, section and version next to each observation.', meta: '02 / REVIEW' }, { id: 'three', title: 'Return to the work', description: 'A private feedback bundle carries the context back to your session.', meta: '03 / HANDOFF' }]} />
      <h2>Let the data stay readable.</h2><DataTable selectable inspectable persistenceKey="synthetic-component-lab" rows={rows} rowKey={row => row.id} caption="Synthetic fixture · item counts, not production metrics" columns={[{ id: 'stream', header: 'Workstream', value: row => row.stream }, { id: 'state', header: 'State', value: row => row.state }, { id: 'count', header: 'Items', type: 'number', aggregate: 'sum', value: row => row.count }]} />
      <Callout title="A boundary worth keeping" tone="note">A graph connection explains shared context. It does not establish cause and effect.</Callout>
      <Timeline items={[{ id: 'now', title: 'Review the evidence', date: 'Step 01', current: true, children: <p>Open the document, inspect sources and leave an anchored comment.</p> }, { id: 'next', title: 'Carry the context forward', date: 'Step 02', children: <p>Load the feedback bundle in the intended agent session and prepare a draft.</p> }]} />
      <section className="lab-catalog"><p className="bf-meta">THE COMPLETE RECIPE CATALOG</p><h2>Explore the same core.</h2><p>These previews isolate the original HTML runtime inside a sandboxed frame. The primitives above are native React.</p><label>Choose a recipe <select value={recipe} onChange={event => setRecipe(event.target.value as RecipeId)}>{recipes.map(item => <option key={item.id} value={item.id}>{item.id} · {item.name}</option>)}</select></label><RecipePreview id={recipe} theme={theme} mode={mode} /></section>
    </Artifact><footer className="lab-footer">Margen · Synthetic component fixture · No account or private documents.</footer></>;
}
createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
