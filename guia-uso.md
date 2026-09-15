# Componer con Nota Tikin

Esta es una biblioteca de HTML, CSS y JavaScript, y también un skill para que un agente la use.
La guía visual [guia.html](guia.html) contiene todas las recetas completas. [registro.json](registro.json)
es el inventario ejecutable; [componentes.md](componentes.md) conserva HTML, criterio y límites.
El generador proporciona la experiencia común. No es un paquete React ni un registro del CLI de shadcn.

## Antes de escoger piezas

Identifica lector, pregunta, evidencia disponible y acción siguiente. Recorre el inventario entero;
selecciona componentes por su función, no por su aspecto. Una gráfica sin una pregunta y una nota
manuscrita que repite el párrafo añaden trabajo al lector. La cobertura completa pertenece al catálogo;
en un documento real se aprovecha la biblioteca escogiendo bien.

Escribe una breve justificación de composición en tus notas de trabajo: pregunta → componente →
dato o texto que lo alimenta → límite. No conviertas esa justificación en instrucciones técnicas
para el lector del informe. Si falta una fuente, muestra el vacío o pide el dato; no inventes cifras.

También existe un vocabulario mínimo, documentado al inicio de componentes.md: `.marca` para
un énfasis estático, `.dato`/`.datos` para valor y procedencia, `.pildora` para estado, `.medida`
para una magnitud acotada y `.aviso` para condiciones. No conviertas un dato sencillo en una
card sólo para usar una receta. Los patrones `.con-margen`, `.extracto` y `.kept` se conservan
para documentos existentes; para nuevas anotaciones animadas consulta `apuntes`.

## Recorridos que se pueden adaptar

| Entregable | Hilo editorial | Piezas que conviene consultar | Evita |
|---|---|---|---|
| Informe de decisión | Conclusión provisional → evidencia → alternativas → decisión pendiente | `hallazgo`, `decision`, `criterios`, `comparacion`, `riesgos`, `apuntes` | Presentar una hipótesis como resultado demostrado |
| Informe financiero | Período y moneda → cambio → composición → conciliación → supuestos | `temporal`, `cascada`, `totales`, `sparkline`, `torta`, `conciliacion`, `metodologia` | Mezclar monedas, balances y flujos; comparar ventanas de distinta duración sin aclararlo |
| Operación logística | Servicio observado → dónde → dispersión → capacidad → siguiente acción | `globo-flota`, `ficha-entrega`, `cola-novedades`, `mapa-rutas`, `mapa-burbujas`, `caja`, `almacen`, `arcos-mapa`, `recorrido` | Inferir tiempos, distancias o rutas óptimas desde líneas decorativas |
| Artículo o blog | Pregunta → argumento → ejemplo → contrapunto → fuentes → siguiente lectura | `articulo`, `autor`, `apuntes`, `conversacion`, `codigo-lineas`, `referencias`, `relacionados` | Convertir cada párrafo en card o usar manuscrita para toda la explicación |
| Documentación técnica | Contrato → ejemplo mínimo → salida → fallos → recuperación | `anotaciones`, `codigo-poliglota`, `codigo-lineas`, `terminal`, `avisos-animados`, `pestanas` | Copiar código sin lenguaje, ocultar pasos de recuperación o simular una consola ejecutable |
| Revisión de prototipo | Tarea → interfaz → variantes → hallazgo → ajustes | `visor`, `antes-despues`, `anotaciones`, `hallazgo`, comentarios estándar | Confundir tamaño visual con hardware real; prometer embeds que la CSP bloquea |
| Portafolio o publicación | Selección → contexto → trayectoria → evidencia → contacto | `cards-trazadas`, `archivo`, `lista-proyectos`, `trayectoria`, `galeria`, `invitacion`, `pie-editorial` | Fotos ficticias presentadas como evidencia o formularios locales que prometen enviar |
| Estado y prioridades | Fecha de corte → activo → bloqueado → decisión siguiente | `lista-estados`, `cronologia`, `actividad-editorial`, `calendario`, `riesgos` | Confundir actividad, avance y productividad |

Consulta `casos-uso.json` si necesitas estos recorridos con IDs verificables. Cambia el orden cuando
el argumento lo requiera. No son plantillas que haya que llenar por obligación.

## Dos voces: argumento y nota al margen

