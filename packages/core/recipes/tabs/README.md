## Pestañas dentro de una pieza

<!-- nota:ejemplo pestanas -->
```html
{{EXAMPLE}}
```

**Cuándo:** alternar vistas cortas de una misma pregunta: hallazgo/evidencia/límite, diseño/datos
u otras vistas relacionadas. Incluye `packages/core/components/tabs.js` después de `packages/core/components/reader.js`.
Flechas, Inicio y Fin mueven el foco; Enter o Espacio activan (comportamiento nativo del botón).
El ratón activa al pulsar. Hay un solo tabulador activo; cada panel tiene nombre y foco.

**Cuándo no / límite:** no uses pestañas para ocultar pasos obligatorios o avisos esenciales.
Para capítulos largos usa navegación multipágina. No carga datos, no sincroniza la URL, no
ofrece pestañas deshabilitadas ni persistencia. Mantén botones y paneles en el mismo orden,
con IDs únicos. No anides instancias. Sin JS se ven todas las secciones; al imprimir también.
`NotaPestanas.init(raíz)`, `get(elemento).select(índice)` y `destroy()` siguen el ciclo habitual.
`select` no mueve foco; se emite `nota:pestana` al cambiar para que otras piezas puedan medir.
