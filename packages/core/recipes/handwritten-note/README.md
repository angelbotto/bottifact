## Nota manuscrita señalada

<!-- nota:ejemplo manuscrita -->
```html
{{EXAMPLE}}
```

**Cuándo:** destacar una observación breve con escritura que aparece al llegar a ella. Incluye
packages/core/components/handwriting.js: `data-mano="fuente"` revela Reenie Beanie por caracteres, como cmrg.me; no sustituye
sus glifos por dibujos. Cada carácter aparece en 375 ms, escalonado para terminar con una
muestra original de lápiz de aproximadamente 2,18–3,03 s. El ejemplo se anima una vez al
entrar un 30 %; el botón permite repetirlo. `.manuscrita` sin atributo conserva texto estático.

**Límite:** notas breves, con fuente incrustada; no animar párrafos extensos ni información
crítica. Admite mayúsculas y puntuación de la fuente; palabras largas pueden partirse sin
comprimir letras. Texto equivalente completo para lectores y comentarios. Sin JS se lee completo.
Al salir, ocultar la pestaña o reducir movimiento se cancela la animación y se completa el texto.
No hay RAF. `data-escritura-sonora` reproduce una grabación original sólo tras activar Sonidos;
se corta al salir. No se normaliza, estira ni repite el audio. Sin el atributo permanece silenciosa.
La variante anterior `data-mano` sin valor sigue disponible con su alfabeto SVG y sus límites
(minúsculas, 240 caracteres, palabras de hasta 160 px). Para nuevas notas elige `fuente`.
`NotaMano.init/get/destroy` permite insertar o retirar la mejora preservando los nodos originales.
