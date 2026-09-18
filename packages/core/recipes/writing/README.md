## Writing

<!-- nota:ejemplo escritura -->

```html
{{EXAMPLE}}
```

<a id="recetas-three"></a>

**Use and limits:** Use ordered SVG centerline paths for a brief secondary handwritten gesture. It does not turn arbitrary text or filled font outlines into handwriting. Update `data-texto-escritura` whenever paths change; permanent equivalent text remains and SVG is aria-hidden. `data-al-ver` starts once at 30% visibility; otherwise readers choose replay. `data-escritura-sonora` requests approved pencil sound only after audio unlock and respects mute. Supported duration is 100–10000 ms. Leaving view, hiding the tab or reduced motion cancels/completes the gesture with no RAF or queued replay. `NotaEscritura.init/get`, `play()`, `finish()` and `destroy()` manage lifecycle. `play()` respects reduced motion.
