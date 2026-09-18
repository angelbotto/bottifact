## Velas financieras OHLC

<!-- nota:ejemplo velas -->
```html
{{EXAMPLE}}
```

**Cuándo:** mostrar apertura, extremos y cierre de un mismo período. No para saldos que no tengan apertura/cierre definidos ni para mezclar unidades.

**Límite:** Incluye packages/core/components/analytics.js. 1–60 fechas ISO únicas; mínimo ≤ apertura y cierre ≤ máximo. No calcula indicadores técnicos ni conecta mercados. Posiciones temporales reales; limita el número de observaciones para conservar cuerpos legibles. Si todo es constante, muestra un dominio auxiliar ±10 % o ±1 alrededor del valor.
