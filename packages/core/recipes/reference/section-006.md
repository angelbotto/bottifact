## Pastillas, lista mono y medida

```html
<p>El valor está <span class="dato">pendiente de medir</span>.</p>
<p><span class="pildora p-si">✓ Aplicado</span>
   <span class="pildora p-medio">≈ Parcial</span>
   <span class="pildora p-no">× No disponible</span></p>
<dl class="datos">
  <div><dt>Fuente</dt><dd>CSS publicado de cmrg.me</dd></div>
  <div><dt>Tamaño original</dt><dd>15,5 px</dd></div>
  <div><dt>Interlineado original</dt><dd>1,55</dd></div>
</dl>
<div class="medida">
  <label for="cobertura">Páginas revisadas</label><span class="pct">100 %</span>
  <meter id="cobertura" min="0" max="10" value="10">10 de 10 páginas</meter>
</div>
```

**Cuándo:** la lista `dl` asocia etiquetas y valores; una pastilla representa un estado o dato
breve. La barra usa `meter` porque mide cobertura, no una operación en curso. No conviertas
fechas o nombres en controles falsos. Las pastillas saltan de línea si hace falta.
