# Theme families, modes and typography

Appearance has independent family, light/dark/system mode and typography choices. Changing family preserves the selected mode; device changes affect only system mode. The compact browser offers search, category filtering, favorites and a scrollable list of previews. Sound controls stay in their own tab.

There are 15 families and 30 palettes. Preview swatches follow the effective mode. Linear is one family, not separate light/dark entries.

| Family ID | Modes |
| --- | --- |
| `editorial` | Light, dark, system |
| `sea` | Light, dark, system |
| `olive` | Light, dark, system |
| `clay` | Light, dark, system |
| `plum` | Light, dark, system |
| `liftit` | Light, dark, system |
| `tikin` | Light, dark, system |
| `catabum` | Light, dark, system |
| `blueprint` | Light, dark, system |
| `hacker` | Light, dark, system |
| `linear` | Light, dark, system |
| `modern` | Light, dark, system |
| `github` | Light, dark, system |
| `catppuccin` | Light, dark, system |
| `solarized` | Light, dark, system |

Six typography presets separate headings from body: Editorial (Instrument Serif/Geist), Sobrio (Geist/Geist), Técnico (Geist Mono/Geist), Libro (Literata/Literata), Revista (Instrument Serif/Literata), Bitácora (Geist Mono/Literata). Reenie Beanie is reserved for handwritten notes. Fonts are embedded with their licenses; code and controls retain their intended families.

Family sources live in `packages/core/themes/families/`; `scripts/themes.py` generates tokens, aliases and runtime metadata. Define complete light/dark tokens, preserve graph/chart states and run theme validation when adding a family. Do not put custom source CSS after the generated-theme marker. The catalog and counts are generated, not manually copied into the reader.

Preferences are scoped by origin or artifact defaults as documented by the reader. Without storage, controls still work for the session. System mode follows the device; embedded prototypes are independent documents. Paper grain is optional and removed for print. Editor and Linear themes are adaptations, not official integrations.

See [brand identity](brands.md), [contributing components](contributing-components.md) and [the runnable theme guide](../examples/generated/themes.html).