El texto normal afirma algo verificable; la manuscrita introduce una pregunta o matiz. Por ejemplo:
«El costo por entrega bajó» necesita período, moneda y denominador. Subraya «por entrega completada»
y anota «¿incluye devoluciones?». Así la nota mejora la interpretación en lugar de decorar.

1. Escribe primero el párrafo sin efectos. Debe entenderse sin animación, sonido ni nota.
2. Marca una frase breve con `data-subrayar="referencia"`; no subrayes todo el párrafo.
3. Copia `apuntes`: `.apunte` coloca el margen a la derecha; `.apunte.izquierda`, a la izquierda.
   El contenedor `.apuntes.ancho` es hijo directo de la hoja o página. La nota cae después en móvil.
4. Usa `data-mano="fuente" data-escritura-sonora`, Reenie Beanie incrustada, ID único y botón
   `data-mano-repetir="ese-id"`. No sustituyas por una fuente cursiva del sistema ni el alfabeto SVG antiguo.
5. La escritura entra al verla; no empieza durante la carga fuera de pantalla. Sonidos requiere
   clic explícito en Apariencia. Movimiento reducido muestra el texto completo y cancela audio/animación.

Alterna lados sólo cuando el argumento se beneficie de una segunda voz. Para una precisión formal,
una definición larga o la única advertencia de seguridad usa `glosario`, `referencias` o `avisos-animados`.
Un `.aviso` comunica un estado con título y símbolo; el icono puede pulsar brevemente, el mensaje no.
Una nota lateral nunca reemplaza el pie de fuente de una gráfica.

## Barras que ayudan a leer y revisar

La cabecera contiene la llave sol/luna y los capítulos. El índice izquierdo sigue las secciones del
capítulo visible; la regla derecha colorea el avance y muestra el porcentaje. En móvil se adaptan:
no deben desaparecer porque el documento sea multipágina. El generador los monta automáticamente.
Los `h2` con IDs describen el recorrido; evita títulos vacíos como «Más información».

El botón flotante de comentarios permite señalar un punto, escribir un ajuste y revisar los pines.
«Ver comentarios» reúne contexto, capítulo, fragmento y posición en un prompt copiable. No dupliques
el montaje en cada página. Los comentarios son locales y se pierden al recargar: invita a copiar
el prompt al terminar la revisión; no prometas colaboración o guardado que no existe.

## Dar escala a la evidencia

- Comparar categorías: `barras`. Secuencia ordenada: `lineas`. Fechas con distancia real y cambio
  contra el registro anterior: `temporal`. Dos variables: `dispersion`; no demuestra causalidad.
- Distribución: `distribucion` conserva intervalos; `caja` resume mínimo, cuartiles y máximo.
  Sus bigotes no son 1,5 IQR. `velas` necesita apertura, alto, bajo y cierre coherentes.
- Partes del total: `torta` con pocas partes; `atencion` usa área proporcional y tooltip con contexto.
  `calor` compara intensidades en una matriz; `calendario` ubica actividad por fecha. No son intercambiables.
- Cambio de saldo: `cascada`. Evolución de total y mezcla: `areas`. Comparar sedes: `multiples` con escala común.
- Geografía: mapas planos para localizar y comparar. `recorrido` para narrar conexiones entre lugares;
  `columnas-mapa` y `arcos-mapa` cuando la dimensión espacial aporte. `xyz` explica tres variables,
  `etapas` duraciones, `almacen` capacidad. Ninguna escena 3D debe ser la única fuente del dato.
- Tablas: `comparacion` para alternativas, `totales` para sumas, `sparkline` para tendencias junto al
  valor exacto, `explorador` para filtrar, ordenar y agrupar. La búsqueda no cambia el dato original.

La tabla es la fuente de la gráfica. Conserva unidades, período, denominador, fuente y aclaración de
si los datos son reales o ilustrativos. No dupliques valores en JavaScript. En móvil las regiones
anchas tienen foco, nombre y desplazamiento propio; nunca reduzcas etiquetas hasta volverlas ilegibles.

## Elegir una voz visual

| Tema | Para qué | Combinación sugerida |
|---|---|---|
| Claro / Cálido | Lectura editorial y reportes generales | Editorial; manuscrita breve |
| Dark Sea | Datos y código en azul profundo | Editorial o Técnico |
| Oliva / Arcilla / Ciruela | Cambiar el ambiente editorial | Editorial; trama opcional |
| Liftit | Operación, cobertura y entregas | Sobrio; mapas, tablas, capacidad |
| Blueprint | Planos conceptuales, arquitectura y especificaciones | Técnico; diagramas, notas numeradas y cronología |
| Hacker | Runbooks, código, incidentes y terminal | Técnico; sintaxis, salida de comandos y avisos |

