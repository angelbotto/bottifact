## Hand-drawn underline

Use `.marca` for a short decision-bearing phrase. Its two embedded SVG strokes have distinct curves; `box-decoration-break:clone` handles wrapping. Text remains selectable and retains its contrast. An underline does not replace a link, a status label or a heading.

```html
<p>El estado definitivo debe vivir en <span class="marca">un solo registro</span>.
  El <a href="#evidencia">detalle de la evidencia</a> se puede consultar después.</p>
```
