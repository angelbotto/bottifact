## Document and themes — legacy compatibility

This skeleton explains older documents with a simple selector. Use the artifact contract for new documents: this historical shell omits current controls. Replace embedding comments with complete local files, not remote dependencies. Use `.amplio` instead of `.ancho` for a wider figure; do not widen the entire reading column.

```html
<title>Nota — decisión y evidencia</title>
<meta charset="utf-8">
<style>/* Pegar aquí packages/core/styles/fonts.css y packages/core/styles/artifact.css completos, incluidas las licencias */</style>
<meta name="viewport" content="width=device-width, initial-scale=1">
<a class="salto" href="#contenido">Saltar al contenido</a>
<main class="hoja" data-lectura lang="es">
  <div class="herramientas">
    <span class="firma-editorial"><span>Margen</span><small>Cuadernos</small></span>
    <div class="temas">
      <label for="tema">Papel</label>
      <select id="tema" data-tema>
        <option value="system">Sistema</option>
        <option value="light">Claro</option>
        <option value="dark">Oscuro cálido</option>
        <option value="sea">Dark Sea</option>
      </select>
    </div>
  </div>
  <header class="cabecera" id="contenido" tabindex="-1">
    <p class="ceja">Decisión / septiembre 2026</p>
    <h1>Una fuente de verdad.</h1>
    <p class="bajada">Registrar el movimiento una vez y conservar su trazabilidad.</p>
  </header>
  <!-- Secciones y figuras como hermanos; ver los bloques siguientes. -->
</main>
<script>/* Pegar aquí packages/core/components/reader.js completo */</script>
```
