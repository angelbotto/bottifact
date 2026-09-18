import { readFile, writeFile } from 'node:fs/promises';
const fonts = await readFile(new URL('../../core/styles/fonts.css', import.meta.url), 'utf8');
const styles = await readFile(new URL('../src/styles.css', import.meta.url), 'utf8');
await writeFile(new URL('../dist/styles.css', import.meta.url), fonts + '\n' + styles + '\n' + await readFile(new URL('../../core/styles/table-content.css', import.meta.url), 'utf8'));
