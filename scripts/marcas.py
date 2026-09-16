"""Identidad del documento: logos locales e incrustados, independiente del tema del lector."""
from pathlib import Path
from html import escape
import base64
import json

ROOT = Path(__file__).resolve().parents[1]
BRANDS = json.loads((ROOT / 'marcas.json').read_text())['marcas']


def identity(marca, theme):
    if marca is not None and marca not in [*BRANDS, 'bottifact']:
        raise ValueError('Marca desconocida: ' + str(marca))
    return None if marca == 'bottifact' else marca or (theme if theme in BRANDS else None)


def logo(marca):
    brand = BRANDS[marca]
    source = (ROOT / brand['logo']).read_text()
    images = []
    for mode, color in [('light', '#181A2A'), ('dark', '#F4F4F4')]:
        # SVG como imagen aislada: no inserta scripts ni IDs en el documento.
        svg = source.replace('currentColor', color)
        data = base64.b64encode(svg.encode()).decode()
        images.append('<img class="marca-logo marca-logo-'+mode+'" src="data:image/svg+xml;base64,'+data+'" alt="" width="'+('36' if marca=='liftit' else '110')+'" height="32">')
    label = '<span class="marca-nombre">'+escape(brand['nombre'])+'</span>' if brand['logo_tipo']=='isotipo' else ''
    return '<span class="marca-firma" data-marca="'+marca+'">'+''.join(images)+label+'</span>'
