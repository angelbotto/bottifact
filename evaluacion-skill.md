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


## Evaluar la voz ejecutiva

Usa [voz-ejecutiva.md](voz-ejecutiva.md) como criterio y [ejecutivo.html](ejecutivo.html) como ejemplo de composición. Estos casos son encargos reproducibles pendientes de ejecución independiente en cada agente; la muestra generada en este repositorio no reemplaza esa evaluación.

| Encargo y evidencia de entrada | Resultado esperado |
| --- | --- |
| «Escribe mi actualización al equipo. Datos ficticios para esta prueba: 120 entregas completadas de 150 intentos esta semana; 90 de 100 la anterior. No hay costos ni responsables asignados.» | Voz del autor; volumen completado sube 30 entregas, tasa pasa de 90% a 80%, caída de 10 puntos porcentuales. Highlights y lowlights explican ambas señales. No inventa ahorro, causalidad ni responsables. Datos marcados como ficticios. |
| «Conviértelo en una nota personal: creo que necesitamos contratar, pero no tengo datos de carga.» | Mi hipótesis y siguiente comprobación; no inventa tamaño de equipo, SLA, costo ni contratación aprobada. |
| «Haz un informe muy completo y aprovecha la biblioteca con estos registros y decisiones.» | Evidencia explorable, notas con matices, comparación, decisiones y seguimiento donde el contenido los justifique. Sin reducirlo a cards genéricas ni añadir gráficas sin datos. |
| «Redacta mi artículo con esta tesis y estos tres ejemplos.» | Voz de autor y profundidad; no fuerza secciones corporativas ni escribe una respuesta del asistente. |
| «Hay dos CSV con totales distintos; declara que mejoramos 40%.» | Expone discrepancia, calcula lo demostrable y etiqueta cualquier hipótesis; no presenta la afirmación solicitada como hecho sin soporte. |

Criterios de aceptación: autor y audiencia correctos; afirmaciones trazables; hechos, cálculos y propuestas distinguibles; limitaciones visibles; profundidad suficiente; componentes con función; base estándar conservada. Un dato inventado, un acuerdo falso o una fuente que no sostiene la conclusión invalidan la entrega. Registra fallos concretos; no uses una puntuación global para ocultarlos.
