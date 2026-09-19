# Presentation and document ecosystem assessment

Reviewed 2026-09-18. This is a selection guide and integration plan, not a claim that external engines are bundled or validated end to end in Margen.

## Native default and extension points

Keep ordinary shared documents, chapters and briefing slides in the native generator. That preserves the sandbox, portable HTML, company identity and existing review anchors. The presentation view reuses the chapter runtime instead of importing a second navigation system. An advanced export adapter should consume the same declared project identity and content outline, then validate its own output.

| Tool | Useful extension | Boundary for Margen |
| --- | --- | --- |
| [Reveal.js](https://revealjs.com/) | Rich HTML presentations, fragments, slide overview and presenter tooling | Best candidate for a future advanced web-deck adapter. Bundle reviewed assets and explicitly test sandbox policy, keyboard ownership and anchor coordinates. Its [MIT license](https://github.com/hakimel/reveal.js/blob/master/LICENSE) permits an open-source integration with required notices. |
| [Slidev](https://sli.dev/guide/) | Developer-authored decks with code and Vue components | Useful for technical talks when a Node/Vue authoring project is acceptable. Its [export modes](https://sli.dev/guide/exporting) include picture-based and editable PPTX; complex browser-only elements can still become images, and font/layout fidelity needs review. |
| [Marp CLI](https://github.com/marp-team/marp-cli) | Markdown authoring and HTML/PDF/PPTX builds | A practical optional batch exporter. Normal PPTX output uses rendered slides; editable PPTX is experimental and requires additional tooling. Do not describe every PPTX as editable. |
| [PptxGenJS](https://gitbrent.github.io/PptxGenJS/) | Editable PowerPoint with native text, shapes, tables and charts | Prefer direct composition when editing in PowerPoint is the deliverable. A browser screenshot of a slide is not a substitute for native objects. Map brand tokens and validate in an Office renderer. |
| [Paged.js](https://pagedjs.org/) | Paginated print publications from web content | Candidate for advanced page layout and print pipelines; keep it separate from chapter navigation in the interactive reader. |

Reveal.js [PDF export](https://revealjs.com/pdf-export/) uses a print workflow and can include speaker notes. Native Margen print CSS is independent; equivalent export fidelity has not been asserted. These engines are alternatives selected for a task, not dependencies to load into every artifact.

## Existing agent skills

The official Anthropic [`pptx`](https://skills.sh/anthropics/skills/pptx) and [`docx`](https://skills.sh/anthropics/skills/docx) entries are relevant to Office creation and editing. The directory reported approximately 223.4K and 190.1K installs respectively, and the source repository approximately 177K stars at review time. These are popularity signals, not quality or compatibility guarantees.

Their current skill frontmatter identifies proprietary terms. The [PPTX license](https://raw.githubusercontent.com/anthropics/skills/main/skills/pptx/LICENSE.txt) contains distribution and derivative-work restrictions. Margen does not copy, bundle, install or derive its implementation from these skill materials. Use an appropriately licensed skill already available in the user's environment when an Office deliverable is explicitly requested; verify its current terms and actual capabilities there. The official skill descriptions are [PPTX](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) and [DOCX](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md).

## Adapter contract

A future adapter should carry stable document/page IDs, company identity, chosen theme/mode/type, source references and declared output requirements. Keep source HTML and the rendered export as separate versioned deliverables. Interactive comments stay in Margen; exported documents link back to the canonical artifact and version rather than implying live synchronization. Private review and speaker material must not be copied into exports by default.

Acceptance requires visual checks on every page, mobile checks for HTML, overflow/font checks for exports, reproducibility, an explicit licensing notice and a documented fallback for unsupported components. Keep generation offline where practical. An HTML source is not a generic, lossless intermediate representation for Word or PowerPoint.
