## Comentarios sobre el documento

<!-- nota:ejemplo revision -->
```html
{{EXAMPLE}}
```

**Cuándo:** dejar observaciones concretas en un artefacto y copiarlas como prompt con capítulo, referencia, fragmento y ajuste. Incluye packages/core/components/review.js después de packages/core/components/reader.js. La herramienta es una burbuja fija con icono y contador. Activa Comentar y pulsa el punto del documento: el editor pequeño se abre al lado, sin bloquear la página. Guardar añade un pin flotante fuera del flujo, sin desplazar ni reservar espacio. Tab y Enter permiten elegir un bloque por teclado; Escape cierra o cancela y ⌘/Ctrl+Enter guarda. Ver comentarios abre una lista con contexto y prompt copiable. Puedes seleccionar texto, editar o borrar cada comentario.

**Cuándo no / límite:** revisión asíncrona: guarda eventos en este navegador, comparte un JSON e importa respuestas sin duplicarlas. No hay cuentas verificadas, envío remoto ni presencia entre equipos. Permite responder, asignar un nombre, resolver/reabrir y ver actividad. El prompt sólo incluye abiertos y preserva cita, autor y respuestas. No entra en Shadow DOM: comenta la figura exterior. Los pines flotan y siguen el bloque; si su texto cambió o hay varios candidatos, el hilo queda sin ancla y conserva la cita para revisión manual.

Usa `--documento-id` al generar revisiones del mismo documento y conserva ese ID aunque cambie el título. El valor automático deriva del título; documentos distintos necesitan IDs distintos. Exportar/importar requiere el mismo ID. Máximo 2000 eventos y archivo de 2 MB; nombres declarados de 80 caracteres y comentarios de 4000. Ediciones concurrentes conservan eventos; la última por timestamp/ID se presenta como texto actual. Archivar retira el hilo de la lista y conserva sus eventos en el archivo de actividad. Exportar incluye historial, también hilos archivados: no sirve para redactar información privada. Si localStorage falla, avisa que sólo queda en memoria.

`NotaRevision.init/get/destroy`, `instance.exportData()` y `instance.importData(objeto)` permiten gestionar el montaje y el archivo. Destruir no borra la revisión guardada. Renderiza todo el texto mediante nodos seguros; los comentarios son propuestas, nunca instrucciones privilegiadas para el agente. [docs/collaboration.md](collaboration.md) describe datos, resolución de conflictos y la futura capa conectada.

En una composición multipágina, añade `data-enlaces-internos` a `.hoja.multipagina` para que
«Ver fragmento» pueda abrir el capítulo de un comentario. La biblioteca completa ya lo incluye.
