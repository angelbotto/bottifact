## Sparkline

<!-- nota:ejemplo sparkline -->

```html
{{EXAMPLE}}
```

<a id="recetas-sonido"></a>

**Use and limits:** Add a trend without separating it from its record. Keep all values in text; the SVG is redundant and aria-hidden. X is equally spaced and all rows must use the same periods. Declare shared `data-min`/`data-max`; out-of-range points are rejected. No per-row autoscaling or irregular-time encoding. Text remains when rendering fails.
