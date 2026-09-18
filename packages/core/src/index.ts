import recipeData from './generated-recipes.json' with { type: 'json' };
export { themeFamilies, getThemeTokens } from './themes.js';
import { getThemeTokens } from './themes.js';
import type { RecipeId, ThemeFamily } from './generated-ids.js';
export type { RecipeId, ThemeFamily } from './generated-ids.js';

export type ColorMode = 'light' | 'dark';
export type ThemeMode = ColorMode | 'system';
export interface Recipe {
  id: RecipeId;
  legacyId: string;
  name: string;
  category: string;
  html: string;
  guidance: string;
  dependencies: readonly string[];
}
export const recipes: readonly Recipe[] = recipeData as Recipe[];
export function getRecipe(id: RecipeId | string): Recipe {
  const recipe = recipes.find(value => value.id === id || value.legacyId === id);
  if (!recipe) throw new RangeError(`Unknown Bottifact recipe: ${id}`);
  return recipe;
}

const escape = (text: string) => text.replace(/[&<>"']/g, value => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[value]!);
const baseModules = ['interface', 'audio', 'controls', 'editorial-pieces', 'reader', 'code'].map(name => `packages/core/components/${name}.js`);
const three = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js';

/** Creates an isolated specimen, not a publishable artifact or an authenticated portal. */
export async function createRecipeDocument(id: RecipeId, options: { theme?: ThemeFamily; mode?: ThemeMode } = {}): Promise<string> {
  const recipe = getRecipe(id);
  const theme = options.theme ?? 'editorial';
  const mode = options.mode ?? 'system';
  getThemeTokens(theme, 'light');
  if (!['light', 'dark', 'system'].includes(mode)) throw new RangeError('Unknown theme mode');
  const { default: data } = await import('./generated-assets.js');
  const modules = data.modules as Record<string, string>;
  const dependencies = [...new Set([...baseModules, ...(recipe.dependencies.includes('packages/core/components/data-explorer.js')?['packages/core/components/table-model.js']:[]), ...recipe.dependencies])];
  const scripts = dependencies.map(path => path === three ? `<script src="${three}"></script>` :
    modules[path] ? `<script>${modules[path].replace(/<\/script/gi, '<\\/script')}</script>` : '').join('\n');
  return `<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(recipe.name)}</title><meta name="nota-tema-inicial" content="${theme}"><meta name="nota-modo-inicial" content="${mode}"><style>${data.styles}</style></head><body><main class="hoja marcos-editoriales"><header class="cabecera"><p class="ceja">Bottifact · illustrative component example</p><h1>${escape(recipe.name)}</h1></header>${recipe.html}</main>${scripts}</body></html>`;
}

export { TableModel, emptyTableQuery, queryTableRows, tableCSV, type TableQuery, type TableRule, type TableValue } from './table-model.js';
