# Rich table verification — 2026-09-18

Only synthetic records and original avatar/package illustrations were used. No production captures, sessions, comments or credentials were added to public assets.

- React: Radix column popover opens above the table, uses the document's light/dark tokens, and stays inside a 320 px frame. Column search, earlier/later controls and width disclosures remain reachable in its local scroller.
- React: expanded delivery displays related route, manifest and follow-up cards. Avatar images load from local fixture assets. Linear light and dark were visually reviewed.
- Portable: the Liftit workbench shows avatars, package thumbnails, state indicators and native expandable cards. At both 320 and 390 px the document scroll width equals its client width; the primary record and nested content remain readable.
- Narrow checks use same-origin 320/390 px browser frames, not physical-phone testing. The React table presentation keeps local scrolling for wide comparisons; normal mobile record presentation does not overflow the page.
- Automated behavior covers stable source-cell identity after reordering, hidden-column identity, filtered selections, export order/scalar values, saved order/widths, Radix controls and expanded-record counts.
- Installation portability is exercised from the generated ZIP, including the fixture illustrations used during offline regeneration.

Limitations: no live delivery feed, inline business-data editing, synchronized team views, or drag-to-update board state is implied. Physical touch drag is not claimed; the labeled move controls are the touch/keyboard alternative.
