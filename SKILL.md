---
name: nota-tikin
description: >-
  Diseña los artefactos e informes HTML de Angel y Tikin con una librería editorial de componentes copiables: lectura serif/sans, figuras anchas, tablas, gráficas a escala, mapas de calor, anotaciones, escritura por trazos, sonido optativo y escenas Three.js con alternativa textual. Siempre en claro, oscuro cálido y Dark Sea, autocontenidos y compatibles con la CSP de artefactos.
---

# Nota Tikin

Angel eligió cmrg.me como referencia para sus artefactos. El resultado debe sentirse como un
cuaderno editorial: una idea principal, lectura tranquila y evidencia que puede ocupar más
espacio. Aplica este lenguaje a los entregables HTML; conserva el formato si se pidió Markdown,
una hoja de cálculo u otro medio.

## ⚠️ La trampa de los anchos

El sistema base exige que `.ancho` y `.amplio` sean **hijos directos de `.hoja`**. Si el documento
se organiza en `<section>` y una figura vive *dentro* de una sección, queda atrapada en la columna
central y termina **más angosta que el párrafo** — que es exactamente lo contrario de lo que se
busca. Ya pasó una vez y Angel lo detectó de inmediato.

Para documentos con secciones, añade la clase `por-seccion` a `.hoja`: repite la rejilla en cada
bloque y las figuras vuelven a desbordar.

**La misma trampa reaparece en multipágina.** Si metes `<article class="pagina">` entre `.hoja` y
las secciones, `por-seccion` deja de alcanzar —usa `>`— y **todo vuelve a medir lo mismo**: texto y
figura daban 1514 px los dos. Usa `multipagina` en vez de `por-seccion` y cada página vuelve a
declarar la rejilla: 560 px de texto contra 992 y 1216 de figura.

```html
<main class="hoja por-seccion">
  <section class="seccion" id="x">
    <p>texto…</p>
    <figure class="amplio">…</figure>   <!-- ahora sí desborda -->
  </section>
</main>
```

**Medidas de la referencia** (viewport 1514 px): texto **33rem** (528 px), figura **48rem**
(768 px) = **1,44×**, ambas **concéntricas**. `.amplio` llega a 62rem.

**Verificar antes de publicar**, con el documento servido en local:

```js
const p=document.querySelector('.seccion p').getBoundingClientRect();
const f=document.querySelector('.amplio').getBoundingClientRect();
({proporcion:(f.width/p.width).toFixed(2),
  concentricos:Math.abs((p.left+p.width/2)-(f.left+f.width/2))<3,
  desborde:document.documentElement.scrollWidth>innerWidth})
```

Comprobar también que el índice lateral no pise las figuras anchas, que la regla derecha tampoco,
y que el título no quede debajo de la barra fija.

## Empezar por la pieza

Lee [estilo.css](estilo.css) y copia la hoja completa dentro de `<style>`; no la recrees de memoria.
Incluye también [fuentes.css](fuentes.css), con los WOFF2 incrustados y sus avisos OFL.
Las familias y pesos son los mismos: la incrustación elimina descargas de fuentes durante la lectura.
Para un informe de varios capítulos, añade [multipagina.js](multipagina.js).
La muestra editorial completa está en [informe.html](informe.html): cuatro capítulos,
apariencia, gráficas, escenario y prototipo. [multipagina.html](multipagina.html) conserva
el ejemplo mínimo compatible con documentos anteriores.
[componentes.md](componentes.md) contiene el HTML y los criterios de cada componente.
[plantilla.html](plantilla.html) muestra todos juntos. Usa solo los que expliquen el contenido;
la plantilla es un catálogo, no una estructura obligatoria para cada informe.

La revisión de septiembre de 2026 está en [referencia-cmrg.md](referencia-cmrg.md): 16 rutas,
estilos calculados, movimiento, fuentes de cada medida y límites de lo observado. Lee las
fuentes actuales antes de modificar piezas; amplía de forma aditiva para conservar artefactos.

- Abre con la decisión, el hallazgo o la pregunta concreta. Luego explica la evidencia y el límite.
- Conserva la lectura en `.hoja`, con un máximo de `35rem`; no fijes un ancho en píxeles.
- Pon tablas, código extenso y gráficos en `.ancho` (`62rem`) o `.amplio` (`76rem`), como hijos
  directos de `.hoja`. Los anchos se contraen con el viewport.
