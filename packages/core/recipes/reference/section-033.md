## Segunda tanda: reportes, artículos y prototipos

Las siguientes recetas amplían el sistema; no cambian los anchos ni los estilos de documentos
previos. Incluye `packages/core/styles/fonts.css`, `packages/core/styles/artifact.css` e `packages/core/components/reader.js`. Añade [packages/core/components/reports.js](../packages/core/components/reports.js)
para `data-reporte`, [packages/core/components/prototype.js](../packages/core/components/prototype.js) para `data-visor`. El recorrido necesita además
`packages/core/components/globe.js` y la única inclusión de Three 0.160.1. Los módulos son independientes de
`packages/core/components/charts.js`; no cargan red. `NotaReportes.init(raíz)` y `NotaVisores.init(raíz)` se pueden
repetir; `get(elemento).destroy()` retira la mejora y restaura los datos originales.
Para cambiar una tabla destruye, edita y vuelve a inicializar. No hay observador de datos.
