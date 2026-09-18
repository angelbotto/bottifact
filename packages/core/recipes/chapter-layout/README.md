## Multipágina

<!-- nota:ejemplo multipagina -->
```html
{{EXAMPLE}}
```

**Cuándo:** un informe con capítulos que se leen por separado y merecen cada uno su temario. No
para una nota de tres secciones: ahí la página única con índice lateral es mejor.

**La rejilla va en `.pagina`, no en `.hoja`.** Por eso la clase es `multipagina` y no
`por-seccion`: con las páginas de por medio, el selector `>` de `por-seccion` ya no alcanza a las
secciones y todo termina del ancho del párrafo.

**Instalación:** pega `packages/core/components/reader.js` y después `packages/core/components/chapters.js`, completos dentro de
sendos `<script>` al final. El primero delega el índice cuando ve `.multipagina`; el segundo
mantiene `aria-current`, `aqui-visto` y `aqui-actual` únicamente en la página visible.
`examples/generated/chapters.html` contiene la receta completa con ambos guiones y el CSS incrustados.

**Límite:** no carga páginas por red ni implementa un router de aplicación. Un enlace de
capítulo usa su ID (`#p2`); los enlaces a secciones son internos a la página ya abierta.
Sin JS sólo se ve el primer capítulo en pantalla; imprime todos los capítulos. No combines
`por-seccion` con `multipagina`. Cada ID y cada `data-ir` debe ser único y corresponderse.

El botón activo lleva `aria-current="page"`; el hash conserva la página abierta, así que un enlace
a un capítulo concreto funciona. Al cambiar de página se emite `nota:pagina` por si hay que
arrancar un lienzo o recalcular una figura.
