## Librería de evidencia: instalación por pieza

La fuente de cada visualización es **su tabla HTML**, no una segunda copia de los datos.
Pega `packages/core/styles/fonts.css` y `packages/core/styles/artifact.css` completos y, al final del documento, los módulos necesarios dentro de
`<script>`: [packages/core/components/charts.js](../packages/core/components/charts.js) para gráficas/calor y [packages/core/components/tables.js](../packages/core/components/tables.js) para
ordenación/sparkline. Son independientes de Three.js. Cada módulo se pega una sola vez.
Se inicializan al cargar; para HTML insertado después usa `NotaGraficas.init(contenedor)`
o `NotaTablas.init(contenedor)`. Repetir `init` devuelve la instancia existente.
`get(elemento).destroy()` devuelve el HTML original; para nuevos datos, destruye la
instancia, modifica la tabla y vuelve a inicializar. No hay red, almacenamiento ni framework.

Los siguientes bloques son también la fuente del catálogo ejecutable: el ensamblador
extrae las recetas marcadas `nota:ejemplo`. Las figuras se copian **como hijas de `.hoja`**.
Para secciones anidadas usa `por-seccion`; para capítulos usa `multipagina` y coloca las
figuras como hijas de `.pagina`. No envuelvas el bloque en otra sección angosta.

`data-valor` usa punto decimal, sin separadores de miles; su texto visible incluye la
unidad y el formato humano. Vacío significa ausencia, `0` es un cero medido. Los ejemplos
son ilustrativos y lo dicen en su pie. Los nombres y los datos se insertan como texto.
Las unidades de los ejes se escriben completas junto al dibujo (`X`, `Y`) para permitir
que envuelvan en varias líneas. El SVG mantiene los ticks y sus valores en la misma escala.
Las gráficas no tienen animación ni tooltip imprescindible: la tabla permite consultar
cada punto por teclado. Las escalas se calculan con los datos, sin recortar extremos.
No se suman ni se interpolan registros ausentes. Los intervalos entre puntos de una línea
son segmentos rectos, no observaciones adicionales.

<a id="recetas-graficas"></a>
