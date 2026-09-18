## Caja y bigotes de entrega

<!-- nota:ejemplo caja -->
```html
{{EXAMPLE}}
```

**Cuándo:** comparar dispersión y mediana por zona, sin dejar que el promedio esconda colas largas. Para conteos por intervalo, usa distribución.

**Límite:** Incluye packages/core/components/analytics.js. Recibe cinco estadísticas ordenadas por fila; no calcula cuartiles desde datos crudos ni identifica atípicos. Hasta 24 grupos. Misma unidad y método de cálculo; si mínimo = máximo, amplía el dominio un punto a cada lado para hacer visible el caso constante.
