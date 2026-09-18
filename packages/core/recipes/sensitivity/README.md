## Sensibilidad de escenarios

<!-- nota:ejemplo sensibilidad -->
```html
{{EXAMPLE}}
```

**Cuándo:** Ver qué supuesto modifica más el resultado, con una base común y extremos A/B identificados por círculo/cuadrado. Seleccionar un supuesto muestra sus cambios absolutos.

**Cuándo no y límite:** 1–16 filas, un resultado base visible y dos resultados declarados por supuesto. Ordena por amplitud absoluta B−A; no presupone que A sea el menor resultado. No calcula un modelo financiero, probabilidades, interpolaciones o efectos conjuntos. El botón restablece la consulta, no modifica la tabla fuente.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
