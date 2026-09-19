# Documents, chapters and presentations

Margen supports three native HTML formats through the same generator, company identity, components and review runtime. These are reading formats, not different authentication or storage systems.

| Format | Use it for | Behavior |
| --- | --- | --- |
| `document` | A memo, article or short report | One continuous page with contents and reading progress |
| `chapters` | Long reports, documentation and evidence appendices | Page navigation, per-page contents, stable deep links and browser history |
| `presentation` | A live discussion or executive briefing | Slide navigation, overview, keyboard controls, continuous reading and printable pages |

If omitted, format follows the source page count. A single source page can still be a presentation. `document` rejects multiple source pages instead of silently discarding them.

## Author once, choose the reading format

```json
{
  "title": "Operational review",
  "document_id": "operations-review",
  "format": "chapters",
  "pages": [
    {"id": "decision", "title": "Decision", "content": "decision.html"},
    {"id": "evidence", "title": "Evidence", "content": "evidence.html"},
    {"id": "next-steps", "title": "Next steps", "content": "next-steps.html"}
  ]
}
```

```bash
python3 scripts/create_artifact.py --config /project/review.json --project-root /project --output /project/review.html
python3 scripts/create_artifact.py --config /project/review.json --format presentation --document-id operations-briefing --output /project/briefing.html
```

English configuration keys are canonical for new work; existing Spanish aliases continue to work. A separately published briefing gets a distinct document ID. A new revision of the same briefing keeps its existing ID and stable page/section IDs. Switching between Present and Read within one artifact reuses the DOM and anchors.

## Presentation controls

- Previous/next buttons, a slide counter and an overview of titles and summaries.
- Arrow keys, Page Up/Down, Home and End when focus is outside interactive controls.
- Shortcuts do not interrupt typing, code, table controls, dialogs or point-comment mode.
- Read shows all slides as a continuous document; Present returns to the selected slide.
- Fullscreen appears only where browser/embedding policy supports it. A hosted sandbox may not offer it.
- Small screens retain readable type and natural vertical scrolling. Dense content is not scaled down to force a fixed canvas.
- Print CSS includes every slide, with landscape pages and page breaks. Long content can span printed pages; inspect the PDF before sending it.

Speaker notes are not private merely because they are visually hidden. Keep confidential presenter material in an authorized private note or a separate restricted document. HTML comments, themes, animation and interactive tables do not become native Office features in an export.

## Composition

A slide should advance one decision or claim. Prefer a conclusion, relevant evidence, comparison or next action over a page of small bullet text. Keep source, date, unit and caveats with the evidence. Put long tables and operational detail in chapters or appendices, while preserving their links. Do not invent figures to fill a slide.

The runnable samples are [chapter report](../examples/generated/project-chapters.html) and [presentation](../examples/generated/project-presentation.html), generated from [one source set](../examples/content/project-formats/presentation.json). All sample business content is illustrative.

For editable Office output, advanced presenter workflows or publication-quality pagination, see [the evaluated tools and integration boundaries](presentation-ecosystem.md). Those external exporters are not installed or bundled by this release.
