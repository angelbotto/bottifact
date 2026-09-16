# Liftit, Tikin y Catabum en Bottifact

Repositorio de la biblioteca: [angelbotto/bottifact](https://github.com/angelbotto/bottifact), privado. Los repositorios de las empresas son fuentes de identidad; esta actualización no modifica sus aplicaciones.

[marcas.html](marcas.html) reúne las tres identidades. Prueba los artefactos [Liftit](liftit.html), [Tikin](tikin.html) y [Catabum](catabum.html) en Claro, Oscuro y Sistema. Los ejemplos usan datos ilustrativos explícitos, no actividad de producción.

## Procedencia

Las rutas y commits consultados, los colores originales y hashes de los logos están en [marcas.json](marcas.json). Se extrajeron los trazos de los SVG originales; los componentes React se convirtieron a SVG sin alterar geometría. Los logos monocromos adaptan su tinta al fondo y se incrustan como imágenes independientes, sin referencias remotas ni IDs compartidos.

| Marca | Fuente elegida | Identidad original | Adaptación editorial |
| --- | --- | --- | --- |
| Liftit | LMS web y UI compartida | Ribbon #465EFF, Bay #2B3492, coral #FF7A57; isotipo del menú | Sustituye el azul extraído antes de la web pública. El texto azul usa #3E54ED para mantener contraste en las tres superficies; Ribbon queda intacto como token de marca. El oscuro usa los neutros Mirage de la fuente y acentos aclarados para lectura |
| Tikin | Design system para tokens; landing para logo | Papel #FAF8F4, lima #85FF85, lavanda #DFE1FF, dorado #FFE680, rojo #FF2E2E | El verde de texto en claro es más oscuro; la lima original queda disponible como color de marca. Superficies claras/oscuras del sistema |
| Catabum | Tokens de la app y logo compartido | Fondo #1A0D2E, violeta #7C4DFF, magenta #FF3E81, naranja #FF8C3B | Claro propio y acentos legibles. La app aporta identidad; el admin usa neutros genéricos que no se tomaron como marca |

La paleta de marca y el color semántico de un dato no son siempre iguales. Los colores originales están en las muestras; enlaces, focos y series usan variantes con contraste. Estos temas son adaptaciones para documentos, no una declaración de que cada variante esté aprobada como manual corporativo.

Se identificaron también las fuentes de los productos: Eina03/CircularStd en Liftit; Funnel Display y la familia Ubuntu en el design system de Tikin; Montserrat en la app Catabum. Esta entrega conserva las seis combinaciones tipográficas de Bottifact, elegibles en Letras. No incorpora los archivos de esas fuentes ni afirma reproducir toda la tipografía de las aplicaciones.

## Elegir identidad y apariencia

```bash
python3 scripts/crear_artefacto.py --contenido contenido.html --titulo 'Mi lectura financiera' --documento-id lectura-financiera --tema tikin --modo system --estilo sobrio --salida informe.html
```

Un tema inicial Liftit, Tikin o Catabum incorpora su logo automáticamente. `--marca` fija la identidad por separado: `--marca tikin --tema blueprint` prepara un documento técnico de Tikin con paleta Blueprint; `--marca bottifact --tema liftit` conserva la firma Bottifact. En JSON usa `"marca": "tikin"`.

La identidad pertenece al documento. Cambiar el tema en el selector cambia sus colores, no la empresa que firma. El logo ajusta su tinta al modo efectivo. El modo Sistema sigue la apariencia del dispositivo. Los controles de comentarios y lectura siguen siendo los de la base.

## Actualizar desde Hermes, Claude o Codex

Para una instalación clonada desde GitHub, revisa primero si tiene cambios propios. Desde su carpeta ejecuta `git status --short`, `git remote -v` y, si está limpia, `git pull --ff-only`. No hagas reset ni borres una copia con cambios. El origen es `https://github.com/angelbotto/bottifact.git`; se requiere acceso al repositorio privado.

Para una instalación desde ZIP, descarga [bottifact-portable.zip](descargas/bottifact-portable.zip), extráelo en una carpeta temporal y ejecuta el instalador incluido allí con `--destino` y `--actualizar`. Verifica el paquete antes y después. El instalador conserva respaldo. No ejecutes `git pull` dentro de un paquete sin `.git`.

En el MacBook configurado en esta sesión, los tres accesos apuntan a `~/.local/share/bottifact/library`. Actualiza esa biblioteca una sola vez desde el ZIP extraído:

```bash
python3 scripts/instalar.py --destino ~/.local/share/bottifact/library --actualizar
python3 ~/.local/share/bottifact/library/scripts/verificar_paquete.py ~/.local/share/bottifact/library
```

Ejecuta con Python 3.10 o posterior. Si el `python3` del sistema es más antiguo y existe Homebrew, usa `/opt/homebrew/bin/python3`. Conserva los enlaces de `~/.agents/skills/bottifact`, `~/.claude/skills/bottifact` y `~/.hermes/skills/bottifact`. Abre una sesión nueva para cargar las instrucciones actualizadas. Otras máquinas pueden tener otra ubicación; compruébala antes de actualizar.

## Mantener las marcas

Consulta el commit y la ruta de cada fuente; no deduzcas una identidad por el nombre de la empresa. Añade los colores a temas.json y registra cualquier adaptación de contraste. Usa el archivo de logo autorizado; no redibujes un wordmark con una fuente parecida. Regenera, valida los tres modos, comprueba móvil y prueba que cambiar de tema conserve la identidad. Los recursos siguen perteneciendo a sus titulares y se distribuyen para el uso autorizado en estos artefactos.
