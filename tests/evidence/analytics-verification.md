# Verificación — diez gráficas y laterales

Ejecutado en el navegador de Orca del Mac mini, con el servidor local y CSP del artefacto.

- `python3 scripts/build.py` y `python3 scripts/validate.py`: seis HTML sincronizados,
  54 recetas, IDs, rejilla, dependencias, CSP, tokens, enlaces y sintaxis de los módulos.
- `python3 scripts/check_analytics.py`: 13 contratos de datos e interacción. Comprueba
  total de torta, fechas reales en áreas, extremos OHLC, mínimo/máximo de cajas, cero/ausencia
  del calendario, área de burbujas, grosor de rutas, alturas y sección de tubos 3D, selección,
  errores de entrada, idempotencia y conservación de tablas al destruir.
- 72 combinaciones: seis paletas × dos capítulos × viewports 320×740, 390×844, 1200×700,
  1440×960, 2048×730 y 2560×900. Sin desborde del documento; tablas y lienzos anchos tienen
  desplazamiento local, foco y nombre. Índice y regla debajo del borde medido de la cabecera.
  Porcentaje separado del cursor; posiciones 0, 24 y 100 % verificadas.
- `python3 scripts/check_analytics_webgl.py`: columnas, arcos y almacén con renderer real.
  RAF activo al activar giro, cero al ocultar el capítulo y con movimiento reducido. Recursos
  liberados en destroy; tabla intacta. Dependencia Three ausente simulada para verificar fallback.
- Se ejecutó también `scripts/check_reading.py` tras corregir el recorte: seguimiento,
  Home/End, cambio de capítulo y 324 combinaciones de navegación anteriores a la ampliación.

- `python3 scripts/check_library.py`: 162 combinaciones (nueve capítulos, seis paletas,
  320/390/1440 px), contraste, rótulos SVG y regiones; ocho interacciones de biblioteca,
  regresiones del informe y catálogo continuo, y exportación PDF con capítulos completos.

Evidencia JSON: analitica-interaccion.json, analitica-pantallas.json, analitica-webgl.json.
Las capturas finales se guardan en capturas/analitica-*.png.

Límites: clics y teclado sintéticos salvo uso nativo del navegador durante inspección visual;
no lector de pantalla ni teléfono físico. Preferencia reducida emulada por Orca con evento MQL
explícito para ejercitar el listener; no cambio físico de la preferencia del sistema operativo.
El fallback sin Three no reproduce un fallo físico de GPU. No se evaluó audición manual porque
las vistas nuevas no emiten sonido. Los ejemplos no se conectan a datos reales de empresas.


En esta sesión, Orca compone mal las capturas de más de 1639 px: repite una franja a la derecha.
Se contrastó con DOM y elementFromPoint: un solo índice visible (x=20, ancho=160) y la regla
correcta en x=1972…2036 a 2048 px, documento de 2048 px. Se descartó esa captura compuesta;
la inspección visual de cabecera usa 1639 px. Las pruebas DOM a 2048/2560 sí se ejecutaron.
