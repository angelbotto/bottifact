import {beforeEach, afterEach, expect, it, vi} from 'vitest';
import {readFileSync} from 'node:fs';
const source=readFileSync('packages/core/components/review.js','utf8');
const markup=readFileSync('packages/core/recipes/review/example.html','utf8');
let instance:any;
beforeEach(()=>{
  localStorage.clear();
  document.body.innerHTML='<main><section id="evidence"><h2>Evidence</h2><p id="claim">Three deliveries need review.</p></section>'+markup+'</main>';
  Object.defineProperty(window,'visualViewport',{configurable:true,value:null});
  vi.stubGlobal('ResizeObserver',class {observe(){} disconnect(){}});
  HTMLElement.prototype.scrollIntoView=vi.fn();
  HTMLDialogElement.prototype.show=function(){this.open=true;};
  HTMLDialogElement.prototype.showModal=function(){this.open=true;};
  HTMLDialogElement.prototype.close=function(){this.open=false;};
  vi.spyOn(HTMLElement.prototype,'getClientRects').mockReturnValue([{x:0,y:0,left:0,right:100,top:0,bottom:20,width:100,height:20,toJSON(){return {};}}] as any);
  delete (window as any).BottifactReviewBridge;
});
afterEach(()=>{instance?.destroy();instance=null;vi.unstubAllGlobals();vi.restoreAllMocks();});
function mount(){window.eval(source);instance=(window as any).NotaRevision.get(document.querySelector('[data-revision]'));}
function open(){(document.querySelector('[data-revision-modo]') as HTMLElement).click();(document.querySelector('#claim') as HTMLElement).click();}
it('keeps metadata optional and preserves note type, session and source context when saving',async()=>{
  mount();open();
  const editor=document.querySelector('[data-revision-editor]') as HTMLDialogElement;
  expect(editor.open).toBe(true);
  expect((editor.querySelector('.review-composer-options') as HTMLDetailsElement).open).toBe(false);
  const type=editor.querySelector('select') as HTMLSelectElement;type.value='note';type.dispatchEvent(new Event('change'));
  const session=editor.querySelector('.revision-session input') as HTMLInputElement;session.value='session-42';
  const draft=editor.querySelector('textarea')!;draft.value='Check the exception source.';
  draft.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',ctrlKey:true,bubbles:true}));
  await vi.waitFor(()=>expect(editor.open).toBe(false));
  const event=instance.exportData().events[0];
  expect(event).toMatchObject({entry_type:'note',session:'session-42',text:'Check the exception source.',anchor:{reference:'claim',text:'Three deliveries need review.'}});
  (document.querySelector('.revision-marca') as HTMLElement).click();
  expect(type.disabled).toBe(true);expect(session.disabled).toBe(true);
  expect(draft.value).toBe('Check the exception source.');
});
it('retains a failed shared draft and its context for retry',async()=>{
  const commit=vi.fn().mockRejectedValue(new Error('Connection unavailable'));
  (window as any).BottifactReviewBridge={commit,subscribe:(fn:any)=>{fn({author:'Reviewer',actor:'r',verified:true,permissions:{comment:true,edit:true},snapshot:{format:'nota-revision',version:2,document:document.title+'@'+location.pathname,events:[]}});return ()=>{};}};
  mount();open();
  const editor=document.querySelector('[data-revision-editor]') as HTMLDialogElement;
  const draft=editor.querySelector('textarea')!;draft.value='Keep this draft.';
  draft.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',ctrlKey:true,bubbles:true}));
  await vi.waitFor(()=>expect(commit).toHaveBeenCalledOnce());
  expect(editor.open).toBe(true);expect(draft.value).toBe('Keep this draft.');
  expect(document.querySelector('[data-revision-estado]')?.textContent).toContain('Connection unavailable');
});
it('can be destroyed and mounted again without losing original controls or duplicating the composer',()=>{
  mount();instance.destroy();
  instance=(window as any).NotaRevision.init()[0];open();
  expect(document.querySelectorAll('.review-composer-header')).toHaveLength(1);
  expect(document.querySelectorAll('.review-composer-options')).toHaveLength(1);
  expect(document.querySelectorAll('[data-revision-cancelar]')).toHaveLength(1);
  expect((document.querySelector('[data-revision-editor]') as HTMLDialogElement).open).toBe(true);
});
it('groups overlapping pins without losing any thread and publishes the open count',async()=>{
 const counts:number[]=[];const receive=(e:any)=>counts.push(e.detail.open);document.addEventListener('bottifact:review-count',receive);
 mount();
 for(const text of ['First point','Second point']){
  open();const editor=document.querySelector('[data-revision-editor]') as HTMLDialogElement;
  const draft=editor.querySelector('textarea')!;draft.value=text;draft.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter',ctrlKey:true,bubbles:true}));
  await vi.waitFor(()=>expect(editor.open).toBe(false));
 }
 // Position inside the visible page (jsdom otherwise has a zero-sized viewport rect).
 const claim=document.querySelector('#claim') as HTMLElement;
 claim.getBoundingClientRect=()=>({x:100,y:100,left:100,right:300,top:100,bottom:200,width:200,height:100,toJSON(){return {};}});
 window.dispatchEvent(new Event('resize'));
 const pins=[...document.querySelectorAll('.revision-marca')].filter(n=>!(n as HTMLElement).hidden);
 expect(pins).toHaveLength(1);expect(pins[0].textContent).toBe('2');
 (pins[0] as HTMLElement).click();expect(document.querySelectorAll('.revision-hilo')).toHaveLength(2);
 expect(counts.at(-1)).toBe(2);
 document.removeEventListener('bottifact:review-count',receive);
});
