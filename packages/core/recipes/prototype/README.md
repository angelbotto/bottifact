## Visor de prototipos con estados

<!-- nota:ejemplo visor -->
```html
{{EXAMPLE}}
```

**Cuándo:** documentar estados de un componente o recorrer un prototipo pequeño dentro de un
artículo. El lienzo cambia entre 320, 390, 768, 1024 y el espacio disponible. Reiniciar reconstruye
la muestra original. El menú de dispositivo elige el ancho; la proporción fija la altura del marco, Rotar intercambia sus dimensiones y Ajustar escala la vista para caber. El estado muestra dimensiones CSS y porcentaje visual. Incluye `packages/core/components/controls.js` y `packages/core/components/prototype.js`. El texto alternativo aparece sin JS y al imprimir. No carga archivos.

**Cuándo no / límite:** no es un emulador de iPhone, una captura ni un navegador remoto. No
modifica la densidad de píxeles, el motor o el viewport del documento. Usa **Shadow DOM y
`@container`**, por eso las reglas responsivas del prototipo deben consultar el contenedor;
`@media (width)` seguiría midiendo la ventana exterior. No hay iframe porque la CSP lo bloquea.
El template contiene HTML/CSS de confianza, sin guiones ni manejadores `on…`; no es un sandbox
para HTML ajeno. Los botones `data-demo-ir` activan un `data-demo-pagina` del mismo visor;
no envían formularios, calculan datos ni persisten cambios. Los IDs, si se usan, viven dentro
del shadow. Los estilos del documento no entran, pero sí se heredan sus tokens y fuentes.
El contenido del prototipo debe respetar reduce; el visor no inicia RAF ni transiciones.
`NotaVisores.get(figura).setWidth('768')` permite controlar el ancho; `setAspect('9/16')` fija la proporción (`auto`, `9/16`, `4/3`, `16/9`, `1/1`). Ajustar reduce visualmente también los textos: usa 100 % para valorar legibilidad. `reset()` reinicia y
`destroy()` devuelve la alternativa textual y retira listeners/observer.
