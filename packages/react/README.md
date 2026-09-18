# @bottifact/react

Typed React components for [Bottifact](https://github.com/angelbotto/bottifact). Requires React/React DOM 18.3 or 19 and the matching `@bottifact/core` package.

```tsx
import { Artifact, Callout, RecipePreview } from '@bottifact/react';
import '@bottifact/react/styles.css';

export function Brief() {
  return <Artifact theme="linear" mode="system">
    <h1>Evidence before a decision</h1>
    <Callout title="Question">What would change our mind?</Callout>
    <RecipePreview id="bar-chart" theme="linear" mode="dark" />
  </Artifact>;
}
```

Eight exports: `Artifact`, `Callout`, `MarginNote`, `Timeline`, `CardGrid`, `DataTable`, `ArtifactFrame`, `RecipePreview`. Native React components scope their theme and clean up effects. `RecipePreview` accesses all 82 original recipes through a sandboxed iframe; these are not 82 native rewrites. Frames do not receive portal credentials or parent DOM access. Shared comments and publication remain portal capabilities.

This version is available through workspace builds or tarballs, not the npm registry. See the [React guide](https://github.com/angelbotto/bottifact/blob/main/docs/react.md) for installation in another app, lifecycle behavior and limitations. Third-party notices ship in `NOTICE` and `licenses/`.
