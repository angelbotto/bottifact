# Bottifact → Margen

Margen is the current product and skill name from v0.6.0. This is an identity migration with compatibility, not a new account or document store.

## What changes

The GitHub repository, visible wordmark, documentation and canonical skill use Margen. Ask an agent to use `$margen`. The installer creates `~/.agents/skills/margen`, `~/.claude/skills/margen` and `~/.hermes/skills/margen`, plus the `margen` command. The old skill name becomes a short forwarding entry.

## What remains compatible

The hosted service remains `https://artifacts.botto.is`. Artifact IDs, URLs, versions, private notes, comments, permissions and session provenance remain intact. The managed library remains at `~/.local/share/bottifact/library`; personal settings remain outside it. The `bottifact` command, `BOTTIFACT_*` environment variables, `@bottifact/core` and `@bottifact/react` package scopes, runtime globals, storage keys and legacy ZIP filenames remain supported. These names are protocol compatibility, not the current product identity.

An updater already installed under the old release must be able to verify and unpack the new release. Therefore the ZIP root and manifest format remain compatible. A follow-up run of the new updater creates the new skill/command aliases. Existing custom directories or unrelated symlinks are preserved rather than overwritten.

```bash
bottifact update
bottifact update
# Subsequent updates:
margen update
```

The second call is needed only when migrating through an older updater that does not yet know the new aliases. Fresh installs create them directly. Open a new conversation or reread the skill. Do not move databases, regenerate artifact IDs or reconnect accounts merely to adopt the new name.

## Documentation language

Repository documentation and contributor instructions are maintained in English. Localized artifact examples, quoted evidence, public API identifiers and reader UI may remain in their original language. Renaming an API or translating a CSS class is not part of this migration.
