## Animated callouts

<!-- nota:ejemplo avisos-animados -->

```html
{{EXAMPLE}}
```

**Use and limits:** Mark brief caution or context with a corner icon that reserves its own space. editorial-pieces.js adds two 1000 ms pulses on entry and optional replay on hover/focus. Motion stops when hidden, outside view, reduced or destroyed. No RAF or sound. Static notices must not use role=alert; meaning does not depend on animation. Existing notice variants remain compatible.
