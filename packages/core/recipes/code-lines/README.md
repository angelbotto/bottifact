## Código numerado y líneas destacadas

<!-- nota:ejemplo codigo-lineas -->
```html
{{EXAMPLE}}
```

**Cuándo:** explicar una sección precisa de código, manteniendo lectura completa. packages/core/components/code.js colorea el bloque y data-destacar admite números o intervalos, por ejemplo 3,6-8. El icono usa data-copiar y conserva nombre accesible y estado de resultado.

**Límite:** resaltado léxico, no un compilador ni editor. Esta variante parte de texto plano dentro de code: no añadas marcado manual a data-lineas. La numeración se dibuja con CSS y no entra en textContent ni en la copia. No atenúa las líneas no destacadas; todas conservan contraste. Código ancho se desplaza localmente.
