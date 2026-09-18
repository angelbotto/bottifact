## Zoomable evidence

<!-- nota:ejemplo evidencia-ampliable -->

```html
{{EXAMPLE}}
```

**Use and limits:** Inspect one embedded data image with 1–12 numbered zones. Percentage `data-x/data-y` coordinates range 0–100; labels up to 100 characters. Zoom/fit supports 100–400%, local two-axis scrolling and keyboard/selector access. Overlapping zones remain accessible in the list. Place markers beside evidence. This does not increase image resolution or perform OCR. Author annotations are separate from reader comments; print preserves the original. Source data stays in one table (or the image zone list). Declare data-unidad (1–40 characters); numeric magnitude is limited to 10^12. Views round to eight significant digits while source values remain. Load evidence.js; NotaEvidencia.init/get/destroy owns lifecycle. Destroy before changing the source. No network or external libraries; data remains if enhancement fails.
