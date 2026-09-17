# Biblioteca y recuperación de archivos

La biblioteca ofrece lista y galería, 12 documentos por página, búsqueda y filtros por espacio/acceso. Las portadas son vistas estáticas sin scripts, fuentes remotas ni red externa. Las páginas construidas por JavaScript muestran una portada con su título. Cada preview y adjunto comprueba los mismos permisos que el documento.

`BOTTIFACT_ADMIN_EMAILS` declara **alias verificados de una sola cuenta**, separados por comas; el primero es la identidad canónica. No usar esta variable para administradores independientes. Al iniciar, el servidor migra sesiones, tokens, propietarios y actividad de alias existentes. No une direcciones arbitrarias ni invitados sin verificar.

## Recuperar un archivo

Primero respalda el NAS. Prepara una copia independiente con CSS, scripts y recursos incrustados. No importes entradas de aplicaciones que necesiten un backend como si fueran documentos completos. Conserva los originales y la procedencia; no añadas informes privados al repositorio.

`python -m portal.import_archive --manifest /data/importacion/manifest.json --data /data --result /data/importacion/resultado.json`

El manifiesto privado es una lista de objetos con `source` (clave de procedencia estable), `file` (ruta HTML), `title`, `space`, y opcionalmente `legacy_url` y `attachments` (mapa de ruta relativa a archivo). La importación reserva IDs, convierte enlaces entre documentos, crea documentos privados y omite contenidos idénticos. Repetir un origen con contenido nuevo añade una versión sin cambiar su enlace ni permisos. El resultado registra los IDs. Los enlaces antiguos migrados se ocultan de la biblioteca, conservando su registro histórico.

Los adjuntos se descargan con autorización y quedan incluidos en `portal.manage backup`. Los archivos y resultados de importación permanecen fuera del ZIP del skill.

## Revisión

La pestaña **Comentarios** reúne hilos, respuestas y contexto. Permite copiar todos o sólo pendientes. Un documento antiguo sin pines puede usar **Comentar** en el lector: toma el texto seleccionado o el título como referencia. Los HTML Bottifact conservan sus pines.

No se importan automáticamente comentarios guardados en el almacenamiento local de otro navegador. La recuperación de HTML no acredita que sus fuentes, cifras históricas o dependencias externas sigan vigentes.
