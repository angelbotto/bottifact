## Mapa de proporción

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

**Cuándo:** participación sobre un total positivo y comparable. Las columnas `3fr 2fr` dan
60/40; las filas `5fr 3fr` subdividen el 40 en 25/15. Esta receta corresponde **solo a esos
pesos**. Al cambiar datos, calcula nuevas fracciones o genera un treemap con sus valores; no
cambies únicamente las etiquetas. Las filas tienen mínimos para proteger texto; con otros
idiomas o texto mucho más largo, verifica el reparto o usa un gráfico de barras y una tabla.

Para más de tres grupos, ordena por peso y considera agrupar la cola como «Otros», desglosada
aparte. No omitas cifras pequeñas ni sustituyas un porcentaje por una celda arbitraria. El
original calcula un treemap squarify; esta receta de rejilla es una versión explícita sin D3.
