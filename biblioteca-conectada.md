# Biblioteca conectada

Bottifact organiza el trabajo en https://artifacts.botto.is. El skill genera el HTML y publica con una conexión personal; el portal guarda sus versiones, permisos y revisión. Compartir el paquete del skill no comparte una cuenta.

## Encontrar y explorar

La biblioteca ofrece galería, lista, tabla y mapa de ideas. Galería, lista y tabla tienen miniaturas estáticas aisladas; la ficha lateral muestra una vista mayor, organización, procedencia y documentos relacionados. Abrir el artefacto activa su experiencia completa. Los documentos dependientes de JavaScript pueden mostrar una portada de referencia en lugar de su aplicación renderizada.

La búsqueda (`⌘ K` / `Ctrl K`) consulta título y contenido, sin controles de apariencia, además de etiquetas, categorías, colecciones y procedencia disponible para el creador. Prioriza coincidencias en el título al ordenar por relevancia. Los filtros combinan categoría, espacio, colección, etiqueta y acceso. Las vistas de documentos cargan por desplazamiento, con un botón accesible de continuación. La tabla permite ordenar desde sus encabezados. La búsqueda de la biblioteca personal se conserva en esa pestaña del navegador al volver de un documento.

## Clasificación y relaciones

Las reglas locales asignan categoría y hasta cinco etiquetas automáticas según términos presentes en título y contenido. No envían el documento a otro servicio ni simulan un análisis semántico de IA. La ficha `Organizar` muestra los términos encontrados; el creador puede fijar una categoría, añadir sus etiquetas y colecciones o desactivar la clasificación automática. Las revisiones conservan esas decisiones manuales. Una categoría vacía vuelve a la selección automática si está habilitada. Sin evidencia suficiente se muestra `Sin clasificar`.

El mapa agrupa por categoría y conecta etiquetas o colecciones compartidas. Cada conexión muestra su motivo. No implica dependencia, causalidad ni acuerdo. Para mantenerlo legible muestra hasta 120 documentos de la selección y cuatro conexiones por documento; los filtros permiten explorar otros subconjuntos. Se puede arrastrar, acercar, alejar, restablecer y seleccionar con teclado. Una lista de documentos ofrece otra forma de recorrerlo. Los permisos se comprueban antes de construir el mapa; las notas privadas y los borradores ajenos no forman parte del índice.

## Procedencia y vuelta a la IA

Cada publicación puede registrar `source.agent`, `source.session` y `source.device`, por versión. El CLI identifica la sesión sólo cuando existe una referencia real y registra el nombre del equipo donde se ejecuta. Si la creación ocurrió en otro dispositivo, indícalo explícitamente:

```bash
python3 scripts/publicar.py publicar --archivo informe.html --titulo 'Informe de operación' --espacio Liftit --agente Hermes --sesion REFERENCIA_REAL --dispositivo 'MacBook'
```

`BOTTIFACT_AGENT`, `BOTTIFACT_SESSION` y `BOTTIFACT_DEVICE` permiten configurar referencias reales en el entorno. `--dispositivo` prevalece sobre el entorno; en su ausencia se usa el hostname. No registres tokens, transcripciones ni rutas privadas. La carga manual permite indicar el dispositivo conocido; no deduce el dispositivo de creación a partir del navegador. En publicaciones antiguas, `No registrado` significa que no hay evidencia conservada. No inventes datos para completar la ficha.

El creador ve procedencia en la ficha lateral y en la versión seleccionada del lector. `Copiar contexto para IA` reúne documento, enlace, ID estable, versión, origen y los comentarios/notas visibles para su cuenta. Funciona también sin comentarios. Cada hilo mantiene su versión original y el contexto del fragmento; una sesión escrita en una nota es distinta de la sesión que creó el artefacto. Los lectores no reciben las referencias de sesión y dispositivo del creador.

Al recibir ese prompt, identifica el artefacto, compara la revisión publicada y conserva URL, audiencia e ID. Prepara un borrador, explica qué comentarios atendiste y no resuelvas hilos automáticamente. La procedencia ayuda a retomar; no concede acceso a otra máquina ni ejecuta agentes por sí sola.