- Usa una ceja en mono para fecha, versión o procedencia, no como decoración repetida.
- Cada cifra real lleva fuente, unidad y fecha cuando corresponde. Identifica los datos de ejemplo.

## Tres invariantes de Angel

1. **Claro y oscuro siempre.** Empieza en la preferencia del sistema y ofrece el selector
   `Sistema / Claro / Oscuro cálido / Dark Sea`. `data-theme` vive en `document.documentElement`.
  El claro es una adaptación; cmrg.me sirve una pantalla oscura cálida, no una pareja de temas.
   Además están disponibles Oliva (`oliva`), Arcilla (`arcilla`) y Ciruela (`ciruela`). Son
   paletas completas optativas; no sustituyen Claro, Cálido o Sea. El icono de Ciruela es luna.
2. **Nada se corta.** Resuelve el ancho con la rejilla y `min-width:0`. No uses márgenes negativos,
   offsets absolutos para contenido, `overflow-x:hidden` en el documento ni elipsis para datos.
   Una tabla o código demasiado ancho tiene desplazamiento local, foco y nombre accesible.
   Un diagrama debe mantener texto legible: reordena su composición en móvil o permite desplazar
   el gráfico completo dentro de una región; no lo reduzcas hasta volverlo ilegible.
3. **El ancho no es único.** Texto angosto, figuras anchas. No encierres `.ancho` dentro de una
   sección angosta: usa secciones de texto y figuras como hermanos en `.hoja`.

## Decisiones de tipografía y color

- **Instrument Serif 400** para títulos. Conserva la condensación, el contraste de trazo y el
  gesto editorial de Editorial New; no es idéntica. La frase de comparación a 48 px midió
  `524.64px` frente a `627.69px` en Editorial New. Por eso esta hoja usa su propia escala,
  no una sustitución silenciosa con los mismos saltos de línea. No estires los glifos con `scaleX`.
- **Geist 400/500/600** para cuerpo, controles y explicaciones; **Geist Mono 400/500** para
  cifras, unidades, código y metadatos; **Reenie Beanie 400** para notas breves.
- El cuerpo es `16px / 1.65`; no uses la serif de exhibición para párrafos largos ni la manuscrita
  para instrucciones críticas. Los títulos usan `clamp()` y peso 400.
- Usa los tokens de superficie, tinta y estado. En oscuro cálido, el fondo es `#13110f`, el
  panel `#231e1a`, la tinta `#e9dfd7` y el secundario `#b7a89b`. No copies el `gray-600` original
  para texto pequeño: daba solo `3.13:1` sobre el fondo.
- **Dark Sea es optativa**, útil en informes con mucho código. Tiene siete tonos seleccionados
  de simurai y superficies adicionales. `uno-2` sirve para texto secundario; `uno-4/5` se reservan
  para estructura. No añadas alertas rojas a una variante de dos matices: usa palabras y símbolos
  de estado, ya presentes en las pastillas y avisos.

## Elegir un componente

