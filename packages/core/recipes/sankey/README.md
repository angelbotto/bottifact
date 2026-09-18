## Sankey

<!-- nota:ejemplo sankey -->

```html
{{EXAMPLE}}
```

**Use and limits:** Compare nonnegative flows with a common thickness scale. Two columns only, 1–24 connections, at most eight nodes per column and positive total. Nodes derive from connections; zero has no thickness. No intermediate stages, cycles, negative values, mixed currencies or crossing optimization. Use the table when dense. Conceptual reference: https://github.com/d3/d3-sankey ; the implementation is local and does not load D3. Source data stays in one table (or the image zone list). Declare data-unidad (1–40 characters); numeric magnitude is limited to 10^12. Views round to eight significant digits while source values remain. Load evidence.js; NotaEvidencia.init/get/destroy owns lifecycle. Destroy before changing the source. No network or external libraries; data remains if enhancement fails.
