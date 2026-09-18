## Subrayado a mano

```html
<p>El estado definitivo debe vivir en <span class="marca">un solo registro</span>.
  El <a href="#evidencia">detalle de la evidencia</a> se puede consultar después.</p>
```

**Cuándo:** una frase que contiene la decisión. `.marca` usa dos trazos SVG incrustados, de
`1.7px`, con curvas distintas; `background-size:100% .32em` y `box-decoration-break:clone`
permiten saltar de línea. El tema Sea cambia el trazo a verde. El texto conserva su tinta,
selección y contraste; el trazo no pretende reemplazar enlaces o negritas.
