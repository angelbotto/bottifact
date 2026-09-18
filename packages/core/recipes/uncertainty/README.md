## Rangos de incertidumbre

<!-- nota:ejemplo incertidumbre -->
```html
{{EXAMPLE}}
```

**Cuándo:** Mostrar una trayectoria central junto con límites explícitos. La banda acompaña los datos; los bordes discontinuos y la línea central se distinguen también por trazo.

**Cuándo no y límite:** 2–48 fechas ISO estrictamente crecientes; inferior ≤ central ≤ superior, todos finitos. Exige un texto visible data-evidencia-metodo. El dominio vertical alcanza los extremos reales; no requiere cero porque representa una serie. No estima confianza, imputa huecos ni genera escenarios: recibe valores ya justificados por el autor.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
