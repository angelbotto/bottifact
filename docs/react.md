# React components

The workspace contains two ESM packages: `@bottifact/core` (catalog, theme tokens, preview assembly) and `@bottifact/react` (typed components and styles). They are source/packed packages, **not published npm registry packages yet**.

## Run the example

From the repository root, with Node 22.12+ and Python 3.10+:

```bash
npm ci
python3 scripts/build.py
npm run build
npm run dev
```

Open the local URL printed by Vite. `examples/react` uses synthetic data and no authentication. `npm run build:demo` creates `dist/react-demo`.

## Install into a separate app

Build and pack both packages from this checkout:

```bash
npm run build
npm pack --workspace @bottifact/core --pack-destination /tmp
npm pack --workspace @bottifact/react --pack-destination /tmp
```

Then, in your existing React application:

```bash
npm install /tmp/bottifact-core-0.2.0.tgz /tmp/bottifact-react-0.2.0.tgz
```

The host supplies React and React DOM (18.3 or 19). Use a bundler with ESM/JSON support, such as Vite. Import the CSS once:

```tsx
import { Artifact, DataTable, RecipePreview } from '@bottifact/react';
import '@bottifact/react/styles.css';

const rows = [{ id: 'a', label: 'Example A', count: 12 }];
export function Example() {
  return <Artifact theme="blueprint" mode="system">
    <DataTable caption="Illustrative records" rows={rows} rowKey={row => row.id}
      columns={[
        { id: 'label', header: 'Label', value: row => row.label },
        { id: 'count', header: 'Count', value: row => row.count },
      ]} />
    <RecipePreview id="attention-map" theme="blueprint" mode="dark" />
  </Artifact>;
}
```

## What is native today?

| Export | Behavior | Boundary |
| --- | --- | --- |
| `Artifact` | Scoped theme family and light/dark/system mode | Does not change the host document theme |
| `Callout` | Note, caution or success content | Plain React children, no HTML injection |
| `MarginNote` | Left/right annotation, viewport reveal, replay control | Lightweight reveal; original handwriting strokes/sound require the recipe |
| `Timeline` | Items with date, title, description; fading vertical line | Text remains available without animation |
| `CardGrid` | Editorial cards with dotted framing and links | Unsafe executable link schemes are refused |
| `DataTable` | Search, numeric/text sort, accessible headers, empty state | No native grouping, virtualization or remote data source yet |
| `ArtifactFrame` | Isolated HTML viewer with explicit title and height | No portal identity bridge or parent DOM access |
| `RecipePreview` | Any of the 82 recipes, selected theme/mode, lazy asset load | Sandboxed original runtime, not 82 native React components |

Props and data interfaces are exported from `packages/react/src/index.ts`. The working example in `examples/react/main.tsx` shows the native components together. `recipes` exposes English IDs, original IDs, HTML, dependencies and guidance. `getRecipe` also accepts a preserved legacy ID. `themeFamilies` and `getThemeTokens` are available through `@bottifact/core/themes` without loading recipe/runtime assets.

## Lifecycle and server rendering

Theme subscriptions and visibility observers are installed in effects and cleaned up on unmount. Native components render without reading browser APIs during server rendering; system appearance initially renders light and updates after mount. In Next.js, import interactive Bottifact components from your own `'use client'` wrapper. `RecipePreview` begins as a loading state and assembles its document in an effect. Do not use it as a replacement for SEO-visible article text.

## Isolation and persistence

Frames allow scripts and downloads, but not `allow-same-origin`, forms, popups or top navigation. Some clipboard/storage/browser APIs are consequently unavailable. Recipe examples display fallback states where applicable; shared comments and portal tokens are not passed to preview frames. To publish a complete artifact with review controls, use the Python generator and portal workflow.

The core preview runtime includes embedded fonts/audio and can be large. Import native components for ordinary application UI, defer previews until needed, and avoid a live iframe per row in a large gallery. Native components do not automatically attach analytics, feedback or remote storage.
