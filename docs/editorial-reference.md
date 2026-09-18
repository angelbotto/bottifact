# Editorial reference and adaptation

The original inspection of [cmrg.me](https://www.cmrg.me/) was performed on September 13, 2026 with Orca browser tools. The evidence inventory is [reference.json](../tests/evidence/reference.json). It covered the current sitemap's 16 routes, their DOM and computed geometry. External destinations and the historical v1 site were outside that inspection.

Observed patterns included serif headings, handwritten marginal notes and underlines, article grids, an attention treemap, reading contents/progress, code blocks, timeline, horizontal photo galleries, shelf objects and small sound interactions. Full-page screenshots repeated the first viewport and were not accepted as complete visual evidence; viewport captures and DOM measurements supported the review.

## Adaptation

Margen uses an editorial reading grid, restrained dotted/fading frames, inline evidence and marginal annotations. Wide figures remain siblings of text blocks. Tables and charts retain accessible source values. Handwritten motion starts when seen, respects reduced motion and uses the approved font/audio assets. Gallery captions stay within images, with native scrolling and a drag affordance.

The library adds executive evidence, portable review, typed tables, themes and permission-aware hosting. These are independent product decisions, not features attributed to the reference. No claim of pixel-perfect equivalence is made. Do not reproduce personal photographs, commercial covers or private account data as public fixtures.

Fonts and approved audio have separate provenance and licenses under `licenses/`, `packages/core/assets/` and `tests/evidence/`. Keep original sound levels, pitch and duration where documented; synthesized replacements should not be described as the original recording. A measured Web Audio graph does not prove perceived sound quality.

## Validation

Inspect actual content at desktop and narrow widths, not only isolated samples. Check line wrapping, local scrolling, margins, focus, keyboard navigation, reduced motion, touch access, printing and no-JavaScript alternatives. A decorative fade must not obscure the sole copy of a conclusion or evidence. See [advanced components](advanced-components.md) and [interface direction](interface-direction.md).
