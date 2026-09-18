## Informe de cuatro capítulos

El ejemplo [examples/generated/report.html](../examples/generated/report.html) reúne piezas existentes como una lectura coherente.
Los botones superiores son navegación de capítulos (`aria-current="page"`), no tabs ARIA;
las pestañas locales de Evidencia sí son un tablist. Cada capítulo sigue la rejilla multipágina.

<!-- nota:ejemplo informe -->
```html
{{EXAMPLE}}
```

**Cuándo:** un reporte con varias tareas de lectura: comprender la decisión, consultar datos,
probar una propuesta y revisar los próximos pasos. La cabecera conserva una firma editorial
compacta. Añade una sola llave de apariencia de su receta en `.edicion-acciones` si se necesita;
el ensamblador del ejemplo ya lo hace. No copies las tres variantes del control.

**Instalación:** `packages/core/components/reader.js`, `packages/core/components/chapters.js`, `packages/core/components/charts.js`, `packages/core/components/reports.js`, `packages/core/components/prototype.js`
y `packages/core/components/tabs.js`, incrustados al final; fuentes y CSS completos. Este ejemplo no necesita Three.
`data-historial` activa historial de capítulos para Atrás/Adelante; sin ese atributo sigue el
contrato anterior con replaceState. Los enlaces `#evidencia` y `#prototipo` abren esos capítulos.

**Cuándo no / límite:** no es un router ni carga HTML remoto. Los enlaces a secciones no abren
otros capítulos; comparte el ID del capítulo. Sin JS sólo se ve el primero en pantalla;
impresión incluye los cuatro. Si el informe es corto, usa página única. Para alternar sólo
vistas de una figura, usa la receta de pestañas. Los anchos grandes son hijos de `.pagina`.
