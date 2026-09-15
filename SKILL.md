---
name: nota-tikin
description: >-
  Genera y valida los artefactos e informes HTML de Angel y Tikin con una base estándar de temas sol/luna, comentarios flotantes y sonido optativo, más una librería editorial de componentes copiables: lectura serif/sans, figuras anchas, tablas, gráficas a escala, mapas de calor, anotaciones, escritura por trazos, sonido optativo y escenas Three.js con alternativa textual. Siempre en claro, oscuro cálido y Dark Sea, autocontenidos y compatibles con la CSP de artefactos.
---

# Nota Tikin

Angel eligió cmrg.me como referencia para sus artefactos. El resultado debe sentirse como un
cuaderno editorial: una idea principal, lectura tranquila y evidencia que puede ocupar más
espacio. Aplica este lenguaje a los entregables HTML; conserva el formato si se pidió Markdown,
una hoja de cálculo u otro medio.

## Base obligatoria para nuevos artefactos de Angel

Angel pidió estandarizar la experiencia. En cada nuevo entregable HTML usa el generador de
[estandar.md](estandar.md): **llave circular sol/luna con nueve paletas y Sistema, comentarios
flotantes, sonido habilitado con prueba, silencio y volumen, índice y progreso de lectura**. Los capítulos
conservan estas piezas. No omitas los comentarios por no aparecer en el contenido del informe.
Una petición explícita de Angel de omitir o cambiar una pieza prevalece; indica esa excepción.

1. Consulta el inventario completo y lee las recetas elegidas como se explica abajo.
2. Escribe sólo el contenido editorial en un archivo; cada `h2` necesita un ID propio o en su
   sección. Las figuras anchas son hermanas de las secciones dentro de la hoja o página.
3. Ejecuta `python3 scripts/crear_artefacto.py --contenido /ruta/contenido.html --titulo 'Título' --salida /ruta/artefacto.html`
   desde el skill, o usa la ruta absoluta del script. Para capítulos, usa `--config` según estandar.md.
4. Ejecuta **`python3 scripts/validar_artefacto.py /ruta/artefacto.html` sobre la salida final**.
   `scripts/validar.py` comprueba la biblioteca; no reemplaza la revisión del artefacto entregado.
5. Comprueba en navegador 320/390 px y escritorio, temas, comentarios y sonido. No anuncies
   audición si sólo comprobaste actividad de Web Audio.

La base incrusta las fuentes actuales y detecta dependencias. No reconstruyas los controles de
memoria ni copies un informe viejo para comenzar. [estandar.html](estandar.html) y
[estandar-capitulos.html](estandar-capitulos.html) son las bases reproducibles. Los ejemplos previos
siguen sirviendo para consultar piezas y para mantener documentos ya publicados.

La llave organiza **Temas / Letras / Sonido**: busca por nombre/color, filtra familias y mantiene
el tema actual visible. No vuelvas a crear una lista vertical con todos los ajustes. Las combinaciones
Libro/Revista/Bitácora añaden Literata incrustada; lee los usos en guia-uso.md. El interruptor de silencio
está en la pestaña Sonido. Nunca crees Web Audio antes de una interacción real.

## La misma base en Claude, Codex y Hermes

Este skill es un directorio portable: las instrucciones, el registro y los scripts son los mismos
para cualquier agente. Resuelve las rutas desde el directorio donde cargaste `SKILL.md`, no desde
el proyecto actual ni desde una ruta fija de Claude. Python 3 genera y valida sin instalar paquetes.
Orca sirve para revisar/publicar cuando está disponible; si no lo está, usa el navegador y el medio
de entrega disponibles y declara qué verificaciones faltan. No omitas por ello los controles comunes.
En este Mac, Claude conserva la copia canónica; Codex y Hermes la leen mediante enlaces al mismo
directorio. Una conversación ya iniciada puede requerir volver a cargar el skill para ver cambios.

## Componer, no sólo colocar componentes

