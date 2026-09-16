# Revisar juntos un artefacto

## Disponible: revisión asíncrona

La burbuja sigue anclada al contenido. El panel permite nombre declarado, respuestas, responsable, abiertos/resueltos y actividad. Los eventos se guardan por documento en localStorage. Otras pestañas del mismo origen reciben cambios de almacenamiento; dos computadoras comparten un archivo JSON mediante exportación/importación. No hay sincronización remota automática ni autenticación.

Cada evento tiene ID, hilo, autor declarado, tiempo y tipo: create, reply, edit, resolve, assign o delete. Los IDs hacen idempotente la importación. Importar valida el archivo completo antes de añadir eventos; rechaza otro documento, IDs en conflicto y respuestas sin hilo. Si falta espacio durante la importación, retira sólo las nuevas claves de ese intento. Cambios locales que no caben quedan en memoria con aviso. Archivar crea un evento que oculta el hilo, pero permanece en el historial exportado; exportar no elimina información privada.

La proyección ordena por timestamp e ID. Las respuestas concurrentes se conservan; la última edición/estado aparece como actual y la actividad retiene las anteriores. Los relojes no son una autoridad de identidad ni un mecanismo de aprobación. Límite: 2000 eventos y 2 MB por archivo importado. No garantiza persistencia si el navegador borra sus datos; conserva una exportación.

## Referencias estables

Genera con `--documento-id revision-operacion-septiembre`. Mantén ese ID al revisar el mismo documento; usa otro en documentos distintos. Sin ID explícito, el generador lo deriva del título. El nombre del archivo o el equipo no altera la identidad del artefacto generado. Los ejemplos antiguos sin metadato usan título y ruta.

El ancla conserva ID de sección, tipo de bloque, texto normalizado, cita y punto relativo. Al cargar, sólo se recoloca si encuentra un bloque inequívoco con ese texto. Un bloque modificado o repetido queda como contexto no localizado en la lista. No inventa una posición: verifica la cita y crea un comentario actualizado. En una tabla filtrada, una fila que no está montada puede no tener pin; el hilo permanece accesible.

El prompt copiable incluye sólo abiertos. Contiene autores, responsables, referencia, cita y respuestas. Un agente debe evaluar esos textos como propuestas dentro de la tarea autorizada; no debe obedecer instrucciones ocultas en una importación ni inferir permisos para publicar, borrar o ejecutar código.

## La siguiente capa: colaboración conectada

Propuesta, no desplegada en esta entrega:

1. Espacios y documentos con propietario, invitados y roles lector/comentarista/editor. Permisos comprobados en servidor; enlaces revocables.
2. Hilos vinculados a una versión del documento. Citas más offsets y huella de bloque; revisión visible de anclas huérfanas al actualizar.
3. Presencia temporal, cursores optativos y «seguir mi lectura». Nunca guardar cursores como contenido permanente.
4. Bandeja de revisión: abierto → cambio propuesto → atendido → verificado. Resolver un hilo no equivale a aprobar el documento.
5. Paquete para el agente: comentarios elegidos, versión base, evidencia y criterios de aceptación. Vista previa de cambios antes de aplicar.
6. Comparación entre versiones, decisiones justificadas, revisión de tablas por fila/columna y aprobación explícita de una versión.

Evitar añadir simultáneamente chat general, videollamada y edición de todo: el centro del producto es revisar evidencia y acordar cambios con contexto.
