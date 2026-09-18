## Gantt

<!-- nota:ejemplo gantt -->

```html
{{EXAMPLE}}
```

**Use and limits:** Show 1–24 tasks with actual dates, owners and finish-to-start dependencies. Unique ASCII IDs up to 12 characters; valid ISO dates over at most ten years. Comma-separated dependency IDs or an em dash for none. Reject cycles, absent IDs and dependencies ending after their successor starts. Explicit text/symbol status, never inferred from today. Duration is elapsed time, not inclusive working days. No holiday calendar, critical-path calculation or scheduler. Source data stays in one table (or the image zone list). Declare data-unidad (1–40 characters); numeric magnitude is limited to 10^12. Views round to eight significant digits while source values remain. Load evidence.js; NotaEvidencia.init/get/destroy owns lifecycle. Destroy before changing the source. No network or external libraries; data remains if enhancement fails.
