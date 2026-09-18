## Sonido: control central y canal independiente

En la biblioteca, Apariencia controla todo el audio con [packages/core/components/audio.js](../packages/core/components/audio.js), incluido antes de `packages/core/components/reader.js`. Para copiar sólo un canal independiente usa [packages/core/components/sound.js](../packages/core/components/sound.js). En nuevos artefactos, el control central empieza habilitado y espera el primer clic real para abrir Web Audio; recuerda el silencio elegido. El canal independiente conserva su inicio apagado y su botón de activación. El control central oculta los interruptores locales cuando está presente.

<!-- nota:ejemplo sonido -->
```html
{{EXAMPLE}}
```

**Cuándo:** confirmar una acción explícita y breve, en una experiencia donde la persona
puede apagarlo siempre. No añade sonido a gráficos, scroll genérico, foco ni cambios de tema. El botón de activación no emite una señal. El canal independiente no recuerda la preferencia y vuelve a apagado al ocultar la pestaña; la base central recuerda el silencio y pausa al ocultarse. Sólo los elementos con atributos de escritura o hover autorizan esos gestos sonoros.

**Límite:** Web Audio y gesto real de botón; eventos sintéticos no activan ni reproducen.
El canal independiente de `packages/core/components/sound.js` usa seno, ganancia pico 0,025, ataque 3 ms y caída a 0,0001 en 55 ms;
acción 660→440 Hz, confirmación 520→780 Hz, atención 440→360→440 Hz. Cada nota dura 60 ms,
separada por 5 ms; total 125 o 190 ms. Son decisiones de Nota, no mediciones del sitio.
Una nueva señal interrumpe la anterior. No son alarmas, sonificación de series ni audio de
fondo, y la ganancia digital no garantiza un nivel acústico en el dispositivo.
`NotaSonido.get(contenedor).disable()` apaga; `.destroy()` cierra el contexto y listeners.
`NotaSonido.init(contenedor)` inicializa HTML nuevo. No hay método público de reproducción
automática. Sin `packages/core/components/audio.js`, `[data-sonido]` conserva el comportamiento anterior.

Con la base estándar, `packages/core/components/audio.js` usa los MP3 originales de cmrg.me, incrustados en base64 y
decodificados por Web Audio al activar Sonidos. Clic, hover, confirmación, atención y tres
lápices; sin descargas durante la lectura. Conserva los niveles de la referencia (clic .9,
hover .4, lápiz .6, positivo/negativo .8) multiplicados por el volumen maestro inicial .65.
Hover usa playbackRate .9; el lápiz mantiene su tono y duración original, sin bucle ni normalización.
El canal independiente anterior se conserva sólo cuando falta `packages/core/components/audio.js`; con él, sus botones
usan las mismas grabaciones y el mismo interruptor de la cabecera.
`NotaAudio.enabled`, `activeVoices`, `plays` y `samples` permiten inspeccionar el estado;
`NotaAudio.disable()` apaga y cancela las voces. `data-audio="accion|confirmacion|atencion|escritura"`
en botones conserva su resultado textual. Procedencia y hashes en `packages/core/assets/reference-audio/PROVENANCE.md`
y `tests/evidence/sounds-cmrg.json`. La sustitución de síntesis por grabaciones fue pedida por Angel.

<a id="recetas-escritura"></a>
