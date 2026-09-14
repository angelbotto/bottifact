/* Nota Tikin. Pegar una vez al final del fragmento, dentro de <script>. */
(() => {
  'use strict';
  const root = document.documentElement;
  const selectors = document.querySelectorAll('[data-tema]');
  const themes = ['system','light','dark','sea'];
  function theme(value) {
    if (!themes.includes(value)) value = 'system';
    if (value === 'system') delete root.dataset.theme; else root.dataset.theme = value;
    selectors.forEach(selector => { selector.value = value; });
    document.querySelectorAll('[data-elegir-tema]').forEach(input => { input.checked = input.value === value; });
    try { localStorage.setItem('nota-tema',value); } catch {}
    document.dispatchEvent(new CustomEvent('nota:tema'));
  }
  let stored = 'system';
  try { stored = localStorage.getItem('nota-tema') || 'system'; } catch {}
  theme(stored);
  selectors.forEach(selector => selector.addEventListener('change', e => theme(e.target.value)));
  document.addEventListener('change', e => {
    if (e.target.matches('[data-elegir-tema]')) theme(e.target.value);
  });
  // Variante optativa: las notas antiguas conservan su escala de lectura.
  function comfort(enabled) {
    root.toggleAttribute('data-lectura-comoda', enabled);
    document.querySelectorAll('[data-comodidad]').forEach(button => button.setAttribute('aria-pressed', String(enabled)));
    try { localStorage.setItem('nota-lectura-comoda', String(enabled)); } catch {}
  }
  let comfortable = false;
  try { comfortable = localStorage.getItem('nota-lectura-comoda') === 'true'; } catch {}
  if (document.querySelector('[data-comodidad]')) comfort(comfortable);
  document.addEventListener('click', e => {
    if (e.target.closest('[data-comodidad]')) comfort(!root.hasAttribute('data-lectura-comoda'));
  });

  // El progreso pertenece al artículo, no al footer del documento envolvente.
  const article = document.querySelector('[data-lectura]');
  const links = [...document.querySelectorAll('.indice a[href^="#"]')];
  const sections = links.map(a => document.getElementById(a.hash.slice(1)));
  const ruler = document.querySelector('.regla');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
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
    // En multipágina el índice pertenece a multipagina.js; no medir páginas ocultas.
    if (article.classList.contains('multipagina')) return;
    let active = -1;
    sections.forEach((section,index) => { if (section?.getBoundingClientRect().top <= 120) active = index; });
    if (progress === 1 && links.length) active = links.length - 1;
    links.forEach((a,index) => {
      a.closest('li')?.classList.toggle('visto',index < active);
      if (index === active) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current');
    });
  }
  const schedule = () => { if (motion.matches) { if(frame)cancelAnimationFrame(frame);update(); } else if (!frame) frame = requestAnimationFrame(update); };
  motion.addEventListener('change',schedule);
  addEventListener('scroll',schedule,{passive:true});
  addEventListener('resize',schedule);
  document.addEventListener('nota:pagina',schedule);
  if (article && window.ResizeObserver) new ResizeObserver(schedule).observe(article);
  document.fonts?.ready.then(schedule);
  update();

  document.querySelectorAll('[data-copiar]').forEach(button => {
    button.addEventListener('click',async () => {
      const code = document.getElementById(button.dataset.copiar);
      const status = button.closest('.codigo,.terminal')?.querySelector('[role="status"]');
      if (!code) return;
      try {
        if (!navigator.clipboard?.writeText) throw new Error('clipboard unavailable');
        await navigator.clipboard.writeText(code.textContent);
        if (status) status.textContent = 'Código copiado.';
        // Conservar hijos, icono y nombre accesible; el estado comunica el resultado.
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
  addEventListener('beforeprint',() => { closedForPrint=[...document.querySelectorAll('.metodologia:not([open]),.extracto details:not([open]),[data-grafica] details:not([open]),[data-escena] details:not([open])')]; closedForPrint.forEach(e=>e.open=true); });
  addEventListener('afterprint',() => { closedForPrint.forEach(e=>e.open=false); closedForPrint=[]; });
})();
