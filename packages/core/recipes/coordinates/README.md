## Three.js: dispersión XYZ

Usa **una sola** inclusión externa para toda la nota (compartida con `NotaGlobo`):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js"></script>
```

Después pega [packages/core/components/scene.js](../packages/core/components/scene.js) completo dentro de `<script>`, una vez, al final.
No necesita `packages/core/components/globe.js`, `packages/core/components/charts.js`, controles externos ni importaciones adicionales.

<!-- nota:ejemplo xyz -->
```html
{{EXAMPLE}}
```

**Cuándo:** la tercera variable aporta una relación espacial que conviene explorar. Los
controles giran la vista e identifican registros sin depender de arrastrar ni acertar a un punto.
Si dos variables bastan, la dispersión SVG es más fácil de leer y comparar.

**Límite:** 1–100 registros finitos; sin ausencias, regresión, jitter ni inferencias de
correlación. Cada eje tiene dominio propio, por lo que distancia geométrica no equivale
a una métrica entre variables de unidades distintas. Los puntos pueden ocluirse: elegir
uno atenúa los demás y escribe su valor. El lienzo conserva 600 px de ancho mínimo con
scroll local; las etiquetas de ejes deben ser breves, con las unidades en las cabeceras.
La tabla siempre queda visible, con o sin WebGL. Ningún dato existe sólo en una textura.
