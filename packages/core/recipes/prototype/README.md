## Prototype

<!-- nota:ejemplo visor -->

```html
{{EXAMPLE}}
```

**Use and limits:** Preview trusted declarative component states at 320, 390, 768, 1024 px or available width. Named icon controls choose device, aspect, rotation and fit; report CSS dimensions and visual scale. Uses Shadow DOM and @container, not a remote iframe or hardware emulator; @media(width) measures the outer window. No scripts, inline event handlers, submissions or arbitrary remote resources. loadHTML accepts up to 100000 characters of trusted local HTML/CSS with raster data images, rejecting scripts, iframes, external URLs and CSS imports. This is not a sanitizer for hostile content. `NotaVisores.get().setWidth()`, `setAspect(auto|9/16|4/3|16/9|1/1)`, `reset()` and `destroy()` preserve the textual/print alternative. Fit can shrink text; use 100% to judge readability.
