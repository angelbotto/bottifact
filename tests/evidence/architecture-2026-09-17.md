# Source organization and portability verification

Scope: English source paths, per-component manifests and theme files, React adapters, installation documentation, contextual feedback handoff and synthetic public captures.

- Standalone generation and validation: generated artifact contracts, catalog coverage, theme families and published identities pass.
- Reproducibility: a second build creates no tracked diff.
- Python artifact contract suite: 9 tests pass.
- Portal suite: 49 existing tests pass; an additional CLI feedback integration test verifies the export endpoint and preserved version/session context.
- Feedback bundle: 3 tests cover private permissions, evidence preservation, ambiguous origin and overwrite/empty-export refusal.
- Portable installation: 2 tests cover checksums, install/update/backup, isolated artifact generation and adding a recipe from an installed source package.
- React: 6 behavior tests pass, including StrictMode cleanup, numeric sort/filter, unsafe-link refusal, observer cleanup, sandbox boundaries and shared catalog/theme coverage.
- Packed consumer: both tarballs installed in a separate temporary app; server rendering and async preview generation pass.
- Browser: native showcase checked at 1280px and 390px; no document overflow or offscreen form controls. Catalog preview loads in an opaque-origin sandbox. A dynamic JSON import issue found in the browser was fixed by emitting an ESM asset module.
- Docker: isolated app/worker started healthy with empty dedicated volumes; health, portable downloads and backup creation succeed. Production volumes were not used.
- Privacy: historical captures removed from the current tree. New README image captured from the synthetic React showcase and visually inspected. Allowlist/checksum verification passes. Staged source scan reports no detected secrets; that is not proof that the full Git history is free of sensitive content.

Limits: eight native React exports, not full native parity for every recipe. Feedback delivery is manual session read. No npm registry publication, automated agent message injection or semantic graph model is claimed.
