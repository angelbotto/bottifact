# La misma biblioteca en otro equipo

Nota Tikin incluye un skill (`SKILL.md`), 71 recetas con HTML, criterio y límites, CSS, fuentes,
sonidos y módulos, más scripts Python para generar y validar. Claude, Codex y Hermes pueden leer
exactamente ese directorio. Los artefactos generados son HTML; no dependen de que el lector tenga
instalado un agente. Three.js requiere su CDN permitido; los demás recursos van incrustados.

## Hermes en el MacBook

Descarga [nota-tikin-portable.zip](descargas/nota-tikin-portable.zip) desde el servidor privado de
Tailscale, descomprímelo y abre una terminal dentro de la carpeta `nota-tikin` extraída:

```bash
python3 scripts/instalar.py --destino ~/.hermes/skills/nota-tikin
```

El instalador verifica los SHA-256 del paquete, copia sólo sus archivos y no instala dependencias,
no ejecuta comandos de red ni toca la configuración de Hermes. Si el destino existe se detiene;
para actualizar deliberadamente añade `--actualizar`: conserva la versión anterior en una carpeta
hermana fuera del directorio de skills y luego sustituye la copia. No sobreescribe el destino de un
symlink compartido: respalda el enlace y crea una copia independiente en la ruta indicada.

Abre una conversación nueva de Hermes y pide:

> Usa el skill nota-tikin. Lee su guia-uso.md, recorre registro.json y elige piezas que expliquen
> este contenido. Genera el HTML con scripts/crear_artefacto.py y valida el archivo final. Conserva
> la llave de apariencia, los comentarios flotantes y las ayudas de lectura. No inventes datos.

Hermes descubre carpetas con `SKILL.md` bajo `~/.hermes/skills`, según su [documentación oficial de skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills). Si tienes un perfil o un
`HERMES_HOME` personalizado, usa su directorio de skills como `--destino`. La carga automática
depende de tu configuración de Hermes; una copia instalada no garantiza que una sesión ya abierta
haya recargado sus instrucciones. La instalación en el MacBook debe comprobarse allí.

## Claude y Codex

Usa el mismo instalador cambiando el destino: `~/.claude/skills/nota-tikin` para Claude Code y
`~/.agents/skills/nota-tikin` para Codex. También puedes mantener una sola copia canónica y enlaces
locales deliberados. Nunca uses en el MacBook un enlace a una ruta del Mac mini: no comparte su disco.
El generador resuelve recursos desde su propia ubicación, no desde un directorio fijo de Claude.

## Comprobar la instalación sin conectarse a servicios

```bash
python3 ~/.hermes/skills/nota-tikin/scripts/verificar_paquete.py ~/.hermes/skills/nota-tikin
python3 ~/.hermes/skills/nota-tikin/scripts/crear_artefacto.py --contenido ~/.hermes/skills/nota-tikin/ejemplos/estandar-contenido.html --titulo 'Prueba local' --tema blueprint --estilo tecnico --salida /tmp/prueba-nota.html
python3 ~/.hermes/skills/nota-tikin/scripts/validar_artefacto.py /tmp/prueba-nota.html
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
