## Globo narrado por etapas

<!-- nota:ejemplo recorrido -->
```html
{{EXAMPLE}}
```

**Cuándo:** la ubicación y el orden de una historia importan. Las etapas escritas siempre están
visibles; el mapa orienta una ruta a la vez. Incluye Three una sola vez y `packages/core/components/globe.js` antes de
`packages/core/components/reports.js`. Comparte la dependencia con todos los demás globos/escenas del documento.

**Cuándo no / límite:** no convierte etapas abstractas en geografía. `data-lugar` identifica
un lugar; repetir un ID exige las mismas coordenadas y nombre. Cada ruta necesita un ID único
y dos lugares. No autoavanza ni añade sonido. Empieza pausado; conserva controles de NotaGlobo,
reduce, pausa por visibilidad y destroy. Sin Three queda mensaje y relato; sin WebGL queda
además la lista de rutas. No añade mapas, texturas ni geocodificación remota.
La lista del globo también cambia la etapa del relato. Una ruta seleccionada mantiene su
orientación: para giro libre usa «Vista inicial» y «Reanudar giro»; anterior/siguiente vuelve
a orientar la etapa. No interpreta el giro manual como un cambio de etapa.