Lee [guia-uso.md](guia-uso.md) al crear un nuevo documento: explica cómo combinar las piezas
para decisiones, finanzas, logística, artículos, documentación técnica y prototipos. La guía visual
[guia.html](guia.html) reúne todos los ejemplos, su HTML y sus límites. [casos-uso.json](casos-uso.json)
relaciona preguntas con IDs de recetas para explorar combinaciones sin reducir el inventario.

Antes de redactar identifica lector, pregunta, evidencia y siguiente acción. Selecciona las piezas
que cumplan una función en ese argumento. Considera notas izquierda/derecha cuando añadan un matiz,
texto animado para una segunda voz breve, avisos para límites y tablas/gráficas para evidencia.
No llenes una cuota de componentes ni inventes cifras para usar uno. En una muestra completa sí
comprueba cobertura de todos los IDs del registro. El generador conserva ayudas, temas y comentarios.

Liftit (`liftit`), Blueprint (`blueprint`) y Hacker (`hacker`) amplían las paletas. Usa `--tema` y
`--estilo` del generador para una presentación inicial reproducible; `tema` y `estilo` también se
admiten en el JSON. Liftit + Sobrio acompaña logística; Blueprint + Técnico, planos conceptuales;
Hacker + Técnico, código y runbooks. No cambies silenciosamente el tema de un artefacto existente.
Para instalar la misma biblioteca en otro equipo o en Hermes consulta [instalacion.md](instalacion.md).

## Subrayar y anotar con intención

Al componer un informe o artículo, busca la decisión, la tensión o el límite que más merece una
segunda lectura. Considera la receta `apuntes` si una observación lateral añade algo útil:

- Subraya con `data-subrayar` una frase corta del argumento, no todo el párrafo. Conserva el texto
  principal completo; un enlace sigue siendo un enlace y no se disfraza de subrayado manuscrito.
- El apunte responde a esa frase con una pregunta, un matiz o una consecuencia. Por ejemplo:
  «conservar las revisiones» → «¿y si cambia el texto?». Evita repetir la frase o poner elogios vacíos.
- Usa `.apunte` a la derecha y `.apunte.izquierda` cuando ayude al ritmo de lectura. Copia la rejilla
  completa de `apuntes`; no saques notas del documento con offsets. En móvil van después del párrafo.
- La información crítica y las fuentes se escriben en texto normal. La manuscrita es una segunda
  voz breve, no el lugar único de una fecha, advertencia o decisión. Si no añade contexto, omítela.
- Conserva `data-mano="fuente" data-escritura-sonora`, IDs únicos y el botón de repetición. El gesto arranca
  cuando se ve; el contexto de sonido espera el primer clic real y respeta el silencio elegido. Con movimiento reducido
  se muestra completo. Comprueba entrando desde otra sección, no sólo recargando en la anotación.

