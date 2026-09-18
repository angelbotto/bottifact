## Escritura: trazo a trazo

Pega [packages/core/components/writing.js](../packages/core/components/writing.js) una vez al final. La frase de ejemplo está dibujada con
paths originales; la animación recorre **su longitud**, no un rectángulo que descubre texto.

<!-- nota:ejemplo escritura -->
```html
{{EXAMPLE}}
```

**Cuándo:** una anotación corta y secundaria que gana significado con el gesto del trazo.
Con `data-al-ver` se escribe una vez al entrar al menos un 30 % de su caja en pantalla; sin ese atributo empieza completa y la persona decide repetirla. En la base estándar el sonido está habilitado y espera un primer clic real; si estaba silenciado, actívalo en Apariencia. En un canal independiente pulsa Activar sonido y después Repetir escritura. Con `data-escritura-sonora`, y sólo después de que un clic habilite el contexto de audio, el lápiz acompaña la animación al entrar y se detiene al salir. Sin el atributo la entrada es silenciosa. Incluye `packages/core/components/audio.js` con Apariencia para el sonido de lápiz; si copias la escritura sola, `packages/core/components/sound.js` ofrece el mismo gesto de lápiz desde su botón local. El acceso «Ver escritura animada» aparece sólo en documentos que incluyen un trazo. Conserva `.manuscrita` para texto corriente
que deba seleccionarse, traducirse o cambiar con datos.

**Límite:** recibe paths SVG ordenados, no transforma automáticamente cualquier fuente
en escritura cursiva. Cada path es un trazo continuo; separa levantamientos de lápiz en
paths distintos. No uses contornos de glifos rellenos si esperas un trazo central de pluma.
Al cambiar la frase, dibuja paths correspondientes y actualiza `data-texto-escritura`.
El SVG es redundante (`aria-hidden`), el texto equivalente es permanente. Admite 100–10000 ms,
no música sincronizada. Web Animations se cancela y completa al salir de pantalla, ocultar
la pestaña o activar movimiento reducido; no hay RAF ni colas que se reanuden al volver. La entrada automática ocurre una sola vez por instancia; Repetir permite verla de nuevo.
`NotaEscritura.get(elemento).play()`, `.finish()` y `.destroy()` controlan la instancia;
`.play()` respeta movimiento reducido. `NotaEscritura.init(elemento)` admite inserción tardía.

<a id="recetas-three"></a>
