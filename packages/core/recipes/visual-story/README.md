## Relato visual por pasos

<!-- nota:ejemplo relato-visual -->
```html
{{EXAMPLE}}
```

**Cuándo:** Acompañar un argumento con una figura compartida. El scroll selecciona el paso en escritorio; los botones y el selector permiten fijarlo manualmente.

**Cuándo no y límite:** 2–8 filas: nombre, magnitud no negativa y explicación breve (hasta 100 caracteres cada texto). Escala común con cero. En móvil la figura vuelve al flujo; cada paso conserva su dato escrito. No cambia cifras ni altera el scroll del lector. Sin JavaScript queda la tabla. No hace transiciones ni RAF; usa IntersectionObserver, que se desconecta al destruir la instancia.

**Datos comunes:** una sola tabla fuente; unidad en `data-unidad` de 1–40 caracteres (la imagen usa una lista de zonas). Valores finitos de magnitud máxima 10¹². La vista redondea a ocho cifras significativas y usa notación científica en extremos; la tabla conserva los valores originales.

**Dependencia:** packages/core/components/evidence.js. Inicializa con `NotaEvidencia.init(raíz)`, consulta con `NotaEvidencia.get(elemento)` y llama a `destroy()` antes de retirar la pieza o actualizar su fuente. No hace fetch ni carga bibliotecas externas. Los datos fuente permanecen disponibles si JavaScript falla.
