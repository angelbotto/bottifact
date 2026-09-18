import React, { StrictMode, useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Artifact, TablePerson, TableMedia, TableStatus, TableDetailCard, Callout, CardGrid, DataTable, MarginNote, Timeline, RecipePreview, recipes, themeFamilies, type RecipeId, type ThemeFamily, type ThemeMode } from '@bottifact/react';
import '@bottifact/react/styles.css';
import './showcase.css';

const rows = [
 {id:'L-101',name:'Morning distribution',city:'Bogotá',state:'Delivered',owner:'Ana Rivera',avatar:'amber',count:18},
 {id:'L-102',name:'Store replenishment',city:'Medellín',state:'In transit',owner:'Daniel Torres',avatar:'violet',count:12},
 {id:'L-103',name:'Regional transfer',city:'Cali',state:'Exception',owner:'Lucía Gómez',avatar:'mint',count:4},
 {id:'L-104',name:'Afternoon distribution',city:'Bogotá',state:'In transit',owner:'Ana Rivera',avatar:'amber',count:11},
 {id:'L-105',name:'Store collection',city:'Cali',state:'Delivered',owner:'Lucía Gómez',avatar:'mint',count:9},
 {id:'L-106',name:'Warehouse transfer',city:'Medellín',state:'Exception',owner:'Daniel Torres',avatar:'violet',count:2},
];
function App() {
  const [theme, setTheme] = useState<ThemeFamily>('linear');
  const [mode, setMode] = useState<ThemeMode>('light');
  const [recipe, setRecipe] = useState<RecipeId>('margin-notes');
  return <><nav className="lab-toolbar" aria-label="Component lab"><a href="#intro">margen <small>/ component lab</small></a><div><label>Theme<select value={theme} onChange={event => setTheme(event.target.value as ThemeFamily)}>{themeFamilies.map(family => <option key={family.id} value={family.id}>{family.name}</option>)}</select></label><label>Mode<select value={mode} onChange={event => setMode(event.target.value as ThemeMode)}><option>light</option><option>dark</option><option>system</option></select></label></div></nav>
    <Artifact theme={theme} mode={mode} id="intro">
      <header className="lab-intro"><p className="bf-meta">OPEN SOURCE / REACT + HTML</p><h1>From evidence<br/>to a decision.</h1><p>Components for documents that deserve a second read.<br/>This lab contains synthetic examples only.</p></header>
      <MarginNote note="What would change our mind?" side="right"><h2>Make the reasoning visible.</h2><p>A useful artifact connects a claim to its evidence and leaves space for a thoughtful question in the margin.</p></MarginNote>
      <CardGrid items={[{ id: 'one', title: 'Compose with intent', description: 'Typed React primitives and a catalog of 88 existing recipes.', meta: '01 / COMPONENTS' }, { id: 'two', title: 'Discuss in context', description: 'Keep the quote, section and version next to each observation.', meta: '02 / REVIEW' }, { id: 'three', title: 'Return to the work', description: 'A private feedback bundle carries the context back to your session.', meta: '03 / HANDOFF' }]} />
      <section id="rich-records"><p className="bf-meta">RECORDS / SYNTHETIC DELIVERY WORKSPACE</p><h2>The right detail, in the right place.</h2><p>Reorder columns, combine filters and save a view. Expand a delivery to inspect related cards. The avatar illustrations, people and deliveries below are fictional.</p>
      <DataTable selectable inspectable persistenceKey="synthetic-rich-records" rows={rows} rowKey={row => row.id} caption="Illustrative deliveries · no live connection" columns={[
        {id:'name',header:'Delivery',width:220,mobile:'primary',value:r=>r.name,render:r=><span className="bf-media"><span><strong>{r.name}</strong><small>{r.id} · {r.city}</small></span></span>},
        {id:'state',header:'Status',width:130,value:r=>r.state,render:r=><TableStatus tone={r.state==='Delivered'?'success':r.state==='Exception'?'danger':'info'}>{r.state}</TableStatus>},
        {id:'owner',header:'Owner',value:r=>r.owner,render:r=><TablePerson name={r.owner} detail="Operations" src={`/avatar-${r.avatar}.svg`}/>},
        {id:'cargo',header:'Cargo',width:225,mobile:'detail',value:()=> 'Boxed goods',render:()=> <TableMedia src="/cargo.svg" alt="Illustration of a package" title="Boxed goods" detail="Illustrative manifest"/>},
        {id:'count',header:'Trips',type:'number',aggregate:'sum',value:r=>r.count},
        {id:'city',header:'City',width:110,mobile:'detail',value:r=>r.city},
      ]} renderExpanded={row=><div className="bf-detail-grid"><TableDetailCard title="Route"><p>{row.city} · distribution circuit</p><small>Illustrative route; no GPS telemetry.</small></TableDetailCard><TableDetailCard title="Manifest"><TableMedia src="/cargo.svg" alt="Illustration of a package" title="Boxed goods" detail={`${row.count} example trips`}/></TableDetailCard><TableDetailCard title="Follow-up"><TablePerson name={row.owner} src={`/avatar-${row.avatar}.svg`} /><p>{row.state === 'Exception' ? 'Confirm the incident before closing the delivery.' : 'Review the delivery evidence.'}</p></TableDetailCard></div>} /></section>
      <Callout title="A boundary worth keeping" tone="note">A graph connection explains shared context. It does not establish cause and effect.</Callout>
      <Timeline items={[{ id: 'now', title: 'Review the evidence', date: 'Step 01', current: true, children: <p>Open the document, inspect sources and leave an anchored comment.</p> }, { id: 'next', title: 'Carry the context forward', date: 'Step 02', children: <p>Load the feedback bundle in the intended agent session and prepare a draft.</p> }]} />
      <section className="lab-catalog"><p className="bf-meta">THE COMPLETE RECIPE CATALOG</p><h2>Explore the same core.</h2><p>These previews isolate the original HTML runtime inside a sandboxed frame. The primitives above are native React.</p><label>Choose a recipe <select value={recipe} onChange={event => setRecipe(event.target.value as RecipeId)}>{recipes.map(item => <option key={item.id} value={item.id}>{item.id} · {item.name}</option>)}</select></label><RecipePreview id={recipe} theme={theme} mode={mode} /></section>
    </Artifact><footer className="lab-footer">Margen · Synthetic component fixture · No account or private documents.</footer></>;
}
createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
