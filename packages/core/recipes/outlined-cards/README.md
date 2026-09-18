## Cards delineadas de publicaciones

<!-- nota:ejemplo cards-trazadas -->
```html
{{EXAMPLE}}
```

**Cuándo:** una rejilla editorial de artículos o documentos con bordes compartidos, fondo suave y
sombra breve al pasar el puntero. Cada card es un único enlace, también accesible por teclado.
Incluye packages/core/components/audio.js y Apariencia si quieres el hover sonoro optativo; el estilo no necesita JS.

**Límite:** títulos y extractos completos, sin elipsis ni alturas fijas. No mezcles botones dentro
del enlace. Hover sólo con ratón moviéndose realmente sobre `data-audio-hover`, después de activar
Sonidos; nunca al enfocar, desplazar o cargar. Señal propia de 60 ms y separación mínima de 160 ms;
reproduce el MP3 hover original incrustado, al nivel de referencia y con el volumen maestro. En móvil basta el enlace; sin sonido no se pierde información.
