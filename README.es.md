# Bottifact

Biblioteca de componentes, skill para agentes y portal opcional para crear, compartir y revisar artefactos HTML. Incluye 82 recetas, 15 familias de temas con claro/oscuro/sistema, comentarios, notas, versiones, búsqueda y grafos de relaciones.

[README completo y variables de entorno](README.md) · [Documentación](docs/README.md) · [Arquitectura](docs/architecture.md)

## Instalar el skill

Python 3.10+; generar HTML no requiere cuenta, Node ni variables de entorno.

```bash
git clone https://github.com/angelbotto/bottifact.git
cd bottifact
python3 scripts/package.py
python3 scripts/update.py --package dist/bottifact-portable.zip
```

Instala una biblioteca compartida y enlaces para Claude Code, Codex y Hermes. Conserva carpetas independientes existentes. Añade `~/.local/bin` al PATH y recarga el descubrimiento de skills del agente. No instala un skill en la web de ChatGPT.

Desde un portal propio:

```bash
curl -fsSL https://artifacts.example.com/install.sh -o /tmp/bottifact-install.sh
# Revisa el script antes de ejecutarlo.
bash /tmp/bottifact-install.sh
bottifact connect --server https://artifacts.example.com
```

El token se obtiene iniciando sesión en el portal. El CLI lo pide sin mostrarlo. Actualizar: `bottifact update`. Para instalaciones independientes, reconstruye el ZIP y repite la instalación local.

## Desplegar tu portal

```bash
python3 scripts/configure_portal.py \
  --origin https://artifacts.example.com --admin owner@example.com
docker compose -f compose.yaml -f deploy/https.yaml up -d --build
```

Configura DNS y puertos 80/443. El comando genera un `.env` privado. Requiere `BOTTIFACT_ORIGIN`, `BOTTIFACT_DOMAIN`, `BOTTIFACT_ADMIN_EMAILS` y un `BOTTIFACT_AUTH_SECRET` aleatorio. Google usa `BOTTIFACT_GOOGLE_ENABLED`, `BOTTIFACT_GOOGLE_ID` y `BOTTIFACT_GOOGLE_SECRET`. Correo usa `BOTTIFACT_EMAIL_PROVIDER`, `BOTTIFACT_EMAIL_URL`, `BOTTIFACT_EMAIL_FROM` y `BOTTIFACT_EMAIL_KEY`. La tabla completa, valores predeterminados y requisitos están en el [README](README.md#environment-variables) y [`.env.example`](.env.example).

Primer administrador:

```bash
docker compose exec app python -m portal.manage bootstrap --email owner@example.com
```

Abre el enlace temporal en privado. Configura Google o correo antes de invitar usuarios. No necesitas botto.is, Cloudflare ni Supabase. [Autenticación, backups y actualizaciones](docs/self-hosting.md).

## Componentes y React

Las recetas viven en `packages/core/recipes/`, los temas en `packages/core/themes/families/` y las interacciones en `packages/core/components/`. React añade 8 exports nativos y un visor aislado para las 82 recetas. **No son 82 componentes React reescritos**. Los paquetes aún no están publicados en npm; usa el workspace o tarballs según la [guía React](docs/react.md).

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
