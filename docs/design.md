# Bottifact portal

El creador recorre documentos y revisiones durante su jornada en portátil y escritorio. La apariencia sigue su preferencia clara u oscura; las miniaturas conservan la identidad del documento.

## Sistema visual

La gestión usa Geist, con etiquetas compactas de 11–13 px, títulos de ficha de 15 px y título de página de 28 px. Instrument Serif se conserva sólo en la marca. Neutros cálidos OKLCH con acento terracota; tokens en `portal/static/library.css`. Una segunda superficie distingue navegación, filtros y selección. Bordes de un píxel, radios de 7–12 px y foco visible. Los colores del mapa ayudan a separar grupos, pero los nombres y motivos explican las relaciones.

## Composición

Navegación lateral de 226 px en escritorio; navegación horizontal desplazable bajo 850 px. Buscador principal, filtros progresivos y cuatro vistas. Galería de tres columnas (dos bajo 1250 px y una en móvil), lista con miniaturas, tabla con scroll local y atlas con inspector. La ficha de vista previa ocupa hasta 500 px y se cierra con Escape. Evitar controles de gestión dentro del documento compartido.

## Interacción

Miniaturas estáticas en iframes aislados y carga próxima al viewport. Abrir la ficha no ejecuta el artefacto. Cambios visuales de 150–180 ms, sin animaciones decorativas de carga y con movimiento reducido. El mapa tiene botones de zoom, arrastre y selección con teclado, además de lista alternativa. Controles de interfaz con iconos coherentes y nombre accesible.

## Controles y revisión

La dirección detallada y sus referencias están en [interface-direction.md](interface-direction.md). Jerarquía primaria/secundaria/discreta, iconos SVG de 16–19 px, radios de 8 px y transiciones de 120 ms. Conserva texto para acciones ambiguas. La barra del lector agrupa apariencia, comentario/nota/revisión y compartir/más; usa áreas de 44 px en móvil, ayuda con hover/foco y estados activos. La biblioteca carga el CSS de controles desde un archivo para conservar su CSP estricta.
