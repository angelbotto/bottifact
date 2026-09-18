## Avisos con icono animado

<!-- nota:ejemplo avisos-animados -->
```html
{{EXAMPLE}}
```

**Cuándo:** señalar una precaución o contexto breve dentro de un artículo. La variante aviso-esquina reserva espacio al icono; packages/core/components/editorial-pieces.js añade dos pulsos al entrar, y permite repetir al pasar el ratón o enfocar contenido interior. También admite las variantes ojo y bien existentes.

**Límite:** la lectura no depende del pulso. Son 2 ciclos de 1000 ms; se cancela al salir, ocultar la pestaña, reducir movimiento o destruir la instancia. No usa RAF ni sonido. No uses role=alert para avisos estáticos: evita anuncios automáticos innecesarios. El componente original aviso conserva su forma.
