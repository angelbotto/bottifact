# Changelog

## 0.5.1 — Tables and mobile reading

- Consolidate portable table controls with source-value facets, removable filter chips, contextual selection actions and clearer column settings.
- Add automatic mobile record cards and explicit Table/Cards switching to portable and React tables, preserving source cells, IDs and selection.
- Improve mobile detail sheets, reader safe areas, touch targets, reading progress placement and narrow fleet projections.
- Document mobile composition and revision migration; extend the synthetic workbench and behavior tests. Historical HTML is not silently rewritten.


## 0.5.0 — Unified reading and connected context

- Add one artifact toolbar for personal appearance, review, sharing and contextual actions, with a compatible portal adapter for historical HTML.
- Introduce a shared typed table-query model, TanStack React DataTable, filter builder, row inspector, stable selection, local saved views and portable table upgrades. Include synthetic Liftit, Tikin and Catabum scenarios.
- Add authorized library conditions, account-private saved filters, explicit batch tagging/collections/archive, command search, working sets and movable private boards.
- Add personal company/project/topic entities with aliases and properties, version-pinned directional references, backlinks, literal mention suggestions, relationship filters and saved graph positions.
- Add session-output browsing and a previewable context composer with selected comments, opt-in own notes and selected reference evidence. Copy and download do not send to an agent or publish a revision.
- Keep source versions immutable, validate both endpoints of every relationship and restrict cited historical versions to confirmed references and current permissions.
- Document surface-specific capabilities and boundaries; update the canonical portable skill for Codex, Claude Code and Hermes.

## 0.4.0 — Administrator knowledge workbench

- Connect artifacts to companies/spaces, manual or automatic topics, and collections in the actual portal graph. Explain membership, explore one/two-hop neighborhoods, search nodes, pan, zoom and move nodes.
- Add searchable library facets, server-wide bidirectional column sorting, agent and pending-review filters, column visibility, density and scroll-preserving table loading.
- Add opt-in six-hour skill updates for macOS LaunchAgents and Linux user timers, preserving each installation’s chosen server and credentials. Skip unchanged downloads and lock concurrent updates.
- Document the portal/local-component distinction and update lifecycle. Add graph, cursor, privacy, filter UI and scheduler regression checks.
- The core/React package API remains at 0.3.0; this release changes the portal and portable skill.

## 0.3.0 — Component discovery and local relationship exploration

- Expand the library to 88 documented recipes with six continuity compositions.
- Add local relationship exploration: named nodes, directed explanations, search, one/two-hop focus, state/type filters, history, zoom and source tables.
- Make the visual guide searchable by need, category and composition journey; add a component playbook.
- Document 36 workbench directions while distinguishing local examples from connected portal capabilities.
- Add regression checks for graph navigation, invalid data, lifecycle and catalog discovery. The portal graph model is unchanged.

## 0.2.1 — Hosted onboarding

- Make artifacts.botto.is the primary onboarding path, with account connection, publication, review handoff and update instructions.
- Keep self-hosting and local-only installation as independent documented paths.
- Teach the shared skill to preserve the chosen service and avoid asking hosted users for server configuration.
- Correct outdated composition and review descriptions; no portal runtime changes.

## 0.2.0 — Organized sources and React adapter

- Move runtime, recipes, themes, examples, documentation and verification records into explicit English paths. Preserve published identities and legacy selectors.
- Add per-recipe manifests and a component scaffolder; split theme families into individual source files.
- Add typed core/React workspaces with eight native exports and sandbox access to the existing 82 recipes. Packages are available from source/packed tarballs, not the npm registry.
- Add a private feedback handoff bundle that preserves artifact/version/anchor/session context. Delivery remains manual.
- Document installation variables, self-hosting, architecture, graphs, React, contribution and migration. Replace historical screenshots in the current tree with a synthetic fixture.


## 0.1.0 — First open-source release

- Portable editorial library: 82 recipes, 15 theme families, light/dark/system and six typography combinations.
- Shared skill and verified installer for Claude Code, Codex and Hermes; local ZIP installation without a hosted account.
- Optional FastAPI/SQLite portal with native Google/email authentication, document permissions, comments, private notes, drafts, published versions and context exports.
- Searchable library with gallery, list, table, editable classification and shared-tag/collection relationship map.
- Generic Docker Compose deployment, private environment setup, optional HTTPS proxy and administrator bootstrap.
- Self-hosted installers remember their own update origin; authentication emails and installation links use the configured domain.
- MIT licensing for original code, third-party notices, contributor/security policies and public project documentation.

This release opens an existing working system to the community. It does not include automatic conversation synchronization, an MCP server, model training or live collaborative text editing. Historical library versions retain their dated identifiers in VERSION.json.
