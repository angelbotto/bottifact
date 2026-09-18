#!/usr/bin/env python3
"""Sirve los artefactos locales con la CSP de prueba. No instala ni publica."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import argparse

ROOT=Path(__file__).resolve().parents[1]
CSP=("default-src 'none'; script-src 'unsafe-inline' https://cdnjs.cloudflare.com "
     "https://cdn.jsdelivr.net/npm/ https://cdn.tailwindcss.com https://code.jquery.com; "
     "style-src 'unsafe-inline' https://fonts.googleapis.com; font-src data:; "
     "img-src data:; connect-src 'none'; media-src data:; base-uri 'none'; form-action 'none'")

class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
 def end_headers(self):
  self.send_header('Content-Security-Policy',CSP)
  self.send_header('Cache-Control','no-store')
  super().end_headers()
 def log_message(self,*a):pass

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port','--puerto',dest='puerto',type=int,default=8766);args=p.parse_args()
 print(f'Local con CSP: http://127.0.0.1:{args.puerto}/examples/generated/template.html',flush=True)
 ThreadingHTTPServer(('127.0.0.1',args.puerto),Handler).serve_forever()
