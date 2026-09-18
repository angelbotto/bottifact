## Wide tables and diagrams

Tables are wide by default. Do not apply nowrap to every cell; wrap long identifiers and scroll locally where structure needs width. SVG diagrams need a viewBox, title and equivalent text. Protect label readability with a scrollable region or a mobile vertical composition. The example diagram contains exactly three steps; adding steps requires updating geometry, equivalent text and viewBox. It neither simulates a process nor calculates duration.

```html
<figure class="amplio">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Medidas tipográficas, desplazable">
    <table><caption>Valores observados en cmrg.me</caption>
      <thead><tr><th scope="col">Uso</th><th scope="col">Tamaño</th><th scope="col">Interlineado</th></tr></thead>
      <tbody><tr><th scope="row">Cuerpo</th><td>15,5 px</td><td>1,55</td></tr>
        <tr><th scope="row">Título, escritorio</th><td>44,5 px</td><td>1,1111</td></tr></tbody>
    </table>
  </div>
  <figcaption>Fuente: hoja CSS y estilo calculado a 1639 px de viewport.</figcaption>
</figure>
```

```html
<figure class="ancho">
  <div class="diagrama-caja" tabindex="0" role="region" aria-label="Proceso de revisión, desplazable">
    <svg class="diagrama" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 160" role="img" aria-labelledby="proceso-titulo proceso-desc">
      <title id="proceso-titulo">De la fuente a la decisión</title>
      <desc id="proceso-desc">Observar la fuente, verificar la evidencia y registrar la decisión.</desc>
      <g fill="none" stroke="currentColor"><rect x="10" y="40" width="200" height="80" rx="4"/>
        <rect x="260" y="40" width="200" height="80" rx="4"/><rect x="510" y="40" width="200" height="80" rx="4"/>
        <path d="M210 80h42m-9-7 9 7-9 7M460 80h42m-9-7 9 7-9 7"/></g>
      <g fill="currentColor" text-anchor="middle" font-size="17"><text x="110" y="87">Observar</text><text x="360" y="87">Verificar</text><text x="610" y="87">Registrar</text></g>
    </svg>
  </div>
  <figcaption>Fuente → verificación → decisión registrada. Las flechas indican orden, no duración.</figcaption>
</figure>
```
