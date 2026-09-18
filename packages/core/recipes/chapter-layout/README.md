## Chapter layout

<!-- nota:ejemplo multipagina -->

```html
{{EXAMPLE}}
```

**Use and limits:** Use separate chapters when each has its own reading task and contents. Put the grid on `.pagina`, never combine `por-seccion` with `multipagina`. Load reader then chapters once. Active navigation uses `aria-current=page`; hashes identify chapters and `nota:pagina` announces changes. IDs and `data-ir` targets must match. This is local navigation, not a network router. Historical chapter layouts show only the first chapter without JavaScript; print includes all chapters. The standard contract provides its own no-JavaScript fallback.
