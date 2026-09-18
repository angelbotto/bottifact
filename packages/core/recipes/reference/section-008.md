## Código con encabezado y copia

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

**Cuándo:** la persona necesita inspeccionar, comparar o copiar una entrada exacta. El encabezado
usa mono `12px`; el código `13px / 1.65`, con desplazamiento y selección nativos. Si la API del
portapapeles está bloqueada, el script selecciona el contenido y explica cómo copiarlo. Usa
identificadores únicos por bloque. Escapa `&`, `<` y `>` al insertar código dentro del HTML.
