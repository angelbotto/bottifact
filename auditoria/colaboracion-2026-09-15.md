# Revisión, tablas y distribución · 15 septiembre 2026

Versión `2026.09.15-colaboracion.1`: 82 recetas, once paletas y seis estilos. Dos temas nuevos: Linear Light/Dark, adaptaciones propias. Las demos `colaborativo.html`, `linear-light.html` y `linear-dark.html` reúnen una tabla de 36 filas ficticias y los controles estándar.

## Cambios

- Comentarios: guardado de eventos locales por documento, respuestas, responsables declarados, resolver/reabrir, archivo de hilos, historial y exportación/importación JSON idempotente. Ancla semántica con cita; los bloques modificados no reciben pines equivocados. El prompt incorpora sólo abiertos. No hay backend, identidad verificada ni sincronización entre equipos.
- Tabla exploradora: ya no exige cuatro columnas. Hasta 16 columnas y 2000 filas; texto, número y fecha ISO. Filtros por columna/rango, orden múltiple con Mayús, grupos plegables de la página, selección entre páginas, CSV, densidad y paginación. El total es de la vista filtrada. Imprimir recupera la fuente completa y después restaura la vista.
- Temas: neutros fríos, lavanda, tokens completos para piezas y datos. Se corrigió la regla del sistema oscuro para que no sobrescriba paletas explícitas.
- Skill: entrada de 72 líneas con catálogo compacto por CLI y referencias específicas. Mismo generador para Claude/Codex/Hermes; metadatos de interfaz para Codex. No depende de Orca para crear HTML.
- Distribución: repositorio privado, instrucciones de clone/ZIP y CI con acciones fijadas por commit y permisos de lectura. ZIP con manifiesto, instalación con respaldo y pruebas independientes del cwd.

## Evidencia

`probar_revision_store.cjs` comprueba convergencia entre instancias sobre el mismo almacenamiento, respuestas, historial, importación duplicada, documento equivocado, colisión de IDs, anclas inválidas y rollback por cuota. Los cambios en memoria se señalan cuando localStorage falla.

`comprobar_colaboracion.py` comprueba filas/paginación, selección, CSV, filtros numéricos/fechas, grupo plegable, impresión, creación/respuesta/resolución, recarga y ancla cambiada. Geometría y contraste textual ≥4.5:1 sobre tres superficies, en ambos temas a 320, 390 y 1440 px. La selección de archivo y la descarga del navegador no se acreditan por comprobar el API de importación/exportación.

`comprobar_colaboracion_ui.py` recorre ambas paletas con el sistema claro/oscuro, verifica selector e interfaz de revisión en 320/390/1440 px. Las capturas pueden usar el tamaño de la ventana anfitriona de Orca; las medidas JSON registran el viewport efectivo. Las interacciones son eventos DOM, no una sesión de teclado físico, pantalla táctil o lector de pantalla.

Se ejecutaron generación, validación estática, siete grupos de contrato y validación del skill. El ZIP se instaló en una carpeta aislada y generó un documento desde /tmp. Esto no acredita que el MacBook haya instalado o recargado el skill.

## Decisión de stack

Conservar el núcleo portable. Proponer una aplicación conectada TypeScript/React, TanStack Table y Postgres/Auth/Realtime para permisos, versiones y presencia. No se provisionó ese servicio. Detalles y fuentes primarias en arquitectura.md y colaboracion.md.

## Repositorio y automatización

Repositorio privado: https://github.com/angelbotto/nota-tikin, rama main. Primera CI correcta sobre 5cb30c7: https://github.com/angelbotto/nota-tikin/actions/runs/35040944132. Generó y comprobó fuentes, contratos, revisión, skill y paquete en Ubuntu/Python 3.11. Las pruebas de navegador registran por separado anchos efectivos e interacción DOM local.
