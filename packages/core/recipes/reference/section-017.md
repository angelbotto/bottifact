## Evidence modules

Each visualization uses its HTML table as the source of truth. Embed complete fonts/styles and each necessary script once: charts.js for charts/heatmaps and tables.js for sorting/sparklines. These modules are independent of Three. `NotaGraficas.init(root)` and `NotaTablas.init(root)` are idempotent; get(element).destroy() restores the original markup. Destroy, edit source data, then initialize again. No network or framework is required.

Keep wide figures as direct children of `.hoja` or `.pagina`, using por-seccion for nested sections. `data-valor` uses decimal points without thousands separators. Empty means missing; zero is a measured zero. Visible text includes units. Scales include extremes; missing records are not summed or interpolated. Straight line segments between observations do not imply additional measurements. Exact values remain available in the table.

<a id="recetas-graficas"></a>
