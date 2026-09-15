# Entrega y verificación · TIKIN-629

13-sep-2026, Bogotá. Librería aditiva de HTML/CSS/JS copiables; sin framework, instalación
de paquetes ni publicación. [Catálogo ejecutable](../plantilla.html),
[capítulos completos](../multipagina.html), [recetas y contratos](../componentes.md).

## Componentes entregados

13 recetas nuevas: barras, líneas, temporal con variación, dispersión, histograma,
mapa de calor, tabla de comparación, tabla de totales ordenable, tabla con sparkline,
sonido por canal, escritura por paths, XYZ y etapas con duración en Three.js.
El catálogo tiene navegación directa entre 16 recetas, incluidas terminal, tabla densa
y manuscrita del sistema base; mantiene también las muestras editoriales originales y el globo.

Las tablas son la fuente de las visualizaciones. Las escalas relacionan coordenadas,
marcas y ejes; ausencia no significa cero. El histograma codifica frecuencia por área
con densidad en Y. Las escenas empiezan inmóviles y conservan la tabla visible.
La escritura usa seis paths originales de «a mano», no contornos de una fuente ni
revelado de cajas. Sonido independiente por canal, apagado al cargar y limitado a botones.

## Referencia

Se recorrieron las 16 rutas del sitemap de cmrg.me antes de escribir componentes.
El inventario, selectores, tamaños calculados, CSS/JS de procedencia, duraciones de
animación y audio decodificado están en [referencia-cmrg.md](../referencia-cmrg.md)
y [referencia.json](referencia.json). La propuesta se publicó en
[el comentario previo de TIKIN-629](https://linear.app/botto/issue/TIKIN-629#comment-5db982c3-9ce9-45a0-98c6-4acc5b3dc274)
antes de construir la familia de componentes.

## Comprobaciones ejecutadas

Orca CLI 1.4.192, navegador incrustado; UA reportada Chrome 150. Los scripts usan sólo
el CLI público. Las verificaciones de PDF usaron `pypdf` y `pypdfium2`, ya instalados;
no se instaló nada. Los JSON registran valores crudos y resultados.

| Comprobación | Resultado y evidencia |
|---|---|
| Ensamblado y validación | `python3 scripts/ensamblar.py` y `python3 scripts/validar.py` pasan. Cuatro fragmentos sincronizados; charset temprano, IDs, fuentes incrustadas, CSP, rejilla y regiones con foco/nombre. `node --check` para todos los módulos. |
| Escalas y comportamiento | 15 pruebas pasan: negativos/cero/ausencia, fechas desiguales/inválidas, áreas del histograma, límites de calor, ordenación, footer fijo, sparkline común, idempotencia/destroy, XYZ y fallback. [componentes.json](componentes.json). |
| Responsive y temas | 9 combinaciones: 320×740, 390×844, 1639×939, cada una en claro, oscuro cálido y Sea. Ancho del documento igual al viewport; se llega al final de cada región ancha; ningún rótulo SVG fuera del viewBox. [navegador.json](navegador.json). |
| Tres medidas | Escritorio: 560/992/1216 px. 320: 280/280/280. 390: 350/350/350. Repetido en base, `por-seccion` y multipágina. |
| Contraste nuevo | Todos los pares de texto medidos ≥4,5:1; trazos ≥3:1. Mínimo del texto de calor: claro 4,85:1, Sea 4,92:1. Se corrigieron los niveles que fallaban. |
| Movimiento | 17 comprobaciones pasan: RAF sólo visible/activo, pausa fuera de pantalla, cancelación con reduce, trazos secuenciales, finalización y destroy. [movimiento.json](movimiento.json), [método exacto](movimiento-metodo.json). |
| Sonido | Web Audio **offline real**, a 48 kHz: acción/confirmación terminan a 124,98 ms, atención a 189,98 ms; picos menores de 0,025. Activación sin señal, apagado sin voces, promesa de resume cancelada. [audio.json](audio.json). |
| Regresiones base | 19 comprobaciones pasan: barra sin solapamientos, índice de una página y multipágina, copia de terminal con icono/estado, denegación de portapapeles, hash de capítulo y rejillas. [base.json](base.json). |
| Impresión | PDF del catálogo: 13 páginas; fixture: 4; ejemplo multipágina: 2. Conservan capítulos, tablas, terminal y detalles; se restaura el estado de `details` al volver. [impresion.json](impresion.json). |
| CSP en ejecución | Servidor local con `default-src 'none'`, `connect-src 'none'`, `font-src data:`, imágenes `data:`, estilos inline/Google APIs y scripts permitidos. Único recurso remoto observado: Three `0.160.1/three.min.js`. |

## Correcciones de base y preservación

Los casos reproducidos y sus resultados anteriores están en [regresiones.md](regresiones.md):
índice global midiendo páginas ocultas, neutralización del enlace activo, copia de terminal
que borraba el icono y no anunciaba estado, páginas omitidas y terminal cortada al imprimir,
tintas de Sea demasiado claras sobre blanco y navegación móvil debajo del selector de tema.
Los cambios visuales de base se limitan a esos fallos comprobados.

Mientras se trabajaba apareció una corrección paralela de las divisorias `por-seccion`
en el checkout instalado. Se guardó íntegra en `9da3978`, rama `tikin-629/base-paralela`,
y se integró sin conflictos en la librería (`becf908`). El estado inicial `628fb93` permanece
en `main`; no hay remoto. La rama de desarrollo es `nota-libreria`; la instalación final
se identifica con `tikin-629/libreria` en `~/.claude/skills/nota-tikin`.

Las fuentes mantienen familias y pesos; `fuentes.css` incrusta 16 WOFF2 (211.396 bytes
antes de base64) para evitar descargas de fuentes durante la lectura. Conserva avisos OFL;
URLs y SHA-256 están en [fuentes.json](fuentes.json). El ensamblador sólo lee archivos locales.

## Límites de la verificación

- La referencia se cubrió mediante snapshots y medidas DOM completas, con capturas puntuales;
  no se afirma inspección visual píxel a píxel de las 16 páginas ni de sitios externos enlazados.
- No hubo audición manual ni clic físico de activación: Computer Use devolvió
  `window_not_focused` incluso tras restaurar. La síntesis se comprobó con OfflineAudioContext
  y un evento unitario explícito; los clics sintéticos reales del navegador fueron rechazados.
- `set media reduced-motion` emula CSS y `matches`. El host entregó `change` de forma
  intermitente; la cancelación del listener se ensayó con `MediaQueryListEvent` explícito.
  No se afirma un cambio físico de la preferencia del sistema. Visibilidad se ensayó con scroll
  y cuadros de captura que entregan los observers, sin inventar eventos de IntersectionObserver.
- Pérdida/restauración de contexto usa eventos sintéticos; la ausencia de Three sí se probó
  creando una instancia sin la dependencia. No se simuló una avería física de GPU.
- El foco programático alcanzó las regiones y controles y se verificaron sus nombres;
  Orca no activó la modalidad de teclado. El anillo `:focus-visible` se revisó en CSS,
  sin acreditar un recorrido físico con Tab ([foco.json](foco.json)). No se realizó una sesión con lector de pantalla.
  Éxito/denegación de portapapeles usan stubs para aislar el manejador; no acreditan permisos del SO.

## Repetir

```sh
python3 scripts/ensamblar.py
python3 scripts/validar.py
python3 scripts/servir.py
```

Con el servidor anterior abierto, en otra terminal del mismo worktree:

```sh
python3 scripts/comprobar_navegador.py
python3 scripts/pruebas_movimiento.py
python3 scripts/pruebas_regresiones.py
```

Esas pruebas usan y modifican sólo la pestaña local del catálogo; no publican, instalan ni
envían mensajes. La emulación es de viewport CSS, no una prueba en hardware iPhone.

## Capturas inspeccionadas

[XYZ claro, 1639×939](capturas/xyz-claro.png),
[barras, 1639×939](capturas/barras-oscuro.png),
[escritura, 1639×939](capturas/escritura-oscuro.png),
[calor Sea, 320×740](capturas/calor-320-sea.png),
[tablas claras, 390×844](capturas/tabla-390-claro.png),
[impresión desde Sea](capturas/impresion-sea.png).


La ampliación de diez gráficas, la regla coloreada y el recorte de laterales se verificaron
en [analitica-verificacion.md](analitica-verificacion.md), con 54 recetas y capturas nuevas.

La recuperación de notas manuscritas, cards delineadas y attention map está documentada en
[gesto-verificacion.md](gesto-verificacion.md).

Ampliación editorial (65 recetas): [tooltip, lápiz y composiciones](editorial-verificacion.md).
