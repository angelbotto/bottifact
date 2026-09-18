## Biblioteca completa y registro local

[examples/generated/library.html](../examples/generated/library.html) reúne **44 recetas en nueve capítulos**: inicio,
publicaciones, artículos, reportes, gráficas, tablas, prototipos, espacio y gesto, y edición.
Cada pieza se genera desde el HTML anterior, con su criterio, límites y dependencias al lado.
El estudio narrativo sigue en [examples/generated/report.html](../examples/generated/report.html); el cuaderno continuo, en
[examples/generated/template.html](../examples/generated/template.html). Son tres composiciones del mismo sistema.

**Cuándo:** explorar y copiar piezas, evaluar temas con contenidos distintos o compartir
un componente concreto. `data-enlaces-internos` en `.hoja.multipagina` habilita enlaces a
IDs descendientes y su historial, por ejemplo `examples/generated/library.html#receta-calor`. Es optativo:
las notas anteriores conservan su contrato. La barra navega capítulos, no es un tablist. Cada capítulo conserva además su índice de secciones y la regla muestra su progreso; en portátil ambos disponen de espacio reservado.
El destino se muestra, recibe foco al navegar y queda fuera de la barra fija. Para enlazar
vistas de pestañas usa el ID de la receta, no un panel oculto de la pieza.

**Límite:** es una biblioteca HTML local, no un CMS ni un tema Ghost instalable. No crea
usuarios, comentarios, pagos o suscripciones. La búsqueda encuentra recetas locales y el
archivo filtra las publicaciones que ya contiene. Al imprimir se incluyen todos los capítulos;
la búsqueda y la configuración son controles de pantalla. Sin JS se muestran todos los
capítulos de esta edición, con los datos originales y las alternativas de cada componente.

[packages/core/registry/registry.json](../packages/core/registry/registry.json) contiene HTML, capítulo, dependencias y documentación de cada
receta. Es un formato local versionado, **no el esquema de instalación de shadcn**. No lo
cargues por fetch dentro de un artefacto. El ensamblador lo construye junto al HTML, sin red.
`NotaEditorial.init(raíz)` y `get(elemento).destroy()` permiten inicializar y desmontar archivo
/configurador. No anides archivos ni dupliques configuradores; los IDs de copiado son únicos.

La configuración de Ghost inspira la separación entre contenido y presentación. Una futura
integración necesita plantillas Handlebars, contexto del CMS, `package.json` y validación
GScan; copiar este HTML no cumple ese contrato. La comparación y sus fuentes están en
[edition-complete.md](../tests/evidence/edition-complete.md).
