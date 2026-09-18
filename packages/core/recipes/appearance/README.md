## Apariencia y lectura cómoda

<!-- nota:ejemplo apariencia -->
```html
{{EXAMPLE}}
```

**Cuándo:** un control discreto de lectura en la cabecera. El círculo sol/luna es la opción
principal; la etiqueta hace explícita su función y la cápsula muestra la preferencia elegida.
Copia un solo `details` en una nota. El ejemplo reúne tres variantes para compararlas.
La cabecera del catálogo reutiliza exactamente el primer control con IDs/nombres propios.

**Interacción:** Temas, Letras y Sonido son pestañas con flechas izquierda/derecha, Home y End.
Escape cierra y devuelve el foco a la llave; pulsar o enfocar fuera cierra. Un solo panel abierto.
Los radios conservan la selección; elegir una familia no cierra el panel para poder comparar.
Claro, Oscuro y Sistema son modos independientes: cambiar de familia mantiene el modo.
El tema actual se nombra arriba aunque un filtro lo oculte. Búsqueda sin tildes por nombre o
 descripción, categoría, contador y restablecimiento. Las muestras tienen scroll local con foco y nombre.
El silencio y volumen están sólo en Sonido. Sin JS el disclosure abre, pero los ajustes
no cambian el documento: no es una configuración persistida en el propio HTML.

**Tipografía:** seis combinaciones, independientes de los colores. Editorial: Instrument Serif / Geist;
Sobrio: Geist / Geist; Técnico: Geist Mono / Geist. Libro: Literata / Literata; Revista: Instrument Serif /
Literata; Bitácora: Geist Mono / Literata. El primer nombre corresponde a títulos y el segundo a lectura.
Literata normal e itálica, pesos 400–700, latín y latín extendido, están incrustados; OFL y procedencia en
`licenses/literata-OFL.txt` y `tests/evidence/literata-fonts.json`. Reenie Beanie sigue reservada a notas;
código y controles conservan sus familias. Instrument Serif es de títulos, no se usa como cuerpo largo.

**Cuándo no / límite:** no modifica prototipos ni emula preferencias del sistema. Los temas son opciones
predefinidas, no un editor de tokens ni una descarga de temas. Para ampliar, copia una etiqueta con radio,
muestra y `data-tema-familia`; define todos los tokens, registra su clave en packages/core/components/reader.js/contrato y
actualiza validación. La búsqueda descubre las etiquetas disponibles sin una lista de resultados duplicada.
No inserta controles dinámicamente. Cada copia necesita IDs, aria-controls, aria-labelledby y nombres de
radio únicos. Incluir packages/core/components/reader.js una vez. Tipografía puede cambiar altura y saltos: revisar contenido real.
Las preferencias se guardan por origen, o por archivo cuando hay presentación inicial; el silencio se comparte
por origen. Sin localStorage funcionan durante la sesión. Sin Web Audio se explica el fallo; habilitado no
significa que el navegador o dispositivo ya esté reproduciendo. El grano incrustado es independiente de la
paleta; se retira al imprimir. Lectura cómoda sigue siendo 18 px/1,7, sin comprimir datos.
