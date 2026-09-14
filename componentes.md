# Componentes de Nota Tikin

Los bloques siguientes son HTML completo de componente, para copiar dentro de `.hoja`, después
de pegar `estilo.css` en `<style>`. Los comportamientos se activan pegando `interacciones.js`
una vez al final del documento. No introducen clases de Tailwind ni dependen de React.

## Documento y temas

```html
<title>Nota — decisión y evidencia</title>
<meta charset="utf-8">
<style>/* Pegar aquí estilo.css completo */</style>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Geist:wght@400;500;600&family=Geist+Mono:wght@400;500&family=Reenie+Beanie&display=swap">
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

```html
<div class="barra">
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
    <figure class="amplio">…</figure>   <!-- hermana de la sección, no hija -->
  </article>

  <article class="pagina" id="p2" data-pagina hidden>…</article>

  <div class="paginacion" data-paginacion>
    <button type="button" data-nav="prev"><span class="et">Anterior</span><span class="tit"></span></button>
    <button type="button" data-nav="next"><span class="et">Siguiente</span><span class="tit"></span></button>
  </div>
  <footer class="pie">…</footer>
</main>

<script>/* interacciones.js */</script>
<script>/* multipagina.js — DESPUÉS del anterior */</script>
```

**Cuándo:** un informe con capítulos que se leen por separado y merecen cada uno su temario. No
para una nota de tres secciones: ahí la página única con índice lateral es mejor.

**La rejilla va en `.pagina`, no en `.hoja`.** Por eso la clase es `multipagina` y no
`por-seccion`: con las páginas de por medio, el selector `>` de `por-seccion` ya no alcanza a las
secciones y todo termina del ancho del párrafo.

**El orden de los guiones importa.** El índice de `interacciones.js` mide todos los enlaces del
documento; las secciones ocultas miden cero y las cree ya leídas, así que tacha el temario
completo. `multipagina.js` lo recalcula sobre la página viva usando `aqui-visto` y `aqui-actual`,
y la hoja anula las marcas del otro. Si sólo pegas uno de los dos, verás el temario tachado.

El botón activo lleva `aria-current="page"`; el hash conserva la página abierta, así que un enlace
a un capítulo concreto funciona. Al cambiar de página se emite `nota:pagina` por si hay que
arrancar un lienzo o recalcular una figura.

## Tablas densas

```html
<figure class="amplio">
  <div class="tabla-caja densa" tabindex="0" role="region" aria-label="Brechas, desplazable">
    <table><caption>Seis columnas no caben en un teléfono</caption>…</table>
  </div>
</figure>
```

**Cuándo:** desde cinco columnas. `.tabla-caja table` ya trae `min-width: 34rem`; `densa` lo sube a
`58rem`. Sin ese mínimo la tabla no se desplaza, se comprime: medido a 390 px, seis columnas daban
celdas de 50 px y filas de **581 px de alto**. Con `densa`, celdas de 139–285 px y filas de 140 px.
El desplazamiento es local —la página nunca se mueve de lado— y la caja es alcanzable por teclado.

## Terminal

```html
<figure class="ancho">
  <div class="terminal">
    <div class="cab"><span>saldo por bolsillo · producción</span>
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
  <figcaption>Medido el 12-sep. La columna que importa va señalada, no en negrita.</figcaption>
</figure>
```

**Cuándo:** una salida de consola, una consulta y su resultado, un volcado — cuando la evidencia
*es* el texto tal como se vio. No para código fuente de ejemplo: para eso está `.codigo`.

Se queda **oscura en los dos temas** a propósito: una terminal clara no se lee como una terminal.
La variante Sea sí cambia sus tonos, porque ahí el documento entero es oscuro y una caja con otro
negro se vería sucia. El botón de copia usa el mismo `data-copiar` del sistema. Alinea las columnas
con espacios dentro del `<pre>`; no uses una tabla disfrazada.

## Nota manuscrita señalada

```html
<p class="manuscrita">las fechas dicen cuándo pasó cada cosa. lo que explica cómo una llevó a la
  otra está <span class="senalado"><a href="#brechas">en las brechas</a></span>, donde dejo de
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
