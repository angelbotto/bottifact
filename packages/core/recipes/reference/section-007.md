## Índice lateral y regla de lectura

Patrón por defecto para nuevos artefactos de Angel con varias secciones. Pega `packages/core/styles/fonts.css` y
`packages/core/styles/artifact.css` inline, este HTML y `packages/core/components/reader.js` una vez al final.

```html
<main class="hoja lectura-guiada" data-lectura lang="es">
  <header class="cabecera"><p class="ceja">Informe</p><h1>Una decisión con evidencia</h1></header>
  <nav class="indice" tabindex="0" aria-label="Índice del documento">
    <p class="ceja">En esta nota</p>
    <ol><li><a href="#criterio">El criterio</a></li>
        <li><a href="#evidencia">La evidencia</a></li></ol>
  </nav>
  <section class="seccion" id="criterio"><h2>El criterio</h2><p>Qué necesitamos resolver.</p></section>
  <section class="seccion" id="evidencia"><h2>La evidencia</h2><p>Qué sostiene la decisión.</p></section>
</main>
<div class="regla regla-guiada" role="slider" tabindex="0" aria-orientation="horizontal"
     aria-label="Progreso de lectura" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
  <div class="ticks"></div><div class="cursor"></div><span class="val">0%</span>
</div>
```

**Cuándo:** orientar un documento de varias secciones. Desde 1200 px, `lectura-guiada` reserva
200 px a la izquierda y 76 px a la derecha; el índice fijo mide 160 px y la regla 44 px.
Son decisiones de esta variante, no medidas de cmrg. Figuras y texto siguen calculando sus
anchos dentro del espacio disponible. Debajo, el índice se lee en el flujo y el progreso aparece
como control compacto en la esquina inferior izquierda; no tapa el control de comentarios.
El índice marca la sección actual y tacha las anteriores. El tachado indica posición, no prueba de lectura.
La regla admite clic, flechas, PageUp/Down y Home/End; actualiza su orientación accesible al cambiar de tamaño.

**Multipágina:** conserva las pestañas y añade un `nav.indice` dentro de cada `.pagina`, con enlaces
sólo a sus secciones. El contenedor usa `class="hoja multipagina lectura-guiada" data-lectura data-progreso-pagina`.
Para enlaces profundos con historial añade `data-historial data-enlaces-internos`, como en la biblioteca.
Coloca una sola `.regla.regla-guiada` después de `main`. Incluye `packages/core/components/chapters.js` después de
`packages/core/components/reader.js`. El porcentaje corresponde al capítulo visible, excluye el pie y la paginación,
y se recalcula al cambiar de capítulo o abrir contenido. Si un capítulo cabe completo, indica 100 % al quedar visible entero.

**Cuándo no / límite:** una pieza aislada sin secciones no necesita un índice vacío. Los enlaces
exigen IDs únicos y existentes; no añadas `aria-live` al porcentaje porque anunciaría cada scroll.
No anides los componentes anchos dentro del índice ni alteres sus contenedores de rejilla.
El HTML funciona como navegación sin JS; el seguimiento y el porcentaje requieren el módulo.
Al imprimir se ocultan controles y se recupera el ancho. El patrón anterior `.hoja` + `.indice` +
`.regla`, sin las nuevas clases, conserva su comportamiento y el umbral de 1600 px.
