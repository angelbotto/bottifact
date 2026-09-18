## Elegir y copiar desde el catálogo

`examples/generated/template.html` ofrece búsqueda por nombre/propósito y el HTML exacto de cada receta en un
`details` junto al ejemplo. La búsqueda filtra **el índice de recetas**, no borra secciones de
la nota ni altera su progreso. Acentos y mayúsculas no cambian los resultados. El índice
completo sigue disponible sin JS. El botón usa el mismo contrato de copia y alternativa por
selección de `packages/core/components/reader.js`. El módulo [packages/core/components/catalog.js](../packages/core/components/catalog.js) sólo hace falta en un
catálogo que incluya `data-buscador-recetas`; no se necesita en artículos normales.

Las muestras son componentes de documento, no un constructor de aplicaciones. Cada snippet
requiere las fuentes y módulos indicados arriba; el botón copia el componente, no toda la
biblioteca. La plantilla y los ejemplos completos sí son autocontenidos.
