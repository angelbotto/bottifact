## Data explorer

<!-- nota:ejemplo explorador -->

```html
{{EXAMPLE}}
```

**Use and limits:** Explore 1–16 columns and up to 2000 local rows. Load table-model before data-explorer and include controls.js. Search stays visible; Filters, Display, Views and More form one action group. Table/Cards changes presentation while preserving source cells and IDs; auto uses cards at 640 px or below. Use stable table/row/cell identifiers for review anchors. Text, finite numbers (`data-valor`, header `data-tipo=numero`) and ISO dates (`data-tipo=fecha`) are supported. State/total column indexes are zero-based and default to 2/3; declare the additive unit and never mix currencies. Facets, AND/OR conditions, empty values, numeric/date ranges, chips, multi-sort, grouping, visibility, density and local saved views share one query model. Incomplete ranges match nothing. Paging offers 10/25/50/100 rows; totals cover all filtered rows while group counters cover the page. Selection persists across pages; selection export includes selected rows outside the filter using visible columns, otherwise exports the filtered set. CSV neutralizes formulas. Printing restores the complete source. No editing, virtualization or remote fetching. `NotaExplorador.init/get/destroy`, `.visible`, `.selected` and `.exportCSV()` preserve original data. The detail action exposes all fields with keyboard access. Fixed columns and widths are open-table adjustments; saved views retain query/grouping/visibility/density/presentation. See docs/mobile-and-tables.md. React uses its native adapter; standalone does not download React/TanStack. The administrator queries the authorized server collection with progressive scrolling.
