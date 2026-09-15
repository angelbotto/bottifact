#!/usr/bin/env python3
"""Verifica un archivo final contra el contrato estándar; no prueba su navegador."""
import argparse
from pathlib import Path
from contrato_artefacto import validate

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('archivo',type=Path);args=p.parse_args()
 try:errors=validate(args.archivo.read_text())
 except OSError as e:p.exit(1,str(e)+'\n')
 if errors:p.exit(1,'\n'.join('ERROR: '+e for e in errors)+'\n')
 print('Contrato estándar correcto: apariencia, audio con silencio/prueba/volumen, comentarios, lectura, dependencias, fuentes y referencias. Falta comprobar comportamiento en navegador.')
if __name__=='__main__':main()
