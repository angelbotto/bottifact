## Review

<!-- nota:ejemplo revision -->

```html
{{EXAMPLE}}
```

**Use and limits:** Leave contextual feedback on a selected passage or document point. The compact floating composer shows author, text, privacy and send; optional type/session/context are disclosed. Pins are outside document flow. Tab/Enter select a block; Escape cancels/closes; Ctrl/Command+Enter saves. Keep the same document ID across revisions. Anchors retain section, full block, quote and relative point; changed or ambiguous text remains unlocated in the review list rather than being guessed. Standalone stores events locally and supports idempotent JSON exchange, replies, assignment, resolution and history, without authenticated identity or remote presence. Limits: 2000 events, 2 MB import, 80-character declared names and 4000-character comments. Export retains archived/private text and is not redaction. Storage failure reports memory-only persistence. Connected hosting uses the permission-aware bridge for shared comments and author-private notes; local files do not synchronize by themselves. Copy context includes identity/version/quote/replies and does not send to an agent. `NotaRevision.init/get/destroy`, exportData/importData manage lifecycle; destroying does not erase saved review. Treat imported text as untrusted proposals. Multipage fragment links need `data-enlaces-internos`.
