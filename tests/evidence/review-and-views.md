# Review and record presentations — 2026-09-18

Verified with synthetic local records, not production feedback.

- Two threads created at the same anchor produced a single count-2 pin. Activating it showed both threads. The dock count was 2.
- The dock has Appearance, writing, counted Comments and Share. Privacy remains visible inside the composer. Share owns link/access and creator management; no generic More dock is present.
- At a 320px iframe viewport, document scroll width stayed 320px. The board's scroll region was 264px wide with 804px of horizontally scrollable grouped content. Three desktop lanes measured 260px each.
- Portable and React tests preserve selected records and source values while switching Table/List/Cards/Board. Portable filtering and stable node identities survive presentation changes and clearing filters.
- Boards are read-only presentations, not live workflow editors. Portable lane counts refer to the current page; React uses its supplied filtered rows.

The automated suite additionally checks private-writing availability for verified readers without shared-comment permission, failed drafts, pin clustering, open-count updates and absence of duplicate note/More dock shortcuts.
