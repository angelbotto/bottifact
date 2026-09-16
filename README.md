# Nota Tikin

Biblioteca editorial y skill para crear artefactos HTML con datos, notas manuscritas, revisión y navegación de lectura. **82 componentes, 13 familias con versiones clara y oscura y seis combinaciones tipográficas.** Funciona con Claude, Codex y Hermes; los HTML generados no necesitan un agente para leerse.

- `guia.html`: biblioteca documentada y recetas copiables.
- `colaborativo.html`: tabla de 36 filas y revisión local con hilos.
- `temas.html`: catálogo vivo de familias, Claro / Oscuro / Sistema.
- `linear-light.html` / `linear-dark.html`: ejemplos de Linear, ahora una sola familia.
- `evidencia.html`: ocho piezas de evidencia, de Sankey a imagen ampliable.
- [Arquitectura y stack](arquitectura.md) · [Colaboración y límites](colaboracion.md).

## Instalar el skill

Clona el repositorio como carpeta de skill con nombre `nota-tikin`:

```bash
git clone https://github.com/angelbotto/nota-tikin.git ~/.hermes/skills/nota-tikin
```

Usa `~/.agents/skills/nota-tikin` para Codex o `~/.claude/skills/nota-tikin` para Claude Code. No ejecutes ese clone sobre una instalación existente: consulta [instalacion.md](instalacion.md) para actualización con respaldo o enlaces deliberados. Un repo privado requiere acceso de tu cuenta. Abre una conversación nueva y pide usar `nota-tikin`.

También puedes descargar el ZIP de una ejecución correcta de GitHub Actions: contiene manifiesto y verificación de archivos, sin historia ni capturas. Instálalo con `scripts/instalar.py` según la guía. El generador necesita Python 3.10+ y ningún paquete externo. Node se usa para pruebas, no para generar.

## Crear y comprobar

```bash
python3 scripts/crear_artefacto.py --contenido ejemplos/colaborativo-contenido.html --titulo 'Mi revisión' --documento-id mi-revision --tema linear --modo dark --estilo sobrio --salida /tmp/mi-revision.html
python3 scripts/validar_artefacto.py /tmp/mi-revision.html
```

Guarda el mismo documento-id entre versiones. Los comentarios persisten en el navegador y pueden compartirse como JSON; no existe sincronización remota ni autenticación en el HTML. El historial exportado conserva eventos de edición y archivado. La colaboración conectada es una propuesta documentada, no un servicio activo.

Para mantener la biblioteca: `python3 scripts/ensamblar.py`, `python3 scripts/validar.py`, `python3 scripts/probar_contrato.py`, `node scripts/probar_revision_store.cjs`, `node scripts/probar_temas.cjs` y `python3 scripts/validar_skill.py`. Las pruebas de navegador están en `scripts/comprobar_*.py`; requieren Orca y el servidor local. CI verifica contratos y paquete, no audición humana ni lector de pantalla.

## Recursos y procedencia

Las fuentes tienen sus avisos OFL en `licencias/`. Los recursos de referencia y sus hashes están documentados en `referencia-cmrg.md` y `auditoria/`. La biblioteca mantiene los recursos aprobados durante el diseño. Las paletas Linear y de editores son adaptaciones propias, no oficiales; [temas.md](temas.md) registra las referencias y ajustes. Publicar este repositorio no concede una licencia adicional sobre recursos de terceros.
