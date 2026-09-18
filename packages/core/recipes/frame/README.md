## Marco de líneas desvanecidas

<!-- nota:ejemplo marco -->
```html
{{EXAMPLE}}
```

**Cuándo:** enmarcar una composición de cards, una estantería o una invitación. `marco-difuso`
reserva entre 12 y 32 px dentro de su caja para prolongar las líneas sin desbordar la página.
Puedes añadirlo a una rejilla existente como `cards-trazadas cards-abiertas marco-difuso`.

**Límite:** el desvanecido sólo afecta a dos pseudoelementos decorativos. No borra texto, no
reemplaza foco ni bordes que comuniquen estado. No combinar con componentes que ya usen ambos
pseudoelementos; envuélvelos dentro de la caja. Sin máscaras se conserva el marco discontinuo.
Es una adaptación con espacio reservado, no los márgenes negativos de la referencia.
