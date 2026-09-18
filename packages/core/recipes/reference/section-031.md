## Límites de las piezas editoriales base

Estas condiciones complementan el HTML y el criterio de cada receta anterior. No cambian
las clases existentes; ayudan a elegir una pieza antes de copiarla.

| Pieza | Cuándo no usarla / qué no hace / qué puede romperla |
|---|---|
| Documento y temas | No reemplaza un formato solicitado distinto de HTML. Un solo selector y `data-theme` en la raíz; mezclar CSS parciales puede dejar tokens sin definir. |
| `.marca` | No señalar un párrafo entero ni expresar un estado sólo con el trazo. No transforma texto en enlace ni dibuja escritura animada. |
| `.con-margen` / `.margen` / `.nota` | No esconder una condición crítica al margen. Varias páginas de texto manuscrito desbordan el propósito de la anotación; el bloque base de margen es hijo directo de `.hoja`. |
| `.aviso` ×4 | No asignar urgencia a todos los párrafos. Una numeración no implica pasos ejecutables; para alertas dinámicas se necesita gestionar el anuncio sin duplicarlo. |
| `.mapa` | No negativos, ausencias ni datos nuevos con proporciones viejas. Esta receta fija sólo representa 60/25/15; usa barras si no vas a recalcular la rejilla. |
| `.dato` / `.datos` / `.pildora` | No falsear controles ni eliminar unidades para que quepan. No calculan ni validan datos; el texto debe incluir el estado además del color. |
| `.medida` | No representar una tarea en ejecución: usa `progress` para eso. `min/max/value`, porcentaje y texto deben describir el mismo denominador. |
| `.indice` / `.regla` | No en una nota breve. IDs duplicados, destinos inexistentes o falta de `data-lectura` rompen seguimiento; el tachado indica posición, no lectura demostrada. |
| `.codigo` | No sustituye un editor ni ejecuta código. Portapapeles puede estar denegado; conserva selección manual y estado. Resaltado escrito a mano, no detección automática de sintaxis. |
| `.tabla-caja` / `.densa` | No grandes bases de datos virtualizadas. Cinco o más columnas usan `densa`; alterar mínimos sin verificar 320/390 puede comprimir las celdas. |
| `.terminal` | No usar para una tabla analítica que necesite ordenar o cabeceras semánticas. Sólo copia texto, no ejecuta comandos. Las columnas dependen de mono y espacios; el ancho se desplaza dentro del `pre`. |
| `.extracto` | No degradar datos críticos ni aplicar máscara al único ejemplar del texto. La copia decorativa debe ser `aria-hidden`; la versión completa vive en `details`. |
| `.kept` | No envoltorio universal para el informe. No carga portadas ni convierte tarjetas en enlaces; añade un `a` real si hay navegación y datos de imagen incrustados. |
| `.manuscrita` / `.senalado` | No instrucciones críticas ni frases llenas de corchetes. Sin atributos es tipografía estática y seleccionable. Para texto breve animado usa `data-mano` con `packages/core/components/handwriting.js`; para paths propios usa `NotaEscritura`. |
| `NotaGlobo` | No topografía, fronteras políticas ni distancias medidas. Una instancia por contenedor, IDs de puntos/rutas únicos; `destroy()` al retirarlo. Sin Three/WebGL conserva lista y mensaje. |
