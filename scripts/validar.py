#!/usr/bin/env python3
"""Verifica fragmentos de artefacto y sus límites de CSP, sin dependencias externas."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
import re
ROOT=Path(__file__).resolve().parents[1]
class Fragment(HTMLParser):
 def __init__(self):super().__init__();self.ids=set();self.refs=[];self.errors=[];self.scripts=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag in ['html','head','body']:self.errors.append('Etiqueta envolvente: '+tag)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('ID duplicado: '+a['id'])
   self.ids.add(a['id'])
  if a.get('href','').startswith('#'):self.refs.append(a['href'][1:])
  if 'data-copiar' in a:self.refs.append(a['data-copiar'])
  if tag=='img' and not a.get('src','').startswith('data:'):self.errors.append('Imagen sin incrustar')
  if tag=='script' and a.get('src'):
   src=a['src'];u=urlparse(src)
   allowed=u.scheme=='https' and (u.hostname in ['cdnjs.cloudflare.com','cdn.tailwindcss.com','code.jquery.com'] or (u.hostname=='cdn.jsdelivr.net' and u.path.startswith('/npm/')))
   if not allowed:self.errors.append('Script fuera de CSP: '+src)
  if tag=='link' and a.get('rel')=='stylesheet' and not a.get('href','').startswith('https://fonts.googleapis.com/'):
   self.errors.append('Hoja externa fuera de CSP')
for name in ['plantilla.html','globo.html']:
 p=ROOT/name;content=p.read_text();f=Fragment();f.feed(content)
 assert content.startswith('<title>'),name+': falta título inicial'
 assert '<meta charset="utf-8">' in content[:1024],name+': charset tardío'
 assert not f.errors,(name,f.errors)
 assert all(ref in f.ids for ref in f.refs),(name,'referencia local inexistente')
 for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',content):
  assert url.startswith('data:'),(name,'recurso CSS externo: '+url)
 assert '<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js"></script>' in content
 print(name+': fragmento, referencias, UTF-8 y recursos CSP correctos')
for ref in re.findall(r'\]\(([^)]+)\)',(ROOT/'SKILL.md').read_text()):
 assert (ROOT/ref.split('#')[0]).is_file(),ref
print('Referencias del skill correctas')
