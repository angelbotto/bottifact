## Fixed proportion map

This grid represents exactly 60/25/15: columns 3fr/2fr, then rows 5fr/3fr subdividing the second column. Recalculate proportions when data changes; changing labels alone misrepresents values. Only comparable nonnegative values with a positive total fit this recipe. Check text minimums against actual areas. Use the attention map or bars for other distributions, and disclose any grouped tail separately.

```html
<figure class="ancho">
  <div class="mapa" role="group" aria-label="Reparto ilustrativo de cien horas">
    <div class="bloque destaca"><span class="n">Investigar</span><span class="d">60 h · 60 %</span></div>
    <div class="bloque"><span class="n">Construir</span><span class="d">25 h · 25 %</span></div>
    <div class="bloque"><span class="n">Revisar</span><span class="d">15 h · 15 %</span></div>
  </div>
  <figcaption>Ejemplo de cien horas. Las áreas incluyen el borde interior de cada celda.</figcaption>
</figure>
```
