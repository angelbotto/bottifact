/* Invitación local: copia el texto con contexto; no envía ni conserva mensajes. */
(()=>{'use strict';const instances=new WeakMap();
 class Invitacion{
  constructor(element){this.element=element;this.abort=new AbortController();this.form=element.querySelector('form');this.input=this.form?.querySelector('textarea');this.status=this.form?.querySelector('[role="status"]');if(!this.input||!this.status)throw Error('Faltan formulario, texto y estado.');
   this.form.querySelector('[data-invitacion-copiar]').addEventListener('click',async event=>{event.preventDefault();const value=this.input.value.trim();if(!value){this.input.setCustomValidity('Escribe una idea antes de copiar.');this.input.reportValidity();return;}this.input.setCustomValidity('');const title=element.querySelector('h3')?.textContent||'Invitación';this.prompt=title+'\nDocumento: '+document.title+'\nReferencia: #'+element.id+'\n\n'+value;try{await navigator.clipboard.writeText(this.prompt);if(!this.abort.signal.aborted)this.status.textContent='Copiado con contexto. Pégalo donde quieras compartirlo.';}catch{if(!this.abort.signal.aborted){this.status.textContent='No se pudo copiar. Selecciona y copia tu texto manualmente.';this.input.focus();this.input.select();}}},{signal:this.abort.signal});
   this.input.addEventListener('input',()=>{this.input.setCustomValidity('');this.status.textContent='Borrador local; copia antes de cerrar.';},{signal:this.abort.signal});instances.set(element,this);
  }
  destroy(){this.abort.abort();instances.delete(this.element);}
 }
 function init(root=document){return [...(root.matches?.('[data-invitacion]')?[root]:[]),...root.querySelectorAll('[data-invitacion]')].map(e=>instances.get(e)||new Invitacion(e));}
 window.NotaInvitacion={init,get:e=>instances.get(e)};init();
})();
