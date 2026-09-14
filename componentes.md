# Componentes de Nota Tikin

Los bloques siguientes son HTML completo de componente, para copiar dentro de `.hoja`, después
de pegar `fuentes.css` y `estilo.css` en `<style>`. Los comportamientos se activan pegando `interacciones.js`
una vez al final del documento. No introducen clases de Tailwind ni dependen de React.

Para empezar por una pieza: [gráficas](#recetas-graficas),
[calor](#recetas-calor), [tablas](#recetas-tablas),
[sonido](#recetas-sonido), [escritura](#recetas-escritura),
[Three.js](#recetas-three). `plantilla.html` es el catálogo ejecutable;
`multipagina.html` muestra capítulos completos. Las recetas marcadas son sus fuentes.

## Documento y temas

```html
<title>Nota — decisión y evidencia</title>
<meta charset="utf-8">
<style>/* Pegar aquí fuentes.css y estilo.css completos, incluidas las licencias */</style>
<meta name="viewport" content="width=device-width, initial-scale=1">
<a class="salto" href="#contenido">Saltar al contenido</a>
<main class="hoja" data-lectura lang="es">
  <div class="herramientas">
    <span class="mono">nota / tikin</span>
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
<script>/* Pegar aquí interacciones.js completo */</script>
```

La plantilla ejecutable ya contiene los archivos incrustados. Los comentarios de este ejemplo
se sustituyen por los archivos indicados; no son dependencias remotas. Para una figura aún más
ancha, cambia `.ancho` por `.amplio`, nunca el ancho de todo el documento.

## Subrayado a mano

```html
<p>El estado definitivo debe vivir en <span class="marca">un solo registro</span>.
  El <a href="#evidencia">detalle de la evidencia</a> se puede consultar después.</p>
```

**Cuándo:** una frase que contiene la decisión. `.marca` usa dos trazos SVG incrustados, de
`1.7px`, con curvas distintas; `background-size:100% .32em` y `box-decoration-break:clone`
permiten saltar de línea. El tema Sea cambia el trazo a verde. El texto conserva su tinta,
selección y contraste; el trazo no pretende reemplazar enlaces o negritas.

## Nota manuscrita y corchete

```html
<div class="con-margen">
  <p>El dato necesita unidad, fecha y origen. Mientras se confirma, debe decir
    <span class="dato">pendiente de medir</span>.</p>
  <aside class="margen" aria-label="Nota al margen">
    ¿se entiende sin estar en la reunión?
  </aside>
</div>
<p class="nota">una buena nota le ahorra contexto a la siguiente persona</p>
```

**Cuándo:** una perspectiva complementaria, no una condición que cambia la decisión principal.
El párrafo ocupa la celda central; a partir de `1184px` la nota usa una celda real a su derecha.
Debajo, sigue al párrafo. La nota usa Reenie Beanie `26px / 1.18`; el corchete es CSS de `1px`
con remates de `9px`. Solo los remates decorativos son absolutos.

## Avisos con círculo

```html
<aside class="aviso ojo" aria-label="Aviso 1: condición">
  <span class="num">1</span>
  <div><p class="titulo">La medición todavía es parcial.</p>
    <p>Falta el volumen de una sede; el total no representa toda la operación.</p></div>
</aside>
<aside class="aviso bien" aria-label="Aviso 2: resultado">
  <span class="num">2</span>
  <div><p class="titulo">La fuente está identificada.</p>
    <p>El registro incluye la fecha de corte y la unidad de cada cifra.</p></div>
</aside>
<aside class="aviso mal" aria-label="Aviso 3: error">
  <span class="num">3</span>
  <div><p class="titulo">El archivo no se pudo leer.</p>
    <p>La última medición válida sigue disponible en el registro.</p></div>
</aside>
<aside class="aviso cita">
  <span class="num" aria-hidden="true">↳</span>
  <div><blockquote>Dejar una buena nota es dejar contexto.</blockquote>
    <p class="secundario">Principio de esta plantilla</p></div>
</aside>
```

**Cuándo:** condiciones, errores, confirmaciones o citas breves. Omite la variante para una nota
informativa azul. Círculo `28px`, dos columnas `30px minmax(0,1fr)`, borde izquierdo `3px`;
el número pertenece al flujo y no invade un margen. No uses `role="alert"` para avisos estáticos.
El original usa símbolos dentro de un círculo; la numeración es la adaptación pedida por Angel.

## Mapa de proporción

```html
<figure class="ancho">
  <div class="mapa" role="group" aria-label="Reparto ilustrativo de cien horas">
    <div class="bloque destaca"><span class="n">Investigar</span><span class="d">60 h · 60 %</span></div>
    <div class="bloque"><span class="n">Construir</span><span class="d">25 h · 25 %</span></div>
    <div class="bloque"><span class="n">Revisar</span><span class="d">15 h · 15 %</span></div>
  </div>
  <figcaption>Ejemplo de cien horas. Las áreas incluyen el borde interior de cada celda.</figcaption>
</figure>
```

**Cuándo:** participación sobre un total positivo y comparable. Las columnas `3fr 2fr` dan
60/40; las filas `5fr 3fr` subdividen el 40 en 25/15. Esta receta corresponde **solo a esos
pesos**. Al cambiar datos, calcula nuevas fracciones o genera un treemap con sus valores; no
cambies únicamente las etiquetas. Las filas tienen mínimos para proteger texto; con otros
idiomas o texto mucho más largo, verifica el reparto o usa un gráfico de barras y una tabla.

Para más de tres grupos, ordena por peso y considera agrupar la cola como «Otros», desglosada
aparte. No omitas cifras pequeñas ni sustituyas un porcentaje por una celda arbitraria. El
original calcula un treemap squarify; esta receta de rejilla es una versión explícita sin D3.

## Pastillas, lista mono y medida

```html
<p>El valor está <span class="dato">pendiente de medir</span>.</p>
<p><span class="pildora p-si">✓ Aplicado</span>
   <span class="pildora p-medio">≈ Parcial</span>
   <span class="pildora p-no">× No disponible</span></p>
<dl class="datos">
  <div><dt>Fuente</dt><dd>CSS publicado de cmrg.me</dd></div>
  <div><dt>Tamaño original</dt><dd>15,5 px</dd></div>
  <div><dt>Interlineado original</dt><dd>1,55</dd></div>
</dl>
<div class="medida">
  <label for="cobertura">Páginas revisadas</label><span class="pct">100 %</span>
  <meter id="cobertura" min="0" max="10" value="10">10 de 10 páginas</meter>
</div>
```

**Cuándo:** la lista `dl` asocia etiquetas y valores; una pastilla representa un estado o dato
breve. La barra usa `meter` porque mide cobertura, no una operación en curso. No conviertas
fechas o nombres en controles falsos. Las pastillas saltan de línea si hace falta.

## Índice lateral y regla de lectura

```html
<nav class="indice" aria-label="Índice del documento">
  <p class="ceja">En esta nota</p>
  <ol><li><a href="#criterio">El criterio</a></li>
      <li><a href="#evidencia">La evidencia</a></li></ol>
</nav>
<section class="seccion" id="criterio"><h2>El criterio</h2><p>Qué necesitamos resolver.</p></section>
<section class="seccion" id="evidencia"><h2>La evidencia</h2><p>Qué sostiene la decisión.</p></section>
<!-- La regla va fuera de main; interacciones.js vincula los elementos. -->
<div class="regla" role="slider" tabindex="0" aria-orientation="vertical"
     aria-label="Progreso de lectura" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
  <div class="ticks"></div><div class="cursor"></div><span class="val">0%</span>
</div>
```

**Cuándo:** un texto con varias secciones que se beneficiaría de navegación. El índice se fija
solo desde `1600px`, dejando espacio incluso junto a figuras de `76rem`; en pantallas pequeñas
sigue visible en el flujo. La regla admite clic, flechas, PageUp/Down y Home/End. El progreso se
calcula sobre `[data-lectura]`, tolera documentos cortos y se actualiza al cambiar sus dimensiones.
El tachado indica secciones anteriores a la actual, no una afirmación de que la persona las leyó.

## Código con encabezado y copia

```html
<figure class="ancho">
  <div class="codigo">
    <div class="cab"><span>registro.js · JavaScript</span>
      <button type="button" data-copiar="registro-codigo" aria-label="Copiar registro.js">Copiar</button>
      <span class="copia-estado" role="status" aria-live="polite"></span>
    </div>
    <pre tabindex="0" aria-label="Código de registro"><code id="registro-codigo"><span class="com">// La procedencia forma parte del dato.</span>
<span class="kw">const</span> fuente = <span class="str">"CSS publicado de cmrg.me"</span>;</code></pre>
  </div>
  <figcaption>Ejemplo verificable; la copia conserva el texto, sin los colores del resaltado.</figcaption>
</figure>
```

**Cuándo:** la persona necesita inspeccionar, comparar o copiar una entrada exacta. El encabezado
usa mono `12px`; el código `13px / 1.65`, con desplazamiento y selección nativos. Si la API del
portapapeles está bloqueada, el script selecciona el contenido y explica cómo copiarlo. Usa
identificadores únicos por bloque. Escapa `&`, `<` y `>` al insertar código dentro del HTML.

## Tablas y diagramas anchos

```html
<figure class="amplio">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Medidas tipográficas, desplazable">
    <table><caption>Valores observados en cmrg.me</caption>
      <thead><tr><th scope="col">Uso</th><th scope="col">Tamaño</th><th scope="col">Interlineado</th></tr></thead>
      <tbody><tr><th scope="row">Cuerpo</th><td>15,5 px</td><td>1,55</td></tr>
        <tr><th scope="row">Título, escritorio</th><td>44,5 px</td><td>1,1111</td></tr></tbody>
    </table>
  </div>
  <figcaption>Fuente: hoja CSS y estilo calculado a 1639 px de viewport.</figcaption>
</figure>
```

Las tablas son anchas por defecto. No apliques `white-space:nowrap` a toda la tabla. Si una
columna contiene identificadores largos, permite partirlos; si la estructura necesita más
ancho, conserva el desplazamiento local. Los diagramas SVG deben tener `viewBox`, título y
una descripción equivalente en texto. El tamaño del dibujo debe proteger la lectura de sus
etiquetas; usa una región desplazable para figuras densas, o una composición vertical en móvil.

Diagrama completo, sin dependencias:

```html
<figure class="ancho">
  <div class="diagrama-caja" tabindex="0" role="region" aria-label="Proceso de revisión, desplazable">
    <svg class="diagrama" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 160" role="img" aria-labelledby="proceso-titulo proceso-desc">
      <title id="proceso-titulo">De la fuente a la decisión</title>
      <desc id="proceso-desc">Observar la fuente, verificar la evidencia y registrar la decisión.</desc>
      <g fill="none" stroke="currentColor"><rect x="10" y="40" width="200" height="80" rx="4"/>
        <rect x="260" y="40" width="200" height="80" rx="4"/><rect x="510" y="40" width="200" height="80" rx="4"/>
        <path d="M210 80h42m-9-7 9 7-9 7M460 80h42m-9-7 9 7-9 7"/></g>
      <g fill="currentColor" text-anchor="middle" font-size="17"><text x="110" y="87">Observar</text><text x="360" y="87">Verificar</text><text x="610" y="87">Registrar</text></g>
    </svg>
  </div>
  <figcaption>Fuente → verificación → decisión registrada. Las flechas indican orden, no duración.</figcaption>
</figure>
```

**Cuándo:** una relación o secuencia concreta se entiende mejor como dibujo. Para registros
comparables usa la tabla; para magnitudes, una gráfica a escala.

**Límite:** esta composición contiene tres pasos. Cambiar sólo las etiquetas no añade nodos
ni rutas; para más pasos ajusta SVG, texto equivalente y viewBox. Conserva los IDs únicos,
el mínimo de 640 px y su región desplazable. No simula procesos ni calcula tiempos.

## Texto que se desvanece

```html
<div class="extracto">
  <p class="desvanece" aria-hidden="true">La forma prepara el terreno; la evidencia sostiene
    lo que decimos. Una nota se termina cuando permite decidir.</p>
  <details><summary>Leer la nota completa</summary>
    <p>La forma prepara el terreno; la evidencia sostiene lo que decimos. Una nota se termina
      cuando permite decidir. Si falta una fuente, debe quedar identificada como pendiente.</p>
  </details>
</div>
```

**Cuándo:** un anticipo opcional. La máscara `35% → 100%` afecta solo una copia decorativa;
el contenido íntegro siempre está disponible por teclado, lector de pantalla e impresión.
No apliques `.desvanece` al cierre de una conclusión, una alerta, una tabla o un pie con la fuente.

## Tarjetas «kept»

```html
<div class="kept ancho">
  <article>
    <svg class="portada" viewBox="0 0 180 220" aria-hidden="true">
      <rect x="2" y="2" width="176" height="216" rx="2" fill="#755a42"/>
      <circle cx="90" cy="85" r="48" fill="none" stroke="#fef8f2"/>
      <text x="24" y="166" fill="#fef8f2" font-family="Georgia" font-size="24">La decisión</text>
    </svg>
    <h3>La decisión</h3><p>Qué se eligió y por qué. Un registro al que podamos volver.</p>
    <p class="meta">NOTA / 01 · ejemplo editorial</p>
  </article>
  <article>
    <h3>La evidencia</h3><p>Medidas, fuentes y límites, con el contexto que les da sentido.</p>
    <p class="meta">REGISTRO / 02 · ejemplo editorial</p>
  </article>
</div>
```

**Cuándo:** objetos o referencias seleccionados, no un catálogo exhaustivo. Portada opcional,
título completo y una nota personal o útil. `auto-fit` con mínimo adaptable de `240px`; el hover
inclina la portada `−2deg` y la eleva `3px` durante `320ms`, sin mover el texto. Con movimiento
reducido no hay transición. Si toda la tarjeta debe navegar, usa un enlace real con nombre;
no añadas un `onclick` a un `div`. Las portadas con `<img>` deben ser `data:` URI, como las de
`plantilla.html`, que se generan localmente y no reproducen carátulas comerciales.

## Multipágina

<!-- nota:ejemplo multipagina -->
```html
<a class="salto" href="#contenido">Saltar al contenido</a>
<div class="barra" tabindex="0" role="region" aria-label="Páginas y tema, desplazable">
  <span class="sello">nota / tikin</span>
  <nav aria-label="Páginas del informe">
    <button type="button" data-ir="p1" aria-current="page"><span class="n">01</span>El destino</button>
    <button type="button" data-ir="p2"><span class="n">02</span>La evidencia</button>
  </nav>
  <div class="temas">
    <label for="tema" class="sr-only">Papel</label>
    <select id="tema" data-tema>
      <option value="system">Sistema</option><option value="light">Claro</option>
      <option value="dark">Oscuro cálido</option><option value="sea">Dark Sea</option>
    </select>
  </div>
</div>

<main class="hoja multipagina" data-lectura lang="es">
  <article class="pagina viva" id="p1" data-pagina>
    <header class="cabecera" id="contenido" tabindex="-1">
      <p class="ceja">Página 01 / el destino</p>
      <h1>A dónde tenemos que ir.</h1>
      <p class="bajada">Una frase que dice de qué trata el capítulo.</p>
    </header>
    <nav class="indice" aria-label="Índice de esta página">
      <p class="ceja">En esta página</p>
      <ol><li><a href="#criterio">El criterio</a></li></ol>
    </nav>
    <section class="seccion" id="criterio"><h2>El criterio</h2><p>Texto.</p></section>
    <figure class="amplio">
      <div class="tabla-caja" tabindex="0" role="region" aria-label="Criterios del destino, desplazable">
        <table><caption>Criterios ilustrativos</caption>
          <thead><tr><th scope="col">Criterio</th><th scope="col">Resultado esperado</th></tr></thead>
          <tbody><tr><th scope="row">Trazabilidad</th><td>Conservar la fuente y la fecha de cada registro.</td></tr></tbody>
        </table>
      </div><figcaption>Figura hermana de la sección; conserva el ancho amplio.</figcaption>
    </figure>
  </article>

  <article class="pagina" id="p2" data-pagina hidden>
    <header class="cabecera"><p class="ceja">Página 02 / evidencia</p><h1>Qué lo sostiene.</h1></header>
    <nav class="indice" aria-label="Índice de evidencia"><ol><li><a href="#registro">El registro</a></li></ol></nav>
    <section class="seccion" id="registro"><h2>El registro</h2><p>Una muestra ilustrativa conserva su origen y distingue lo medido de lo pendiente.</p></section>
    <figure class="ancho"><div class="codigo"><div class="cab"><span>registro.txt</span>
      <button type="button" data-copiar="registro-p2">Copiar registro</button><span class="copia-estado" role="status"></span></div>
      <pre tabindex="0" aria-label="Registro ilustrativo"><code id="registro-p2">fuente: ejemplo local
fecha: 2026-09-13
estado: pendiente de medir</code></pre></div><figcaption>Datos de ejemplo, sin una medición de producción.</figcaption></figure>
  </article>

  <div class="paginacion" data-paginacion>
    <button type="button" data-nav="prev"><span class="et">Anterior</span><span class="tit"></span></button>
    <button type="button" data-nav="next"><span class="et">Siguiente</span><span class="tit"></span></button>
  </div>
  <footer class="pie">Nota Tikin · Dos capítulos de ejemplo.</footer>
</main>
```

**Cuándo:** un informe con capítulos que se leen por separado y merecen cada uno su temario. No
para una nota de tres secciones: ahí la página única con índice lateral es mejor.

**La rejilla va en `.pagina`, no en `.hoja`.** Por eso la clase es `multipagina` y no
`por-seccion`: con las páginas de por medio, el selector `>` de `por-seccion` ya no alcanza a las
secciones y todo termina del ancho del párrafo.

**Instalación:** pega `interacciones.js` y después `multipagina.js`, completos dentro de
sendos `<script>` al final. El primero delega el índice cuando ve `.multipagina`; el segundo
mantiene `aria-current`, `aqui-visto` y `aqui-actual` únicamente en la página visible.
`multipagina.html` contiene la receta completa con ambos guiones y el CSS incrustados.

**Límite:** no carga páginas por red ni implementa un router de aplicación. Un enlace de
capítulo usa su ID (`#p2`); los enlaces a secciones son internos a la página ya abierta.
Sin JS sólo se ve el primer capítulo en pantalla; imprime todos los capítulos. No combines
`por-seccion` con `multipagina`. Cada ID y cada `data-ir` debe ser único y corresponderse.

El botón activo lleva `aria-current="page"`; el hash conserva la página abierta, así que un enlace
a un capítulo concreto funciona. Al cambiar de página se emite `nota:pagina` por si hay que
arrancar un lienzo o recalcular una figura.

## Tablas densas

<!-- nota:ejemplo tabla-densa -->
```html
<figure class="amplio">
  <div class="tabla-caja densa" tabindex="0" role="region" aria-label="Brechas, desplazable">
    <table><caption>Seguimiento ilustrativo de brechas</caption>
      <thead><tr><th scope="col">Brecha</th><th scope="col">Responsable</th><th scope="col">Estado</th><th scope="col">Inicio</th><th scope="col">Revisión</th><th scope="col">Evidencia esperada</th></tr></thead>
      <tbody><tr><th scope="row">Fuente sin fecha de corte</th><td>Equipo de datos</td><td>Pendiente</td><td><time datetime="2026-09-13">13-sep-2026</time></td><td><time datetime="2026-09-18">18-sep-2026</time></td><td>Registro con fecha y criterio de inclusión.</td></tr>
        <tr><th scope="row">Definición de unidad</th><td>Equipo de análisis</td><td>En revisión</td><td><time datetime="2026-09-12">12-sep-2026</time></td><td><time datetime="2026-09-16">16-sep-2026</time></td><td>Diccionario con unidad y denominador.</td></tr></tbody>
    </table>
  </div>
  <figcaption>Ejemplo de seis columnas; desplaza la tabla para consultar la última.</figcaption>
</figure>
```

**Cuándo:** desde cinco columnas. `.tabla-caja table` ya trae `min-width: 34rem`; `densa` lo sube a
`58rem`. Sin ese mínimo la tabla no se desplaza, se comprime: medido a 390 px, seis columnas daban
celdas de 50 px y filas de **581 px de alto**. Con `densa`, celdas de 139–285 px y filas de 140 px.
El desplazamiento es local —la página nunca se mueve de lado— y la caja es alcanzable por teclado.

## Terminal

<!-- nota:ejemplo terminal -->
```html
<figure class="ancho">
  <div class="terminal">
    <div class="cab"><span>saldo por bolsillo · ejemplo ilustrativo</span>
      <button type="button" data-copiar="t-saldos" aria-label="Copiar la salida">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
          <rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>
        </svg>
      </button>
      <span class="copia-estado" role="status" aria-live="polite"></span>
    </div>
    <div class="cuerpo">
      <pre tabindex="0" aria-label="Distribución del saldo"><code id="t-saldos"><span class="tenue">       rango   bolsillos        total COP</span>
<span class="tenue">  ------------  ---------  ---------------</span>
  menos de $100        349            5.120
    más de $1M          5    <span class="subra">14.434.490</span></code></pre>
    </div>
  </div>
  <figcaption>Datos ilustrativos. La columna que importa va señalada, no en negrita.</figcaption>
</figure>
```

**Cuándo:** una salida de consola, una consulta y su resultado, un volcado — cuando la evidencia
*es* el texto tal como se vio. No para código fuente de ejemplo: para eso está `.codigo`.

Se queda **oscura en los dos temas** a propósito: una terminal clara no se lee como una terminal.
La variante Sea sí cambia sus tonos, porque ahí el documento entero es oscuro y una caja con otro
negro se vería sucia. El botón de copia usa el mismo `data-copiar` del sistema. Alinea las columnas
con espacios dentro del `<pre>`; no uses una tabla disfrazada.

## Nota manuscrita señalada

<!-- nota:ejemplo manuscrita -->
```html
<p class="manuscrita">las fechas dicen cuándo pasó cada cosa. lo que explica cómo una llevó a la
  otra está <span class="senalado">en las brechas</span>, donde dejo de
  hablar de porcentajes</p>
```

**Cuándo:** una frase en primera persona que comenta el documento desde afuera —una duda, una
advertencia, un apunte—. El corchete señala **una** cosa: el enlace o la idea que importa. Dos
corchetes en la misma frase anulan el gesto.

No la uses para información crítica: la manuscrita es difícil de leer en pantallas pequeñas y no
todos los lectores de pantalla la anuncian distinto del resto. Lo que no se puede perder va en
prosa normal o en un `.aviso`.

## Globo de rutas

```html
<figure class="ancho">
  <div id="mi-globo"></div>
  <figcaption>Rutas ilustrativas. La lista permanece disponible sin WebGL.</figcaption>
</figure>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js"></script>
<script>/* Pegar aquí globo.js completo, con su licencia MIT */</script>
<script>
const rutas = new NotaGlobo(document.getElementById('mi-globo'), {
  points: [
    {id:'BOG',label:'Bogotá',lat:4.711,lon:-74.0721},
    {id:'MAD',label:'Madrid',lat:40.4168,lon:-3.7038},
    {id:'HND',label:'Tokio',lat:35.5494,lon:139.7798}
  ],
  arcs: [
    {id:'bog-mad',from:'BOG',to:'MAD',label:'BOG → MAD',detail:'Bogotá · Madrid'},
    {id:'mad-hnd',from:'MAD',to:'HND',label:'MAD → HND',detail:'Madrid · Tokio'}
  ]
});
</script>
```

`globo.html` es la versión completa ejecutable de ese contrato, sin comentarios por sustituir.
La máscara terrestre está incrustada dentro de `globo.js`. No necesita APIs, claves, imágenes
externas ni solicitudes `fetch`.

| Entrada / método | Contrato |
|---|---|
| `points` | Array; `id` string único, `lat` número entre −90 y 90, `lon` entre −180 y 180; `label` opcional. |
| `arcs` | Array; `from` y `to` son IDs existentes; `id` opcional pero único, `label` y `detail` opcionales. Las coordenadas y unidades son geográficas. |
| `select(id)` | Selecciona y centra una ruta; `select(null)` vuelve a todas. Error si el ID no existe. |
| `setData({points,arcs})` | Reemplaza los datos validados, libera geometrías anteriores y reconstruye la lista. Datos inválidos lanzan `TypeError` y conservan el conjunto anterior. |
| `rotate(dx,dy)` | Radianes; giro horizontal e inclinación limitada a ±1,2. |
| `pause()` / `resume()` | Controlan el giro; `resume()` sigue respetando movimiento reducido. |
| `destroy()` | Detiene RAF, desconecta listeners/observers, libera WebGL y vacía el contenedor. |

Los puntos coincidentes no dibujan una curva degenerada; los antípodas usan un eje determinista.
Las etiquetas entran por `textContent`, no por HTML. Cuando serialices JSON dentro de un script,
escapa `<` como `\u003c`; nunca interpoles datos sin escapar dentro de `innerHTML`.

La proyección y la atmósfera siguen COBE; los arcos son bandas cuadráticas con 64 segmentos,
con ocultación tras la esfera. El giro es `0.072rad/s`, equivalente a los `0.0012rad/cuadro`
originales a 60 Hz, pero estable a otras frecuencias. El suavizado conserva el factor original
`0.09` a 60 Hz. En modo reducido el cambio de selección se resuelve inmediatamente; hay
botones y flechas de teclado. Con touch se puede girar horizontalmente y conservar el scroll
vertical de la página. Sin WebGL queda un mensaje y la lista completa de rutas.

El globo no es un mapa político ni una medición de distancias. La máscara de 256×128 describe
masas terrestres; no añade fronteras. No inventes kilómetros, vuelos o sedes: recibe datos reales
o identifica el ejemplo como ilustrativo. Los arcos y marcadores se han aclarado frente al
original, una decisión deliberada para informes, no una afirmación de igualdad píxel a píxel.


## Librería de evidencia: instalación por pieza

La fuente de cada visualización es **su tabla HTML**, no una segunda copia de los datos.
Pega `fuentes.css` y `estilo.css` completos y, al final del documento, los módulos necesarios dentro de
`<script>`: [graficas.js](graficas.js) para gráficas/calor y [tablas.js](tablas.js) para
ordenación/sparkline. Son independientes de Three.js. Cada módulo se pega una sola vez.
Se inicializan al cargar; para HTML insertado después usa `NotaGraficas.init(contenedor)`
o `NotaTablas.init(contenedor)`. Repetir `init` devuelve la instancia existente.
`get(elemento).destroy()` devuelve el HTML original; para nuevos datos, destruye la
instancia, modifica la tabla y vuelve a inicializar. No hay red, almacenamiento ni framework.

Los siguientes bloques son también la fuente del catálogo ejecutable: el ensamblador
extrae las recetas marcadas `nota:ejemplo`. Las figuras se copian **como hijas de `.hoja`**.
Para secciones anidadas usa `por-seccion`; para capítulos usa `multipagina` y coloca las
figuras como hijas de `.pagina`. No envuelvas el bloque en otra sección angosta.

`data-valor` usa punto decimal, sin separadores de miles; su texto visible incluye la
unidad y el formato humano. Vacío significa ausencia, `0` es un cero medido. Los ejemplos
son ilustrativos y lo dicen en su pie. Los nombres y los datos se insertan como texto.
Las unidades de los ejes se escriben completas junto al dibujo (`X`, `Y`) para permitir
que envuelvan en varias líneas. El SVG mantiene los ticks y sus valores en la misma escala.
Las gráficas no tienen animación ni tooltip imprescindible: la tabla permite consultar
cada punto por teclado. Las escalas se calculan con los datos, sin recortar extremos.
No se suman ni se interpolan registros ausentes. Los intervalos entre puntos de una línea
son segmentos rectos, no observaciones adicionales.

<a id="recetas-graficas"></a>

## Barras: cantidades y diferencias

<!-- nota:ejemplo barras -->
```html
<figure class="ancho" id="barras-ejemplo" data-grafica="barras" data-unidad="Horas">
  <details open><summary>Ver los datos de balance de horas</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Balance de horas, tabla desplazable">
      <table><caption>Balance de horas</caption>
        <thead><tr><th scope="col">Actividad</th><th scope="col">Horas</th></tr></thead>
        <tbody><tr><th scope="row">Investigar</th><td data-valor="60">60 h</td></tr>
<tr><th scope="row">Construir</th><td data-valor="25">25 h</td></tr>
<tr><th scope="row">Revisar</th><td data-valor="15">15 h</td></tr>
<tr><th scope="row">Ajuste de registro</th><td data-valor="-10">−10 h</td></tr></tbody>
      </table>
    </div>
  </details>
  <figcaption>Datos ilustrativos; corte 13-sep-2026.</figcaption>
</figure>
```

**Cuándo:** comparar magnitudes en la misma unidad; admite negativos y hasta cuatro series agrupadas. Cero siempre está en la escala. Usa línea si importa la continuidad temporal.

**Límite:** hasta 500 filas y cuatro series. Muchas barras requieren una figura alta: para centenares de registros, prefiere tabla ordenable. El ancho mínimo del dibujo es 800 px con desplazamiento local; las categorías largas saltan de línea. No son barras apiladas ni porcentajes normalizados.

## Líneas: secuencia y datos ausentes

<!-- nota:ejemplo lineas -->
```html
<figure class="ancho" id="lineas-ejemplo" data-grafica="lineas" data-unidad="Horas">
  <details open><summary>Ver los datos de tiempo de resolución</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Tiempo de resolución, tabla desplazable">
      <table><caption>Tiempo de resolución</caption>
        <thead><tr><th scope="col">Etapa</th><th scope="col">Equipo A</th><th scope="col">Equipo B</th></tr></thead>
        <tbody><tr><th scope="row">Entrada</th><td data-valor="12">12 h</td><td data-valor="16">16 h</td></tr>
<tr><th scope="row">Revisión</th><td data-valor="8">8 h</td><td data-valor="11">11 h</td></tr>
<tr><th scope="row">Validación</th><td data-valor="">Sin dato</td><td data-valor="9">9 h</td></tr>
<tr><th scope="row">Cierre</th><td data-valor="6">6 h</td><td data-valor="7">7 h</td></tr></tbody>
      </table>
    </div>
  </details>
  <figcaption>Datos ilustrativos; corte 13-sep-2026.</figcaption>
</figure>
```

**Cuándo:** seguir una secuencia ordenada de categorías comparables. Trazo y número en la leyenda distinguen series incluso en Sea. Para fechas con separaciones distintas, usa temporal; para categorías independientes, barras.

**Límite:** los intervalos en X son categóricos y equidistantes. La ausencia corta el trazo, no se convierte en cero. El eje Y muestra el dominio completo observado; no tiene que comenzar en cero porque codifica posición. Hasta cuatro series; no calcula suavizados ni intervalos de confianza.

## Serie temporal con variación

<!-- nota:ejemplo temporal -->
```html
<figure class="ancho" id="temporal-ejemplo" data-grafica="temporal" data-unidad="Solicitudes">
  <details open><summary>Ver los datos de solicitudes por día</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Solicitudes por día, tabla desplazable">
      <table><caption>Solicitudes por día</caption>
        <thead><tr><th scope="col">Día UTC</th><th scope="col">Solicitudes</th></tr></thead>
        <tbody><tr><th scope="row"><time datetime="2026-09-01">1 sep</time></th><td data-valor="80">80 solicitudes</td></tr>
<tr><th scope="row"><time datetime="2026-09-03">3 sep</time></th><td data-valor="100">100 solicitudes</td></tr>
<tr><th scope="row"><time datetime="2026-09-08">8 sep</time></th><td data-valor="90">90 solicitudes</td></tr>
<tr><th scope="row"><time datetime="2026-09-13">13 sep</time></th><td data-valor="120">120 solicitudes</td></tr></tbody>
      </table>
    </div>
  </details>
  <figcaption>Ejemplo: conteos diarios independientes. Último registro frente al registro anterior (13 sep frente a 8 sep), no totales de ventanas de distinta duración.</figcaption>
</figure>
```

**Cuándo:** comparar observaciones fechadas. La posición usa milisegundos UTC: dos días y cinco días no ocupan el mismo espacio. El delta compara los dos últimos registros y nombra ambos.

**Límite:** fechas ISO diarias válidas, únicas y crecientes; no agrega días ni corrige zonas horarias. El delta absoluto es actual − anterior y el relativo divide por |anterior|; base 0 indica porcentaje no definido, ausente indica sin comparación. Si tus registros representan ventanas, deben tener duración/composición comparables. No infiere causalidad ni si subir es bueno.

## Dispersión: relación entre dos variables

<!-- nota:ejemplo dispersion -->
```html
<figure class="ancho" id="dispersion-ejemplo" data-grafica="dispersion" >
  <details open><summary>Ver los datos de carga y latencia</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Carga y latencia, tabla desplazable">
      <table><caption>Carga y latencia</caption>
        <thead><tr><th scope="col">Muestra</th><th scope="col">Carga (solicitudes/s)</th><th scope="col">Latencia (ms)</th></tr></thead>
        <tbody><tr><th scope="row">A</th><td data-valor="10">10</td><td data-valor="80">80 ms</td></tr>
<tr><th scope="row">B</th><td data-valor="20">20</td><td data-valor="95">95 ms</td></tr>
<tr><th scope="row">C</th><td data-valor="35">35</td><td data-valor="140">140 ms</td></tr>
<tr><th scope="row">D</th><td data-valor="50">50</td><td data-valor="170">170 ms</td></tr>
<tr><th scope="row">E</th><td data-valor="65">65</td><td data-valor="165">165 ms</td></tr></tbody>
      </table>
    </div>
  </details>
  <figcaption>Datos ilustrativos; corte 13-sep-2026.</figcaption>
</figure>
```

**Cuándo:** explorar pares X/Y medidos en la misma observación. Las dos variables tienen ejes numéricos con unidades. Para una sola secuencia de tiempo usa temporal.

**Límite:** cada punto exige ambos valores finitos. Hasta 500 puntos; coincidentes se superponen y siguen separados en la tabla. No ajusta regresiones, no aplica jitter, no representa incertidumbre ni permite inferir causalidad.

## Distribución: histograma con intervalos reales

<!-- nota:ejemplo distribucion -->
```html
<figure class="ancho" id="distribucion-ejemplo" data-grafica="distribucion">
  <details open><summary>Ver los datos de duración</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Distribución de duración, tabla desplazable">
      <table><caption>Duración de 30 sesiones</caption>
        <thead><tr><th scope="col">Duración (min)</th><th scope="col">Sesiones</th><th scope="col">Sesiones/min</th></tr></thead>
        <tbody>
          <tr><th scope="row" data-desde="0" data-hasta="10">0 a menos de 10 min</th><td data-valor="5">5</td><td data-valor="">0,5</td></tr>
          <tr><th scope="row" data-desde="10" data-hasta="20">10 a menos de 20 min</th><td data-valor="15">15</td><td data-valor="">1,5</td></tr>
          <tr><th scope="row" data-desde="20" data-hasta="40">20 a 40 min (incluido)</th><td data-valor="10">10</td><td data-valor="">0,5</td></tr>
        </tbody>
      </table>
    </div>
  </details>
  <figcaption>Ejemplo de 30 sesiones. Altura = frecuencia / ancho del intervalo; el área representa la frecuencia. El último intervalo tiene el doble de ancho.</figcaption>
</figure>
```

**Cuándo:** mostrar la distribución de una variable continua agrupada en intervalos explícitos. Los bordes de las barras corresponden a los bordes del intervalo.

**Límite:** frecuencias enteras no negativas; intervalos crecientes sin solapamientos. La densidad se calcula como frecuencia/ancho; con intervalos desiguales es el área la que representa el conteo. La tabla declara inclusión/exclusión de extremos; el módulo no agrupa muestras individuales ni inventa bins. No es una curva de probabilidad ni un gráfico de categorías.

<a id="recetas-calor"></a>

## Attention map: matriz de intensidad

<!-- nota:ejemplo calor -->
```html
<figure class="ancho" id="calor-ejemplo" data-grafica="calor" data-umbrales="0,30,60,90,120,150" data-unidad="Minutos">
  <details open><summary>Ver los datos de tiempo por actividad y día</summary>
    <div class="tabla-caja" tabindex="0" role="region" aria-label="Tiempo por actividad y día, tabla desplazable">
      <table><caption>Tiempo por actividad y día</caption>
        <thead><tr><th scope="col">Actividad</th><th scope="col">Lun</th><th scope="col">Mar</th><th scope="col">Mié</th><th scope="col">Jue</th><th scope="col">Vie</th></tr></thead>
        <tbody><tr><th scope="row">Investigar</th><td data-valor="0">0 min</td><td data-valor="30">30 min</td><td data-valor="60">60 min</td><td data-valor="90">90 min</td><td data-valor="120">120 min</td></tr>
<tr><th scope="row">Construir</th><td data-valor="150">150 min</td><td data-valor="120">120 min</td><td data-valor="90">90 min</td><td data-valor="">Sin dato</td><td data-valor="30">30 min</td></tr>
<tr><th scope="row">Revisar</th><td data-valor="10">10 min</td><td data-valor="20">20 min</td><td data-valor="40">40 min</td><td data-valor="80">80 min</td><td data-valor="110">110 min</td></tr></tbody>
      </table>
    </div>
  </details>
  <figcaption>Ejemplo ilustrativo, minutos por día. Límites de clase: [0,30), [30,60), [60,90), [90,120), [120,150]. Ausencia distinta de cero.</figcaption>
</figure>
```

**Cuándo:** buscar concentraciones entre dos dimensiones discretas. Cada celda muestra su valor y la leyenda tiene intervalos explícitos. Para partes de un total usa `.mapa`, que conserva el treemap original.

**Límite:** cinco niveles, definidos por seis límites crecientes; máximo incluido en el último nivel. Un valor fuera del dominio produce error visible y conserva la tabla, nunca se satura en secreto. Hasta 31 × 31 celdas con ancho mínimo por columna y scroll local. No usa degradado ni escala implícita por fila. Las cifras mantienen el significado con colores forzados.

<a id="recetas-tablas"></a>

## Tabla de comparación

<!-- nota:ejemplo comparacion -->
```html
<figure class="amplio">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Comparación de fuentes, desplazable">
    <table class="tabla-comparacion"><caption>Fuentes candidatas · ejemplo</caption>
      <thead><tr><th scope="col">Criterio</th><th scope="col" class="elegida">Registro A · elegido</th><th scope="col">Registro B</th></tr></thead>
      <tbody>
        <tr><th scope="row">Fecha de corte</th><td class="elegida">13-sep-2026</td><td>10-sep-2026</td></tr>
        <tr><th scope="row">Trazabilidad</th><td class="elegida">✓ Identificador por movimiento</td><td>≈ Resumen por día</td></tr>
        <tr><th scope="row">Límite</th><td class="elegida">Falta una sede</td><td>Faltan tres días</td></tr>
      </tbody>
    </table>
  </div>
  <figcaption>Datos ilustrativos. «Elegido» expresa la decisión, no una puntuación automática.</figcaption>
</figure>
```

**Cuándo:** comparar las mismas propiedades de pocas alternativas. Escribe la decisión en la cabecera además de señalarla con color. No uses un ranking si los criterios son cualitativos.

**Límite:** la clase `.elegida` se aplica a cada celda de la columna; no calcula ganadores. Para cinco columnas o más añade `densa`. No vuelve sticky la primera columna, para que el espacio útil del teléfono quede disponible al desplazar.

## Tabla de totales y ordenación

<!-- nota:ejemplo totales -->
```html
<figure class="ancho">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Horas por actividad, tabla ordenable y desplazable">
    <table class="tabla-totales" data-tabla><caption>Horas registradas · ejemplo</caption>
      <thead><tr><th scope="col"><button type="button" data-ordenar="texto">Actividad</button></th><th scope="col"><button type="button" data-ordenar="numero">Horas</button></th></tr></thead>
      <tbody>
        <tr><th scope="row">Investigar</th><td class="numero" data-valor="60">60 h</td></tr>
        <tr><th scope="row">Construir</th><td class="numero" data-valor="25">25 h</td></tr>
        <tr><th scope="row">Revisar</th><td class="numero" data-valor="15">15 h</td></tr>
      </tbody>
      <tfoot><tr><th scope="row">Total de horas registradas</th><td class="numero">100 h</td></tr></tfoot>
    </table>
  </div>
  <figcaption>Ejemplo: 60 + 25 + 15 = 100 h. Los botones ordenan sólo las filas de datos; el total permanece al pie.</figcaption>
</figure>
```

**Cuándo:** consultar registros y su total aditivo; ofrece ordenación cuando ayuda a encontrar extremos. Sin `data-tabla` funciona como tabla estática.

**Límite:** el total lo calcula quien prepara los datos, no el DOM. No sumar porcentajes, tasas o promedios. Un solo `tbody`, sin celdas combinadas ni filas de subtotal dentro de él; no hay paginación o filtrado. La ordenación numérica requiere `data-valor`; ausencias quedan al final en ambos sentidos. Repetidos conservan su orden, `tfoot` no se mueve.

## Tabla con serie embebida

<!-- nota:ejemplo sparkline -->
```html
<figure class="ancho">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Serie semanal de solicitudes, desplazable">
    <table data-tabla data-min="0" data-max="120"><caption>Solicitudes de lunes a jueves · ejemplo</caption>
      <thead><tr><th scope="col">Canal</th><th scope="col">Serie L / M / X / J, dominio común 0–120</th><th scope="col">Último día</th></tr></thead>
      <tbody>
        <tr><th scope="row">Web</th><td data-sparkline><span class="sparkline-datos"><span data-valor="80">80</span>, <span data-valor="100">100</span>, <span data-valor="90">90</span>, <span data-valor="120">120</span></span></td><td class="numero">120</td></tr>
        <tr><th scope="row">App</th><td data-sparkline><span class="sparkline-datos"><span data-valor="40">40</span>, <span data-valor="">sin dato</span>, <span data-valor="70">70</span>, <span data-valor="60">60</span></span></td><td class="numero">60</td></tr>
      </tbody>
    </table>
  </div>
  <figcaption>Valores ilustrativos. Misma escala Y en ambas filas. El dato ausente corta la línea y todos los valores permanecen escritos.</figcaption>
</figure>
```

**Cuándo:** añadir tendencia a una tabla sin apartarse del registro. El texto de la celda nombra cada valor; el SVG es redundante y lleva `aria-hidden`.

**Límite:** X equidistante; todas las filas deben describir los mismos períodos. Exige `data-min`/`data-max` comunes y rechaza dibujar puntos fuera de ellos. No autoescala por fila, no es una gráfica con ejes ni codifica tiempo irregular; para eso usa la serie temporal. El texto sigue disponible si el dibujo no se puede generar.

<a id="recetas-sonido"></a>

## Sonido: un canal que empieza apagado

Pega [sonido.js](sonido.js) una vez al final, además del CSS. No necesita `interacciones.js`.

<!-- nota:ejemplo sonido -->
```html
<aside class="nota-sonido" data-canal-sonido aria-labelledby="sonido-titulo">
  <h3 id="sonido-titulo">Una señal breve.</h3>
  <p>Activa el sonido y prueba una señal. Cada acción también se describe en texto.</p>
  <div><button type="button" data-audio-activar aria-pressed="false">Activar sonido</button></div>
  <div>
    <button type="button" data-audio="accion" data-mensaje="Ejemplo de acción seleccionada.">Acción</button>
    <button type="button" data-audio="confirmacion" data-mensaje="Ejemplo de confirmación completada.">Confirmación</button>
    <button type="button" data-audio="atencion" data-mensaje="Ejemplo: revisa el dato antes de continuar.">Atención</button>
  </div>
  <p role="status" aria-live="polite">Sonido apagado.</p>
</aside>
```

**Cuándo:** confirmar una acción explícita y breve, en una experiencia donde la persona
ha optado por escuchar. No añade sonido a gráficos, scroll, foco, lectura, cambios de tema
ni entradas automáticas. El botón de activación no emite una señal. La preferencia no se
recuerda al recargar y vuelve a apagado al ocultar la pestaña.

**Límite:** Web Audio y gesto real de botón; eventos sintéticos no activan ni reproducen.
Las señales usan seno, ganancia pico 0,025, ataque 3 ms y caída a 0,0001 en 55 ms;
acción 660→440 Hz, confirmación 520→780 Hz, atención 440→360→440 Hz. Cada nota dura 60 ms,
separada por 5 ms; total 125 o 190 ms. Son decisiones de Nota, no mediciones del sitio.
Una nueva señal interrumpe la anterior. No son alarmas, sonificación de series ni audio de
fondo, y la ganancia digital no garantiza un nivel acústico en el dispositivo.
`NotaSonido.get(contenedor).disable()` apaga; `.destroy()` cierra el contexto y listeners.
`NotaSonido.init(contenedor)` inicializa HTML nuevo. No hay método público de reproducción
automática. `[data-sonido]` del sistema anterior conserva su comportamiento fuera del canal.

<a id="recetas-escritura"></a>

## Escritura: trazo a trazo

Pega [escritura.js](escritura.js) una vez al final. La frase de ejemplo está dibujada con
paths originales; la animación recorre **su longitud**, no un rectángulo que descubre texto.

<!-- nota:ejemplo escritura -->
```html
<figure class="ancho nota-escritura" data-escritura data-duracion="2400">
  <div class="escritura-caja" tabindex="0" role="region" aria-label="Escritura a mano, desplazable">
    <svg viewBox="0 0 420 110" aria-hidden="true">
      <path data-trazo d="M55 51 C43 38 27 51 30 68 C34 83 52 69 54 53 L52 76 Q58 78 65 71"/>
      <path data-trazo d="M96 77 L101 48 L99 69 Q111 41 120 52 L117 74 Q132 42 142 54 L140 74 Q142 81 151 73"/>
      <path data-trazo d="M179 53 C167 40 154 55 157 69 C161 84 179 68 180 54 L178 77 Q185 78 193 71"/>
      <path data-trazo d="M207 77 L212 49 L210 68 Q224 41 235 53 L232 74 Q236 81 246 72"/>
      <path data-trazo d="M274 50 C259 44 249 59 254 72 C260 85 280 75 281 61 Q279 50 271 51 Q270 58 289 56"/>
      <path data-trazo d="M28 91 Q123 84 214 91 T293 89"/>
    </svg>
  </div>
  <div class="escritura-controles">
    <button type="button" data-escribir>Repetir escritura</button>
    <button type="button" data-finalizar>Mostrar trazo completo</button>
  </div>
  <p data-texto-escritura>«a mano»</p>
  <p role="status" aria-live="polite">Trazo completo.</p>
  <figcaption>Gesto ilustrativo original de Nota Tikin. 2400 ms repartidos por la longitud de cada trazo; la frase siempre permanece escrita debajo.</figcaption>
</figure>
```

**Cuándo:** una anotación corta y secundaria que gana significado con el gesto del trazo.
Empieza completa; la persona decide repetirla. Conserva `.manuscrita` para texto corriente
que deba seleccionarse, traducirse o cambiar con datos.

**Límite:** recibe paths SVG ordenados, no transforma automáticamente cualquier fuente
en escritura cursiva. Cada path es un trazo continuo; separa levantamientos de lápiz en
paths distintos. No uses contornos de glifos rellenos si esperas un trazo central de pluma.
Al cambiar la frase, dibuja paths correspondientes y actualiza `data-texto-escritura`.
El SVG es redundante (`aria-hidden`), el texto equivalente es permanente. Admite 100–10000 ms,
no música sincronizada. Web Animations se cancela y completa al salir de pantalla, ocultar
la pestaña o activar movimiento reducido; no hay RAF ni colas que se reanuden al volver.
`NotaEscritura.get(elemento).play()`, `.finish()` y `.destroy()` controlan la instancia;
`.play()` respeta movimiento reducido. `NotaEscritura.init(elemento)` admite inserción tardía.

<a id="recetas-three"></a>

## Three.js: dispersión XYZ

Usa **una sola** inclusión externa para toda la nota (compartida con `NotaGlobo`):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js"></script>
```

Después pega [escena.js](escena.js) completo dentro de `<script>`, una vez, al final.
No necesita `globo.js`, `graficas.js`, controles externos ni importaciones adicionales.

<!-- nota:ejemplo xyz -->
```html
<figure class="ancho" data-escena="xyz" id="xyz-ejemplo">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Carga, latencia y memoria, tabla desplazable">
    <table><caption>Tres variables de una misma prueba</caption>
      <thead><tr><th scope="col">Prueba</th><th scope="col">Carga (req/s)</th><th scope="col">Latencia (ms)</th><th scope="col">Memoria (MB)</th></tr></thead>
      <tbody>
        <tr><th scope="row">A</th><td data-valor="10">10</td><td data-valor="80">80</td><td data-valor="100">100</td></tr>
        <tr><th scope="row">B</th><td data-valor="20">20</td><td data-valor="95">95</td><td data-valor="120">120</td></tr>
        <tr><th scope="row">C</th><td data-valor="35">35</td><td data-valor="140">140</td><td data-valor="150">150</td></tr>
        <tr><th scope="row">D</th><td data-valor="50">50</td><td data-valor="170">170</td><td data-valor="210">210</td></tr>
      </tbody>
    </table>
  </div>
  <figcaption>Datos ilustrativos. Posiciones X/Y/Z normalizadas por sus dominios, con valores reales en los ejes. Selecciona un registro para identificarlo; proyección ortográfica, sin tamaños por perspectiva.</figcaption>
</figure>
```

**Cuándo:** la tercera variable aporta una relación espacial que conviene explorar. Los
controles giran la vista e identifican registros sin depender de arrastrar ni acertar a un punto.
Si dos variables bastan, la dispersión SVG es más fácil de leer y comparar.

**Límite:** 1–100 registros finitos; sin ausencias, regresión, jitter ni inferencias de
correlación. Cada eje tiene dominio propio, por lo que distancia geométrica no equivale
a una métrica entre variables de unidades distintas. Los puntos pueden ocluirse: elegir
uno atenúa los demás y escribe su valor. El lienzo conserva 600 px de ancho mínimo con
scroll local; las etiquetas de ejes deben ser breves, con las unidades en las cabeceras.
La tabla siempre queda visible, con o sin WebGL. Ningún dato existe sólo en una textura.

## Three.js: etapas con duración

Misma instalación de `escena.js` y la misma inclusión única de Three.js.

<!-- nota:ejemplo etapas -->
```html
<figure class="ancho" data-escena="etapas" id="etapas-ejemplo">
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Duración por etapa, tabla desplazable">
    <table><caption>Dónde tarda una solicitud</caption>
      <thead><tr><th scope="col">Etapa</th><th scope="col">Tiempo (ms)</th><th scope="col">Qué ocurre</th></tr></thead>
      <tbody>
        <tr><th scope="row">1 · Recibir</th><td data-valor="20">20 ms</td><td>Leer la entrada.</td></tr>
        <tr><th scope="row">2 · Validar</th><td data-valor="40">40 ms</td><td>Comprobar el contrato.</td></tr>
        <tr><th scope="row">3 · Consultar</th><td data-valor="120">120 ms</td><td>Esperar la fuente de datos.</td></tr>
        <tr><th scope="row">4 · Responder</th><td data-valor="30">30 ms</td><td>Entregar la salida.</td></tr>
      </tbody>
    </table>
  </div>
  <figcaption>Ejemplo ilustrativo: 210 ms si las cuatro etapas ocurren en serie. Alturas proporcionales al tiempo, orden horizontal secuencial; anchura y profundidad constantes sin significado cuantitativo.</figcaption>
</figure>
```

**Cuándo:** explicar etapas de un proceso junto con su duración. Seleccionar una etapa
conecta su caja con la explicación escrita. Empieza inmóvil; el giro continuo es optativo.
Usa las barras SVG para comparar muchas categorías o cuando girar no aporte información.

**Límite:** 1–12 etapas en orden, duraciones no negativas. La altura cero no se infla para
hacer visible una caja. No representa dependencias, paralelismo, un waterfall acumulado
ni una simulación física. No sumes duraciones como tiempo total si las etapas se solapan.
Los números 1…N identifican las filas de la tabla. Rotar puede superponer etiquetas; los
valores exactos permanecen en la tabla y «Vista inicial» devuelve la composición inicial.

### Ciclo de vida de NotaEscena

| Operación | Contrato |
|---|---|
| `NotaEscena.init(raíz)` | Inicializa `data-escena` una vez por figura; el segundo llamado devuelve la instancia existente. |
| `new NotaEscena(figura)` | Alternativa manual; rechaza una segunda instancia para el mismo contenedor. |
| `NotaEscena.get(figura)` | Recupera la instancia automática. |
| `select(índice)` / `select(null)` | Selecciona una fila, índice desde cero, o muestra todas. Rechaza índices inexistentes. |
| `rotate(dx,dy)` | Giro manual inmediato, en radianes. |
| `pause()` / `resume()` | Desactiva/solicita giro. `resume()` respeta movimiento reducido, visibilidad y estado WebGL. |
| `destroy()` | Cancela RAF, aborta listeners, desconecta observers, libera geometrías/materiales/texturas/renderer y devuelve la tabla original. Es idempotente. |

El giro es 0,15 rad/s, limitado por tiempo, no por cuadros. Sólo hay RAF mientras la vista
es visible, la pestaña está activa, se pidió girar y no hay movimiento reducido. Cambiar
esa preferencia cancela el RAF pendiente; el giro manual sigue siendo instantáneo.
Colores leídos de los tokens claros/oscuros/Sea; los rótulos son canvas locales. Al retirar
la figura de una aplicación llama `destroy()`. Para reemplazar datos: destruye, modifica
la tabla e inicializa otra vez. No hay `fetch`, modelos, mapas ni imágenes externas.

## Límites de las piezas editoriales base

Estas condiciones complementan el HTML y el criterio de cada receta anterior. No cambian
las clases existentes; ayudan a elegir una pieza antes de copiarla.

| Pieza | Cuándo no usarla / qué no hace / qué puede romperla |
|---|---|
| Documento y temas | No reemplaza un formato solicitado distinto de HTML. Un solo selector y `data-theme` en la raíz; mezclar CSS parciales puede dejar tokens sin definir. |
| `.marca` | No señalar un párrafo entero ni expresar un estado sólo con el trazo. No transforma texto en enlace ni dibuja escritura animada. |
| `.con-margen` / `.margen` / `.nota` | No esconder una condición crítica al margen. Varias páginas de texto manuscrito desbordan el propósito de la anotación; el bloque base de margen es hijo directo de `.hoja`. |
| `.aviso` ×4 | No asignar urgencia a todos los párrafos. Una numeración no implica pasos ejecutables; para alertas dinámicas se necesita gestionar el anuncio sin duplicarlo. |
| `.mapa` | No negativos, ausencias ni datos nuevos con proporciones viejas. Esta receta fija sólo representa 60/25/15; usa barras si no vas a recalcular la rejilla. |
| `.dato` / `.datos` / `.pildora` | No falsear controles ni eliminar unidades para que quepan. No calculan ni validan datos; el texto debe incluir el estado además del color. |
| `.medida` | No representar una tarea en ejecución: usa `progress` para eso. `min/max/value`, porcentaje y texto deben describir el mismo denominador. |
| `.indice` / `.regla` | No en una nota breve. IDs duplicados, destinos inexistentes o falta de `data-lectura` rompen seguimiento; el tachado indica posición, no lectura demostrada. |
| `.codigo` | No sustituye un editor ni ejecuta código. Portapapeles puede estar denegado; conserva selección manual y estado. Resaltado escrito a mano, no detección automática de sintaxis. |
| `.tabla-caja` / `.densa` | No grandes bases de datos virtualizadas. Cinco o más columnas usan `densa`; alterar mínimos sin verificar 320/390 puede comprimir las celdas. |
| `.terminal` | No usar para una tabla analítica que necesite ordenar o cabeceras semánticas. Sólo copia texto, no ejecuta comandos. Las columnas dependen de mono y espacios; el ancho se desplaza dentro del `pre`. |
| `.extracto` | No degradar datos críticos ni aplicar máscara al único ejemplar del texto. La copia decorativa debe ser `aria-hidden`; la versión completa vive en `details`. |
| `.kept` | No envoltorio universal para el informe. No carga portadas ni convierte tarjetas en enlaces; añade un `a` real si hay navegación y datos de imagen incrustados. |
| `.manuscrita` / `.senalado` | No instrucciones críticas ni frases llenas de corchetes. Es tipografía estática y texto seleccionable; la animación exige los paths de `NotaEscritura`. |
| `NotaGlobo` | No topografía, fronteras políticas ni distancias medidas. Una instancia por contenedor, IDs de puntos/rutas únicos; `destroy()` al retirarlo. Sin Three/WebGL conserva lista y mensaje. |

## Alcance de esta versión

Es una librería de recetas HTML/CSS/JS copiables, sin instalación de framework. No incluye
un CLI de generación, React, una dependencia de shadcn, un constructor de consultas,
streaming, mapas políticos o conversión automática de fuentes a caligrafía. Cualquier pieza
nueva debe conservar los tres temas, los datos accesibles, los mínimos locales y el ciclo
de vida documentado. Los ejemplos no se publican ni envían datos.

## Segunda tanda: reportes, artículos y prototipos

Las siguientes recetas amplían el sistema; no cambian los anchos ni los estilos de documentos
previos. Incluye `fuentes.css`, `estilo.css` e `interacciones.js`. Añade [reportes.js](reportes.js)
para `data-reporte`, [visor.js](visor.js) para `data-visor`. El recorrido necesita además
`globo.js` y la única inclusión de Three 0.160.1. Los módulos son independientes de
`graficas.js`; no cargan red. `NotaReportes.init(raíz)` y `NotaVisores.init(raíz)` se pueden
repetir; `get(elemento).destroy()` retira la mejora y restaura los datos originales.
Para cambiar una tabla destruye, edita y vuelve a inicializar. No hay observador de datos.

## Apariencia y lectura cómoda

<!-- nota:ejemplo apariencia -->
```html
<div class="pieza" id="apariencia-ejemplo">
  <h3>Un papel para cada lectura</h3>
  <fieldset class="apariencia">
    <legend>Apariencia del documento</legend>
    <div class="apariencia-opciones">
      <label><input type="radio" name="papel-ejemplo" value="light" data-elegir-tema><span class="papel-muestra claro" aria-hidden="true"></span>Claro</label>
      <label><input type="radio" name="papel-ejemplo" value="dark" data-elegir-tema><span class="papel-muestra calido" aria-hidden="true"></span>Cálido</label>
      <label><input type="radio" name="papel-ejemplo" value="sea" data-elegir-tema><span class="papel-muestra sea" aria-hidden="true"></span>Sea</label>
      <label><input type="radio" name="papel-ejemplo" value="system" data-elegir-tema checked>Sistema</label>
    </div>
  </fieldset>
  <button type="button" data-comodidad aria-pressed="false">Lectura cómoda</button>
  <p>El color cambia el papel; la lectura cómoda amplía texto y datos secundarios.</p>
</div>
```

**Cuándo:** preferencias de lectura de una nota. Muestras, etiquetas y radios nativos ofrecen
selección y teclado sin un desplegable. Usar una vez en la cabecera; este segundo grupo existe
sólo como ejemplo del catálogo. Todos los grupos se sincronizan.

**Cuándo no / límite:** no es un selector de variantes del prototipo. `Sistema` sigue la
preferencia del SO; la elección manual vive en `data-theme`. Cada grupo necesita un `name`
propio. La lectura cómoda es optativa: cuerpo 18px/1,7, tablas 16px, rótulos secundarios 14px.
Las gráficas base suben a 13px dentro del SVG para no invadir sus márgenes. Se conserva el
`select[data-tema]` antiguo. Preferencias locales por origen, sin cookies ni red; si se bloquea
localStorage, funcionan durante la sesión. Los documentos que no incluyen `data-comodidad`
conservan su escala original aunque exista una preferencia guardada. Sin JS quedan controles
sin comportamiento y el contenido sigue legible con el tema del sistema.

## Ficha de decisión

<!-- nota:ejemplo decision -->
```html
<aside class="pieza ficha-decision" id="decision-ejemplo" aria-labelledby="decision-titulo">
  <p class="ceja">Decisión 02 · ejemplo</p>
  <h3 id="decision-titulo">Una revisión al final del registro</h3>
  <p>Validar la información en un único paso antes de enviarla.</p>
  <dl>
    <div><dt>Por qué</dt><dd>Permite detectar omisiones sin pedir a la persona que repita datos.</dd></div>
    <div><dt>Alternativa considerada</dt><dd>Confirmar cada campo por separado; interrumpe la tarea con demasiada frecuencia.</dd></div>
    <div><dt>Qué falta comprobar</dt><dd>Que se detecten los errores antes del envío en una prueba de uso.</dd></div>
    <div><dt>Cuándo revisarla</dt><dd>Si la revisión final se omite o no ayuda a corregir los errores.</dd></div>
  </dl>
</aside>
```

**Cuándo:** conservar el razonamiento de una decisión con sus condiciones de revisión.
**Cuándo no / límite:** no es un aviso urgente ni un registro de aprobación. El estado,
responsables y fechas son contenido editorial; no guarda aceptación, firmas ni historial.

## Cronología anotada

<!-- nota:ejemplo cronologia -->
```html
<div class="pieza" id="cronologia-ejemplo">
  <h3>De la observación a la prueba</h3>
  <ol class="cronologia">
    <li><time datetime="2026-09-01">01 sep 2026</time><div><h4>Observar</h4><p>Se registran las dudas al completar un formulario.</p></div></li>
    <li><time datetime="2026-09-04">04 sep 2026</time><div><h4>Prototipar</h4><p>Se reúnen los campos en dos pasos y se añade una revisión final.</p></div></li>
    <li><time datetime="2026-09-14">14 sep 2026</time><div><h4>Contrastar</h4><p>Se prepara una prueba con tareas, criterios de éxito y observaciones.</p></div></li>
  </ol>
  <p class="procedencia">Cronología ilustrativa; no representa una prueba realizada.</p>
</div>
```

**Cuándo:** ordenar eventos y explicar qué cambió. En móvil la fecha queda sobre su evento.
**Cuándo no / límite:** no codifica duración ni distancia temporal; el espacio entre filas no
representa días. Para comparar duraciones usa etapas. No afirma causalidad por proximidad.

## Ficha de artículo

<!-- nota:ejemplo articulo -->
```html
<div class="pieza" id="articulo-ejemplo">
  <h3>El contexto antes de empezar</h3>
  <dl class="ficha-articulo">
    <div><dt>Autoría</dt><dd>Equipo editorial</dd></div>
    <div><dt>Publicado</dt><dd><time datetime="2026-09-14">14 sep 2026</time></dd></div>
    <div><dt>Tipo de pieza</dt><dd>Ensayo con ejemplos</dd></div>
    <div><dt>Revisión</dt><dd>Primera edición</dd></div>
  </dl>
  <p>Una propuesta para separar lo observado de lo supuesto al escribir un informe.</p>
</div>
```

**Cuándo:** artículos que necesitan autoría, fecha y estado editorial sin ocupar una portada.
**Cuándo no / límite:** no inventa tiempo de lectura, credenciales ni revisión por pares. Los
campos son opcionales y no son botones. No genera metadatos SEO ni tarjetas para redes.

## Referencias con regreso al texto

<!-- nota:ejemplo referencias -->
```html
<div class="pieza" id="referencias-ejemplo">
  <h3>La evidencia queda a un paso</h3>
  <p>Una afirmación debe permitir volver a su origen
    <a id="llamada-fuente-1" href="#fuente-1" aria-label="Consultar referencia 1">[1]</a>.
    Cuando una cifra es ilustrativa, debe decirlo
    <a id="llamada-fuente-2" href="#fuente-2" aria-label="Consultar referencia 2">[2]</a>.</p>
  <ol class="nota-referencias" aria-label="Referencias del ejemplo">
    <li id="fuente-1" tabindex="-1">Nota metodológica del ejemplo: acompañar cada afirmación con su procedencia.
      <a href="#llamada-fuente-1" aria-label="Volver a la llamada de referencia 1">Volver al texto ↑</a></li>
    <li id="fuente-2" tabindex="-1">Los ejemplos de esta biblioteca no representan datos de producción.
      <a href="#llamada-fuente-2" aria-label="Volver a la llamada de referencia 2">Volver al texto ↑</a></li>
  </ol>
</div>
```

**Cuándo:** citas, aclaraciones o fuentes extensas que interrumpirían el párrafo. Funcionan sin JS.
**Cuándo no / límite:** no es una bibliografía automática. IDs únicos por nota y una llamada
por retorno; si una fuente se cita varias veces, añade retornos distintos y explícitos. Las
fuentes reales requieren autor, título, fecha y enlace verificable. Estas dos son aclaraciones
internas, no citas bibliográficas. Mantén llamada y referencia en la misma página multipágina.

## Glosario editorial

<!-- nota:ejemplo glosario -->
```html
<div class="pieza" id="glosario-ejemplo">
  <h3>Palabras que conviene acordar</h3>
  <dl class="nota-glosario">
    <div><dt><dfn>Observación</dfn></dt><dd>Lo que se registró directamente, con su contexto y procedencia.</dd></div>
    <div><dt><dfn>Hipótesis</dfn></dt><dd>Explicación provisional que puede contrastarse con evidencia.</dd></div>
    <div><dt><dfn>Prototipo</dfn></dt><dd>Representación parcial de una solución para explorar una pregunta.</dd></div>
  </dl>
</div>
```

**Cuándo:** vocabulario propio de un informe o artículo que necesita definiciones compartidas.
**Cuándo no / límite:** no es una ayuda que aparece sólo al pasar el cursor; las definiciones
permanecen visibles. No incluye búsqueda ni traduce términos. Las definiciones son editoriales.

## Metodología desplegable

<!-- nota:ejemplo metodologia -->
```html
<div class="pieza" id="metodologia-ejemplo">
  <h3>Cómo leer esta evidencia</h3>
  <p>El ejemplo compara la duración declarada de una tarea bajo dos supuestos.</p>
  <details class="metodologia">
    <summary>Consultar método, supuestos y exclusiones</summary>
    <dl class="nota-glosario">
      <div><dt>Unidad</dt><dd>Minutos por operación; volumen mensual constante.</dd></div>
      <div><dt>Supuesto</dt><dd>Las tareas comparadas tienen el mismo alcance.</dd></div>
      <div><dt>Exclusión</dt><dd>No incluye capacitación, espera ni fallos de otros sistemas.</dd></div>
      <div><dt>Límite</dt><dd>El resultado estima capacidad, no demuestra ahorro realizado.</dd></div>
    </dl>
  </details>
</div>
```

**Cuándo:** explicar detalles del método después de un resumen que ya declara el límite principal.
**Cuándo no / límite:** no ocultes condiciones que cambian la conclusión. `details` funciona sin
JS; `interacciones.js` abre y restaura el método al imprimir. No verifica ni ejecuta el método.

## Antes y después editorial

<!-- nota:ejemplo antes-despues -->
```html
<figure class="pieza ancho" id="antes-despues-ejemplo">
  <h3>Un cambio que se puede leer</h3>
  <div class="antes-despues">
    <div><h4>Antes · mensaje genérico</h4><p><del>No se pudo completar la acción.</del></p><p>La persona debe adivinar qué falta.</p></div>
    <div class="despues"><h4>Después · siguiente paso concreto</h4><p><ins>Añade la fecha del registro para continuar.</ins></p><p>El mensaje identifica el campo que necesita atención.</p></div>
  </div>
  <figcaption>Ejemplo de redacción. Las dos versiones permanecen completas; en móvil se leen una después de otra.</figcaption>
</figure>
```

**Cuándo:** mostrar una corrección de texto, una decisión de interfaz o una revisión de contenido.
**Cuándo no / límite:** no calcula un diff, ni compara capturas con un deslizador. `del`/`ins`
identifican cambios editoriales; para alternativas sin relación temporal usa comparación.

## Cascada de cantidades

<!-- nota:ejemplo cascada -->
```html
<figure class="pieza ancho" id="cascada-ejemplo" data-reporte="cascada">
  <h3>Cómo se llega al resultado</h3>
  <p>Horas disponibles, ajustes y trabajo añadido. Cada tramo empieza donde termina el anterior.</p>
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Balance de capacidad en horas, desplazable">
    <table><caption>Balance ilustrativo · eje X en horas</caption>
      <thead><tr><th scope="col">Concepto</th><th scope="col">Cambio (h)</th><th scope="col">Acumulado (h)</th></tr></thead>
      <tbody>
        <tr><th scope="row">Capacidad inicial</th><td data-valor="120">+120</td><td>120</td></tr>
        <tr><th scope="row">Mantenimiento</th><td data-valor="-30">−30</td><td>90</td></tr>
        <tr><th scope="row">Apoyo adicional</th><td data-valor="20">+20</td><td>110</td></tr>
        <tr><th scope="row">Revisión</th><td data-valor="-15">−15</td><td>95</td></tr>
      </tbody>
      <tfoot><tr><th scope="row">Resultado</th><td>Horas netas</td><td>95</td></tr></tfoot>
    </table>
  </div>
  <figcaption>Ejemplo: 120 − 30 + 20 − 15 = 95 h. Signos y tabla distinguen aumentos y reducciones sin depender del color.</figcaption>
</figure>
```

**Cuándo:** explicar un total como suma de aportes positivos y negativos en la misma unidad.
**Cuándo no / límite:** no sumar tasas, porcentajes ni monedas distintas. Tres columnas,
1–60 filas; valores y acumulados finitos de hasta ±10⁹. La primera fila también es un cambio
desde cero; no admite subtotales intermedios ni reinicios. El módulo calcula acumulados y
resultado, nunca toma la tercera columna como entrada. Tabla visible y dibujo de 860px con
scroll local. Cero y todos los acumulados están en la escala. Sin animación.

## Pequeños múltiples con escala común

<!-- nota:ejemplo multiples -->
```html
<figure class="pieza amplio" id="multiples-ejemplo" data-reporte="multiples">
  <h3>La misma pregunta en tres sedes</h3>
  <p>Solicitudes por semana. Los tres paneles comparten el eje Y; el eje X corresponde al orden de la tabla.</p>
  <div class="tabla-caja" tabindex="0" role="region" aria-label="Solicitudes por sede y semana, desplazable">
    <table><caption>Solicitudes semanales · ejemplo · eje Y en solicitudes</caption>
      <thead><tr><th scope="col">Período</th><th scope="col">Bogotá</th><th scope="col">Medellín</th><th scope="col">Cali</th></tr></thead>
      <tbody>
        <tr><th scope="row">1 · Semana 1</th><td data-valor="40">40</td><td data-valor="20">20</td><td data-valor="30">30</td></tr>
        <tr><th scope="row">2 · Semana 2</th><td data-valor="60">60</td><td data-valor="30">30</td><td data-valor="">Sin dato</td></tr>
        <tr><th scope="row">3 · Semana 3</th><td data-valor="50">50</td><td data-valor="35">35</td><td data-valor="40">40</td></tr>
        <tr><th scope="row">4 · Semana 4</th><td data-valor="80">80</td><td data-valor="40">40</td><td data-valor="45">45</td></tr>
      </tbody>
    </table>
  </div>
  <figcaption>Datos ilustrativos. Escala común de 0 a 80; sin dato corta el trazo. La pendiente no demuestra causalidad.</figcaption>
</figure>
```

**Cuándo:** comparar patrones de hasta cuatro grupos sin superponer sus líneas.
**Cuándo no / límite:** los períodos son equidistantes y deben ser los mismos para todos los
grupos; no codifica fechas irregulares. Entre 2 y 60 filas. Valores finitos de hasta ±10⁹,
vacío distinto de cero. Cada panel conserva 360px mínimos dentro de su región desplazable.
Sin valores, el dominio convencional es 0–1 y no hay puntos; no se inventan observaciones.

## Conciliación de registros

<!-- nota:ejemplo conciliacion -->
```html
<figure class="pieza amplio" id="conciliacion-ejemplo" data-reporte="conciliacion">
  <h3>Una diferencia necesita explicación</h3>
  <div class="tabla-caja densa" tabindex="0" role="region" aria-label="Conciliación de operaciones, desplazable">
    <table class="tabla-calculo"><caption>Operaciones esperadas y observadas · ejemplo</caption>
      <thead><tr><th scope="col">Canal</th><th scope="col">Esperadas</th><th scope="col">Observadas</th><th scope="col">Diferencia</th><th scope="col">Explicación</th></tr></thead>
      <tbody>
        <tr><th scope="row">Web</th><td data-valor="120">120</td><td data-valor="118">118</td><td>−2</td><td>Dos operaciones siguen en revisión.</td></tr>
        <tr><th scope="row">App</th><td data-valor="80">80</td><td data-valor="80">80</td><td>0</td><td>Conteos coincidentes.</td></tr>
        <tr><th scope="row">Asistido</th><td data-valor="30">30</td><td data-valor="33">33</td><td>+3</td><td>Tres registros pendientes de clasificar.</td></tr>
      </tbody>
      <tfoot><tr><th scope="row">Total</th><td>230</td><td>231</td><td>1</td><td>El saldo neto no compensa las diferencias por canal.</td></tr></tfoot>
    </table>
  </div>
  <figcaption>Datos ilustrativos. Diferencia = observado − esperado; una diferencia cero no prueba igualdad de los registros individuales.</figcaption>
</figure>
```

**Cuándo:** comparar conteos esperados/observados y conservar la explicación por fila.
**Cuándo no / límite:** requiere conteos enteros no negativos (≤10⁹), no importes monetarios.
No cruza IDs, no detecta duplicados ni demuestra conciliación contable. Si falta un observado,
el total indica incompleto y no da un saldo neto. Cinco columnas exactas, hasta 60 filas.
Las explicaciones son editoriales: el módulo no las infiere de la diferencia.

## Calculadora de escenarios

<!-- nota:ejemplo escenario -->
```html
<div class="pieza ancho" id="escenario-ejemplo" data-reporte="escenario">
  <h3>¿Qué cambia si la tarea toma menos tiempo?</h3>
  <p>Explora capacidad mensual con un volumen fijo. Los valores iniciales son ilustrativos.</p>
  <form class="escenario-form" aria-label="Supuestos de capacidad mensual">
    <label>Operaciones al mes<input name="volumen" type="number" min="0" max="1000000" step="1" value="1200" required></label>
    <label>Antes, minutos por operación<input name="antes" type="number" min="0" max="1440" step="0.1" value="8" required></label>
    <label>Después, minutos por operación<input name="despues" type="number" min="0" max="1440" step="0.1" value="5" required></label>
    <button type="reset">Restablecer supuestos</button>
  </form>
  <div class="escenario-resultados">
    <output data-resultado aria-live="polite">60 h/mes liberadas</output>
    <p data-formula>1.200 × (8 − 5) ÷ 60 = 60 h/mes. Es capacidad estimada, no ahorro monetario ni una predicción.</p>
  </div>
</div>
```

**Cuándo:** explicar la sensibilidad de un resultado a supuestos explícitos y reversibles.
**Cuándo no / límite:** modelo lineal de capacidad, sin simulación, predicción ni valoración
financiera. Minutos no negativos, hasta un día por operación y un millón de operaciones al mes;
volumen entero y tiempos en décimas. Si después es mayor, muestra horas adicionales. Vacíos y
entradas fuera de límites invalidan el resultado; no conserva silenciosamente una cifra previa.
Sin JS se ve el cálculo inicial; no usar los controles como formulario de recolección.

## Globo narrado por etapas

<!-- nota:ejemplo recorrido -->
```html
<figure class="pieza ancho" id="recorrido-ejemplo" data-reporte="recorrido">
  <h3>Seguir el viaje de una idea</h3>
  <p>Una ruta por etapa, con contexto escrito. Selecciona anterior o siguiente para orientar el globo.</p>
  <div data-recorrido-globo></div>
  <div class="acciones">
    <button type="button" data-paso="prev">← Etapa anterior</button>
    <button type="button" data-paso="next">Etapa siguiente →</button>
  </div>
  <p data-recorrido-estado role="status">Tres etapas ilustrativas; el recorrido empieza inmóvil.</p>
  <ol class="recorrido-pasos">
    <li data-ruta="idea-bog-mad"><strong><span data-lugar="BOG" data-lat="4.711" data-lon="-74.0721">Bogotá</span> → <span data-lugar="MAD" data-lat="40.4168" data-lon="-3.7038">Madrid</span></strong><p>Se comparte la primera propuesta para revisión.</p></li>
    <li data-ruta="idea-mad-hnd"><strong><span data-lugar="MAD" data-lat="40.4168" data-lon="-3.7038">Madrid</span> → <span data-lugar="HND" data-lat="35.5494" data-lon="139.7798">Tokio</span></strong><p>La propuesta se convierte en una prueba de interacción.</p></li>
    <li data-ruta="idea-hnd-bog"><strong><span data-lugar="HND" data-lat="35.5494" data-lon="139.7798">Tokio</span> → <span data-lugar="BOG" data-lat="4.711" data-lon="-74.0721">Bogotá</span></strong><p>Las observaciones regresan al equipo que decide.</p></li>
  </ol>
  <figcaption>Relato ficticio. Las coordenadas son geográficas; no representan vuelos, distancias ni actividad real.</figcaption>
</figure>
```

**Cuándo:** la ubicación y el orden de una historia importan. Las etapas escritas siempre están
visibles; el mapa orienta una ruta a la vez. Incluye Three una sola vez y `globo.js` antes de
`reportes.js`. Comparte la dependencia con todos los demás globos/escenas del documento.

**Cuándo no / límite:** no convierte etapas abstractas en geografía. `data-lugar` identifica
un lugar; repetir un ID exige las mismas coordenadas y nombre. Cada ruta necesita un ID único
y dos lugares. No autoavanza ni añade sonido. Empieza pausado; conserva controles de NotaGlobo,
reduce, pausa por visibilidad y destroy. Sin Three queda mensaje y relato; sin WebGL queda
además la lista de rutas. No añade mapas, texturas ni geocodificación remota.

## Visor de prototipos con estados

<!-- nota:ejemplo visor -->
```html
<figure class="pieza amplio" id="visor-ejemplo" data-visor>
  <h3>Una interfaz, varios tamaños</h3>
  <p>Explora los estados vacío, revisión y confirmado de un registro ilustrativo.</p>
  <div class="acciones" role="group" aria-label="Ancho de la vista del prototipo">
    <button type="button" data-ancho-visor="320" aria-pressed="false">320 px</button>
    <button type="button" data-ancho-visor="390" aria-pressed="true">390 px</button>
    <button type="button" data-ancho-visor="768" aria-pressed="false">768 px</button>
    <button type="button" data-ancho-visor="1024" aria-pressed="false">1024 px</button>
    <button type="button" data-ancho-visor="auto" aria-pressed="false">Ajustar</button>
    <button type="button" data-reiniciar-visor>Reiniciar ejemplo</button>
  </div>
  <p data-visor-estado role="status">Vista inicial: 390 px CSS.</p>
  <div class="visor-caja" tabindex="0" role="region" aria-label="Prototipo interactivo, desplazable horizontalmente"></div>
  <template data-prototipo>
    <style>
      .demo { padding: 24px; min-width: 0; }
      .demo nav { display: flex; flex-wrap: wrap; gap: 8px; padding-bottom: 20px; border-bottom: 1px solid var(--pieza-linea); }
      .demo button { min-height: 44px; padding: 8px 12px; color: var(--pieza-tinta); background: var(--pieza-papel); border: 1px solid var(--pieza-linea); border-radius: 4px; font: inherit; cursor: pointer; }
      .demo button[aria-pressed='true'] { background: var(--pieza-suave); border-color: var(--pieza-acento); }
      .demo h2 { font: 400 32px/1.15 var(--serif); margin: 0 0 16px; }
      .demo p { margin: 0 0 18px; overflow-wrap: anywhere; }
      .demo .contexto { margin-top: 24px; font-size: 14px; color: var(--pieza-secundaria); }
      .demo article { padding-top: 28px; }
      .demo dl { margin: 0 0 20px; display: grid; gap: 12px; }
      .demo dt { font-size: 13px; color: var(--pieza-secundaria); }
      .demo dd { margin: 0; }
      .demo .estado { padding: 16px; border: 1px dashed var(--pieza-linea); }
      @container (min-width: 600px) {
        .demo article { display: grid; grid-template-columns: minmax(0,1.5fr) minmax(0,1fr); gap: 32px; }
        .demo .contexto { margin-top: 0; padding-top: 4px; }
      }
    </style>
    <div class="demo">
      <nav aria-label="Estados del prototipo">
        <button type="button" data-demo-ir="vacio" aria-pressed="true">Vacío</button>
        <button type="button" data-demo-ir="revision" aria-pressed="false">Revisión</button>
        <button type="button" data-demo-ir="confirmado" aria-pressed="false">Confirmado</button>
      </nav>
      <article data-demo-pagina="vacio">
        <div><h2>Tu primer registro</h2><p>Todavía no hay registros en este ejemplo.</p><button type="button" data-demo-ir="revision">Crear borrador de ejemplo</button></div>
        <aside class="contexto"><p>Empieza con un nombre, una fecha y una explicación del movimiento.</p><p class="estado">Estado: sin registros</p></aside>
      </article>
      <article data-demo-pagina="revision" hidden>
        <div><h2>Revisa antes de confirmar</h2><dl><div><dt>Nombre</dt><dd>Sesión de revisión</dd></div><div><dt>Fecha</dt><dd>14 de septiembre de 2026</dd></div><div><dt>Duración</dt><dd>30 minutos</dd></div></dl><button type="button" data-demo-ir="confirmado">Confirmar ejemplo</button></div>
        <aside class="contexto"><p>Comprueba los datos del borrador. Este prototipo usa un registro fijo para explorar la interacción.</p><p class="estado">Estado: pendiente de confirmar</p></aside>
      </article>
      <article data-demo-pagina="confirmado" hidden>
        <div><h2>Registro confirmado</h2><p>La sesión de revisión aparece en el ejemplo con su fecha y duración.</p><button type="button" data-demo-ir="vacio">Volver al inicio</button></div>
        <aside class="contexto"><p class="estado">Estado: confirmado en el prototipo</p><p>No se envió ni se guardó información.</p></aside>
      </article>
    </div>
  </template>
  <div class="visor-fuente"><h4>Estados del ejemplo</h4><ol><li>Vacío: crear un borrador de ejemplo.</li><li>Revisión: sesión del 14-sep-2026, 30 minutos, pendiente de confirmar.</li><li>Confirmado: resultado ilustrativo; no se envían datos.</li></ol></div>
  <figcaption>Vista interactiva local. El ancho conserva píxeles CSS reales; en una pantalla pequeña se desplaza la región completa.</figcaption>
</figure>
```

**Cuándo:** documentar estados de un componente o recorrer un prototipo pequeño dentro de un
artículo. El lienzo cambia entre 320, 390, 768, 1024 y el espacio disponible. Reiniciar reconstruye
la muestra original. El texto alternativo aparece sin JS y al imprimir. No carga archivos.

**Cuándo no / límite:** no es un emulador de iPhone, una captura ni un navegador remoto. No
modifica la densidad de píxeles, el motor o el viewport del documento. Usa **Shadow DOM y
`@container`**, por eso las reglas responsivas del prototipo deben consultar el contenedor;
`@media (width)` seguiría midiendo la ventana exterior. No hay iframe porque la CSP lo bloquea.
El template contiene HTML/CSS de confianza, sin guiones ni manejadores `on…`; no es un sandbox
para HTML ajeno. Los botones `data-demo-ir` activan un `data-demo-pagina` del mismo visor;
no envían formularios, calculan datos ni persisten cambios. Los IDs, si se usan, viven dentro
del shadow. Los estilos del documento no entran, pero sí se heredan sus tokens y fuentes.
El contenido del prototipo debe respetar reduce; el visor no inicia RAF ni transiciones.
`NotaVisores.get(figura).setWidth('768')` permite controlar el ancho; `reset()` reinicia y
`destroy()` devuelve la alternativa textual y retira listeners/observer.

## Elegir y copiar desde el catálogo

`plantilla.html` ofrece búsqueda por nombre/propósito y el HTML exacto de cada receta en un
`details` junto al ejemplo. La búsqueda filtra **el índice de recetas**, no borra secciones de
la nota ni altera su progreso. Acentos y mayúsculas no cambian los resultados. El índice
completo sigue disponible sin JS. El botón usa el mismo contrato de copia y alternativa por
selección de `interacciones.js`. El módulo [catalogo.js](catalogo.js) sólo hace falta en un
catálogo que incluya `data-buscador-recetas`; no se necesita en artículos normales.

Las muestras son componentes de documento, no un constructor de aplicaciones. Cada snippet
requiere las fuentes y módulos indicados arriba; el botón copia el componente, no toda la
biblioteca. La plantilla y los ejemplos completos sí son autocontenidos.
