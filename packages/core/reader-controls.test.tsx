import {beforeEach,afterEach,expect,it,vi} from 'vitest';
import {readFileSync} from 'node:fs';
const source=readFileSync(process.cwd()+'/packages/core/components/reader-controls.js','utf8');
beforeEach(()=>{document.body.replaceChildren();document.documentElement.className='';delete (window as any).BottifactReaderControls;delete (window as any).BottifactReviewBridge;});
afterEach(()=>{document.querySelectorAll('[data-bottifact-controls]').forEach(e=>e.remove());});
it('renders one toolbar for hosted legacy markup and routes sharing to the host',()=>{
 const action=vi.fn().mockResolvedValue({ok:true}),subscribe=vi.fn(),ready=vi.fn();(window as any).BottifactReviewBridge={action,subscribe,controlsReady:ready};
 window.eval(source);document.dispatchEvent(new Event('DOMContentLoaded'));window.eval(source);document.dispatchEvent(new Event('DOMContentLoaded'));
 expect(document.querySelectorAll('.bottifact-toolbar')).toHaveLength(1);(document.querySelector('button[aria-label="Compartir"]') as HTMLButtonElement).click();expect(action).toHaveBeenCalledWith('share');expect(ready).toHaveBeenCalledOnce();
});
it('keeps the existing appearance and review controls as the action owners',()=>{
 document.body.innerHTML='<details data-apariencia-menu><summary>Appearance</summary><div class="apariencia-panel"></div></details><div class="revision-barra"><button>Comment</button><button aria-label="Añadir nota privada">Note</button><button>List</button></div>';
 const appearance=document.querySelector('[data-apariencia-menu]'),note=document.querySelector('[aria-label="Añadir nota privada"]')!,click=vi.fn();note.addEventListener('click',click);
 window.eval(source);document.dispatchEvent(new Event('DOMContentLoaded'));expect(document.querySelector('.bottifact-toolbar [data-apariencia-menu]')).toBe(appearance);
 const addNote=[...document.querySelectorAll('.bf-menu button')].find(b=>b.textContent==='Añadir nota personal') as HTMLButtonElement;addNote.click();expect(click).toHaveBeenCalledOnce();
});
