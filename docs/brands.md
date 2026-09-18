# Liftit, Tikin and Catabum

Brand assets and provenance are recorded in [brands.json](../packages/core/brands/brands.json). Use the embedded authorized logo rather than reconstructing a wordmark with a similar font. Brand identity and reader palette are related but separate choices.

- **Liftit:** logistics identity from the documented frontend sources, including LMS Ribbon/Bay and coral tokens. Route and fleet examples are illustrative unless connected to an actual feed.
- **Tikin:** white, black and red, explicitly confirmed by the owner. Do not use the lime/lavender palette from an unrelated repository. Its logo must remain legible in both light and dark modes.
- **Catabum:** the documented community identity and violet/magenta palette. Do not infer assets from the company name.

The corresponding families each include light/dark variants. System mode follows the device. `--theme tikin` selects the family and its default identity; `--marca` can select identity independently. Check contrast, backgrounds, logo variants, chart colors and print output. Choosing a reader theme must not silently replace the artifact's company identity.

To update a brand, inspect the recorded repository path and commit, verify current authorized assets, edit family tokens and asset records, rebuild and test both modes and mobile. Do not overwrite unrelated checkouts or discard local changes. Logo rights remain with their owners; the project license does not grant trademark rights.

Agent installation is documented in [installation](installation.md); upgrading a library updates its shared skill, not existing immutable artifact versions.
