# Project identity and visual preferences

Margen uses its cube alone in generic headers. A company artifact shows the company's registered or project-supplied logo. The Margen cube remains the favicon. The project name and identifier are embedded as metadata; a single-page header also displays the project name. Company identity does not change when a reader chooses another palette.

## Resolve the project

The generator searches upward from the content/config directory for `.margen.json`, stopping at the repository boundary. Use `--project-root /path/to/project` when the content lives in a temporary directory. `--project-profile /path/to/.margen.json` selects an explicit profile; `--no-project` disables discovery.

Without a profile, an exact GitHub `origin` organization can identify an existing registered brand: `Liftitapp` → Liftit, `Tikinis` → Tikin, `CATABUM-SAS` → Catabum. Other repositories supply a project name only. Remote credentials, full URLs and filesystem paths are never written to the artifact. A folder or document containing the word “Liftit” is not evidence of company ownership.

```json
{
  "version": 1,
  "project": {"id": "delivery-experience", "name": "Delivery experience"},
  "company": {"brand": "liftit"},
  "preferences": {
    "theme": "liftit",
    "mode": "system",
    "typography": "sobrio",
    "format": "chapters",
    "themePolicy": "project"
  }
}
```

Explicit CLI appearance/format flags take precedence over document configuration, then profile preferences, then defaults. Registered companies default to their corporate family, system mode and `sobrio` typography. `--brand margen` keeps the compact Margen identity even when using a corporate palette; `--brand bottifact` remains a compatibility alias.

`themePolicy: "project"` starts with the published project appearance rather than the portal's saved account-wide appearance. Readers can change it during reading. Local standalone preferences remain browser-specific; a sandboxed portal cannot rely on local storage for per-artifact persistence. `themePolicy: "reader"` allows saved portal appearance to take precedence. Sound and favorites remain reader preferences in either policy.

## Another company's logo

Use local assets with a declared company name:

```json
{
  "version": 1,
  "project": {"id": "example-board", "name": "Board review"},
  "company": {
    "name": "Example Company",
    "logo": {"light": "assets/logo-light.svg", "dark": "assets/logo-dark.svg"}
  },
  "preferences": {"theme": "linear", "mode": "system", "themePolicy": "project"}
}
```

Logo paths resolve relative to the profile and must stay inside that directory, including through symlinks. SVG, PNG and JPEG are embedded, with a 500 KB limit per file. SVGs must contain self-contained geometry without scripts, event handlers or external references. Provide separate light/dark variants when contrast requires it; otherwise the light asset is reused. A custom logo and registered `brand` are mutually exclusive. Company logo rights remain with their owners.

## Publishing

Keep the document ID through revisions. Publish to the intended company or project space with `--space`; detecting a company is not authorization to change an existing artifact's audience or library space. The generated HTML records project/company/format metadata. This release does not automatically create or confirm knowledge-graph entities from that metadata.
