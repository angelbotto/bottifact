"""Assemble the component reference from independently editable recipe sources."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT / 'packages/core/recipes'


def assemble():
    parts = []
    for entry in json.loads((RECIPES / 'index.json').read_text()):
        text = (RECIPES / entry['file']).read_text()
        if 'example' in entry:
            text = text.replace('{{EXAMPLE}}', (RECIPES / entry['example']).read_text().rstrip('\n'))
        parts.append(text.rstrip() + '\n\n')
    target = ROOT / 'docs/components.md'
    target.write_text(''.join(parts).rstrip() + '\n')
    return target


if __name__ == '__main__':
    assemble()


def metadata():
    """Validated per-component metadata, in documented display order."""
    result = []
    for entry in json.loads((RECIPES / 'index.json').read_text()):
        if 'example' not in entry:
            continue
        path = RECIPES / entry['example']
        item = json.loads((path.parent / 'component.json').read_text())
        if item.get('category') == 'layout':
            continue
        result.append(item)
    return result
