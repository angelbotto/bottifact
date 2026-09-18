## Stages

<!-- nota:ejemplo etapas -->

```html
{{EXAMPLE}}
```

**Use and limits:** Explain ordered process stages with durations. Supports 1–12 stages with nonnegative duration; zero height is not inflated. No dependency planning, parallelism, cumulative waterfall or physical simulation. Do not sum overlapping durations as elapsed time. Selection connects a stage to its written explanation; initial rotation is paused. `NotaEscena.init/get`, `select(index|null)`, `rotate(dx,dy)`, `pause/resume` and idempotent `destroy()` manage instances. Rotation is .15 rad/s and runs only while visible, active and requested without reduced motion. Destroy releases RAF, observers, listeners and WebGL resources while restoring the source table. Destroy/reinitialize to replace data.
