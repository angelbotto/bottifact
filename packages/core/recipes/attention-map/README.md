## Attention map de áreas

<!-- nota:ejemplo atencion -->
```html
{{EXAMPLE}}
```

**Cuándo:** ver cómo se reparte atención, tiempo o gasto entre partes de un total. Incluye packages/core/components/attention-map.js;
packages/core/components/audio.js ofrece hover optativo con el interruptor general. Este treemap recupera el tipo de mapa
de la referencia; `data-grafica="calor"` sigue disponible para intensidades en una matriz.

**Límite:** 1–40 categorías únicas, valores finitos no negativos de hasta 10⁹ y total positivo. Área
calculada con una partición binaria; no imita posiciones fijas ni soporta jerarquías. Cero no ocupa
área, pero sigue en la tabla y controles. Las celdas pequeñas muestran un número o sólo su área;
los nombres y valores completos se conservan fuera del mapa, sin elipsis. Para diferencias
pequeñas o un ranking preciso, usa barras. ViewBox de 1000×380, mínimo legible de 900 px con
scroll local. No mide productividad ni conecta aplicaciones. `NotaAtencion.init/get/destroy`
conserva la tabla original; destruye y reinicia tras cambiar sus datos. Tooltip al pasar el ratón,
al enfocar un control o al tocar una celda: valor, porcentaje, total y `data-contexto` optativo en
un texto de la fila (también visible en la tabla). Se puede mantener el puntero sobre el tooltip; Escape lo cierra. Los mismos datos
siguen disponibles en la tabla y selección. No añadas HTML ni información exclusiva al contexto.
