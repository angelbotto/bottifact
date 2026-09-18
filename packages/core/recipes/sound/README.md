## Sound

<!-- nota:ejemplo sonido -->

```html
{{EXAMPLE}}
```

<a id="recetas-escritura"></a>

**Use and limits:** The standard base loads `audio.js` before reader and uses the approved embedded cmrg.me recordings. It starts enabled by preference but requires a real interaction to unlock Web Audio; mute and volume are remembered. Click .9, hover .4, pencil .6 and positive/negative .8 are multiplied by initial master volume .65. Hover playback rate is .9; pencil pitch/duration stay original, without loops or normalization. No runtime downloads. Only explicitly marked interactions produce sound; theme changes, focus and generic scrolling remain silent. Hiding the tab pauses/cancels voices. Inspect `NotaAudio.enabled`, `activeVoices`, `plays` and `samples`; `disable()` stops voices. Provenance is in reference-audio/PROVENANCE.md and tests/evidence/sounds-cmrg.json. The older independent sound.js channel starts muted, does not persist preference, and stops when hidden. Its 60 ms sine signals are a legacy fallback, not the reference recording. A digital gain does not establish physical loudness. init/get/destroy clean up contexts and listeners.
