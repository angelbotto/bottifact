import data from './generated-themes.json' with { type: 'json' };
import type { ThemeFamily } from './generated-ids.js';
export type { ThemeFamily } from './generated-ids.js';
export type ThemeMode = 'light' | 'dark' | 'system';
export const themeFamilies = data.map(theme => ({ id: theme.id as ThemeFamily, name: theme.name }));
export function getThemeTokens(family: ThemeFamily, mode: 'light' | 'dark'): Readonly<Record<string, string>> {
  const theme = data.find(value => value.id === family);
  if (!theme) throw new RangeError(`Unknown Bottifact theme: ${family}`);
  return Object.fromEntries(Object.entries(theme.modes[mode]).filter((entry): entry is [string, string] => typeof entry[1] === 'string'));
}
