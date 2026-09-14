/* Nota Tikin · señales breves, exclusivamente por botones y apagadas al cargar.
   Cada canal es independiente. Sin archivos, fetch, autoplay ni persistencia. */
(() => {
  'use strict';
  const instances=new WeakMap();
  const notes={accion:[660,440],confirmacion:[520,780],atencion:[440,360,440]};
  class NotaSonido {
    constructor(element) {
      if(instances.has(element))throw new TypeError('Ya hay un canal en este contenedor.');
      const toggle=element.querySelector('[data-audio-activar]'),status=element.querySelector('[role="status"]');
      if(!toggle||!status)throw new TypeError('El canal necesita botón de activación y estado.');
      this.element=element;this.toggle=toggle;this.status=status;this.enabled=false;this.dead=false;
      this.audio=null;this.voices=[];this.epoch=0;this.plays=0;this.abort=new AbortController();
      this.sync();
      element.addEventListener('click',async event=>{
        const button=event.target.closest('button');
        if(!event.isTrusted||!button||button.disabled||button.closest('[data-canal-sonido]')!==element||this.dead)return;
        if(button===toggle){
          if(this.enabled){this.disable();return;}
          const Audio=window.AudioContext||window.webkitAudioContext;
          if(!Audio){this.status.textContent='Este navegador no ofrece Web Audio. Las acciones siguen disponibles.';return;}
          try{
            this.audio ||= new Audio();this.enabled=true;const epoch=++this.epoch;
            await this.audio.resume();
            if(this.dead||epoch!==this.epoch||!this.enabled)return;
            this.sync();this.status.textContent='Activado. Elige una señal para escucharla.';
          }catch{this.disable();this.status.textContent='No se pudo activar el audio. Puedes seguir sin sonido.';}
          return;
        }
        const kind=button.dataset.audio;
        if(!notes[kind])return;
        // El significado de la acción siempre se escribe, incluso con audio apagado.
        this.status.textContent=button.dataset.mensaje || button.textContent.trim();
        if(!this.enabled)return;
        const epoch=this.epoch;
        try {
          await this.audio.resume();
          // Una promesa de resume no puede hacer sonar una acción ya cancelada.
          if(!this.enabled||this.dead||document.hidden||epoch!==this.epoch)return;
          this.stopVoices();
          const now=this.audio.currentTime;
          notes[kind].forEach((frequency,i)=>{
            const osc=this.audio.createOscillator(),gain=this.audio.createGain(),time=now+i*.065;
            osc.type='sine';osc.frequency.setValueAtTime(frequency,time);
            gain.gain.setValueAtTime(0,time);gain.gain.linearRampToValueAtTime(.025,time+.003);
            gain.gain.exponentialRampToValueAtTime(.0001,time+.055);
            osc.connect(gain);gain.connect(this.audio.destination);
            const voice={osc,gain};this.voices.push(voice);
            osc.onended=()=>{osc.disconnect();gain.disconnect();this.voices=this.voices.filter(v=>v!==voice);};
            osc.start(time);osc.stop(time+.06);
          });
          this.plays++;
        }catch{this.disable();this.status.textContent='El audio no está disponible. La acción sigue indicada en texto.';}
      },{signal:this.abort.signal});
      document.addEventListener('visibilitychange',()=>{if(document.hidden)this.disable();},{signal:this.abort.signal});
      addEventListener('pagehide',()=>this.disable(),{signal:this.abort.signal});
      instances.set(element,this);
    }
    sync(){this.toggle.setAttribute('aria-pressed',String(this.enabled));this.toggle.textContent=this.enabled?'Desactivar sonido':'Activar sonido';}
    stopVoices(){for(const {osc,gain} of this.voices){try{osc.stop();}catch{}osc.disconnect();gain.disconnect();}this.voices=[];}
    disable(){this.enabled=false;this.epoch++;this.stopVoices();this.audio?.suspend().catch(()=>{});this.sync();this.status.textContent='Sonido apagado.';}
    destroy(){if(this.dead)return;this.disable();this.dead=true;this.abort.abort();this.audio?.close().catch(()=>{});instances.delete(this.element);}
  }
  function init(root=document){return [...(root.matches?.('[data-canal-sonido]')?[root]:[]),...root.querySelectorAll('[data-canal-sonido]')].map(e=>instances.get(e)||new NotaSonido(e));}
  window.NotaSonido=NotaSonido;NotaSonido.init=init;NotaSonido.get=e=>instances.get(e);init();
})();
