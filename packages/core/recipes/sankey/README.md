## Flujos Sankey

<!-- nota:ejemplo sankey -->
```html
{{EXAMPLE}}
```

**Cuándo:** Comparar cómo se distribuye una magnitud entre orígenes y destinos. El grosor representa el valor con una escala compartida; el selector revela valor y participación.

**Cuándo no y límite:** 1–24 conexiones, hasta ocho nodos por columna, valores no negativos y total positivo. Esta versión es de dos columnas: no admite etapas intermedias, ciclos, cantidades negativas o monedas mezcladas. Nodos calculados desde sus conexiones, cero sin grosor. No ordena para minimizar cruces; usa la tabla cuando haya demasiados. Referencia conceptual: https://github.com/d3/d3-sankey ; implementación local sin D3 ni descarga.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
