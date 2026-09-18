# Fidelidad de escritura, sonido y galería · 15 septiembre 2026

Petición de Angel: usar el sonido original, conservar la tipografía manuscrita y acercar la
presentación de galería a cmrg.me. Sustituye la decisión anterior de sintetizar el audio.

## Medido en la referencia

Orca, /work a 1440×960, getComputedStyle y recursos servidos por el sitio:

- Reenie Beanie 400; nota lateral 28.5px/32px, tracking −.7125px; nota editorial grande
  36.4px/40px, tracking −.91px. Archivo WOFF2 de 17936 bytes: SHA-256
  aa3901be682af0f1faac8436a1f25438b0cc541b6ad2ece5668ae4c0ea70594a.
  La fuente ya incrustada es idéntica byte por byte. El problema era que packages/core/components/handwriting.js la sustituía
  por un alfabeto SVG propio. La variante nueva conserva esa fuente real y revela caracteres.
- El chunk 13nl53-l3csj9.js aplica transición de opacidad de 375ms por carácter, escalonada
  para terminar sobre una de las tres grabaciones de lápiz (2.181333, 2.565333, 3.034667s).
  La referencia introduce 1000ms de demora en la nota lateral; Nota empieza al entrar/repetir,
  sin esa demora ni el disparador de escritorio exclusivo. No se afirma una copia de toda la animación.
- En /, los subrayados inspeccionados tienen tres pasadas irregulares, grosor 2px, color
  naranja al 25%, aproximadamente 1s entre todas. Nota usa tres curvas normalizadas y
  conserva ese grosor/opacidad/duración, sin importar un motor adicional.
- Galería: 232px de altura, separación 12px, sombra 3px 4px 10px; radio 28px con
  corner-shape:superellipse(1.6). Un radio circular de 28px no tenía la misma silueta.
  El velo va desde oscuro abajo, 40% de opacidad a 45%, hasta transparente arriba.
  El pie no tiene fondo propio: padding 0 16px 10px, mono 12.1px/16.1333px.
  Cursor calculado grab; arrastre de ratón, desplazamiento nativo con tacto.

Datos crudos en fidelidad-cmrg-medidas.json. La muestra sigue usando ilustraciones propias,
rotuladas como tales; el componente admite fotografías incrustadas con el mismo tratamiento.

## Sonidos

Siete MP3 originales sin modificar: pencil-1/2/3, hover, click, positive y negative.
Procedencia y hashes: sonidos-cmrg.json y packages/core/assets/reference-audio/PROVENANCE.md.
Los bytes incrustados en packages/core/components/audio.js son idénticos a esos archivos; no hay fetch ni descargas
al leer. Se decodifican al activar; se conservan dinámica y tono, sin ruido generado,
normalización ni bucle. Volúmenes del sitio multiplicados por el maestro del lector (.65).
La base usa grabaciones también para los botones del componente Sonido: no abre otro
sintetizador cuando packages/core/components/audio.js está presente. La implementación aislada antigua se conserva.

Sigue apagado al cargar, con gesto real, estado de error, volumen y cancelación. No se
adoptó el sonido automático sobre foco/scroll de otros sitios. La escritura sólo suena al
activar Sonidos y llevar data-escritura-sonora.

## Verificación ejecutada

- Ensamblador, validador y seis grupos del contrato; 71 recetas componibles.
- Skill Creator quick_validate.py: metadatos válidos.
- comprobar_fidelidad.py: 54 combinaciones (tres piezas, seis paletas, 320×740, 390×844,
  1440×960); medidas de ancho/scroll/contraste, fuente real, progreso de caracteres,
  entrada única, salida, repetición, cancelación MQL y restauración de nodos.
- Arrastre nativo mediante Orca mouse move/down/up: 180px, pointerdown isTrusted,
  cursor grab y liberación correcta. No encabezado interno de galería.
- comprobar_audio_salida.py: clic nativo y analizador tras volumen maestro, lápiz con señal
  RMS .003999 y pico .048036 en la ejecución registrada; volumen cero termina en cero,
  y AudioContext bloqueado mantiene apagado con explicación. El test anterior exigía RMS
  mayor a .01, que forzaría amplificar el original: ahora comprueba señal >.0001 y pico <1.
- Cancelación integrada: audio y animación se detienen al emitir cambio MQL reducido.
  Los siete buffers se decodifican; cero recursos /sounds/ descargados en el artefacto.
- Después del ajuste final a 25% de opacidad del subrayado: seis paletas de contraste
  manuscrito (28.5px, mínimo 3.34:1, texto grande) y nuevas capturas a 320/390/1440.
- Corrección de contexto: al comentar texto animado se ignoran copias aria-hidden;
  una frase se captura una sola vez. Evidencia en fidelidad-contexto.json.

Capturas finales inspeccionadas en escritorio y móvil. Reducción mediante evento MQL explícito;
no audición humana, no prueba de altavoces del MacBook ni sesión de lector de pantalla.
