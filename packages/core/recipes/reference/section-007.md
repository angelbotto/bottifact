## Reading outline and progress ruler

Use for a document with multiple sections. At 1200px, `lectura-guiada` reserves 200px left and 76px right, with a 160px outline and a 44px ruler. Below that, the outline is in flow and progress is compact. Previous sections are struck through to indicate position, not proof of reading. The ruler supports click, arrows, PageUp/Down and Home/End. Keep IDs unique; never announce every scroll through aria-live.

For chapters, use `hoja multipagina lectura-guiada`, `data-lectura data-progreso-pagina`, one outline per `.pagina`, and one ruler after main. Add `data-historial data-enlaces-internos` for deep links. Load chapters after reader. Progress tracks the visible chapter and excludes footer/pagination. Without JS, navigation remains available. Print removes controls. The older non-guided layout retains its 1600px threshold.

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
