## Áreas apiladas de ingresos

<!-- nota:ejemplo areas -->
```html
{{EXAMPLE}}
```

**Cuándo:** ver el total y su composición a lo largo del tiempo. Para comparar el crecimiento exacto de una banda intermedia, usa líneas o pequeños múltiples.

**Límite:** Incluye packages/core/components/analytics.js. Exactamente tres series aditivas en la misma unidad, 2–60 fechas ISO únicas, valores no negativos. Une observaciones por interpolación lineal; no agrega transacciones ni inventa días faltantes. Las fechas usan distancia real; no mezcla monedas. Un total constantemente cero usa dominio auxiliar 0–1 explícito.
