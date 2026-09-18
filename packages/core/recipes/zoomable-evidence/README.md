## Evidencia ampliable

<!-- nota:ejemplo evidencia-ampliable -->
```html
{{EXAMPLE}}
```

**Cuándo:** Examinar una captura con zoom y puntos numerados. Los controles +/−/ajustar amplían de 100 a 400 %, y cada punto puede seleccionarse con teclado o desde el selector.

**Cuándo no y límite:** Una imagen data: y 1–12 zonas con data-x/data-y porcentuales de 0 a 100, texto de hasta 100 caracteres. La lista conserva el contexto y el original se imprime. Desplazamiento local en ambos ejes; no cambia la resolución del archivo ni aplica reconocimiento de texto. Las zonas cercanas pueden solaparse: el selector y la lista permiten consultar todas. Coloca los puntos junto al dato para no taparlo. No sustituye comentarios: las zonas son anotaciones del autor, la burbuja común recoge la revisión del lector.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
