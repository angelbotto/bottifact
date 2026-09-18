## Actividad con contexto editorial

<!-- nota:ejemplo actividad-editorial -->
```html
{{EXAMPLE}}
```

**Cuándo:** introducir actividad reciente con relato y conteos consultables. packages/core/components/editorial-pieces.js deriva las celdas, suma y escala desde la tabla; ratón, foco y clic muestran el contexto.

**Límite:** 1–52 períodos, conteos enteros 0–1.000.000. Tamaño igual por período, intensidad por cantidad; no área proporcional, ni mapa de calor de dos variables. No conecta GitHub ni atribuye productividad. Los intervalos positivos se calculan desde el máximo y se recortan al valor alcanzado; el cero tiene su propia muestra. Conserva tabla, unidad y fechas reales al adaptar. `data-actividad-tabla` nombra el ID de los datos, hermanos del marco: copia ambos bloques y cambia ambos IDs juntos. La tabla queda fuera de la figura y visible al imprimir. Sin ese atributo se conserva la compatibilidad con tablas dentro de la pieza. Un destino ausente muestra un error, nunca datos inventados.
