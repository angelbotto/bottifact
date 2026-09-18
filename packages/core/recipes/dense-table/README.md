## Tablas densas

<!-- nota:ejemplo tabla-densa -->
```html
{{EXAMPLE}}
```

**Cuándo:** desde cinco columnas. `.tabla-caja table` ya trae `min-width: 34rem`; `densa` lo sube a
`58rem`. Sin ese mínimo la tabla no se desplaza, se comprime: medido a 390 px, seis columnas daban
celdas de 50 px y filas de **581 px de alto**. Con `densa`, celdas de 139–285 px y filas de 140 px.
El desplazamiento es local —la página nunca se mueve de lado— y la caja es alcanzable por teclado.
