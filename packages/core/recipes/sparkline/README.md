## Tabla con serie embebida

<!-- nota:ejemplo sparkline -->
```html
{{EXAMPLE}}
```

**Cuándo:** añadir tendencia a una tabla sin apartarse del registro. El texto de la celda nombra cada valor; el SVG es redundante y lleva `aria-hidden`.

**Límite:** X equidistante; todas las filas deben describir los mismos períodos. Exige `data-min`/`data-max` comunes y rechaza dibujar puntos fuera de ellos. No autoescala por fila, no es una gráfica con ejes ni codifica tiempo irregular; para eso usa la serie temporal. El texto sigue disponible si el dibujo no se puede generar.

<a id="recetas-sonido"></a>
