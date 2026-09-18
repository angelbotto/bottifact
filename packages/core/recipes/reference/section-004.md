## Avisos con círculo

```html
<aside class="aviso ojo" aria-label="Aviso 1: condición">
  <span class="num">1</span>
  <div><p class="titulo">La medición todavía es parcial.</p>
    <p>Falta el volumen de una sede; el total no representa toda la operación.</p></div>
</aside>
<aside class="aviso bien" aria-label="Aviso 2: resultado">
  <span class="num">2</span>
  <div><p class="titulo">La fuente está identificada.</p>
    <p>El registro incluye la fecha de corte y la unidad de cada cifra.</p></div>
</aside>
<aside class="aviso mal" aria-label="Aviso 3: error">
  <span class="num">3</span>
  <div><p class="titulo">El archivo no se pudo leer.</p>
    <p>La última medición válida sigue disponible en el registro.</p></div>
</aside>
<aside class="aviso cita">
  <span class="num" aria-hidden="true">↳</span>
  <div><blockquote>Dejar una buena nota es dejar contexto.</blockquote>
    <p class="secundario">Principio de esta plantilla</p></div>
</aside>
```

**Cuándo:** condiciones, errores, confirmaciones o citas breves. Omite la variante para una nota
informativa azul. Círculo `28px`, dos columnas `30px minmax(0,1fr)`, borde izquierdo `3px`;
el número pertenece al flujo y no invade un margen. No uses `role="alert"` para avisos estáticos.
El original usa símbolos dentro de un círculo; la numeración es la adaptación pedida por Angel.
