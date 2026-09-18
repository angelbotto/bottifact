## Cohortes de recurrencia

<!-- nota:ejemplo cohortes -->
```html
{{EXAMPLE}}
```

**Cuándo:** Comparar recurrencia de grupos con distintas fechas de entrada. Cada celda muestra recuento, base y porcentaje; no convierte lo pendiente en cero.

**Cuándo no y límite:** 1–20 cohortes y 1–12 períodos con cabeceras de hasta 24 caracteres. Base entera positiva, recuentos enteros entre cero y la base. Las celdas con data-estado="pendiente" deben quedar al final de cada fila. No calcula cohortes desde eventos, ni compara meses de distinta definición. Cinco intensidades: [0,20), [20,40), [40,60), [60,80), [80,100] %. Los porcentajes exactos siempre se escriben.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
