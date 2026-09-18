## Reports, articles and prototypes

Embed complete fonts/styles and reader once. Add reports.js for data-reporte, prototype.js for data-visor, and globe.js plus pinned Three for journey globes. `NotaReportes.init(root)` and `NotaVisores.init(root)` are idempotent; get(element).destroy() removes enhancement and restores source data. To change a source table, destroy, edit and reinitialize; there is no data observer.