[prioridades.html](prioridades.html#leer-entre-lineas) muestra esta selección sobre un argumento real.
El HTML interactivo no decide dónde anotar: esa selección la hace el agente al componer el contenido.

## Consultar la biblioteca completa

Antes de componer un artefacto, revisa **todo el inventario vigente** de [registro.json](registro.json),
incluidos sus capítulos y dependencias. Las tablas de orientación de este skill son parciales;
no limites la selección a esos ejemplos ni a componentes recordados de una versión anterior.
También están disponibles las piezas base documentadas en [componentes.md](componentes.md).

Para recorrer las recetas sin cargar todo su HTML, ejecuta desde el directorio de este skill:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for pieza in json.loads(Path('registro.json').read_text())['componentes']:
    print(pieza['capitulo'], '|', pieza['id'], '|', pieza['nombre'], '|', ', '.join(pieza['dependencias']))
PY
```

Para cada pieza elegida, lee su receta completa en `componentes.md` o los campos `html`,
`criterio_y_limites` y `dependencias` del registro. Copia la implementación actual e incrusta
sus módulos; conserva sus interacciones, accesibilidad, temas y alternativas textuales.
Tablas interactivas, mapas con tooltip, escritura sonora optativa, comentarios, prototipos,
marcos, listas y composiciones editoriales forman parte de la biblioteca utilizable.

Si Angel pide una biblioteca o muestra con **todos los componentes**, parte de
[biblioteca.html](biblioteca.html) y comprueba que estén representados todos los IDs del registro,
además de las piezas base solicitadas. Para artículos e informes, selecciona del inventario
completo las piezas que expliquen su contenido. No inventes datos para llenar componentes.

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

## Navegación de lectura que debe acompañar el artefacto

Para los artefactos HTML de Angel con varias secciones, incluye por defecto **índice izquierdo
con seguimiento y regla de progreso**. Las pestañas de capítulos no los sustituyen.
Usa `.hoja.lectura-guiada`, un `nav.indice` con enlaces a IDs reales y una sola `.regla.regla-guiada`
fuera de `main`; el HTML completo está en [componentes.md](componentes.md#índice-lateral-y-regla-de-lectura).
En multipágina, cada `.pagina` lleva su propio índice y `main` añade `data-progreso-pagina`:
la regla mide el capítulo visible, se reinicia al cambiar y llega a 100 % antes de la paginación.
Incluye `interacciones.js` y, para capítulos, `multipagina.js` después.

Desde 1200 px, esta variante reserva espacio real para ambos laterales; mantiene texto y
figuras en su rejilla. Debajo, el índice vuelve al flujo y la regla se vuelve un control compacto
con porcentaje. No escondas ambos por trabajar en portátil ni tapes las figuras con ellos.
Comprueba sección actual, anteriores, cambio de capítulo, Home/End y tamaños 320/390/1440 px.
Una pieza aislada sin secciones no necesita un índice vacío. El patrón anterior sin estas clases
conserva su umbral de 1600 px y sus anchos originales.

## Fuentes y compatibilidad de las piezas

El generador incrusta [estilo.css](estilo.css) completa; no la recrees de memoria. Para mantener un artefacto anterior, lee y conserva sus fuentes antes de editarlo.
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
- El generador incorpora [audio.js](audio.js), [controles.js](controles.js) e
  [interacciones.js](interacciones.js) en orden. Interacciones gestiona temas, índice, regla y copia;
  audio.js gestiona el sonido global. Copiar interacciones.js solo no basta para el audio.
- Por petición explícita de Angel del 15/09/2026, la base nueva empieza con sonido **habilitado**; Web Audio se crea sólo tras el primer clic real. El silencio elegido se recuerda en localStorage y cancela voces/activaciones pendientes. Esto sustituye el requisito anterior de OFF inicial. El canal independiente sin audio.js conserva su botón de activación. Usa las grabaciones originales de cmrg.me incrustadas,
  decodificadas con Web Audio; Angel pidió sustituir la síntesis anterior. No sonorices scroll ni foco. La escritura optativa `data-escritura-sonora` puede acompañar el trazo visible tras activar Sonidos; el resto de lectura automática permanece silencioso.
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

En nuevas composiciones con varias secciones conserva índice y regla incluso si hay pestañas. Los ejemplos mínimos anteriores pueden conservar su estructura; no los uses para justificar omitir la navegación en un artefacto completo.
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
  anteriores para artefactos publicados. Las variantes con etiqueta y cápsula se conservan para ejemplos y documentos anteriores; los nuevos entregables usan la llave circular.
  No muestres todas las preferencias permanentemente en la cabecera.
- Color y estilo son independientes: Editorial (original), Sobrio (Geist en títulos),
  Técnico (Geist Mono en títulos), Libro (Literata), Revista (Instrument / Literata) y
  Bitácora (Mono / Literata). Se activan por `data-elegir-estilo`; nunca cambies la
  tipografía original de una nota que no ofrece esa elección. Las tres nuevas cambian el cuerpo
  de lectura; gráficos, código y controles conservan sus familias. Lectura cómoda (`data-comodidad`) y trama (`data-papel-tramado`) son optativas.
  Las seis combinaciones funcionan en todas las paletas: Editorial, Sobrio, Técnico, Libro, Revista y Bitácora. Literata añade lectura serif larga; Reenie Beanie mantiene las notas aprobadas. Comprueba los saltos de títulos al cambiar.
- La búsqueda del catálogo sólo filtra su índice; cada receta tiene un botón para copiar
  su HTML. [catalogo.js](catalogo.js) no es necesario en artículos normales.
- La firma de cabecera es `.firma-editorial`: “tikin” en serif y una leyenda corta en sans.
  Usa el nombre de la serie o del documento; evita presentar la marca como una ruta de código.
- La ficha de hallazgo separa afirmación, evidencia disponible, límite y siguiente prueba.
  No atribuye certeza: una hipótesis se identifica como tal. Las siguientes posibilidades
  analizadas están en [capitulos-propuesta.md](auditoria/capitulos-propuesta.md).

El catálogo se sirve en el Mac mini; Angel lo prueba desde el MacBook. Usa la dirección
HTTPS de Tailscale Serve que confirme el host, no un enlace localhost para la entrega remota.

### Edición completa para explorar y componer

Abre [biblioteca.html](biblioteca.html) para 74 recetas en nueve capítulos, con HTML,
dependencias, criterio y límites junto al ejemplo. Incluye archivos de publicaciones,
autoría, lecturas relacionadas, anotaciones numeradas, revisiones, criterios y riesgos.
[editorial.js](editorial.js) ofrece búsqueda/filtro local y configuración de lista/rejilla,
extractos y metadatos. No conecta un CMS ni envía información.

[registro.json](registro.json) es el inventario generado para componer artefactos desde
fuentes locales. No es un registro compatible con el CLI de shadcn. Usa sólo las dependencias
indicadas por cada receta, incrustadas; nunca descargues el registro con fetch en un artefacto.
`data-enlaces-internos` permite URLs a recetas dentro de los capítulos; sin ese atributo
multipagina conserva el comportamiento de los artefactos anteriores.

### Revisar artefactos con comentarios

La edición completa incorpora [revision.js](revision.js): pines flotantes en el punto elegido, editor pequeño y prompt copiable con capítulo, referencia, fragmento y coordenadas relativas, sin red ni persistencia. Una instancia por documento; copia antes de recargar. [explorador.js](explorador.js) añade búsqueda y menús compactos de filtros, grupos, columnas y orden a la tabla de cuatro columnas documentada. Cards editoriales, de indicador y de proyecto están en componentes.md.

El visor permite pegar HTML declarativo local y alternar Móvil/Escritorio; los embeds remotos siguen fuera de CSP. Escritura admite `data-al-ver` para una primera animación al entrar en pantalla; el sonido se activa con un botón explícito. [codigo.js](codigo.js) colorea HTML, CSS, JavaScript, TypeScript, JSON, Python, SQL, Shell y salida de terminal creando nodos de texto seguros y conserva exactamente el contenido copiable. Grano de papel usa SVG de ruido incrustado, no una rejilla de puntos.

[controles.js](controles.js) coloca los menús de tabla y visor dentro del viewport; se incluye antes de interacciones.js. [audio.js](audio.js), antes de interacciones.js, centraliza el audio y el interruptor en la pestaña Sonido: habilitado inicialmente, espera el primer clic, botón Probar sonido, volumen y estado. Requiere gesto real; no suena por scroll genérico. «Ver escritura animada» lleva a la nota manuscrita animada, o al SVG de Edición si no hay nota. El visor ofrece dispositivo, proporción, rotación y escala visual; conserva píxeles CSS para las consultas de contenedor. La trama se aplica también a la barra de capítulos.


### Analítica financiera y logística

Hay diez recetas adicionales en [componentes.md](componentes.md#calendario-de-actividad):
calendario, torta/donut, áreas apiladas, caja y bigotes, velas OHLC, mapas de rutas y volumen,
columnas geográficas, arcos logísticos y capacidad de almacén. Usa [analitica.js](analitica.js)
para las siete vistas SVG; [escena.js](escena.js) incorpora las tres nuevas vistas 3D.
Los mapas requieren [geografia.js](geografia.js) antes del módulo de dibujo: Colombia de
Natural Earth incrustada, sin tiles ni conexión externa. No atribuyas los datos ficticios de
estas recetas a Tikin o Liftit. Los límites territoriales generalizados no sirven para navegar.

Elige según la pregunta: calendario para frecuencia diaria; torta para pocas partes de un total;
áreas para total y mezcla temporal; caja para dispersión; velas para apertura/extremos/cierre;
mapas cuando importe la ubicación. Los bigotes documentados son mínimo/máximo, no 1,5 IQR.
Los controles permiten consultar un registro sin depender de hover. `NotaAnalitica.init(raíz)`
y `NotaAnalitica.get(elemento).destroy()` permiten insertar y retirar componentes; las cifras
vienen de la tabla y las fechas son ISO UTC. No son conectores a Superset ni a GitHub.

Comprueba los laterales también **al inicio** de la página: la cabecera aún no está pegada al
borde y tiene otra altura. La lectura guiada mide su borde inferior; no reemplaces ese cálculo
por `top:100px`. La regla separa porcentaje y cursor, y colorea las marcas ya recorridas.


### Gesto manuscrito, cards delineadas y attention map

Incluye [mano.js](mano.js) y `data-mano="fuente"`: la Reenie Beanie incrustada coincide byte
por byte con la de cmrg.me. Revela caracteres de esa fuente en 375 ms cada uno, escalonados
sobre la duración original del lápiz. No reconstruyas glifos ni uses el alfabeto SVG anterior
para las nuevas notas. La receta manuscrita conserva texto equivalente y repetición. Los apuntes
izquierdo/derecho reservan espacio con rejilla y pasan al flujo en móvil. `data-subrayar="referencia"`
añade tres pasadas irregulares y tenues en un segundo. Movimiento reducido cancela animaciones.

El **attention map de áreas** está en `atencion`, con [atencion.js](atencion.js). No lo omitas del
catálogo ni lo sustituyas por el mapa de calor: son preguntas distintas. El área se calcula desde
una tabla no negativa; categorías pequeñas mantienen nombres y cifras en controles y tabla.
`.mapa` y `.con-margen/.margen` continúan disponibles en documentos antiguos.

La receta `cards-trazadas` ofrece rejilla delineada, sombra suave y títulos completos. El atributo
`data-audio-hover` usa el MP3 original incrustado en [audio.js](audio.js) sólo con contexto habilitado por un clic real y movimiento real del ratón. El usuario autorizó hover sonoro: respeta el silencio guardado,
no suena al hacer scroll ni recibir foco. Angel pidió además lápiz durante la escritura visible:
`data-escritura-sonora` permite acompañar esa animación, únicamente con el contexto activo y la preferencia habilitada.
Se cancela al salir, finalizar, ocultar el documento o reducir movimiento; sin el atributo sigue silenciosa.


### Composición editorial ampliada

La biblioteca ofrece marcos de líneas discontinuas con extremos desvanecidos (`marco-difuso`),
estantería, invitación tramada, listas de estados/proyectos/conversación, navegación con `/` y
footer editorial. Copia las recetas completas de componentes.md; el marco reserva su espacio,
no necesita márgenes negativos y nunca enmascara texto. La navegación discreta conserva índice,
regla y capítulos; en móvil sólo su fila de enlaces tiene desplazamiento local.

El attention map tiene tooltip con nombre, valor, porcentaje y total; `data-contexto` en un texto visible de la fila
permite explicar el dato. Ratón, foco y toque dan acceso; Escape cierra. Mantén tabla y controles.
La invitación requiere invitacion.js y copia un borrador con contexto: no promete enviar, guardar
ni conectar un formulario a un servicio. Las cubiertas y los datos de ejemplo son ficticios.

### Piezas editoriales y bordes de figuras

Las nuevas bases llevan `marcos-editoriales`: todas las piezas `.ancho` y `.amplio` reciben
líneas punteadas de extremos difusos. `piezas-editoriales.js` añade una capa decorativa independiente;
no reemplaces pseudoelementos que ya usa una invitación o textura. No enmascares contenido ni
envuelvas una figura ancha dentro de una sección de texto para conseguir el borde. La biblioteca
activa el acabado; los ejemplos publicados anteriores conservan sus clases.

Las recetas `actividad-editorial`, `codigo-lineas`, `enlaces-icono`, `avisos-animados`, `trayectoria`
y `galeria` amplían el inventario. La conversación existente tiene variante `suelta` para burbujas
editoriales. `codigo.js` conserva exactamente el código copiado al numerar y destacar líneas.
`piezas-editoriales.js` gestiona actividad, pulso y galería, además de los marcos.
La galería desliza sin autoavance; imágenes incrustadas y pies con contexto. Los avisos tienen
un pulso acotado, cancelado fuera de pantalla y con movimiento reducido. Nunca animan el texto.

[prioridades.html](prioridades.html) reúne las prioridades propuestas y estas muestras en dos
páginas. Las propuestas de persistencia, migraciones y nuevos estados no se presentan como hechas.

Para la galería fiel a /work copia `galeria-fotografica`: sin encabezado ni introducción dentro
de la pieza, sólo imágenes con pies breves superpuestos, velo sobre toda la foto y contorno tenue.
No añadas una banda negra al pie. Mantén la curva superellipse y el arrastre con cursor grab;
en móvil se desliza de forma nativa. La muestra lleva ilustraciones rotuladas como tales:
para evidencia fotográfica incrusta las fotos proporcionadas y conserva su contexto.


### Operación logística con contexto

Para explicar flota o reparto, considera las recetas `globo-flota`, `ficha-entrega` y
`cola-novedades`. [liftit.html](liftit.html) las combina. El globo tiene Colombia resaltada,
ciudades, selección por vehículo y acercamiento a la ruta; su reproducción es una simulación
explícita de 45 segundos. Conserva el corte, la hora con zona y la tabla. No lo llames tiempo
real, GPS o ETA si no hay una fuente conectada y autorizada. Para otro corte, destroy,
actualización de la tabla e init; no inventes entregas confirmadas por llegar al extremo de un arco.
La ficha distingue recogida, tránsito, recepción y evidencia; la cola permite filtrar y agrupar
con el explorador existente. Todo debe conservar foco, scroll local y alternativa sin WebGL.

Antes de proponer más: ventanas prometidas necesitan timestamps; capacidad necesita unidad y
límite por vehículo; costo por parada necesita costos reales y denominador; una alerta GPS necesita
hora del último mensaje y umbral definido; la prueba de entrega necesita evidencia autorizada.
No deduzcas calles ni velocidad desde un arco entre ciudades. El mapa plano `mapa-rutas` sigue
disponible para volumen agregado y ahora dibuja los nodos después de todas las rutas.


### Controles discretos y navegación espacial

Repetir una nota usa el icono de flecha circular, no un botón con una frase. Conserva el nombre
accesible específico (izquierdo/derecho) y title. Copiar código/terminal usa dos hojas; si la
cabecera sólo dice CSS/HTML/etc., se integra el icono en la esquina y se conserva el lenguaje
para accesibilidad. Los nombres de archivo útiles permanecen visibles.

El visor ofrece iconos directos Móvil/Tablet/Escritorio, proporción y otros tamaños en un menú,
rotar, ajustar y reiniciar. No añadas rótulos visibles a esos controles. El comentario es una
burbuja de una línea que crece, contexto plegable y acciones de guardar/cerrar con iconos;
Ctrl/Cmd+Enter guarda. No pierde referencia ni fragmento al copiar el prompt.

Temas tiene más espacio (hasta 560 px, tres columnas en escritorio y dos en móvil); **el sonido
sólo se controla en Sonido**, por petición explícita de Angel. No restaures un interruptor común.
El globo de flota admite arrastre, desplazamiento con Mayús, zoom con botones/rueda tras enfocarlo,
pellizco y teclado. Home/restablecer recupera el encuadre; los presets mantienen los extremos de
las rutas dentro del mapa, pero una exploración manual puede sacarlos de la vista. No añade
inercia ni RAF para la cámara. Mantén los datos accesibles en la lista y la tabla.
