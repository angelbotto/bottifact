# Ajustes de /work y skill compartido · 15 septiembre 2026

## Referencia medida

Orca `goto`, `exec set viewport 1440 960` y `eval` con `getComputedStyle` sobre
https://www.cmrg.me/work. Datos crudos: referencia-work-ajustes.json.

- Galería: figure 232px de alto, radio 28px; lista gap 12px y padding vertical 12px.
  Sombra de la figura: 3px 4px 10px, color de superficie oscura al 20%.
  Pie absoluto con 16px laterales, 10px inferiores, mono 12.1px/16.1333px.
  Un span añade el degradado de fondo y otro el contorno interior.
- Cronología: conectores de 1px; el primer tramo pasa de naranja a gris, los siguientes
  a grises más apagados. Los conectores medidos prolongan el tramo hasta el siguiente hito.
  Cada hito salvo el último tiene 40px de padding inferior.

## Aplicación

Bug corregido: antes cada li dibujaba una línea desde top:14px hasta bottom:0, dejando
un hueco antes del siguiente punto. Ahora una única línea en la lista cruza todos los
hitos y se desvanece al final. Se conservan texto, fechas y contraste completos.

Actividad: `data-actividad-tabla` referencia datos hermanos del marco. La fuente sigue
siendo una tabla única. El contrato comprueba que exista el ID; sin atributo, los
artefactos anteriores siguen buscando la tabla dentro de la pieza. Se reservan 20px entre
línea vertical del marco y contenido, y se elimina el margen heredado de la segunda columna.

Galería: variante `galeria-fotografica`, scroll nativo y sin botones. Radio/sombra/altura/gap
siguen las medidas; pies superpuestos con rejilla para que un texto que crezca no se corte.
El pie usa contraste de tokens propio en seis paletas. No hay scroll programado ni snap en
esta variante. Los controles del componente anterior siguen funcionando si se incluyen.
Las imágenes de demostración siguen siendo SVG originales, no fotografías de la referencia.

El skill ahora explica cómo elegir la frase que merece un subrayado y añadir un apunte que
aporte pregunta, consecuencia o matiz. prioridades.html incluye ejemplos derecho e izquierdo,
animación al entrar y sonido optativo. La información esencial permanece en texto normal.

## Comprobaciones

- `python3 scripts/ensamblar.py`, `python3 scripts/validar.py`,
  `python3 scripts/probar_contrato.py`: fuentes, CSP, IDs, seis paletas, 71 recetas y contrato.
- `python3 scripts/comprobar_piezas_editoriales.py`: 36 combinaciones de dos páginas × seis
  paletas × 320×740, 390×844 y 1440×960; interacción, copia exacta con destino simulado,
  dato cero/inválido, marcos, pulso, galería nativa y controles anteriores.
- Después de ampliar el margen interno de actividad, `python3 scripts/comprobar_ajustes_work.py`
  comprueba 18 combinaciones de geometría: datos fuera del marco, 20px internos, continuidad
  de línea, texto sin máscara y pie dentro de imagen. Capturas de las tres piezas y de apuntes
  en los tres viewports; inspección visual de escritorio y móvil.
- `python3 scripts/comprobar_biblioteca.py`: 162 combinaciones (nueve capítulos × seis paletas ×
  tres viewports), ocho interacciones, dos regresiones y PDF. Ejecutado tras el último cambio CSS.
- Skill Creator `quick_validate.py .`: metadatos válidos.

Orca keypress/exec press no produjo eventos keydown en esta sesión, pese a tener enfocada
la región. La prueba de galería usa scrollBy/scrollTo y comprueba foco/nombre/desplazamiento;
no acredita teclado físico. No se hizo una sesión de lector de pantalla ni audición humana.

## Hermes

Hermes está instalado en este Mac. Su `agent/skill_utils.py:iter_skill_index_files` recorre
los directorios con `os.walk(..., followlinks=True)`; `tools/skills_tool.py` descubre skills
en ~/.hermes/skills. Se añadió un enlace nota-tikin a ~/.agents/skills/nota-tikin, que resuelve
la misma copia canónica de Claude. Sin copiar archivos ni cambiar configuración de otros skills.
La comprobación usa el descubridor y `skill_view` reales de Hermes, no sólo existencia de archivo.
Hermes emite una advertencia de ubicación por el symlink externo, pero carga la instrucción y
sus recursos correctamente. No se cambió su configuración de confianza.
Las instrucciones resuelven rutas desde el skill y no requieren un agente particular.

Hermes: `auditoria/hermes-compartido.json` registra descubrimiento y lectura de instrucción/registro,
generación y validación desde la ruta Hermes, más igualdad SHA-256 de las dos entregas por HTTPS.
El ensamblador y el validador también se ejecutaron en la copia instalada, sin diferencias git.

Audio del apunte de prioridades: ejecutada la prueba `comprobar_audio_salida.py` adaptando
URL, ID del apunte y nombre del botón al nuevo artefacto. Clic nativo, analizador tras volumen
maestro: tono RMS 0.03899, lápiz RMS 0.05773, pico del lápiz 0.10530. Volumen cero termina
en señal cero y un constructor AudioContext bloqueado conserva el estado apagado. Evidencia
en prioridades-audio.json. Esto acredita señal Web Audio, no audición física en el MacBook.

PDF de prioridades servido por Tailscale: seis páginas; tabla de actividad completa,
último período y ambos capítulos presentes. Evidencia en prioridades-impresion.json.
