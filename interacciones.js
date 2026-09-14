/* Nota Tikin. Pegar una vez al final del fragmento, dentro de <script>. */
(() => {
  'use strict';
  const root = document.documentElement;
  const selector = document.querySelector('[data-tema]');
  const themes = ['system','light','dark','sea'];
  function theme(value) {
    if (!themes.includes(value)) value = 'system';
    if (value === 'system') delete root.dataset.theme; else root.dataset.theme = value;
    if (selector) selector.value = value;
    try { localStorage.setItem('nota-tema',value); } catch {}
    document.dispatchEvent(new CustomEvent('nota:tema'));
  }
  let stored = 'system';
  try { stored = localStorage.getItem('nota-tema') || 'system'; } catch {}
  theme(stored);
  selector?.addEventListener('change', e => theme(e.target.value));

  // El progreso pertenece al artículo, no al footer del documento envolvente.
  const article = document.querySelector('[data-lectura]');
  const links = [...document.querySelectorAll('.indice a[href^="#"]')];
  const sections = links.map(a => document.getElementById(a.hash.slice(1)));
  const ruler = document.querySelector('.regla');
  function goToProgress(value) {
    if (!article) return;
    const distance=Math.max(0,article.getBoundingClientRect().height-innerHeight);
    const top=scrollY+article.getBoundingClientRect().top+distance*Math.max(0,Math.min(100,value))/100;
    scrollTo({top,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  }
  ruler?.addEventListener('click',e=>{const r=ruler.getBoundingClientRect();goToProgress((e.clientY-r.top)/r.height*100);});
  ruler?.addEventListener('keydown',e=>{
    const current=Number(ruler.getAttribute('aria-valuenow'));
    const values={ArrowDown:current+1,ArrowRight:current+1,ArrowUp:current-1,ArrowLeft:current-1,PageDown:current+10,PageUp:current-10,Home:0,End:100};
    if(e.key in values){e.preventDefault();goToProgress(values[e.key]);}
  });
  let frame = 0;
  function update() {
    frame = 0;
    if (!article) return;
    const rect = article.getBoundingClientRect();
    const available = rect.height - innerHeight;
    const progress = available <= 0 ? (rect.bottom <= innerHeight ? 1 : 0) : Math.max(0,Math.min(1,-rect.top / available));
    if (ruler) {
      ruler.style.setProperty('--lectura',progress);
      ruler.setAttribute('aria-valuenow',Math.round(progress * 100));
      const value = ruler.querySelector('.val');
      if (value) value.textContent = Math.round(progress * 100) + '%';
    }
    let active = -1;
    sections.forEach((section,index) => { if (section?.getBoundingClientRect().top <= 120) active = index; });
    if (progress === 1 && links.length) active = links.length - 1;
    links.forEach((a,index) => {
      a.closest('li')?.classList.toggle('visto',index < active);
      if (index === active) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current');
    });
  }
  const schedule = () => { if (!frame) frame = requestAnimationFrame(update); };
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  if (article && window.ResizeObserver) new ResizeObserver(schedule).observe(article);
  document.fonts?.ready.then(schedule);
  update();

  document.querySelectorAll('[data-copiar]').forEach(button => {
    button.addEventListener('click',async () => {
      const code = document.getElementById(button.dataset.copiar);
      const status = button.closest('.codigo')?.querySelector('[role="status"]');
      if (!code) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
        await navigator.clipboard.writeText(code.textContent);
        if (status) status.textContent = 'Código copiado.';
        button.textContent = 'Copiado';
        setTimeout(() => { button.textContent = 'Copiar'; },1600);
      } catch {
        const range = document.createRange(); range.selectNodeContents(code);
        const selection = getSelection(); selection.removeAllRanges(); selection.addRange(range);
        if (status) status.textContent = 'Código seleccionado. Usa ⌘C o Ctrl+C para copiar.';
      }
    });
  });

  // Reproducir un sonido exige activación explícita; no se descargan MP3.
  const soundButton = document.querySelector('[data-sonido]');
  let soundEnabled = false, audio;
  soundButton?.addEventListener('click',() => {
    soundEnabled = !soundEnabled;
    soundButton.setAttribute('aria-pressed',String(soundEnabled));
    soundButton.textContent = soundEnabled ? 'Sonido activado' : 'Sonido apagado';
    if (!soundEnabled) audio?.suspend().catch(()=>{});
  });
  document.addEventListener('click',e => {
    if (!soundEnabled || !e.target.closest('button') || e.target.closest('[data-sonido],[data-canal-sonido]')) return;
    try {
      const Audio = window.AudioContext || window.webkitAudioContext;
      if (!Audio) return;
      audio ||= new Audio(); audio.resume().catch(()=>{});
      const oscillator = audio.createOscillator(), gain = audio.createGain(), t = audio.currentTime;
      oscillator.type = 'sine'; oscillator.frequency.setValueAtTime(680,t);
      oscillator.frequency.exponentialRampToValueAtTime(420,t+.04);
      gain.gain.setValueAtTime(.025,t); gain.gain.exponentialRampToValueAtTime(.0001,t+.055);
      oscillator.connect(gain); gain.connect(audio.destination);
      oscillator.start(t); oscillator.stop(t+.06);
      oscillator.onended = () => { oscillator.disconnect(); gain.disconnect(); };
    } catch {}
  });
  // Imprimir el contenido íntegro de los extractos incluso en motores sin ::details-content.
  let closedForPrint = [];
  addEventListener('beforeprint',() => { closedForPrint=[...document.querySelectorAll('.extracto details:not([open])')]; closedForPrint.forEach(e=>e.open=true); });
  addEventListener('afterprint',() => { closedForPrint.forEach(e=>e.open=false); closedForPrint=[]; });
})();
