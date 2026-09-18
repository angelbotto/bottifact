#!/usr/bin/env python3
"""Scaffold a component recipe without editing a shared source document."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = ('publications', 'reading', 'reports', 'charts', 'tables', 'prototypes', 'expression', 'settings')
LEGACY = dict(zip(CATEGORIES, ('publicaciones', 'lectura', 'reportes', 'graficas', 'tablas', 'prototipos', 'expresion', 'configuracion')))


def scaffold(root, identifier, title, category):
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', identifier):
        raise ValueError('Use an English kebab-case ID, for example delivery-summary.')
    if category not in LEGACY or not title.strip() or any(c in title for c in '\r\n<>'):
        raise ValueError('Use a supported category and a plain-text, single-line title.')
    base = root / 'packages/core/recipes'
    target = base / identifier
    aliases_path = root / 'packages/core/registry/component-aliases.json'
    aliases = json.loads(aliases_path.read_text())
    if identifier in aliases or identifier in aliases.values() or target.exists():
        raise ValueError('That component already exists.')
    index_path = base / 'index.json'
    index = json.loads(index_path.read_text())
    target.mkdir()
    metadata = {'id': identifier, 'legacyId': identifier, 'category': LEGACY[category], 'title': title,
                'dependencies': ['packages/core/styles/fonts.css', 'packages/core/styles/artifact.css']}
    (target / 'component.json').write_text(json.dumps(metadata, indent=2) + '\n')
    (target / 'example.html').write_text(f'<section class="seccion" id="{identifier}"><h2>{title}</h2><p>Illustrative example. Replace with meaningful content.</p></section>\n')
    (target / 'README.md').write_text(f'\n## {title}\n\n<!-- nota:ejemplo {identifier} -->\n```html\n{{{{EXAMPLE}}}}\n```\n\n**When:** Explain the decision this component supports.\n\n**Limits:** Document keyboard access, narrow screens, data provenance and failure states.\n')
    index.append({'file': f'{identifier}/README.md', 'example': f'{identifier}/example.html'})
    index_path.write_text(json.dumps(index, indent=2) + '\n')
    aliases[identifier] = identifier
    aliases_path.write_text(json.dumps(aliases, indent=2) + '\n')
    version_path = root / 'VERSION.json'
    version = json.loads(version_path.read_text())
    version['componentes'] += 1
    version_path.write_text(json.dumps(version, ensure_ascii=False, indent=2) + '\n')
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--id', required=True)
    parser.add_argument('--title', required=True)
    parser.add_argument('--category', choices=CATEGORIES, required=True)
    args = parser.parse_args()
    try:
        target = scaffold(ROOT, args.id, args.title, args.category)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + '\n')
    print(f'Created {target.relative_to(ROOT)}. Edit the example and guidance, then run python3 scripts/build.py and npm run build.')
