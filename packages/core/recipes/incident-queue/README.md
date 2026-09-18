## Cola de despacho y novedades

<!-- nota:ejemplo cola-novedades -->
```html
{{EXAMPLE}}
```

**Cuándo:** Filtrar vehículos con novedad, agrupar por ciudad y ordenar pedidos para revisar la operación. Reutiliza el explorador tabular, con datos de logística. `data-unidad="pedidos"` nombra el total; sin ese atributo el explorador conserva COP para los ejemplos financieros existentes.

**Límite:** Incluye packages/core/components/controls.js y packages/core/components/data-explorer.js además de la base. Corte estático con las mismas cifras iniciales del ejemplo de flota; la simulación no modifica esta tabla. Buscar/filtrar/agrupar no asigna conductores ni envía mensajes. No calcula prioridad automáticamente. Identificar novedad, responsable y siguiente acción en una implementación operativa real. destroy/init del explorador permite sustituir el corte; no hay suscripción en vivo.
