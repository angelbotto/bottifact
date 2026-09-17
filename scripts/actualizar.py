#!/usr/bin/env python3
"""Instala o actualiza Bottifact para Claude Code, Codex y Hermes. Python 3.10+."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile

ORIGIN = 'https://artifacts.botto.is'


def fetch(path, limit):
    req = urllib.request.Request(ORIGIN + path, headers={'User-Agent': 'Bottifact/1.0'})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs): return None
    with urllib.request.build_opener(NoRedirect).open(req, timeout=60) as response:
        data = response.read(limit + 1)
    if len(data) > limit: raise ValueError('La descarga supera el tamaño esperado.')
    return data


def extract(data, expected, destination):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('La descarga no coincide con SHA-256. No se ha cambiado la instalación. Intenta de nuevo.')
    import io
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if sum(i.file_size for i in archive.infolist()) > 200 * 1024 * 1024: raise ValueError('Paquete demasiado grande.')
        for item in archive.infolist():
            path = PurePosixPath(item.filename)
            if path.is_absolute() or '..' in path.parts or not path.parts or path.parts[0] != 'bottifact' or '\\' in item.filename or (item.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError('Ruta no permitida en el paquete.')
        archive.extractall(destination)


def main():
    if sys.version_info < (3, 10): raise ValueError('Bottifact requiere Python 3.10 o posterior. En macOS: brew install python')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', type=Path, default=Path.home()/'.local/share/bottifact/library')
    parser.add_argument('--sin-enlaces', action='store_true', help='Actualiza solo la biblioteca; no modifica carpetas de agentes ni instala el comando.')
    args = parser.parse_args()
    destination = args.destino.expanduser().absolute()
    if (destination/'.git').exists(): raise ValueError('El destino es un checkout Git. Conserva ese desarrollo y elige otra carpeta con --destino.')
    with tempfile.TemporaryDirectory(prefix='bottifact-download-') as temporary:
        root = Path(temporary)
        expected = fetch('/downloads/bottifact-portable.sha256', 1024).decode().split()[0]
        if len(expected) != 64 or any(c not in '0123456789abcdef' for c in expected): raise ValueError('SHA-256 inválido.')
        extract(fetch('/downloads/bottifact-portable.zip', 50*1024*1024), expected, root)
        source = root/'bottifact'
        subprocess.run([sys.executable, str(source/'scripts/instalar.py'), '--destino', str(destination), '--actualizar'], check=True)
    if not args.sin_enlaces:
        for agent,label in [('.agents','Codex'),('.claude','Claude Code'),('.hermes','Hermes')]:
            link = Path.home()/agent/'skills/bottifact'
            link.parent.mkdir(parents=True, exist_ok=True)
            if link.exists() and not link.is_symlink():
                print('Conservado sin cambios (carpeta propia): ' + str(link));continue
            if link.is_symlink() and link.resolve() == destination.resolve():
                print(label + ': listo · ' + str(link));continue
            if link.is_symlink():
                print('Conservado sin cambios (apunta a otra biblioteca): ' + str(link));continue
            link.symlink_to(destination, target_is_directory=True)
            print(label + ': instalado · ' + str(link))
        binary = Path.home()/'.local/bin/bottifact'
        binary.parent.mkdir(parents=True, exist_ok=True)
        if binary.exists() and '# Bottifact managed launcher' not in binary.read_text():
            print('Conservado comando existente: ' + str(binary))
        else:
            text = '#!' + sys.executable + '\n# Bottifact managed launcher\nimport os,sys\nfrom pathlib import Path\nroot=Path(' + repr(str(destination)) + ')\nargs=sys.argv[1:]\nscript="actualizar.py" if args and args[0] in ("actualizar","instalar") else "publicar.py"\nif script=="actualizar.py":args=args[1:]+["--destino",str(root)]\nos.execv(sys.executable,[sys.executable,str(root/"scripts"/script),*args])\n'
            stage = binary.with_name('.bottifact-new')
            stage.write_text(text);stage.chmod(0o755);stage.replace(binary)
            print('Comando: ' + str(binary) + ' (añade ~/.local/bin a PATH si hace falta).')
    version = json.loads((destination/'VERSION.json').read_text())['version']
    print('Bottifact ' + version + '. Generar HTML no requiere cuenta ni token.')
    print('Para publicar: entra en ' + ORIGIN + ' → Conectar un agente. Nunca pegues el token en un artefacto.')
    print('Actualizar después: python3 ' + str(destination/'scripts/actualizar.py'))


if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        sys.exit('No se completó la instalación: ' + str(error))
