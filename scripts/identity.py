"""Original Margen identity, embedded so portable artifacts remain offline."""
from pathlib import Path
from base64 import b64encode
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'packages/core/assets/identity'
def mark():
    return (ASSETS / 'margen-mark.svg').read_text().strip().replace('<svg ', '<svg class="margen-mark" width="30" height="30" aria-hidden="true" focusable="false" ', 1)
def favicon():
    data = b64encode((ASSETS / 'margen-favicon.svg').read_bytes()).decode()
    return '<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,' + data + '">'