| Cuando necesitas… | Usa… | Criterio |
|---|---|---|
| Destacar una idea dentro de un párrafo | `.marca` | Una frase corta; los enlaces siguen pareciendo enlaces. |
| Añadir una observación lateral | `.con-margen` + `aside.margen` | Contexto complementario, una o dos frases; en móvil cae después del párrafo. |
| Advertir, confirmar o establecer un límite | `.aviso` con círculo | Título explícito y texto; el color acompaña el significado. |
| Comparar participaciones de un total | `.mapa` | Áreas proporcionales a una magnitud positiva y valores escritos; no usar como mapa de procesos. |
| Mostrar un valor y su procedencia | `.dato`, `.datos`, `.medida` | Mantén unidades, denominador y valores sin truncar. Un medidor no implica certeza. |
| Orientar una lectura larga | `.indice` + `.regla` | Índice en el flujo en móvil; `aria-current` señala la sección, tachado indica las anteriores. |
| Mostrar una salida de consola como evidencia | `.terminal` | El texto *es* la prueba: se lee como se vio. Oscura en ambos temas; señala un valor con `.subra`. |
| Comentar el documento desde afuera, a mano | `.manuscrita` + `.senalado` | Una frase, un corchete. Nunca para información crítica. |
| Mostrar código verificable | `.codigo` | Nombre, lenguaje, copia y un estado de resultado; nada esencial oculto por máscara. |
| Comparar alternativas | `.tabla-caja` dentro de figura ancha | Cabeceras semánticas, caption y desplazamiento por teclado. |
| Mostrar un anticipo que se desvanece | `.extracto` | Solo una copia decorativa `aria-hidden`; el texto completo se abre con `details`. |
| Guardar referencias que merecen volver a verse | `.kept` | Objeto, título completo y razón concreta; no envolver cada párrafo en tarjeta. |
| Explicar conexiones geográficas | `NotaGlobo` | La ubicación debe importar. Para estados, flujos o arquitectura usa un diagrama apropiado. |
| Comparar cantidades, incluidas negativas | `data-grafica="barras"` + [graficas.js](graficas.js) | Cero en el dominio, unidades compartidas, datos completos en tabla. |
| Seguir categorías o fechas | `lineas` / `temporal` + [graficas.js](graficas.js) | Temporal usa fechas ISO con distancia real y delta frente a la fila anterior; ausencia corta la línea. |
| Explorar dos variables o una distribución | `dispersion` / `distribucion` + [graficas.js](graficas.js) | Puntos finitos; histograma con intervalos reales y densidad para que el área represente frecuencia. |
| Comparar intensidades en una matriz | `calor` + [graficas.js](graficas.js) | Cinco intervalos explícitos, leyenda, valor en cada celda, sin dato distinto de cero. No reemplaza `.mapa`. |
| Comparar opciones, totales o series pequeñas | Recetas de tablas + [tablas.js](tablas.js) | Ordenación optativa, footer fijo, sparkline con escala compartida y serie escrita. |
| Explicar tres variables o etapas | `NotaEscena` + [escena.js](escena.js) | XYZ / duración; tabla siempre visible, una inclusión de Three compartida con el globo. |
| Añadir una señal breve de una acción | `NotaSonido` + [sonido.js](sonido.js) | Canal acotado; apagado al cargar, activación explícita, nunca scroll/foco. |
| Repetir una anotación con gesto de pluma | `NotaEscritura` + [escritura.js](escritura.js) | Paths SVG ordenados y texto equivalente; no convierte una fuente en trazos. |

Las recetas incluyen **HTML completo, cuándo usarlo/cuándo no y sus límites** en
[componentes.md](componentes.md). Copia sólo los módulos que usa la pieza, una vez al final;
`init(raíz)` permite inserción tardía, `get(elemento).destroy()` permite retirarla. No cargues
archivos relativos en un artefacto: incrusta sus contenidos. Las tablas son la fuente de
datos de gráficas y escenas; no dupliques las cifras en objetos JS que puedan desincronizarse.
Three.js siempre en `https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js`.

## Artefactos con CSP estricta

Escribe un fragmento, **sin `<html>`, `<head>` ni `<body>`**. Empieza por `<title>`, declara
`<meta charset="utf-8">` antes de los primeros 1024 bytes y pega `<style>` con la hoja completa.
La declaración temprana evita acentos rotos al abrir el mismo archivo fuera del envoltorio.

- Las hojas externas sólo pueden venir de `https://fonts.googleapis.com`. Estos ejemplos
  incluyen sus fuentes como `data:` URI mediante `fuentes.css`, por lo que no necesitan
  hojas ni fuentes remotas. Conserva las licencias incrustadas al copiar; no añadas `@import`.
- Guiones externos: `cdnjs.cloudflare.com`, `cdn.jsdelivr.net/npm/`, `cdn.tailwindcss.com`,
  `code.jquery.com`. Three.js está fijado a `0.160.1/three.min.js` en cdnjs: versión clásica sin
  importaciones o complementos externos. No dependas de `latest`.
- Todas las imágenes deben ir en `data:` URI. SVG inline también sirve. No cargues capturas,
  carátulas, texturas ni mapas desde otros dominios, tampoco con `fetch`.
