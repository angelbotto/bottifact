# Piezas editoriales · medición y adaptación

Se recorrieron /now, /work, /about y el artículo React 19 Part 2 de cmrg.me con Orca a **1440 × 960 px**.
Las medidas provienen de getComputedStyle, getBoundingClientRect y Animation.effect, después de cargar
las fuentes. Evidencia: referencia-piezas-medidas.json y referencia-cronologia-medidas.json.
La primera consulta web no pudo abrir /now y /about; ambas se inspeccionaron después en el navegador.

| Referencia y selector | Medición | Decisión en Nota Tikin |
|---|---|---|
| [/now](https://www.cmrg.me/now), burbuja `li.rounded-2xl` | Geist 13,7 / 19,57 px; padding 12 × 16 px; radio 16/16/16/2 px; separación 8 px. | Variante `conversacion.suelta`; mantiene el cuerpo legible del sistema y no simula un chat conectado. |
| /now, cabecera del bloque de actividad `h2.text-3xl` | 36,4 / 43,68 px; columna 348,8 px en el viewport medido. | Bloque editorial de dos columnas con mosaico de conteos. Los datos proceden de tabla local rotulada, no de GitHub. |
| [React 19 Part 2](https://www.cmrg.me/blog/react-19-part-2-the-code), `pre` y `[data-line]` | Bloque de 768 px; texto de línea Geist Mono 13,7 / 22 px. | Código a 13 / 21,45 px del sistema, numeración y líneas destacadas; copia exacta del texto. |
| React 19 Part 2, `.blockquote-mask` / icono | Caja 512 px en la lista, padding 16 px, radio 4 px; icono 32 × 32 px. | Variante de aviso que reserva espacio para el círculo, con cuerpo legible y títulos explícitos. |
| React 19 Part 2, `.animate-ping` | Ciclo de 1000 ms; escala hasta 2 y opacidad hasta 0 en 75 %; repetición infinita. | Dos ciclos de 1000 ms hasta escala 1,65. Se cancela fuera de pantalla, con documento oculto y movimiento reducido. |
| [/work](https://www.cmrg.me/work), cronología `li`, `h3`, `time` | Separación inferior 40 px; título 18,5 / 28,78 px; fecha 12,1 / 18,76 px. | Variante vertical con punto actual y fechas completas; separación editorial, no duración a escala. |
| [/about](https://www.cmrg.me/about), galería `figure` | Alto 232 px; anchos observados 232 y 348,13 px; radio 28 px. | Galería horizontal con imágenes y pies; 240 px de alto en escritorio, 190 px en móvil, radio 18 px. Valores elegidos para el sistema, no medidos en la referencia. |
| /about y React 19 Part 2, líneas `border-dashed` | Grosor 1 px; máscara horizontal transparente → negro al 15 % → negro al 85 % → transparente. | Acabado **dotted** pedido por Angel, con capa propia y extremos difusos. No se enmascara contenido. |

Los SVG de la galería son ilustraciones originales de muestra; no son fotos de Angel ni imágenes
remotas copiadas del sitio. Cada receta contiene HTML completo, criterio y límites en componentes.md.
La invitación conserva su textura: la capa de marco no sustituye sus pseudoelementos.

El artefacto prioridades.html distingue capacidades propuestas (persistencia de comentarios,
estados completos, migraciones, lectura asistida y composiciones) de estas piezas ya implementadas.

## Verificaciones ejecutadas

- Ensamblador, validador de biblioteca y validador de prioridades.html; 71 recetas presentes.
- Seis grupos de pruebas de composición del contrato, incluyendo todas las recetas utilizables.
- Prioridades: 36 combinaciones de dos páginas × seis paletas × 320/390/1440 px; sin desbordamiento
  documental, regiones con foco/nombre, desplazamiento local y contraste de los tokens usados.
- Código: seis líneas, selección 3/6, texto completo intacto, interlineado continuo. Clic nativo
  de copiar con writeText sustituido para capturar el argumento; no lectura del portapapeles físico.
- Actividad: suma 30, contexto 8/30 = 26,7 %, escala hasta 8, caso cero y dato negativo inválido.
- Pulso: frames presentados entre scroll y comprobación del observador; entrada, salida, evento
  MQL explícito y destroy/init. Galería: desplazamiento real, avance, fin y regreso; límites con
  movimiento reducido simulado. No prueba de un teléfono físico ni lector de pantalla.
- Biblioteca: 162 combinaciones de nueve capítulos × seis paletas × 320/390/1440 px, interacciones,
  regresiones de informe y plantilla, y PDF. Los últimos ajustes de la capa de marco y los botones
  móviles se verificaron después en las 36 combinaciones del artefacto.

La inspección visual detectó que `.pieza > * + *` daba margen superior a la nueva capa decorativa.
Se fijó su margen a cero y la prueba ahora comprueba la coincidencia de sus bordes con la figura.
Los botones de galería usan una rejilla de tres columnas para mantenerse alineados en móvil.
El texto de las piezas no recibe máscara ni desenfoque.
