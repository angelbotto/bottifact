# Bottifact

![Bottifact: documentos que siguen vivos después del chat](docs/assets/bottifact-banner.svg)

**Crea con tu agente. Comparte con contexto. Hospédalo donde quieras.**

[README en inglés](README.md) · [Despliegue propio](self-hosting.md) · [Componentes](componentes.md) · [Contribuir](CONTRIBUTING.md)

Bottifact combina una biblioteca editorial de HTML, un skill portable para Claude Code, Codex y Hermes, y un portal colaborativo opcional. Sirve para crear reportes, artículos, documentación, presentaciones y prototipos con datos, notas al margen y revisión contextual.

Incluye **82 recetas, 15 familias de temas con modos claro/oscuro/sistema y seis combinaciones tipográficas**. Hay tablas interactivas, gráficas, globos, código, cronologías, galerías, anotaciones manuscritas y comentarios flotantes. El inventario verificable está en [registro.json](registro.json).

## Instalar sin depender de botto.is

Necesitas Python 3.10 o posterior. Para generar no hacen falta Docker, Node ni paquetes externos de Python.

```bash
git clone https://github.com/angelbotto/bottifact.git
cd bottifact
python3 scripts/empaquetar.py
python3 scripts/actualizar.py --paquete descargas/bottifact-portable.zip
```

Instala una biblioteca compartida y enlaces para los tres agentes. Conserva carpetas de skill existentes y respalda actualizaciones. No crea cuentas ni sube documentos. Abre una conversación nueva y pide: «Usa el skill bottifact». Para actualizar una instalación local, descarga una versión nueva y repite los dos últimos comandos.

También hay ZIP y SHA-256 en [Releases](https://github.com/angelbotto/bottifact/releases). ChatGPT depende de las capacidades de importación de tu cuenta; el instalador de terminal no modifica su servicio en la nube.

## Tener tu propio portal

Usa Docker Compose v2, tu dominio y tus credenciales. No necesitas una cuenta de botto.is, Cloudflare ni Supabase.

```bash
python3 scripts/configurar_portal.py \
  --origin https://artifacts.tudominio.com --admin tu@tudominio.com
docker compose -f compose.yaml -f deploy/https.yaml up -d --build
docker compose exec app python -m portal.manage bootstrap --email tu@tudominio.com
```

El dominio debe apuntar a tu servidor y los puertos 80/443 estar disponibles. El primer comando crea un `.env` privado con secreto aleatorio; el último entrega un enlace de administrador temporal de un solo uso. Configura Google o códigos por correo para el ingreso habitual. Si ya tienes proxy HTTPS, usa solamente el Compose principal.

El portal guarda archivos y SQLite en volúmenes propios. Permite documentos privados, públicos o por enlace, permisos por cuenta/correo, notas privadas, comentarios centralizados, versiones, buscador y vistas de galería, lista, tabla y relaciones. El worker realiza respaldos verificados. Lee la [guía de despliegue, operación y recuperación](self-hosting.md) antes de compartirlo.

## El contexto vuelve al agente

Al exportar comentarios se conserva documento, versión, sección, cita y contexto de origen. Puedes registrar agente, sesión y dispositivo al publicar. Esto ayuda a retomar el trabajo sin copiar observaciones sueltas.

El mapa conecta etiquetas y colecciones compartidas: no interpreta automáticamente conversaciones ni demuestra relaciones causales. La sincronización de transcripciones, un servidor MCP y el aprendizaje automático de preferencias están en el [roadmap](ROADMAP.md), no en esta versión.

## Explorar y aportar

Abre `guia.html` tras clonar para ver la biblioteca. Consulta [guia-uso.md](guia-uso.md), [temas.md](temas.md), [voz-ejecutiva.md](voz-ejecutiva.md) y [biblioteca-conectada.md](biblioteca-conectada.md). Puedes aportar componentes, accesibilidad, traducciones, despliegues o correcciones siguiendo [CONTRIBUTING.md](CONTRIBUTING.md).

Código y documentación originales bajo [MIT](LICENSE). Las fuentes, audios y recursos de terceros conservan sus avisos; consulta [NOTICE](NOTICE). Los logos no conceden derechos de marca.
