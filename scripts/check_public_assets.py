#!/usr/bin/env python3
"""Verify the public screenshot allowlist; pixel privacy still requires review."""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def check():
    manifest = json.loads((ROOT / 'docs/assets/manifest.json').read_text())
    allowed = set()
    for item in manifest['images']:
        path = ROOT / item['file']
        assert path.parent == ROOT / 'docs/assets', 'Public captures must live in docs/assets'
        assert item['synthetic'] is True and item['reviewed'] is True
        assert item['source'].startswith('examples/') and (ROOT / item['source']).exists()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], 'Capture changed; review it and update its manifest'
        allowed.add(item['file'])
    for name in ('README.md', 'README.es.md'):
        for link in re.findall(r'!\[[^]]*\]\(([^)]+)\)', (ROOT / name).read_text()):
            # Dynamic badges contain no artifact/account pixels.
            if link.startswith(('https://img.shields.io/', 'https://github.com/angelbotto/margen/actions/workflows/')):continue
            assert link in allowed, 'Unreviewed README image: ' + link
    actual = {str(p.relative_to(ROOT)) for p in (ROOT / 'docs/assets').iterdir() if p.suffix in ('.png','.jpg','.jpeg','.webp')}
    assert actual == allowed, 'Public image manifest is incomplete'
    print(f'Public captures: {len(allowed)} synthetic fixture image(s), checksums and references verified.')

if __name__ == '__main__':check()
