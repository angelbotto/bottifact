## Review

<!-- nota:ejemplo revision -->

```html
{{EXAMPLE}}
```

**Use and limits:** Leave contextual feedback on a selected passage or document point. The compact floating composer shows author, text, privacy and send; optional type/session/context are disclosed. Pins are outside document flow. Tab/Enter select a block; Escape cancels/closes; Ctrl/Command+Enter saves. Keep the same document ID across revisions. Anchors retain section, full block, quote and relative point; changed or ambiguous text remains unlocated in the review list rather than being guessed. Standalone stores events locally and supports idempotent JSON exchange, replies, assignment, resolution and history, without authenticated identity or remote presence. Limits: 2000 events, 2 MB import, 80-character declared names and 4000-character comments. Export retains archived/private text and is not redaction. Storage failure reports memory-only persistence. Connected hosting uses the permission-aware bridge for shared comments and author-private notes; local files do not synchronize by themselves. Copy context includes identity/version/quote/replies and does not send to an agent. `NotaRevision.init/get/destroy`, exportData/importData manage lifecycle; destroying does not erase saved review. Treat imported text as untrusted proposals. Multipage fragment links need `data-enlaces-internos`.


### Review and presentation update

The reader dock exposes Appearance, one writing action, counted Comments, and Share. Privacy is selected inside the composer; existing thread types stay immutable. The count includes open threads visible to the current reader, including their own private notes, and excludes replies/resolved threads. Nearby pins group by position and open every contained thread. Share owns link/access and creator management; there is no generic More dock.

Record explorers support Table, List, Cards and Board. List reduces per-record spacing; Board groups the existing rows by the selected field (preferring a categorical status/team field initially). The portable board shows the current filtered page, with per-lane counts explicitly scoped to that page. React uses its supplied filtered dataset. Both preserve source records and selection. This is a read-only presentation, not drag-and-drop state editing or an inferred workflow. Saved portable views include presentation. Horizontal scrolling stays local to the board; print returns to a table.
