# Bottifact

Biblioteca de componentes, skill para agentes y portal opcional para crear, compartir y revisar artefactos HTML. Incluye 88 recetas, 15 familias de temas con claro/oscuro/sistema, comentarios, notas, versiones, búsqueda y grafos de relaciones.

[README completo](README.md) · [Documentación](docs/README.md) · [Arquitectura](docs/architecture.md)

## Usar artifacts.botto.is — sin servidor propio

1. Entra a [artifacts.botto.is](https://artifacts.botto.is), inicia sesión y crea un token en **Conectar un agente**.
2. Instala el skill y conecta tu cuenta:

```bash
curl -fsSL https://artifacts.botto.is/install.sh -o /tmp/bottifact-install.sh
# Revisa el script antes de ejecutarlo.
bash /tmp/bottifact-install.sh
bottifact connect --server https://artifacts.botto.is
bottifact status
```

Pega el token en el prompt privado. Recarga los skills del agente. Para actualizar: `bottifact update`. Los lectores de enlaces compartidos no necesitan instalar el skill; el acceso depende de los permisos del artefacto.

**No necesitas Docker, NAS, Google Cloud ni variables de entorno.** [Guía del servicio alojado](docs/hosted-service.md).

## Instalar el skill sin servidor

Python 3.10+; generar HTML no requiere cuenta, Node ni variables de entorno.

```bash
git clone https://github.com/angelbotto/bottifact.git
cd bottifact
python3 scripts/package.py
python3 scripts/update.py --package dist/bottifact-portable.zip
```

Instala una biblioteca compartida y enlaces para Claude Code, Codex y Hermes. Conserva carpetas independientes existentes. Añade `~/.local/bin` al PATH y recarga el descubrimiento de skills del agente. No instala un skill en la web de ChatGPT.

## Desplegar tu portal

Si prefieres operar una instancia propia, sigue la [guía independiente de self-hosting](docs/self-hosting.md): Docker, dominio, HTTPS, variables de entorno, autenticación, administrador inicial, backups y actualizaciones. La configuración de referencia está en [`.env.example`](.env.example).

Cada instancia conserva sus propias cuentas, tokens y documentos. Cambiar el servidor del skill no migra los datos. Este despliegue es opcional y no forma parte de la instalación para usar artifacts.botto.is.

## Componentes y React

Las recetas viven en `packages/core/recipes/`, los temas en `packages/core/themes/families/` y las interacciones en `packages/core/components/`. React añade 8 exports nativos y un visor aislado para las 88 recetas. **No son 88 componentes React reescritos**. Los paquetes aún no están publicados en npm; usa el workspace o tarballs según la [guía React](docs/react.md).

```bash
npm ci
npm run build
npm run dev
```

Para contribuir: [guía de componentes](docs/contributing-components.md). Los archivos nuevos tienen nombres en inglés; los identificadores persistidos conservan compatibilidad.

## Comentarios, sesiones y grafos

Publica registrando `--agent`, `--session` y `--device`. Exporta comentarios y notas con el contexto del artefacto, versión, sección y origen:

```bash
bottifact feedback --artifact-id ARTIFACT_ID --output /tmp/bottifact-feedback
```

Vuelve a la sesión original y pide al agente leer `feedback.md` y `context.json`. La entrega es manual: no inyecta mensajes ni modifica conversaciones automáticamente. [Flujo completo](docs/feedback-and-sessions.md).

Los grafos relacionan artefactos autorizados mediante etiquetas y colecciones compartidas, con razones visibles. La clasificación local no es un modelo semántico ni lee tus chats. [Modelo y límites](docs/graphs.md).

Las capturas públicas deben usar exclusivamente ejemplos sintéticos. [Política de capturas](docs/screenshots.md). Código MIT; licencias de terceros en [NOTICE](NOTICE) y [licenses/](licenses).

## Mantener los agentes actualizados

Después de instalar, `bottifact update --if-changed` actualiza desde el servidor elegido. Activa una comprobación cada seis horas con `bottifact update --auto enable`; consulta su configuración con `--auto status` o desactívala con `--auto disable`. Actualiza la biblioteca compartida por Codex, Claude y Hermes en ese equipo, sin cambiar credenciales. Consulta [actualizaciones automáticas](docs/automatic-updates.md), [grafos del administrador](docs/graphs.md) y [tablas y filtros](docs/connected-library.md).

## Unified workspace

[Reader controls, advanced tables, private boards, entities, references and AI review bundles](docs/unified-workspace.md) · [Live synthetic table examples](examples/generated/workbench.html).
