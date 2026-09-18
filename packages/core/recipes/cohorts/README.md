## Cohorts

<!-- nota:ejemplo cohortes -->

```html
{{EXAMPLE}}
```

**Use and limits:** Compare recurrence using 1–20 cohorts and 1–12 periods with labels up to 24 characters. Positive integer bases; integer counts between zero and base. Pending cells (`data-estado=pendiente`) must trail each row and are not zero. Exact count/base/percentage remain visible. Five intensity ranges: [0,20), [20,40), [40,60), [60,80), [80,100]%. No event-to-cohort calculation or incompatible period comparisons. Source data stays in one table (or the image zone list). Declare data-unidad (1–40 characters); numeric magnitude is limited to 10^12. Views round to eight significant digits while source values remain. Load evidence.js; NotaEvidencia.init/get/destroy owns lifecycle. Destroy before changing the source. No network or external libraries; data remains if enhancement fails.
