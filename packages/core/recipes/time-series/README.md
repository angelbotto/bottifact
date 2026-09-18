## Serie temporal con variación

<!-- nota:ejemplo temporal -->
```html
{{EXAMPLE}}
```

**Cuándo:** comparar observaciones fechadas. La posición usa milisegundos UTC: dos días y cinco días no ocupan el mismo espacio. El delta compara los dos últimos registros y nombra ambos.

**Límite:** fechas ISO diarias válidas, únicas y crecientes; no agrega días ni corrige zonas horarias. El delta absoluto es actual − anterior y el relativo divide por |anterior|; base 0 indica porcentaje no definido, ausente indica sin comparación. Si tus registros representan ventanas, deben tener duración/composición comparables. No infiere causalidad ni si subir es bueno.
