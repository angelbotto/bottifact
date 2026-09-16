# La misma biblioteca en otro equipo

Bottifact incluye un skill (`SKILL.md`), 82 recetas con HTML, criterio y límites, CSS, fuentes,
sonidos y módulos, más scripts Python para generar y validar. Claude, Codex y Hermes pueden leer
exactamente ese directorio. Los artefactos generados son HTML; no dependen de que el lector tenga
instalado un agente. Three.js requiere su CDN permitido; los demás recursos van incrustados.

## Hermes en el MacBook

Descarga [bottifact-portable.zip](descargas/bottifact-portable.zip) desde el servidor privado de
Tailscale, descomprímelo y abre una terminal dentro de la carpeta `bottifact` extraída:

```bash
python3 scripts/instalar.py --destino ~/.hermes/skills/bottifact
```

El instalador verifica los SHA-256 del paquete, copia sólo sus archivos y no instala dependencias,
no ejecuta comandos de red ni toca la configuración de Hermes. Si el destino existe se detiene;
para actualizar deliberadamente añade `--actualizar`: conserva la versión anterior en una carpeta
hermana fuera del directorio de skills y luego sustituye la copia. No sobreescribe el destino de un
symlink compartido: respalda el enlace y crea una copia independiente en la ruta indicada.

Abre una conversación nueva de Hermes y pide:

> Usa el skill bottifact. Lee voz-ejecutiva.md y guia-uso.md. Redacta desde mi voz de CTO/CEO
> hacia mi equipo, con evidencia, highlights, lowlights y decisiones; adapta la estructura al formato.
> Recorre registro.json y aprovecha la mayor variedad de componentes que ayude a explicar el contenido. Genera el HTML con scripts/crear_artefacto.py y valida el archivo final. Conserva
> la llave de apariencia, los comentarios flotantes y las ayudas de lectura. No inventes datos.

Hermes descubre carpetas con `SKILL.md` bajo `~/.hermes/skills`, según su [documentación oficial de skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills). Si tienes un perfil o un
`HERMES_HOME` personalizado, usa su directorio de skills como `--destino`. La carga automática
depende de tu configuración de Hermes; una copia instalada no garantiza que una sesión ya abierta
haya recargado sus instrucciones. La instalación en el MacBook debe comprobarse allí.

## Claude y Codex

Usa el mismo instalador cambiando el destino: `~/.claude/skills/bottifact` para Claude Code y
`~/.agents/skills/bottifact` para Codex. También puedes mantener una sola copia canónica y enlaces
locales deliberados. Nunca uses en el MacBook un enlace a una ruta del Mac mini: no comparte su disco.
El generador resuelve recursos desde su propia ubicación, no desde un directorio fijo de Claude.

## Comprobar la instalación sin conectarse a servicios

```bash
python3 ~/.hermes/skills/bottifact/scripts/verificar_paquete.py ~/.hermes/skills/bottifact
python3 ~/.hermes/skills/bottifact/scripts/crear_artefacto.py --contenido ~/.hermes/skills/bottifact/ejemplos/estandar-contenido.html --titulo 'Prueba local' --tema blueprint --estilo tecnico --salida /tmp/prueba-nota.html
python3 ~/.hermes/skills/bottifact/scripts/validar_artefacto.py /tmp/prueba-nota.html
```

Abre `/tmp/prueba-nota.html` en el navegador del MacBook. Comprueba apariencia, comentarios y
Sonidos con un clic. Esa prueba local es la que acredita el dispositivo; la verificación del paquete
sólo acredita archivos íntegros. Python 3 debe estar disponible; no hace falta npm, Orca ni un servidor.

## Qué contiene el paquete

Incluye instrucciones, fuentes, licencias/procedencias, módulos, recetas, ejemplos, guías y scripts.
Excluye historia git, capturas de auditoría, cachés, entornos y otros skills. El manifiesto registra
cada archivo y su hash; `VERSION.json` identifica el conjunto. No incluye configuración ni credenciales
de agentes. El ZIP está en el servidor privado ya usado para revisar los artefactos, no en un enlace público.

Para regenerarlo en una copia de desarrollo ejecuta `python3 scripts/empaquetar.py`. La carpeta
`descargas` es salida, no una fuente: no se incluye recursivamente en el paquete.

## Instalar desde GitHub

El repositorio `angelbotto/bottifact` contiene la misma raíz portable. Puedes clonarlo en el directorio de skills con el nombre `bottifact`; el repositorio privado requiere acceso de GitHub. Un clone se actualiza con `git pull --ff-only` después de revisar los cambios y comprobar que no hay modificaciones locales. No mezcles ese procedimiento con el instalador de ZIP: cada método conserva su propio origen. La CI adjunta el ZIP verificado como artefacto descargable de cada ejecución correcta.


## Migrar del nombre anterior

Bottifact reemplaza el nombre público anterior. Instala el ZIP en una carpeta nueva llamada `bottifact`; su frontmatter declara el mismo nombre. Si tenías un enlace de skill antiguo, consérvalo como respaldo fuera de la carpeta de skills y crea el nuevo acceso. Si era un clone con trabajo local o el repositorio principal de varios worktrees, conserva ese repositorio y registra un acceso `bottifact` a su ubicación; no lo borres ni lo muevas como si fuera una copia descargada.

En Claude Code varios accesos simbólicos al mismo destino se deduplican, según su documentación. En Hermes y Codex mantén un único acceso activo por nombre para no divergir. El equipo de desarrollo puede conservar una ruta histórica para Git/Orca; el paquete descargado y las instalaciones nuevas usan `bottifact`.

El renombrado conserva los IDs de ejemplos publicados, las claves locales de comentarios y preferencias, y los formatos anteriores de revisión. No copies comentarios a otro documento cambiando su ID para forzar la importación. Las versiones antiguas descargadas mantienen su contenido hasta que regeneres o actualices sus archivos.
