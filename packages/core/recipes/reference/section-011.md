## Tarjetas «kept»

```html
<div class="kept ancho">
  <article>
    <svg class="portada" viewBox="0 0 180 220" aria-hidden="true">
      <rect x="2" y="2" width="176" height="216" rx="2" fill="#755a42"/>
      <circle cx="90" cy="85" r="48" fill="none" stroke="#fef8f2"/>
      <text x="24" y="166" fill="#fef8f2" font-family="Georgia" font-size="24">La decisión</text>
    </svg>
    <h3>La decisión</h3><p>Qué se eligió y por qué. Un registro al que podamos volver.</p>
    <p class="meta">NOTA / 01 · ejemplo editorial</p>
  </article>
  <article>
    <h3>La evidencia</h3><p>Medidas, fuentes y límites, con el contexto que les da sentido.</p>
    <p class="meta">REGISTRO / 02 · ejemplo editorial</p>
  </article>
</div>
```

**Cuándo:** objetos o referencias seleccionados, no un catálogo exhaustivo. Portada opcional,
título completo y una nota personal o útil. `auto-fit` con mínimo adaptable de `240px`; el hover
inclina la portada `−2deg` y la eleva `3px` durante `320ms`, sin mover el texto. Con movimiento
reducido no hay transición. Si toda la tarjeta debe navegar, usa un enlace real con nombre;
no añadas un `onclick` a un `div`. Las portadas con `<img>` deben ser `data:` URI, como las de
`examples/generated/template.html`, que se generan localmente y no reproducen carátulas comerciales.
