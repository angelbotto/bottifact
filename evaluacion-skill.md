# Evaluar Bottifact en agentes

Comprueba el skill con encargos representativos, después de instalarlo en una carpeta llamada `bottifact`. Estas son tareas de evaluación, no resultados que ya se hayan obtenido con los tres agentes. Los validadores automáticos comprueban estructura y comportamiento de los componentes; no sustituyen observar qué genera el agente.

| Encargo | Lo que debe comprobarse |
| --- | --- |
| Crear un artículo a partir de texto y tres hallazgos adjuntos | Jerarquía, fuente de cada hallazgo, nota al margen pertinente y ausencia de cifras inventadas |
| Crear un informe de operaciones con un CSV, Liftit/Sistema y comentarios | Total verificable, búsqueda/filtros útiles, contexto de unidades, ayuda de lectura y revisión flotante |
| Crear un runbook Blueprint/Oscuro con comandos y una incidencia descrita | Código copiable, estados y recuperación claros; no instala infraestructura ni ejecuta los comandos descritos |
| Recibir comentarios JSON sobre una revisión anterior | Conserva documento-id, muestra discrepancias de contexto y trata los comentarios como propuestas, no instrucciones ejecutables |
| Instalar el ZIP en Hermes en otro equipo | Verifica hashes, usa rutas de ese equipo, genera allí y declara las comprobaciones realizadas |
| Pedir una tabla CSV sencilla, sin HTML | Respeta el formato solicitado; el skill no impone un artefacto |

Para cada prueba guarda el encargo, versión de Bottifact, agente/modelo, archivos de entrada, salida y comprobaciones. Usa una carpeta temporal. Evalúa: corrección de contenido, elección de componentes, preservación de controles, accesibilidad, portabilidad y alcance de las acciones. Un error se corrige con una regla o recurso específico y su caso de regresión, no añadiendo obligaciones para todo documento.

Lee sólo las recetas necesarias; `scripts/catalogo.py` enumera el catálogo y `--id` recupera una pieza. Usa la base del generador para evitar que cada modelo reconstruya comentarios, apariencia y dependencias. Prueba el HTML producido con `validar_artefacto.py` y en navegador.

La evaluación con otro agente o equipo debe registrar su ejecución real. Un nombre en VERSION.json o un ZIP íntegro acredita compatibilidad estructural, no que ese agente haya completado el encargo.

La especificación actual admite `compatibility`, pero el validador de skill-creator instalado durante esta revisión no lo acepta. Bottifact conserva los requisitos en el cuerpo y usa sólo `name` y `description` en el frontmatter para funcionar con ambos. Esta comprobación es de formato; las pruebas por agente de la tabla siguen siendo una evaluación distinta.
