import {readFileSync} from 'node:fs';
import {afterEach,beforeEach,expect,it,vi} from 'vitest';
const source=readFileSync('packages/core/components/presentation.js','utf8');
let frame:HTMLIFrameElement;
beforeEach(()=>{
 frame=document.createElement('iframe');document.body.append(frame);
 const w=frame.contentWindow!,d=w.document;
 d.body.innerHTML='<header class="barra"><button data-ir="first">First</button><button data-ir="second">Second</button></header><main data-presentation><article class="pagina" id="first"><h1>Decision</h1><p id="point">Evidence</p></article><article class="pagina" id="second" hidden><h1>Next step</h1><input aria-label="Editable"></article></main>';
 (w as any).CSS={escape:(v:string)=>v};
 (w as any).HTMLDialogElement.prototype.showModal=function(){this.open=true;};
 (w as any).HTMLDialogElement.prototype.close=function(){this.open=false;};
 for(const b of d.querySelectorAll<HTMLButtonElement>('[data-ir]'))b.onclick=()=>d.dispatchEvent(new (w as any).CustomEvent('nota:pagina',{detail:{id:b.dataset.ir}}));
 (w as any).eval(source);
});
afterEach(()=>frame.remove());
it('navigates slides and opens an accessible overview without copying source anchors',()=>{
 const w=frame.contentWindow!,d=w.document;
 (d.querySelector('[aria-label="Diapositiva siguiente"]') as HTMLButtonElement).click();
 expect((d.querySelector('#first') as HTMLElement).hidden).toBe(true);expect((d.querySelector('#second') as HTMLElement).hidden).toBe(false);
 expect(d.querySelector('.presentation-count')?.textContent).toBe('Diapositiva 2 de 2');
 (d.querySelector('[aria-haspopup="dialog"]') as HTMLButtonElement).click();
 expect(d.querySelector('dialog')?.open).toBe(true);expect(d.querySelectorAll('#point')).toHaveLength(1);
 (d.querySelector('.presentation-slide-index button') as HTMLButtonElement).click();expect(d.querySelector('dialog')?.open).toBe(false);expect((d.querySelector('#first') as HTMLElement).hidden).toBe(false);
});
it('switches to continuous reading and back without removing slide content',()=>{
 const d=frame.contentDocument!;
 (d.querySelector('[aria-label="Leer como documento continuo"]') as HTMLButtonElement).click();
 expect([...d.querySelectorAll<HTMLElement>('.pagina')].every(p=>!p.hidden)).toBe(true);
 (d.querySelector('[aria-label="Ver como presentación"]') as HTMLButtonElement).click();
 expect(d.querySelectorAll('.pagina[hidden]')).toHaveLength(1);expect(d.querySelector('#point')?.textContent).toBe('Evidence');
});
it('ignores slide shortcuts in input fields, dialogs and point-comment mode',()=>{
 const w=frame.contentWindow!,d=w.document;
 function key(target:Element){target.dispatchEvent(new (w as any).KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true,cancelable:true}));}
 key(d.querySelector('input')!);expect((d.querySelector('#second') as HTMLElement).hidden).toBe(true);
 d.documentElement.setAttribute('data-revisando','');key(d.body);expect((d.querySelector('#second') as HTMLElement).hidden).toBe(true);
 d.documentElement.removeAttribute('data-revisando');key(d.body);expect((d.querySelector('#second') as HTMLElement).hidden).toBe(false);
});
