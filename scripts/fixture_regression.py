"""Fixture local de regresión para los contratos de ancho, índice, copia e impresión."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def build(start,script):
 body='''<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="barra" tabindex="0" role="region" aria-label="Páginas y tema, desplazable">
 <span class="sello">nota / prueba</span><nav aria-label="Páginas"><button type="button" data-ir="p1" aria-current="page">01 · Primera</button><button type="button" data-ir="p2">02 · Segunda</button></nav>
 <div class="temas"><label for="tema">Papel</label><select id="tema" data-tema><option value="system">Sistema</option><option value="light">Claro</option><option value="dark">Oscuro</option><option value="sea">Sea</option></select></div>
</div>
<main class="hoja multipagina" data-lectura lang="es">
 <article class="pagina viva" data-pagina id="p1">
  <header class="cabecera" id="contenido" tabindex="-1"><h1>Primera página.</h1></header>
  <nav class="indice" aria-label="Índice primera página"><ol><li><a href="#uno">Uno</a></li><li><a href="#dos">Dos</a></li></ol></nav>
  <section class="seccion" id="uno"><h2>Uno</h2><p>Texto de referencia para medir el ancho de lectura.</p></section>
  <figure class="ancho"><div class="terminal"><div class="cab"><span>resultado.txt</span><button type="button" data-copiar="copiar-terminal" aria-label="Copiar salida"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 4h12v12H4z" fill="none" stroke="currentColor"/></svg></button><span class="copia-estado" role="status"></span></div><div class="cuerpo"><pre tabindex="0" aria-label="Salida"><code id="copiar-terminal">valor 42 · salida de ejemplo con una línea larga para comprobar el desplazamiento local</code></pre></div></div></figure>
  <section class="seccion" id="dos"><h2>Dos</h2><p>Segunda sección. El encabezado de índice debe marcar el avance.</p><div style="min-height:1100px" aria-hidden="true"></div></section>
 </article>
 <article class="pagina" data-pagina id="p2" hidden>
  <header class="cabecera"><h1>Segunda página.</h1></header>
  <nav class="indice" aria-label="Índice segunda página"><ol><li><a href="#tres">Tres</a></li><li><a href="#cuatro">Cuatro</a></li></ol></nav>
  <section class="seccion" id="tres"><h2>Tres</h2><p>El índice sólo considera la página visible.</p></section>
  <figure class="amplio"><div class="tabla-caja densa" tabindex="0" role="region" aria-label="Tabla densa de prueba, desplazable"><table><caption>Datos de prueba</caption><thead><tr><th scope="col">Nombre</th><th scope="col">Uno</th><th scope="col">Dos</th><th scope="col">Tres</th><th scope="col">Cuatro</th></tr></thead><tbody><tr><th scope="row">Muestra</th><td>1</td><td>2</td><td>3</td><td>4</td></tr></tbody></table></div></figure>
  <section class="seccion" id="cuatro"><h2>Cuatro</h2><p>La tabla ancha queda fuera de la sección de lectura.</p><div style="min-height:1100px" aria-hidden="true"></div></section>
 </article>
 <div class="paginacion" data-paginacion><button type="button" data-nav="prev"><span class="et">Anterior</span><span class="tit"></span></button><button type="button" data-nav="next"><span class="et">Siguiente</span><span class="tit"></span></button></div>
 <footer class="pie">Fixture de regresión. No contiene datos de producción.</footer>
</main>'''
 (ROOT/'examples/generated/checks.html').write_text(start('Bottifact · regresiones')+body+script('packages/core/components/reader.js')+script('packages/core/components/chapters.js'))
