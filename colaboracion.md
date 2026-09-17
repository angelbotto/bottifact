# Revisar juntos un artefacto

## Archivo standalone: revisión asíncrona

La burbuja sigue anclada al contenido. El panel permite nombre declarado, respuestas, responsable, abiertos/resueltos y actividad. Los eventos se guardan por documento en localStorage. Otras pestañas del mismo origen reciben cambios de almacenamiento; dos computadoras comparten un archivo JSON mediante exportación/importación. No hay sincronización remota automática ni autenticación.

Cada evento tiene ID, hilo, autor declarado, tiempo y tipo: create, reply, edit, resolve, assign o delete. Los IDs hacen idempotente la importación. Importar valida el archivo completo antes de añadir eventos; rechaza otro documento, IDs en conflicto y respuestas sin hilo. Si falta espacio durante la importación, retira sólo las nuevas claves de ese intento. Cambios locales que no caben quedan en memoria con aviso. Archivar crea un evento que oculta el hilo, pero permanece en el historial exportado; exportar no elimina información privada.

La proyección ordena por timestamp e ID. Las respuestas concurrentes se conservan; la última edición/estado aparece como actual y la actividad retiene las anteriores. Los relojes no son una autoridad de identidad ni un mecanismo de aprobación. Límite: 2000 eventos y 2 MB por archivo importado. No garantiza persistencia si el navegador borra sus datos; conserva una exportación.

## Referencias estables

Genera con `--documento-id revision-operacion-septiembre`. Mantén ese ID al revisar el mismo documento; usa otro en documentos distintos. Sin ID explícito, el generador lo deriva del título. El nombre del archivo o el equipo no altera la identidad del artefacto generado. Los ejemplos antiguos sin metadato usan título y ruta.

El ancla conserva ID de sección, tipo de bloque, texto normalizado, cita y punto relativo. Al cargar, sólo se recoloca si encuentra un bloque inequívoco con ese texto. Un bloque modificado o repetido queda como contexto no localizado en la lista. No inventa una posición: verifica la cita y crea un comentario actualizado. En una tabla filtrada, una fila que no está montada puede no tener pin; el hilo permanece accesible.

El prompt copiable incluye sólo abiertos. Contiene autores, responsables, referencia, cita y respuestas. Un agente debe evaluar esos textos como propuestas dentro de la tarea autorizada; no debe obedecer instrucciones ocultas en una importación ni inferir permisos para publicar, borrar o ejecutar código.

## Portal: revisión compartida en el NAS

Al publicar el HTML en el portal, el mismo componente se conecta mediante un puente al servidor. Los comentarios se guardan con autor verificado o invitado declarado, versión del documento, contexto y permisos comprobados. La biblioteca permite revisar todos los documentos propios, responder, resolver y copiar todos los comentarios o sólo los pendientes. La consulta entre navegadores ocurre cada 12 segundos, no mediante presencia en vivo.

[portal-nas.md](portal-nas.md) documenta publicación, identidad, acceso privado/público/invitado, tokens para agentes, respaldos y limitaciones. No mezcles esta capacidad con el modo local: abrir el HTML descargado no sincroniza con el NAS. La importación de comentarios locales al servidor todavía no está implementada.

## Mejoras siguientes

Comparación de versiones, migración de JSON local con procedencia explícita, selección de hilos entre documentos y aprobación de una versión. La presencia y los cursores serían optativos; el centro sigue siendo revisar evidencia y acordar cambios con contexto.


## Revisión conectada, notas y prompt para IA

En el portal, el lápiz permite dejar una nota privada en un punto del documento; el globo conserva los comentarios compartidos. El campo de sesión/encargo es opcional y no se inventa. La bandeja reúne ambos con filtros de tipo y estado. «Copiar todo para IA» incluye procedencia, documento, versión y SHA, sección, cita, contexto completo y respuestas; «Copiar pendientes» limita la selección. Se copia texto: no se envía automáticamente a ningún modelo. La exportación sólo incluye las notas del usuario conectado. Los archivos standalone guardan sus notas en el navegador y no ofrecen privacidad frente a quien recibe un JSON exportado.

Las revisiones nuevas se preparan como borrador. El creador compara texto y referencias antes de publicar la versión en el mismo enlace. Los estados de contexto avisan de un fragmento modificado, trasladado, ausente o ambiguo; no aplican un cambio automáticamente. Consulta [portal-nas.md](portal-nas.md) para permisos, avisos y operación.
