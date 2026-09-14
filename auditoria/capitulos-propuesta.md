# Próximos componentes para notas, artículos e informes

La tanda actual implementa capítulos, pestañas locales y ficha de hallazgo. La navegación
por capítulos conserva contexto y URL; las pestañas alternan vistas cortas; la ficha evita
confundir una hipótesis con una observación. La firma y tres paletas nuevas completan la muestra.

Las siguientes son propuestas analizadas, **todavía no implementadas**:

| Prioridad | Componente | Uso concreto | Criterio y límite |
|---|---|---|---|
| Alta | Captura anotada | Explicar dónde ocurre un problema de interfaz con puntos numerados y una lista vinculada. | Imagen incrustada, controles con foco y texto fuera de la imagen. Las coordenadas deben adaptarse al ancho; no basta un tooltip al pasar el cursor. |
| Alta | Comparador de prototipos | Recorrer la misma tarea en dos alternativas A/B. | Reutilizar NotaVisores con estados sincronizados de forma explícita. No emula apps remotas ni constituye un experimento A/B por sí mismo. |
| Alta | Registro de revisiones | Mostrar qué cambió en un artículo o informe y por qué. | Fecha, versión, autor y cambio concreto; comparar fragmentos seleccionados. No inferir ni inventar historial Git/publicación. |
| Media | Matriz de criterios | Comparar alternativas respecto a requisitos, evidencia y concesiones. | Reutilizar las tablas existentes. Pesos y puntuaciones necesitan procedencia; una suma opaca no debe decidir automáticamente. |
| Media | Registro de riesgos y mitigaciones | Conservar causa, consecuencia, responsable, señal observable y siguiente revisión. | Tabla con estados escritos. Evitar multiplicar escalas ordinales para aparentar precisión numérica. |
| Media | Cohortes | Seguir retención por fecha de inicio y edad de cada grupo. | Extender calor con denominadores y ventanas comparables. Distinguir cero, ausencia y período todavía no observable. |

No añadiría por ahora carruseles automáticos, adornos Three sin pregunta concreta ni
contadores que animen cifras: no aportan a la lectura o pueden aparentar evidencia.
