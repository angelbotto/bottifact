## Tabla interactiva

<!-- nota:ejemplo explorador -->
```html
{{EXAMPLE}}
```

**Cuándo:** Investigar una tabla corta: buscar, filtrar un estado, agrupar y ordenar dentro de cada grupo. Incluye `packages/core/components/controls.js` y `packages/core/components/data-explorer.js`. Buscar queda visible; Filtros, Agrupar y Columnas abren paneles compactos. Cada encabezado ofrece ascendente, descendente y restablecer. Escape cierra el menú y devuelve el foco. Las columnas ocultas se pueden recuperar; Nombre permanece. Los encabezados indican `aria-sort`; el total corresponde sólo a las filas visibles.

**Cuándo no / límite:** tabla local de 1–16 columnas y hasta 2000 filas. Admite texto, números con `data-valor` y fechas ISO mediante `data-tipo="fecha"` en el encabezado; declara `data-tipo="numero"` cuando corresponda. La receta de cuatro columnas mantiene equipo, estado e importe, pero el motor no exige ese esquema. `data-columna-estado` y `data-columna-total` usan índices desde cero (por defecto 2 y 3); declara la unidad de la suma. No mezcla monedas ni conecta un servidor.

Incluye filtro por columna (texto, rango numérico o fecha), búsqueda, grupos plegables de la página, columnas visibles, selección de filas entre páginas, paginación 10/25/50/100, espaciado y encabezado fijo. Mayús al elegir otro orden agrega un criterio. El total corresponde a la vista filtrada completa; el contador de grupo corresponde a la página. Exportar selección incluye filas seleccionadas aunque estén fuera del filtro, usando columnas visibles; sin selección exporta toda la vista filtrada. CSV neutraliza fórmulas. Impresión muestra la fuente completa. No hay edición de celdas ni virtualización. `NotaExplorador.init/get/destroy`, `instance.visible`, `instance.selected` e `instance.exportCSV()` conservan los valores originales.
