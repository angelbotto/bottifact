# Advanced composition and behavior

Consult only the sections needed for the selected recipes. Source HTML lives in `packages/core/recipes/`; the generated catalog documents dependencies and limits.

## Marginal notes and handwriting
A marginal note qualifies a nearby underlined claim. Use left and right variants deliberately; keep essential facts in the main paragraph. Real grid columns reserve space on desktop, and notes return to document flow on mobile. Avoid absolute offsets for content.

Use the approved Reenie Beanie font and original audio samples. Reveal when entering the viewport; replay is a small hover/focus control available on touch. Reduced motion displays complete text. Leaving the viewport or hiding the tab cancels animation and audio. Sound requires a real user gesture and respects stored mute/volume. Handwriting is secondary emphasis, not a substitute for readable evidence.

## Frames, cards and galleries
Wide components get one dotted frame with fading decorative extensions. Do not nest frames. Outlined cards keep readable titles and metadata; cover images and full-card links must remain semantic. Gallery captions live on the image with restrained shading, subtle corner rounding and a drag affordance. Preserve native horizontal scrolling, keyboard access and reduced motion; images are embedded or explicitly authorized assets.

## Timeline and callouts
Timeline markers identify events; vertical spacing is not a timescale. Its decorative line fades at the end without clipping content. Callout icon motion is brief and optional, honors reduced motion and never creates urgency for static information. Keep text alternatives and semantic headings.

## Prototype previews
Embed declared local `Shadow DOM` content. Device, fit and rotate controls use named icons, with actual viewport/aspect information. This is a viewport preview, not a device emulator. Do not enable arbitrary remote navigation or scripts to make a demo appear operational.

## Data and maps
Every visual includes source, units and a readable data alternative. Attention maps show name, value, share and denominator through hover, focus and selection. Globe controls support rotation/zoom and retain a non-WebGL list. Routes between cities are illustrative geometry; simulated fleet markers do not establish real-time GPS or ETA.

## Review and appearance
Use one shared dock. Theme family, light/dark/system mode, typography and sound remain independent. Comments prioritize writing; disclose context and session separately. Reader controls inherit document tokens while maintaining focus and touch targets. See [interface direction](interface-direction.md), [collaboration](collaboration.md) and [tables/mobile](mobile-and-tables.md).
