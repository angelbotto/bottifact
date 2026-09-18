## Code with copy control

Use when readers need exact text to inspect or copy. Keep filenames when meaningful; language-only headers are compacted by the interface runtime. Preserve native selection and local scrolling. If clipboard access fails, select the code and explain manual copying. IDs must be unique. Escape &, < and > when inserting source into HTML.

```html
<figure class="ancho">
  <div class="codigo">
    <div class="cab"><span>registro.js · JavaScript</span>
      <button type="button" data-copiar="registro-codigo" aria-label="Copiar registro.js" title="Copiar"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H4v13h4"/></svg></button>
      <span class="copia-estado" role="status" aria-live="polite"></span>
    </div>
    <pre tabindex="0" aria-label="Código de registro"><code id="registro-codigo"><span class="com">// La procedencia forma parte del dato.</span>
<span class="kw">const</span> fuente = <span class="str">"CSS publicado de cmrg.me"</span>;</code></pre>
  </div>
  <figcaption>Ejemplo verificable; la copia conserva el texto, sin los colores del resaltado.</figcaption>
</figure>
```
