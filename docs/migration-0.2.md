# Migrating to the organized source tree

v0.2 introduces an English source layout and a React package without changing published document identity. Back up your checkout and instance data before upgrading. Do not edit generated HTML to migrate a library bug.

| Previous path | Current path |
| --- | --- |
| Root runtime `.js` files | `packages/core/components/` (English module names) |
| Root `tema.css`, `fuentes.css` | `packages/core/styles/artifact.css`, `fonts.css` |
| `componentes.md` | Generated `docs/components.md`; edit `packages/core/recipes/<id>/` |
| `registro.json` | `packages/core/registry/registry.json` |
| `temas.json` | Generated `packages/core/themes/themes.json`; edit `themes/families/` |
| Root example HTML | `examples/generated/` |
| `ejemplos/` | `examples/content/` |
| `auditoria/` | `tests/evidence/`; historical screenshots are not republished |
| `descargas/` | `dist/` (ignored build output) |
| `licencias/` | `licenses/` |
| `scripts/construir.py` | `scripts/build.py` |
| `scripts/crear_artefacto.py` | `scripts/create_artifact.py` |
| `scripts/validar_artefacto.py` | `scripts/validate_artifact.py` |
| `scripts/publicar.py` | `scripts/publish.py` |
| `scripts/actualizar.py` | `scripts/update.py` |

Public English CLI flags are preferred. Previous Spanish CLI aliases remain accepted. The portable ZIP includes temporary legacy script-name shims so older local instructions continue working; the new source tree has English script names.

English component IDs map to legacy IDs in `packages/core/registry/component-aliases.json`. Persisted IDs, old JSON keys and CSS classes are intentionally retained. Do not bulk-translate a published artifact's IDs: that can detach comments, anchors, source references or stored preferences.

Rebuild using `python3 scripts/build.py`, then validate. React users also run `npm ci && npm run build`. Installed agents should update their shared package and reload skill discovery. Personal tokens stay outside the skill; updating the library does not require replacing them.

Self-hosted instances use the root Compose file and their existing `.env`/volumes. The source reorganization does not require moving database files or republishing every existing artifact. The legacy NAS-specific Compose example is not the portable deployment default.
