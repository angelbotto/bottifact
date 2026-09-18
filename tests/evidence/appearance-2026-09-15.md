# Apariencia escalable · 15 septiembre 2026

Cambio solicitado por Angel: organizar muchos temas, habilitar sonido inicialmente, ampliar combinaciones tipográficas. Contrato 4. No añade paletas en esta iteración; conserva las nueve y Sistema.

## Resultado

Llave sol/luna con Temas / Letras / Sonido. Búsqueda por nombre/descripción sin distinguir tildes, familia, contador, restablecimiento y dos columnas de muestras. Tema activo nombrado y tarjeta seleccionada visible al abrir. Panel máximo 360 px, ajustado al viewport con 12 px de separación. Las listas tienen altura máxima de 282 px y desplazamiento local. La pestaña también se desplaza si falta altura; encabezado, pestañas e interruptor no se comprimen. No se añaden animaciones al selector.

Seis combinaciones: Editorial, Sobrio, Técnico, Libro, Revista y Bitácora. Literata normal/itálica 400–700, latín y latín extendido: cuatro WOFF2, 316.776 bytes antes de base64. Procedencia y hashes en literata-fuentes.json; OFL incluida. Este peso se incorpora al HTML autocontenido. Reenie Beanie y las grabaciones originales se conservan.

La preferencia de sonido empieza habilitada en la receta nueva, pero el contexto empieza sin crear. El primer clic real desbloquea el contexto sin sonido de arranque. Apagar se recuerda por origen, detiene voces e invalida una activación pendiente. Salir pausa sin convertir esa pausa en una elección de silencio. El canal independiente conserva su inicio apagado. Esta decisión sustituye expresamente el OFF inicial solicitado en versiones anteriores.

Bug corregido: el empaquetador omitía la carpeta licencias, aunque las fuentes estaban incrustadas. Ahora incluye todos los textos OFL. También se actualizó documentación antigua que todavía describía un tono de prueba de 450 ms: el componente reproduce la grabación original del clic.

## Verificaciones ejecutadas

- `python3 scripts/build.py` y `python3 scripts/validate.py`: fuentes sincronizadas, CSP, IDs, anchos, inventario y contrato 4.
- `python3 scripts/test_contract.py`: siete grupos, incluidas las recetas componibles y rechazo de omisiones de pestañas/búsqueda/estilos.
- `python3 scripts/check_explorer_appearance.py` (ejecutado antes de renombrarlo, con el mismo contenido): 81 combinaciones de nueve paletas × tres pestañas × 320×740, 390×844 y 1440×960; interruptor dentro del panel y viewport; 18 combinaciones de tipografía; filtro con tildes, intersección vacía, restablecimiento y 50 etiquetas de prueba con scroll. Los 40 temas extra sólo viven en el navegador de prueba.
- `python3 scripts/check_typography.py`: 156 combinaciones, 13 páginas × seis estilos × 320/390 px. Sin desbordamiento del documento; regiones amplias con foco, nombre y desplazamiento. No repite toda la matriz de colores de las gráficas, ya que no se cambiaron sus tokens.
- `python3 scripts/check_audio_output.py`: clic y lápiz originales con clic nativo, señal de AnalyserNode después del gain maestro, volumen cero y fallo simulado de AudioContext.
- `python3 scripts/check_audio_preference.py`: silencio durante resume demorado, cancelación de la activación, pagehide simulado y reactivación tras clic real. La primera prueba de ocultación usó document.hidden, pero el host no permite redefinirlo; se cambió a pagehide, sin afirmar una prueba de visibilidad física.
- `python3 scripts/check_guide_interactions.py`: ocho interacciones de tablas, prototipo, comentarios e inicialización; 71 HTML exactos del registro; gesto nativo de lápiz y cancelación con MQL explícito.
- `python3 scripts/test_portability.py`: dos grupos, instalación/actualización en temporal, conservación de copia anterior, verificación, generación desde otro directorio y rechazo de alteraciones.

## Límites

Navegador embebido de Orca en el Mac mini. Las teclas de navegación se ensayaron con eventos DOM, no teclado físico ni lector de pantalla. La señal de audio medida no acredita audición humana ni el dispositivo del MacBook. Las capturas de Orca contienen el lienzo del navegador anfitrión: el viewport CSS medido se registra en JSON. No se instaló Hermes remotamente en el MacBook. El nuevo ZIP permite actualizarlo con las mismas fuentes.
