## Apuntes a izquierda y derecha

<!-- nota:ejemplo apuntes -->
```html
{{EXAMPLE}}
```

**Cuándo:** preguntas o comentarios editoriales secundarios junto al argumento. Incluye packages/core/components/handwriting.js.
La variante izquierda sitúa el apunte antes del texto en el espacio; el orden de lectura mantiene
primero el argumento. El subrayado usa un path propio y comparte entrada y cancelación.
El botón de repetición flota sobre el corchete, sin añadir altura. Con ratón aparece al pasar
por la nota; también al enfocar por teclado. En táctil queda visible. Escritura, subrayado y
tachado comienzan una vez, al entrar un 30 % de la caja en pantalla, no al cargar fuera de vista.
Salir completa el gesto y detiene el sonido; volver no lo repite automáticamente.
`<del data-subrayar="tachado">texto anterior</del>` dibuja el trazo a media altura y conserva
la semántica de corrección. `.tachado` sigue siendo la variante estática anterior.

**Límite:** se reserva una rejilla real dentro de la figura ancha; no son offsets negativos ni
notas fijas que invadan el índice. Bajo 1000 px, los apuntes caen después del párrafo. Frases cortas
y subrayados que quepan en una línea; no para anotaciones largas ni contenido obligatorio. El
alfabeto admite la puntuación española; el texto equivalente siempre se conserva. Sonido optativo sincronizado con el trazo visible tras activar Sonidos; también al repetir. La API y los límites de packages/core/components/handwriting.js son los de la receta manuscrita.
