# Componentes de Bottifact

Para **nuevos artefactos**, escribe contenido con estas recetas y usa el generador de
[docs/artifact-contract.md](artifact-contract.md): incorpora la llave sol/luna, comentarios, sonido y ayudas de lectura.
No reconstruyas esa base copiando el esqueleto histórico de abajo. Cada receta indica sus
módulos; el generador los detecta e incrusta junto con `packages/core/styles/fonts.css` y `packages/core/styles/artifact.css` completos.
Las piezas no requieren React ni clases de Tailwind.

Para empezar por una pieza: [gráficas](#recetas-graficas),
[calor](#recetas-calor), [tablas](#recetas-tablas),
[sonido](#recetas-sonido), [escritura](#recetas-escritura),
[Three.js](#recetas-three). `examples/generated/template.html` es el catálogo ejecutable;
`examples/generated/chapters.html` muestra capítulos completos. Las recetas marcadas son sus fuentes.
