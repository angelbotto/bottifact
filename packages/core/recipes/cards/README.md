## Familia de cards

<!-- nota:ejemplo cards -->
```html
{{EXAMPLE}}
```

**Cuándo:** Agrupar entidades distintas: artículo, indicador y proyecto. La rejilla se adapta al ancho; el enlace está en el título o acción, no en toda la tarjeta.

**Cuándo no / límite:** No uses una tarjeta por párrafo ni escondas una comparación que necesita tabla. Los valores y estados requieren fuente. No hay clics superpuestos, carrusel ni alturas fijas que corten textos. HTML estático con tokens de las seis paletas.

### Pegar un prototipo propio

El visor ofrece **Embeber mi HTML** y `NotaVisores.get(elemento).loadHTML(texto)`. Conserva el ancho elegido y Reiniciar vuelve al template original. Acepta hasta 100.000 caracteres de HTML declarativo con CSS local; rechaza scripts, eventos inline, iframes, envíos, recursos externos y CSS con url()/@import. No es un navegador remoto ni un sanitizador para contenido hostil. Usa HTML de confianza, imágenes raster data: y consultas @container para adaptar el prototipo a su ancho. No modifica ni guarda la fuente del documento.
