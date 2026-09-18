## Embudo explicado

<!-- nota:ejemplo embudo -->
```html
{{EXAMPLE}}
```

**Cuándo:** Mostrar volumen, conversión y abandono entre etapas de una misma población. Barras desde cero permiten comparar recuentos; el selector explica denominadores.

**Cuándo no y límite:** 2–12 etapas, recuentos enteros no crecientes y primera etapa positiva. Desde una etapa con cero, la conversión siguiente no se define. No acepta poblaciones distintas, reingresos o valores negativos; en esos casos usa estados o flujos. No atribuye la caída a una causa que no esté medida.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
