## Documento y temas — compatibilidad histórica

Este esqueleto explica documentos anteriores con selector simple. **No es la base de nuevos
artefactos**: omite los controles que Angel pidió estandarizar. Para crear uno consulta
[docs/artifact-contract.md](artifact-contract.md); la receta `apariencia` documenta la llave vigente con nueve paletas.


```html
<title>Nota — decisión y evidencia</title>
<meta charset="utf-8">
<style>/* Pegar aquí packages/core/styles/fonts.css y packages/core/styles/artifact.css completos, incluidas las licencias */</style>
<meta name="viewport" content="width=device-width, initial-scale=1">
<a class="salto" href="#contenido">Saltar al contenido</a>
<main class="hoja" data-lectura lang="es">
  <div class="herramientas">
    <span class="firma-editorial"><span>Bottifact</span><small>Cuadernos</small></span>
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

La plantilla ejecutable ya contiene los archivos incrustados. Los comentarios de este ejemplo
se sustituyen por los archivos indicados; no son dependencias remotas. Para una figura aún más
ancha, cambia `.ancho` por `.amplio`, nunca el ancho de todo el documento.
