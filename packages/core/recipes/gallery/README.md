## Galería deslizable

<!-- nota:ejemplo galeria -->
```html
{{EXAMPLE}}
```

**Cuándo:** mostrar fotografías, capturas, evidencia de campo o etapas visuales. La variante `galeria-fotografica` usa desplazamiento nativo con ratón/trackpad, tacto o flechas del teclado tras enfocar la región. Sin encabezado interno, botones ni avance automático; pies breves dentro de la imagen, degradado completo, contorno tenue y sombra. Ratón: cursor grab y arrastre con captura de puntero; tacto conserva scroll nativo. Las esquinas usan superellipse(1.6) con radio 28px, como /work; si el navegador no admite esa curva, el radio circular baja a 18px. packages/core/components/editorial-pieces.js anuncia la posición; sin JS se puede recorrer igualmente. Las galerías anteriores con controles siguen funcionando.

**Límite:** no autoavanza, no amplía imágenes ni emula un visor 360°. Las muestras son ilustraciones, no fotografías reales de Angel. Imágenes data: URI y alt; no enlazar carátulas o fotos remotas. Recorta visualmente con object-fit:cover: para capturas cuyo borde importa usa contain. Los pies breves se superponen en una fila de rejilla y pueden crecer sin recortarse; una explicación extensa pertenece fuera de la imagen. El degradado ocupa la imagen completa, no una banda negra detrás del pie. No hay movimiento programado en esta variante. Movimiento reducido cancela el desplazamiento suave de los controles antiguos. init/get/destroy permite añadir o retirar el componente.
