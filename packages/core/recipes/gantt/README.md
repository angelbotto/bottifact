## Gantt editorial

<!-- nota:ejemplo gantt -->
```html
{{EXAMPLE}}
```

**Cuándo:** Explicar fechas, trabajo simultáneo, responsables y dependencias fin→inicio. El estado se escribe y lleva símbolo; nunca se infiere del día actual.

**Cuándo no y límite:** 1–24 tareas, IDs únicos ASCII de hasta 12 caracteres, fechas ISO válidas y rango máximo de diez años. Dependencias separadas por comas, «—» para ninguna. Rechaza ciclos, IDs inexistentes y dependencias cuyo fin supera el inicio dependiente. No es un planificador, no excluye festivos ni calcula ruta crítica. La duración es tiempo transcurrido, no conteo inclusivo de días laborables.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
