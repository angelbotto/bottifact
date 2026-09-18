## Navegación editorial con separadores

<!-- nota:ejemplo navegacion -->
```html
{{EXAMPLE}}
```

**Cuándo:** cabecera discreta para un blog o informe. Enlaces ordinarios para documentos; para
capítulos dinámicos la biblioteca usa `barra capitulos navegacion-editorial`, botones `data-ir`
y una región `data-capitulos-scroll` para desplazar sólo la navegación. Apariencia queda fuera.

**Límite:** conservar índice y regla de lectura en documentos largos. No mezclar múltiples barras
`data-ir` en un mismo documento. El separador es decorativo; cada enlace tiene un nombre propio.
La variante no modifica las barras antiguas. Bajo 700 px, los capítulos pasan a una segunda fila.
