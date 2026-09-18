## Tabla interactiva

<!-- nota:ejemplo explorador -->
```html
{{EXAMPLE}}
```

**Cuándo:** Investigar una tabla corta: buscar, filtrar un estado, agrupar y ordenar dentro de cada grupo. Incluye `packages/core/components/controls.js` y `packages/core/components/data-explorer.js`. Buscar queda visible; Filtros, Agrupar y Columnas abren paneles compactos. Cada encabezado ofrece ascendente, descendente y restablecer. Escape cierra el menú y devuelve el foco. Las columnas ocultas se pueden recuperar; Nombre permanece. Los encabezados indican `aria-sort`; el total corresponde sólo a las filas visibles.

**Cuándo no / límite:** tabla local de 1–16 columnas y hasta 2000 filas. Admite texto, números con `data-valor` y fechas ISO mediante `data-tipo="fecha"` en el encabezado; declara `data-tipo="numero"` cuando corresponda. La receta de cuatro columnas mantiene equipo, estado e importe, pero el motor no exige ese esquema. `data-columna-estado` y `data-columna-total` usan índices desde cero (por defecto 2 y 3); declara la unidad de la suma. No mezcla monedas ni conecta un servidor.

Incluye filtro por columna (texto, rango numérico o fecha), búsqueda, grupos plegables de la página, columnas visibles, selección de filas entre páginas, paginación 10/25/50/100, espaciado y encabezado fijo. Mayús al elegir otro orden agrega un criterio. El total corresponde a la vista filtrada completa; el contador de grupo corresponde a la página. Exportar selección incluye filas seleccionadas aunque estén fuera del filtro, usando columnas visibles; sin selección exporta toda la vista filtrada. CSV neutraliza fórmulas. Impresión muestra la fuente completa. No hay edición de celdas ni virtualización. `NotaExplorador.init/get/destroy`, `instance.visible`, `instance.selected` e `instance.exportCSV()` conservan los valores originales.

### Unified table controls

`table-model.js` must load before `data-explorer.js`. The generator resolves this dependency. Conditions support AND/OR, text equality/contains/multiple values, numeric/date bounds, and empty values. The older quick filter remains additive. Empty range inputs do not match any rows until completed.

Saved views are device-local and scoped by document and table identity. They include search, conditions, sort, grouping, visibility and density. Fixed columns and width sliders are per-open-table adjustments. Give the table an `id`, each row an immutable `data-row-id` and each cell an `id` when a reference must survive a future version; synthesized IDs only remain stable inside the current HTML. Sorting and filtering move existing rows without rewriting their IDs. The ↗ action opens all fields in a keyboard-accessible dialog. Filtered-out references remain reachable from the review list.

Examples: operational, financial and project scenarios in `examples/generated/workbench.html`. React consumers use the native `DataTable` adapter; standalone HTML does not download React or TanStack. The portal's table queries the complete authorized collection and loads more rows as you scroll. Local tables disclose page groups and complete filtered totals separately.