- Pega [interacciones.js](interacciones.js) al final, dentro de un `<script>`. Contiene temas,
  índice, regla, copia, impresión de extractos y sonido opcional. No requiere bibliotecas.
- El sonido empieza **apagado** y solo se activa con un botón. Es una síntesis Web Audio breve,
  no una copia de los MP3 del sitio. No pongas sonido sobre scroll, foco ni lectura automática.
- `prefers-reduced-motion` debe cancelar RAF y transiciones. No basta con esconder el canvas.

## Globo de rutas

Usa [globo.html](globo.html) para ver el componente aislado y [globo.js](globo.js) como fuente.
Incluye Three.js una vez, pega `globo.js` una vez y crea una instancia por contenedor con
`new NotaGlobo(elemento, {points, arcs})`. El contrato, ejemplos y métodos están en
[componentes.md](componentes.md#globo-de-rutas).

La Tierra usa el shader Fibonacci y una máscara de COBE incrustada, con aviso MIT dentro del
archivo: conserva esa licencia al copiar. El círculo, la atmósfera y los puntos usan la misma
proyección que las rutas. La lista es la alternativa textual; no puede quedar oculta si WebGL
falla. El giro se detiene fuera de pantalla, al ocultar la pestaña, al pausar y con movimiento
reducido. Llama `destroy()` al retirar una instancia de una aplicación.

## Leerse bien en un teléfono

El sistema es fluido por construcción —`min()` en todos los anchos, sin `min-width` mayor que la
pantalla—, así que el documento no se desplaza de lado. Pero hay dos piezas que sí necesitan
cuidado, y se resuelven igual: **ancho mínimo propio y desplazamiento local**, nunca compresión.

- **Tablas.** Sin mínimo, una tabla no se desplaza: se aplasta. Medido a 390 px, cuatro columnas
  caían a filas de 97 px de alto y seis columnas a celdas de 50 px con filas de **581 px**.
  `.tabla-caja table` trae `min-width: 34rem`; añade `densa` a la caja desde cinco columnas y
  sube a `58rem`. Con eso las mismas seis columnas dan celdas de 139–285 px y filas de 140 px.
- **Diagramas.** `.diagrama-caja > svg` ya lleva `min-width: 640px`; envuelve siempre el SVG en
  esa caja o sus etiquetas de la derecha quedan fuera de alcance.

Lo demás ya cae solo: el índice vuelve al flujo bajo 1600 px, la nota al margen se coloca después
de su párrafo bajo 1184 px, el código se desplaza dentro de su `pre` y la barra de páginas se
desplaza de lado dentro de su propio ancho. **Comprueba a 390 px que ninguna caja de tabla o
diagrama quede sin barra de desplazamiento**: si no la tiene, está comprimida. Repite
exactamente a **320 px**; en los dos tamaños comprueba también gráficas, calor, escritura
y escenas. Sus lienzos conservan mínimos legibles dentro de regiones con foco y nombre.

## Cuando la nota se parte en páginas

Un informe largo —capítulos, cada uno con su temario— se arma con `multipagina` y
[multipagina.js](multipagina.js). El esqueleto está en
[componentes.md](componentes.md#multipagina). Tres reglas:

1. `main.hoja.multipagina` contiene `article.pagina` con id; la primera lleva `viva`, las demás
   `hidden`. Las figuras `.ancho` y `.amplio` son hijas de `.pagina`, hermanas de las secciones.
2. Pega `multipagina.js` **después** de `interacciones.js`. El índice global delega al detectar
   `.multipagina`; el script de páginas mantiene `aria-current`, `aqui-visto` y `aqui-actual`
   sólo en la página visible. No mezcles versiones antiguas de esos dos archivos.
3. Cada página abre con su `header.cabecera` y su `nav.indice`. El hash guarda la página, así que
   un enlace directo a un capítulo funciona.

En capítulos cortos, como la muestra de informe, puede omitirse el temario lateral.
`data-historial` en `.hoja.multipagina` añade Atrás/Adelante para capítulos; sin él se conserva
el comportamiento anterior. `.barra.capitulos` es la variante editorial de navegación.
Para vistas breves dentro de una pieza usa [pestanas.js](pestanas.js), nunca mezcles los roles
de tablist con los botones de navegación de capítulos. Las pestañas no modifican el hash;
al imprimir se ven todos sus paneles. Copia la receta completa de `componentes.md`.

## Comprobar la entrega

Abre el resultado a 320–390 px y en escritorio; comprueba los tres temas, el índice, el foco y
la copia. Revisa que el documento no tenga desplazamiento horizontal y que el desplazamiento
local permita alcanzar el final de tablas, código y diagramas. Prueba el modo de movimiento
reducido y la lista del globo sin WebGL. No anuncies verificaciones que no ejecutaste.

Si modificas las fuentes de este skill, ejecuta `python3 scripts/ensamblar.py` para actualizar
los HTML y `python3 scripts/validar.py` para comprobar sus restricciones estructurales.
El ensamblador es local, no instala dependencias ni publica nada. Los HTML generados contienen
CSS, JS, portadas y máscara terrestre; no requieren subir archivos relativos.
Incluyen también los 16 WOFF2 de `fuentes.css` (211.396 bytes antes de base64); procedencia
y hashes en [auditoria/fuentes.json](auditoria/fuentes.json). El ensamblador no vuelve a descargarlos.

[multipagina.html](multipagina.html) contiene el ejemplo completo de capítulos;
[pruebas.html](pruebas.html) es la fixture de regresiones (índice, copia, anchos e impresión).
Para comprobar el navegador con CSP usa `python3 scripts/servir.py` y abre el puerto local
8766. Los resultados y las limitaciones de esta revisión se guardan en `auditoria/`.
El [informe de verificación](auditoria/verificacion.md) explica qué se ejecutó, a qué
viewport y con qué límites; incluye los comandos para repetir las pruebas del navegador.


## Reportes, artículos y prototipos

Para nuevas piezas usa las recetas de la [segunda tanda](componentes.md#segunda-tanda-reportes-artículos-y-prototipos):
ficha de decisión, cronología, ficha editorial, referencias con retorno, glosario,
metodología, antes/después, cascada, pequeños múltiples, conciliación de conteos,
calculadora de capacidad, globo narrado y visor de prototipos.

- [reportes.js](reportes.js) mejora las tablas/escenarios y dirige el recorrido con NotaGlobo.
  No infiere explicaciones, no convierte capacidad en ahorro y no compara monedas.
- [visor.js](visor.js) muestra HTML/CSS local de confianza con estados declarativos,
  Shadow DOM y anchos reales. Usa consultas de contenedor, no media queries de ventana.
  No admite scripts, no usa iframe, no carga apps remotas y no emula hardware.
- La apariencia de cabecera usa la llave circular sol/luna de la receta `apariencia`.
  Abre un panel con muestras de color y radios `data-elegir-tema`; conserva los selectores
  anteriores para artefactos publicados. Las variantes con etiqueta y cápsula son alternativas.
  No muestres todas las preferencias permanentemente en la cabecera.
- Color y estilo son independientes: Editorial (original), Sobrio (Geist en títulos),
  Técnico (Geist Mono en títulos). Se activan por `data-elegir-estilo`; nunca cambies la
  tipografía original de una nota que no ofrece esa elección. Cuerpo y gráficos conservan
  sus familias. Lectura cómoda (`data-comodidad`) y trama (`data-papel-tramado`) son optativas.
  Los tres estilos funcionan en Claro, Cálido y Sea. Comprueba los saltos de títulos al cambiar.
- La búsqueda del catálogo sólo filtra su índice; cada receta tiene un botón para copiar
  su HTML. [catalogo.js](catalogo.js) no es necesario en artículos normales.
- La firma de cabecera es `.firma-editorial`: “tikin” en serif y una leyenda corta en sans.
  Usa el nombre de la serie o del documento; evita presentar la marca como una ruta de código.
- La ficha de hallazgo separa afirmación, evidencia disponible, límite y siguiente prueba.
  No atribuye certeza: una hipótesis se identifica como tal. Las siguientes posibilidades
  analizadas están en [capitulos-propuesta.md](auditoria/capitulos-propuesta.md).

El catálogo se sirve en el Mac mini; Angel lo prueba desde el MacBook. Usa la dirección
HTTPS de Tailscale Serve que confirme el host, no un enlace localhost para la entrega remota.
