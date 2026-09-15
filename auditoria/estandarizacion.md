# TIKIN-629 · Estandarizar antes de ampliar

Revisión local del 14–15 de septiembre de 2026. Se inspeccionaron las fuentes, el ensamblador,
las instrucciones que consume Claude, el registro y los artefactos generados. No se recibió aún
la URL de un artefacto específico de Claude que omita controles: el diagnóstico siguiente está
probado sobre la biblioteca, no sobre una entrega externa no inspeccionada.

## Hallazgos y consecuencias

1. **El ejemplo recomendado no cumplía la preferencia.** `SKILL.md` recomendaba `informe.html`
   para informes completos. Su construcción en `scripts/ensamblar.py` cargaba apariencia pero
   no `revision.js` ni su montaje. Por eso partir de ese ejemplo no producía comentarios.
   Se incorporó el montaje flotante y el módulo, conservando el contenido del informe.
2. **La biblioteca y la entrega tenían verificaciones diferentes.** `scripts/validar.py`
   comprobaba ejemplos fijos. Un HTML nuevo podía omitir controles aunque la biblioteca pasara.
   Ahora `crear_artefacto.py` compone la base y `validar_artefacto.py` examina la salida elegida.
3. **Las instrucciones permitían interpretaciones distintas.** Consultar todo el registro no
   distinguía entre controles comunes y componentes de contenido. Ahora se exige una base con
   apariencia circular, comentarios, audio optativo e índice/regla, y se selecciona el contenido
   según su utilidad. Las variantes anteriores conservan compatibilidad.
4. **Audio activo no significaba reproducción comprobada.** El controlador anterior esperaba
   `resume()` sin comprobar explícitamente `state === 'running'` y ocultaba el fallo al usuario.
   Además el interruptor aparecía después de los colores y estilos en un panel largo. Se añadió
   prueba de 450 ms, volumen, estado y reintento al principio del panel. El lápiz usa ruido
   normalizado y envolvente durante el trazo; no se añadió reproducción al cargar.
5. **La entrega no identificaba sus fuentes.** La nueva base incluye un manifiesto con versión
   de contrato y hashes del CSS/JS incrustado. El verificador detecta una fuente vieja o alterada;
   la migración automática de documentos anteriores sigue pendiente.

El estado de AudioContext depende del navegador. La activación requiere interacción del usuario;
una interrupción también puede requerir reanudarlo. Fuentes: [Chrome, Web Audio y autoplay](https://developer.chrome.com/blog/web-audio-autoplay)
y [MDN, estados del contexto](https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/state).
Un contexto activo no acredita volumen físico, salida seleccionada ni retransmisión desde una
vista remota. Abrir el enlace Tailscale en el navegador del MacBook permite probar en ese equipo.

## Cambios implementados

- Generador sin instalaciones/red para una página y capítulos; dependencias declarativas,
  una inclusión de Three fijada cuando corresponde, fuentes inline, índice por h2 y comentarios.
- Verificación de controles, paletas, referencias, rejilla, foco/nombre de regiones, versiones
  exactas de módulos y manifiesto. No es un sanitizador ni una prueba visual.
- Lectura continua de capítulos sin JavaScript; comentarios y controles interactivos requieren JS.
- Entrada principal del skill actualizada: generar, verificar el archivo final y probar en navegador.
- Demostraciones reproducibles `estandar.html` y `estandar-capitulos.html`. No se añadieron recetas
  para inflar el inventario: se conservan las 65 y se probó su composición con la base.

## Prioridades siguientes — propuestas, aún sin implementar

| Prioridad | Mejora | Problema que resuelve | Límite propuesto |
|---|---|---|---|
| 1 | Exportar/importar revisiones | Los comentarios desaparecen al recargar. | Archivo local con versión y contexto; no prometer colaboración remota. Detectar anclas que ya no existan. |
| 2 | Estados completos en las recetas | La demostración feliz no enseña qué hacer cuando falta información. | Vacío, error, carga sólo si hay tarea asíncrona, dato ausente y lectura sin interacción. No simular una conexión. |
| 3 | Versiones y migración revisable | Documentos ya publicados no reciben controles nuevos. | Identificar módulos, proponer diff y conservar contenido/comentarios; no reescribir silenciosamente. |
| 4 | Lectura asistida y exportación | DOM válido y captura correcta no equivalen a experiencia accesible completa. | Sesión con lector de pantalla, teclado, impresión y datos largos; registrar navegador/dispositivo. |
| 5 | Composiciones por intención | Un catálogo de 65 piezas exige elegir bien. | Recetas de informe financiero, artículo y revisión de prototipo sobre la misma base; datos reales o ejemplos rotulados. |

No propongo cambiar otra vez la estética ni añadir una dependencia de React/shadcn: la necesidad
observada es consistencia de la entrega. Un registro compatible con herramientas externas sería
otro alcance, con distribución, versiones y soporte definidos.

## Evidencia de esta revisión

- `python3 scripts/ensamblar.py` y `python3 scripts/validar.py`: generación y contratos locales.
- `python3 scripts/probar_contrato.py`: composición del inventario, una/varias páginas, controles
  ausentes, módulos viejos, referencias rotas y figuras atrapadas. Apariencia/revisión se incorporan
  desde la base; Configuración se prueba con el archivo editorial que necesita.
- `auditoria/estandar-navegador.json`: 36 combinaciones (dos documentos × seis temas × tres
  viewports: 320×740, 390×844, 1440×960), panel y audio visibles, comentarios sin salto de altura,
  prompt con contexto, capítulos y tabla desplazable en ambos anchos móviles.
- `auditoria/audio-salida.json`: clics nativos de Orca, AnalyserNode después del volumen maestro,
  30 muestras cada 20 ms. Pico/RMS máximos del tono: 0,0770/0,0394; lápiz: 0,1053/0,0577.
  Son amplitudes digitales normalizadas, no dB SPL. Con volumen cero, pico 0 tras 200 ms de
  asentamiento; las muestras iniciales aún contienen la cola anterior. Fallo de constructor
  simulado: control apagado y mensaje visible. No se hizo audición manual ni prueba en el MacBook.

Las pruebas estructurales no sustituyen la revisión del archivo final de cada nueva entrega.
Los artefactos publicados no se modifican por sincronizar este skill.

Regresiones adicionales ejecutadas: `comprobar_lapiz.py` (entrada, duración, salida, repetición,
reducción mediante evento MQL, apagado y tooltip con puntero nativo), `comprobar_gesto_audio.py`
(hover nativo, scroll/foco silenciosos, lápiz explícito) y `comprobar_biblioteca.py` (162 combinaciones:
nueve capítulos × seis temas × 320/390/1440 px; regiones, rótulos y contraste, navegación y PDF).
La cabecera del skill también pasó `quick_validate.py`. No equivale a una sesión ejecutada por
Claude ni a una prueba con lector de pantalla.
