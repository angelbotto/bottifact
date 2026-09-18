# Margen interface verification — 2026-09-18

Verified against the local synthetic workbench in Orca's browser. No production documents or account screenshots are included in this evidence.

- Desktop, Linear dark: compact comment composer, author/draft/send hierarchy, optional context and session disclosure, searchable appearance list and grouped table tools.
- 320px iframe viewport: document scroll width 320px. Appearance panel x=12, width=296px, bottom=776px inside an 844px viewport. Comment composer and expanded context both remain within x=12…308.
- 390px iframe viewport: document scroll width 390px; the four table tools share a 334px group with 40px-high controls.
- Functional tests exercise note/session/anchor persistence, failed shared drafts, read-only metadata on existing threads and destroy/remount without duplicate controls.
- Installer tests protect custom skill directories and unmanaged commands while creating the new canonical entry and compatibility forwarding.
- Repeated HTML generation preserves identical hashes for the main stylesheet, component reference and workbench artifact.

These checks do not establish perceptual equivalence with Figma or Linear, and a local fixture does not prove production deployment. Release and deployment status must be checked separately.
