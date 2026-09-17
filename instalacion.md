# La misma biblioteca en otro equipo

Bottifact incluye un skill (`SKILL.md`), 82 recetas con HTML, criterio y límites, CSS, fuentes,
sonidos y módulos, más scripts Python para generar y validar. Claude, Codex y Hermes pueden leer
exactamente ese directorio. Los artefactos generados son HTML; no dependen de que el lector tenga
instalado un agente. Three.js requiere su CDN permitido; los demás recursos van incrustados.

## Instalación y actualización por terminal

Cualquier persona puede descargar el skill sin cuenta. El repositorio sigue siendo privado; el paquete publicado contiene sólo la biblioteca y sus recursos compartibles.

```bash
curl -fsSL https://artifacts.botto.is/install.sh | bash
```

La entrada es Bash y explica los agentes y rutas que prepara. Detecta Python 3.10+ para el generador y la verificación del paquete; si falta, indica cómo instalarlo. En macOS con Homebrew: `brew install python`. No instala dependencias con sudo ni oculta errores. Puedes revisar [instalar.sh](scripts/instalar.sh) antes de ejecutarlo.
El comando descarga el ZIP, verifica su SHA-256 y el manifiesto interno, instala en
`~/.local/share/bottifact/library` y crea enlaces para Codex (`~/.agents/skills/bottifact`),
Claude Code (`~/.claude/skills/bottifact`) y Hermes (`~/.hermes/skills/bottifact`). Conserva carpetas
y enlaces que ya apunten a otras bibliotecas; revisa los avisos si tienes una instalación propia.
Un checkout Git nunca se reemplaza. Si usas un perfil de agente personalizado, enlaza su carpeta
de skills a la copia instalada. No se cambia la configuración global de ningún agente.

Para actualizar, repite el comando o ejecuta:

```bash
python3 ~/.local/share/bottifact/library/scripts/actualizar.py
# Si ~/.local/bin está en PATH:
bottifact actualizar
```

Se respalda la versión anterior fuera de las carpetas de skills. No se copia ni cambia
`~/.config/bottifact/portal.json`, donde vive el token personal. No hay actualización silenciosa:
ejecuta el comando cuando quieras adoptar una nueva versión y abre una conversación nueva.
SHA-256 detecta una descarga corrupta; su publicación en el mismo servidor no constituye una firma independiente.

## ChatGPT

La instalación de ChatGPT se gestiona dentro de la aplicación: Plugins → Skills → Create → Upload from your computer, cuando tu plan y espacio permitan skills. Descarga el ZIP portable desde el portal e impórtalo allí. Bash no modifica tu cuenta de ChatGPT ni acredita que se haya importado. Las actualizaciones en ChatGPT requieren volver a cargar el paquete; son independientes de los enlaces locales de Codex. [Documentación oficial](https://help.openai.com/en/articles/20001066).

## Crear y publicar son pasos separados

Generar HTML funciona sin cuenta. Para alojarlo en el NAS, entra en https://artifacts.botto.is/,
abre **Conectar un agente**, crea un token y ejecuta:

```bash
bottifact conectar --servidor https://artifacts.botto.is
bottifact publicar --archivo informe.html --titulo 'Informe' --visibilidad public
```

El token se pega en una entrada oculta. Omite `--visibilidad` para guardar privado. Una revisión
con `--artefacto-id ID` conserva el enlace y los permisos. Cada persona usa su propio token;
compartir el skill nunca comparte una cuenta. Consulta [portal-nas.md](portal-nas.md).

## Hermes en el MacBook

Descarga [bottifact-portable.zip](descargas/bottifact-portable.zip) desde https://artifacts.botto.is/downloads/bottifact-portable.zip, descomprímelo y abre una terminal dentro de la carpeta `bottifact` extraída:

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
de agentes. El ZIP verificado está disponible públicamente en el portal; no incluye credenciales ni datos del servidor.

Para regenerarlo en una copia de desarrollo ejecuta `python3 scripts/empaquetar.py`. La carpeta
`descargas` es salida, no una fuente: no se incluye recursivamente en el paquete.

Para actualizar la copia compartida del MacBook desde Hermes, consulta [marcas.md](marcas.md): distingue una instalación Git de un paquete ZIP y conserva los enlaces de los tres agentes.

## Instalar desde GitHub

El repositorio `angelbotto/bottifact` contiene la misma raíz portable. Puedes clonarlo en el directorio de skills con el nombre `bottifact`; el repositorio privado requiere acceso de GitHub. Un clone se actualiza con `git pull --ff-only` después de revisar los cambios y comprobar que no hay modificaciones locales. No mezcles ese procedimiento con el instalador de ZIP: cada método conserva su propio origen. La CI adjunta el ZIP verificado como artefacto descargable de cada ejecución correcta.


## Migrar del nombre anterior

Bottifact reemplaza el nombre público anterior. Instala el ZIP en una carpeta nueva llamada `bottifact`; su frontmatter declara el mismo nombre. Si tenías un enlace de skill antiguo, consérvalo como respaldo fuera de la carpeta de skills y crea el nuevo acceso. Si era un clone con trabajo local o el repositorio principal de varios worktrees, conserva ese repositorio y registra un acceso `bottifact` a su ubicación; no lo borres ni lo muevas como si fuera una copia descargada.

En Claude Code varios accesos simbólicos al mismo destino se deduplican, según su documentación. En Hermes y Codex mantén un único acceso activo por nombre para no divergir. El equipo de desarrollo puede conservar una ruta histórica para Git/Orca; el paquete descargado y las instalaciones nuevas usan `bottifact`.

El renombrado conserva los IDs de ejemplos publicados, las claves locales de comentarios y preferencias, y los formatos anteriores de revisión. No copies comentarios a otro documento cambiando su ID para forzar la importación. Las versiones antiguas descargadas mantienen su contenido hasta que regeneres o actualices sus archivos.

## Conexión personal al portal

Después de actualizar el skill, usa `scripts/publicar.py conectar --servidor https://artifacts.botto.is`. La biblioteca se puede compartir; `~/.config/bottifact/portal.json` es personal y queda fuera de la distribución. Consulta [portal-nas.md](portal-nas.md). El portal requiere un despliegue aparte: instalar el ZIP no instala Docker ni el servidor.
