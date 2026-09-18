# @bottifact/core

Framework-independent recipe catalog, theme tokens and isolated preview document assembly. Part of [Bottifact](https://github.com/angelbotto/bottifact).

```js
import { getRecipe, createRecipeDocument } from '@bottifact/core';
import { themeFamilies, getThemeTokens } from '@bottifact/core/themes';

const recipe = getRecipe('bar-chart');
const tokens = getThemeTokens('linear', 'dark');
const html = await createRecipeDocument('bar-chart', { theme: 'linear', mode: 'dark' });
```

The catalog contains 88 existing recipes. Preview assets load asynchronously and include the original runtime and embedded fonts/audio. Use an isolated frame for the generated specimen; it is not an authenticated portal or a complete publishable artifact. The theme entrypoint avoids importing the catalog/runtime.

This version is distributed from the source workspace or packed tarballs, not the npm registry. Build instructions, licensing and deployment boundaries are in the [repository documentation](https://github.com/angelbotto/bottifact/blob/main/docs/README.md). See `NOTICE` and `licenses/` for third-party terms.
