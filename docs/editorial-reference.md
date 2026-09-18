# Referencia y propuesta · TIKIN-629

Inspección del 13-sep-2026 (Bogotá), con Orca CLI 1.4.192. Leídos completos los siete
archivos base antes de editar. La rama `nota-libreria` parte de `628fb93`; el checkout
instalado en `~/.claude/skills/nota-tikin` estaba limpio y en el mismo commit.

## Cobertura y método

El [sitemap actual](https://www.cmrg.me/sitemap.xml) enumera 16 rutas, todas abiertas con
`orca goto`, `orca snapshot` y `orca eval`. Los snapshots cubren el DOM completo; se
midieron las cajas incluso fuera del viewport. Las cifras crudas y URLs de CSS/JS están
en [tests/evidence/reference.json](../tests/evidence/reference.json). No se siguieron destinos externos
ni la versión histórica `v1.cmrg.me`, que no pertenece al sitemap actual.

| Ruta | Inventario observado |
|---|---|
| `/` | Navegación, títulos serif, números animados, subrayados SVG, lista de artículos con máscara, treemap «attention map», objetos guardados, datos inline, manuscrita y botón de sonido. |
| `/blog` | Búsqueda, lista con fecha/tags, anotación lateral manuscrita, suscripción. |
| `/work` | Secciones narrativas, galería de fotos, cronología de trabajos y anotaciones. |
| `/about` | Conversación, globo con rutas y lista, galería, ranking musical con popularidad. |
| `/now` | Snapshot fechado, lista de proyectos, actividad GitHub, listas de estados, ranking musical. |
| `/shelf` | Libros que giran, vinilos que salen de sus fundas, pósteres inclinados, estrellas, ficha extensa y formulario de sugerencia. |
| `/thanks` | Referencias con notas al margen y cierre manuscrito. |
| `/guestbook` | Pared de dibujos, editor de trazos, deshacer/rehacer, herramientas, tamaño, color y captura. No se envió contenido. |
| `/blog/programar-e-uma-merda` | Artículo largo, índice/regla, avisos, siete bloques de código. |
| `/blog/react-19-part-2-the-code` | Índice jerárquico, trece bloques de código, comparación de dos bloques. |
| `/blog/react-19-part-1-the-backstory` | Índice, reacciones, tres bloques de código, imágenes y avisos. |
| `/blog/access-to-your-tailwind-theme-on-the-go` | Seis bloques de código, configuración, máscaras y resaltados. |
| `/blog/contentlayer-git-nextjs` | Tres bloques de código, checklist, notas al pie y retorno. |
| `/blog/htnx-a-htmx-like-experience-in-nextjs` | Vídeo con controles, siete bloques de código y tipos. |
| `/blog/quix-a-lightning-fast-vtex-io-cli-experiment` | Aviso de archivo, comandos, benchmarks como evidencia y dos salidas de consola. |
| `/blog/thm-autoreadme` | Artículo corto, un bloque de código, índice y reacciones. |

Las capturas `full-screenshot` repitieron el primer viewport: no son evidencia visual
válida de la página entera. Se sustituyeron por capturas de viewport con desplazamiento
instantáneo para las zonas inspeccionadas. La cobertura completa se apoya en los snapshots
y las mediciones DOM, no en una afirmación de revisión visual píxel a píxel.

## Medidas con procedencia

Todas las siguientes son del viewport **1639 × 939 CSS px**, salvo donde se indica otro.
`getComputedStyle` da la fuente/tamaño/interlineado; `getBoundingClientRect` da el ancho.

| Magnitud | Valor | Fuente exacta |
|---|---|---|
| Texto de lectura | 528 px | `/`, `main p.text-base`; también `main h1` en las páginas narrativas. |
| Cuerpo | Geist 15,5 px / 24,025 px | `/`, `main p.text-base` (`body` usa 23,25 px, no confundir). |
| Título principal | Editorial New 400, 44,5 px / 49,4444 px, tracking −1,1125 px | `/`, `main h1`; familia CSS `serif`, identidad del archivo en `@font-face`. |
| Título de sección en portada | 28,5 px / 38 px | `/`, `h2.text-2xl.text-pretty`. |
| Título de sección en artículo | 36,4 px / 43,68 px | `/blog/react-19-part-2-the-code`, `main h2`. |
| Nota al margen | Reenie Beanie 28,5 px / 32 px; caja 192 px | `/work`, `.font-handwritten`. |
| Código ancho | 768 px | `/blog/react-19-part-2-the-code`, `pre` (los dos comparados miden 512 px cada uno). |
| Attention map | SVG 1008 × 380 px | `/`, `svg.block.h-full.w-full`; treemap de 23 aplicaciones, áreas desiguales. |
| Globo | canvas 728 × 560 px | `/about`, `main canvas`. |
| Controles compactos | 32 px de alto, transición 150 ms | `/blog`, input de búsqueda y botón de suscripción. Nota conserva sus controles de 44 px. |
| Texto a 390 × 844 | 342 px; h1 36,4 / 43,68 px | `/`, `main p` y `main h1`, viewport emulado por Orca. |
| Texto a 320 × 740 | 272 px; h1 36,4 / 43,68 px | Mismos selectores. |
| Papel / panel / tinta / acento | #13110f / #231e1a / #e9dfd7 / #f1733d | Tokens `--color-gray-950/900/250`, `--color-orange-500`; conversión a sRGB con canvas 2D. |

Hoja publicada: `https://www.cmrg.me/_next/static/immutable/chunks/34moxaufbdj70.css`.
Familias adicionales identificadas por `@font-face`: Geist Mono y Departure Mono (`fancy`).
No se copian sus archivos externos al artefacto. La sustitución Instrument Serif ya elegida
por Angel permanece intacta.

## Movimiento y sonido

`document.getAnimations()` en portada devolvió subrayados con `strokeDashoffset` hasta cero:
tres segmentos de aproximadamente 328/331/341 ms que suman 1000 ms, `ease-out`.
Es una muestra concreta; las longitudes dependen de cada anotación. El chunk
`13nl53-l3csj9.js` distribuye la duración por longitud. Ese mismo chunk usa revelado por
carácter de 375 ms para anotaciones: aparecer un glifo no equivale a dibujar sus trazos.
`0ezhx__mmsfrs.js` define entradas de lista de 750 ms y stagger de 300 ms; blur 4 → 0 px,
desplazamiento 10 → 0 px, curva [0.19,1,0.22,1]. Son valores de código publicado,
no duraciones inferidas de una captura. El movimiento de portadas usa perspectiva y hover;
no se atribuye una duración única sin medir cada variante.

El chunk `407jum8rsxd_g.js` declara 14 sonidos: click, coin, focus, glitch, hover,
negative, pencil-1/2/3, pop, positive, shutter, swoosh y tada. El estado inicial del sitio
es `isMuted:false`; Nota mantuvo **apagado** en la primera versión. Por petición explícita de Angel del 15/09/2026, el contrato 4 comienza habilitado y espera el primer clic real, conservando el silencio elegido. Se midieron duraciones mediante
`AudioContext.decodeAudioData` (sin reproducirlas): click 47,8125 ms, hover 107,1458 ms,
swoosh 160,7292 ms, positive 857,1458 ms y lápices 2181,3333–3034,6667 ms. La tabla completa
está en el JSON con cada URL `/sounds/*.mp3`, canales y frecuencia de decodificación.
No se afirma una evaluación auditiva. La decisión inicial de sintetizar se sustituyó el 15 de septiembre por petición explícita de Angel: packages/core/components/audio.js incrusta ahora las grabaciones originales; véase tests/evidence/sounds-cmrg.json.

## Propuesta publicada antes de construir

1. `packages/core/components/charts.js`: barras, líneas, temporal con delta, dispersión e histograma. Tabla
   semántica como fuente; escala única para marcas/ejes/ticks, datos completos disponibles.
2. Mapa de calor matricial: intervalos discretos con leyenda y cifras en cada celda;
   `null` separado de cero. `.mapa` sigue siendo proporción; no se renombra.
3. Tablas de comparación, totales y sparkline; ordenación optativa con botones y `aria-sort`.
4. `packages/core/components/scene.js`: dispersión XYZ y composición por etapas, con proyección ortográfica,
   alternativa textual, controles, instancia por contenedor y ciclo de vida de `NotaGlobo`.
5. `packages/core/components/sound.js`: canal acotado, apagado al cargar, botón de activación y señales breves
   de acción/confirmación/atención; Web Audio sin recursos externos ni disparadores de lectura.
6. `packages/core/components/writing.js`: secuencia de paths SVG de una frase trazada a mano; controles de repetir
   y finalizar; texto equivalente permanente. No se simula el trazo revelando cajas de glifos.
7. Catálogo ejecutable y recetas completas en `docs/components.md`, incluyendo límites, cero,
   ausencia, valores negativos, escalas y ejemplos largos. Se conservan todos los componentes base.

## Fallos base para reproducir y corregir por separado

- Copia de terminal: el estado busca solamente `.codigo`; además `button.textContent`
  destruye el icono SVG después de copiar. Corregir selección del estado y restauración.
- Multipágina: el CSS puede anular el color/peso de `aqui-actual` cuando el enlace conserva
  `aria-current`; el script global sigue midiendo páginas ocultas. Unificar el dueño del índice.
- Impresión: los mínimos de tablas y las páginas ocultas pueden vencer las reglas print.
  Verificar y corregir únicamente el comportamiento prometido de contenido completo.

No se propone rediseñar en silencio la base. Las nuevas convenciones quedan acotadas a
componentes nuevos y las correcciones verificadas tendrán commits separados.
