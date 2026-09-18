## Tabla de totales y ordenación

<!-- nota:ejemplo totales -->
```html
{{EXAMPLE}}
```

**Cuándo:** consultar registros y su total aditivo; ofrece ordenación cuando ayuda a encontrar extremos. Sin `data-tabla` funciona como tabla estática.

**Límite:** el total lo calcula quien prepara los datos, no el DOM. No sumar porcentajes, tasas o promedios. Un solo `tbody`, sin celdas combinadas ni filas de subtotal dentro de él; no hay paginación o filtrado. La ordenación numérica requiere `data-valor`; ausencias quedan al final en ambos sentidos. Repetidos conservan su orden, `tfoot` no se mueve.
