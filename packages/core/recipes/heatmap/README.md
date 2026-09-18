## Attention map: matriz de intensidad

<!-- nota:ejemplo calor -->
```html
{{EXAMPLE}}
```

**Cuándo:** buscar concentraciones entre dos dimensiones discretas. Cada celda muestra su valor y la leyenda tiene intervalos explícitos. Para partes de un total usa `.mapa`, que conserva el treemap original.

**Límite:** cinco niveles, definidos por seis límites crecientes; máximo incluido en el último nivel. Un valor fuera del dominio produce error visible y conserva la tabla, nunca se satura en secreto. Hasta 31 × 31 celdas con ancho mínimo por columna y scroll local. No usa degradado ni escala implícita por fila. Las cifras mantienen el significado con colores forzados.

<a id="recetas-tablas"></a>
