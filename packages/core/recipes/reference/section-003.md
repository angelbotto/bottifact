## Handwritten note and bracket

Use a margin note for a complementary perspective, never for a critical condition. The paragraph occupies the central grid cell; from 1184px the note occupies a real cell on the right and below that it follows the paragraph. Reenie Beanie supplies the annotation typography; only bracket decorations use absolute positioning. Use the margin-notes recipe for left/right animated variants.

```html
<div class="con-margen">
  <p>El dato necesita unidad, fecha y origen. Mientras se confirma, debe decir
    <span class="dato">pendiente de medir</span>.</p>
  <aside class="margen" aria-label="Nota al margen">
    ¿se entiende sin estar en la reunión?
  </aside>
</div>
<p class="nota">una buena nota le ahorra contexto a la siguiente persona</p>
```
