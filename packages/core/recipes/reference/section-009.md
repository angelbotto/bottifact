## Tablas y diagramas anchos

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

Las tablas son anchas por defecto. No apliques `white-space:nowrap` a toda la tabla. Si una
columna contiene identificadores largos, permite partirlos; si la estructura necesita más
ancho, conserva el desplazamiento local. Los diagramas SVG deben tener `viewBox`, título y
una descripción equivalente en texto. El tamaño del dibujo debe proteger la lectura de sus
etiquetas; usa una región desplazable para figuras densas, o una composición vertical en móvil.

Diagrama completo, sin dependencias:

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

**Cuándo:** una relación o secuencia concreta se entiende mejor como dibujo. Para registros
comparables usa la tabla; para magnitudes, una gráfica a escala.

**Límite:** esta composición contiene tres pasos. Cambiar sólo las etiquetas no añade nodos
ni rutas; para más pasos ajusta SVG, texto equivalente y viewBox. Conserva los IDs únicos,
el mínimo de 640 px y su región desplazable. No simula procesos ni calcula tiempos.