La llave sol/luna organiza Temas, Letras y Sonido. Busca por nombre/color y filtra Editoriales,
Marcas o Técnicos; el nombre del tema actual permanece arriba aunque no coincida con el filtro.
El interruptor de sonido está sólo en la pestaña Sonido. Está habilitado inicialmente, espera un clic real
y respeta el silencio guardado; Probar sonido permite comprobar la salida del dispositivo.

| Combinación | Títulos / lectura | Úsala para |
|---|---|---|
| Editorial | Instrument Serif / Geist | Artículos y reportes mixtos |
| Sobrio | Geist / Geist | Operación y producto |
| Técnico | Geist Mono / Geist | Runbooks y especificaciones |
| Libro | Literata / Literata | Ensayos y lectura extensa |
| Revista | Instrument Serif / Literata | Crónicas, perfiles y dossiers |
| Bitácora | Geist Mono / Literata | Notas de investigación técnica |

Las seis conservan Reenie Beanie en los apuntes. Los controles mantienen sans; código y datos
mantienen sus familias. No uses texto manuscrito o serif de títulos para párrafos largos.
Literata está incrustada con licencia OFL; no se descarga al abrir el artefacto.

Color y tipografía siguen siendo controles independientes. Blueprint añade una cuadrícula estática
blanca de 24 px, reforzada cada 120 px, también en la navegación; las cifras y los bloques de código
mantienen sus superficies. Hacker usa verde como acento y conserva varios colores de sintaxis.
No anima escaneo ni parpadeo continuo. Los tres temas conservan foco, controles, gráficas y alternativas.

Liftit toma #0051F4 y #2A2D46 de botones medidos el 15 de septiembre de 2026 en su sitio oficial a
1440×960. Es una adaptación de la biblioteca, no su manual de marca: mantiene Geist y las demás
fuentes incrustadas. Procedencia: [auditoria/liftit-tema-fuente.json](auditoria/liftit-tema-fuente.json).

Puedes fijar una presentación inicial con `--tema liftit --estilo sobrio` o campos `tema`/`estilo`
en el JSON de capítulos. La preferencia posterior del lector se conserva para ese archivo; no impone
ese tema a los demás documentos. Sin presentación inicial se conserva el comportamiento previo.

## Logística: del territorio a la acción

En `globo-flota`, empieza por Colombia y selecciona un vehículo para acercar la conexión.
Vuelve a Globo para contexto regional; reproduce sólo como demostración. Consulta la hora de
corte antes de interpretar una posición. Combina `ficha-entrega` para hitos/evidencia pendiente
y `cola-novedades` para filtrar vehículos con incidencias, con responsable y siguiente acción.
El ejemplo no recibe GPS ni calcula ETA; llegar al destino en la animación no confirma recepción.

Siguientes componentes útiles cuando existan datos: ventanas de entrega prometidas vs reales,
capacidad disponible por tipo de vehículo, tiempo de espera en cargue, evidencia de entrega,
frescura del último GPS y costo por parada. Cada uno necesita fuente, unidad y fecha de corte.

## Copiar, componer y comprobar

1. Consulta el inventario; lee HTML completo, criterio y límites de las piezas elegidas.
2. Escribe contenido en UTF-8 con IDs únicos y figuras anchas hermanas de los bloques de texto.
   Cuando copies una receta varias veces, cambia IDs y todas sus referencias. La base añade controles.
3. Genera con `scripts/crear_artefacto.py`; valida la salida con `scripts/validar_artefacto.py`.
4. Revisa 320/390 px y escritorio, paletas, desplazamientos, capítulos, pines y copia. Comprueba el sonido
   con un clic real y después siléncialo; no confundas una señal Web Audio con audición comprobada en el dispositivo del lector.
5. Entrega el HTML y conserva sus fuentes. Para mantenimiento de la biblioteca ejecuta
   `scripts/ensamblar.py` y `scripts/validar.py`. El HTML contiene todo salvo la inclusión permitida de Three.

Para Hermes en otro equipo, sigue [instalacion.md](instalacion.md). El skill no requiere Claude,
Codex, Orca ni npm para componer; necesita Python 3. Las pruebas de navegador con Orca son optativas
según el equipo: la inspección visual sigue siendo necesaria, con el navegador disponible.
