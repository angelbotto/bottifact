## Mapa de relaciones explorable

<!-- nota:ejemplo relationship-map -->
```html
{{EXAMPLE}}
```

**Cuándo:** entender la vecindad de una pieza y seguir relaciones con dirección, motivo y estado. Incluye búsqueda global dentro del conjunto local, uno/dos saltos, mapa completo, filtros por relación/estado, historial de navegación, zoom, ajuste y lista equivalente.

**Datos necesarios:** tablas `data-map-nodes` y `data-map-edges`. Cada nodo usa `data-node` único, nombre, tipo y contexto. Cada relación declara `data-source`, `data-target`, tipo, razón y estado `Declarada` o `Sugerida`. Los extremos deben existir. Usa un ID único en el contenedor. No inventes conexiones ni confianza porcentual. Las relaciones del ejemplo fueron escritas para la muestra; no se infieren con IA.

**Interacción y accesibilidad:** botones y controles nativos con teclado; texto completo en inspector y fuente tabular. Buscar encuentra también piezas fuera de la vecindad. En móvil la región tiene scroll local; no encoger el texto por defecto. Ajustar es opcional y puede reducirlo: 100 % recupera su tamaño. Las líneas discontinuas tienen también etiqueta textual de estado. Sin JavaScript quedan las dos tablas. Seleccionar un nodo explora su vecindad; Volver restaura el nodo anterior con los filtros actuales.

**Límite:** componente local, hasta 100 nodos y 250 relaciones. No conecta el grafo del portal, no importa sesiones, no crea proyectos persistentes ni edita relaciones. El servidor debe filtrar permisos antes de generar el HTML: esconder nodos en el navegador no protege datos. La disposición es determinista por tipo; no es un motor de fuerzas ni un trazador de rutas óptimas. Relaciones entrantes y salientes participan en el alcance de uno/dos saltos.

**Runtime:** `BottifactRelationships.init/get/destroy`; destruir limpia controles y listeners, conserva las tablas originales y permite volver a inicializar. Datos inválidos conservan la fuente sin montar un mapa parcial.
