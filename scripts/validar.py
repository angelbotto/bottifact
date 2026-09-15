#!/usr/bin/env python3
"""Contratos estáticos del skill y los fragmentos. Biblioteca estándar, sin red."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
import re, subprocess, shutil, json

ROOT=Path(__file__).resolve().parents[1]
THREE='https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.1/three.min.js'
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}

class Fragment(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.refs=[];self.errors=[];self.scripts=[];self.stack=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);classes=set(a.get('class','').split())
  if tag in ['html','head','body']:self.errors.append('Etiqueta envolvente: '+tag)
  if 'id' in a:
   if a['id'] in self.ids:self.errors.append('ID duplicado: '+a['id'])
   self.ids.add(a['id'])
  if a.get('href','').startswith('#'):self.refs.append(unquote(a['href'][1:]))
  if 'data-copiar' in a:self.refs.append(a['data-copiar'])
  if a.get('aria-labelledby'):self.refs.extend(a['aria-labelledby'].split())
  if a.get('aria-controls'):self.refs.extend(a['aria-controls'].split())
  if 'data-tema' in a and tag!='select':self.errors.append('data-tema está reservado al selector de apariencia')
  if tag=='img' and (not a.get('src','').startswith('data:') or 'alt' not in a):self.errors.append('Imagen sin incrustar o sin alt')
  if tag=='script' and a.get('src'):
   src=a['src'];u=urlparse(src);self.scripts.append(src)
   allowed=u.scheme=='https' and (u.hostname in ['cdnjs.cloudflare.com','cdn.tailwindcss.com','code.jquery.com'] or (u.hostname=='cdn.jsdelivr.net' and u.path.startswith('/npm/')))
   if not allowed:self.errors.append('Script fuera de CSP: '+src)
   if 'three' in src.lower() and src!=THREE:self.errors.append('Three sin versión fijada')
  if tag=='link' and a.get('rel')=='stylesheet' and not a.get('href','').startswith('https://fonts.googleapis.com/'):
   self.errors.append('Hoja externa fuera de CSP')
  if classes & {'tabla-caja','diagrama-caja','grafica-caja','escena-caja','escritura-caja','visor-caja','apariencia-panel','pestanas-caja','barra'} or tag=='pre':
   if a.get('tabindex')!='0' or not (a.get('aria-label') or a.get('aria-labelledby')):self.errors.append('Desplazamiento sin foco/nombre: '+tag+' '+a.get('class',''))
  if classes & {'ancho','amplio'}:
   parent=self.stack[-1][1] if self.stack else set()
   section='seccion' in parent and any('por-seccion' in c for _,c in self.stack)
   page='pagina' in parent and any('multipagina' in c for _,c in self.stack)
   if not ('hoja' in parent or section or page):self.errors.append('Figura atrapada fuera de la rejilla: '+a.get('id',a.get('class','')))
  if tag not in VOID:self.stack.append((tag,classes))
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:del self.stack[i:];break
 def handle_startendtag(self,tag,attrs):
  self.handle_starttag(tag,attrs)
  if tag not in VOID:self.handle_endtag(tag)

MODULES={
 'biblioteca.html':['geografia.js','analitica.js','codigo.js','explorador.js','revision.js','interacciones.js','multipagina.js','globo.js','graficas.js','tablas.js','sonido.js','escritura.js','escena.js','reportes.js','visor.js','pestanas.js','catalogo.js','editorial.js'],
 'plantilla.html':['geografia.js','analitica.js','codigo.js','explorador.js','revision.js','editorial.js','interacciones.js','globo.js','graficas.js','tablas.js','sonido.js','escritura.js','escena.js','reportes.js','visor.js','pestanas.js','catalogo.js'],
 'informe.html':['interacciones.js','multipagina.js','graficas.js','reportes.js','visor.js','pestanas.js'],
 'globo.html':['interacciones.js','globo.js'],
 'multipagina.html':['interacciones.js','multipagina.js'],
 'pruebas.html':['interacciones.js','multipagina.js'],
}
for modules in MODULES.values():modules.extend(['audio.js','controles.js'])
css=(ROOT/'estilo.css').read_text()
for name,modules in MODULES.items():
 content=(ROOT/name).read_text();f=Fragment();f.feed(content)
 assert content.startswith('<title>'),name+': falta título inicial'
 assert b'<meta charset="utf-8">' in content.encode()[:1024],name+': charset tardío'
 assert not f.errors,(name,f.errors)
 assert all(ref in f.ids for ref in f.refs),(name,'referencias inexistentes',set(f.refs)-f.ids)
 assert css in content,(name,'CSS generado desactualizado')
 assert (ROOT/'fuentes.css').read_text() in content,(name,'fuentes sin incrustar o desactualizadas')
 for module in modules:assert (ROOT/module).read_text() in content,(name,'módulo desactualizado',module)
 for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',content):
  assert url.startswith('data:'),(name,'recurso CSS externo: '+url)
 assert f.scripts.count(THREE)==int('globo.js' in modules or 'escena.js' in modules),(name,'inclusión de Three duplicada o ausente')
 assert len(f.scripts)==len(set(f.scripts)),(name,'guiones externos duplicados')
 print(name+': fuentes sincronizadas, CSP, IDs, rejilla y regiones accesibles correctos')

library=css.split('/* 12 — Librería de evidencia.')[1].split('/* 15 —')[0]
palettes=[set(re.findall(r'(--[\w-]+)\s*:',body)) for _,body in re.findall(r'(:root[^{}]*)\{([^{}]*)\}',library) if '--calor-0:' in body]
assert len(palettes)==4 and all(p==palettes[0] for p in palettes), 'Faltan tokens en un tema'
extras=css.split('/* 13 — Reportes, artículos y prototipos.')[1]
extra_palettes=[set(re.findall(r'(--[\w-]+)\s*:',body)) for _,body in re.findall(r'(:root[^{}]*)\{([^{}]*)\}',extras) if '--pieza-papel:' in body]
assert len(extra_palettes)==4 and all(p==extra_palettes[0] for p in extra_palettes), 'Faltan tokens de piezas en un tema'
menu_palettes=[set(re.findall(r'(--[\w-]+)\s*:',body)) for _,body in re.findall(r'(:root[^{}]*)\{([^{}]*)\}',css) if '--apariencia-papel:' in body]
assert len(menu_palettes)==4 and all(p==menu_palettes[0] for p in menu_palettes), 'Faltan tokens de apariencia en un tema'
new_palettes=[set(re.findall(r'(--[\w-]+)\s*:',body)) for _,body in re.findall(r'(:root[^{}]*)\{([^{}]*)\}',css.split('/* 15 —')[1]) if '--calor-0:' in body]
base_colors=set(re.findall(r'(--[\w-]+)\s*:',css.split('/* 01 —')[1].split('--texto:')[0]))
assert len(new_palettes)==3 and all(p==new_palettes[0] and p>=base_colors|palettes[0] for p in new_palettes), 'Paleta adicional incompleta'
for doc in ['SKILL.md','componentes.md','referencia-cmrg.md']:
 for ref in re.findall(r'\]\(([^)]+)\)',(ROOT/doc).read_text()):
  if ref.startswith(('https:','http:','#')):continue
  assert (ROOT/ref.split('#')[0]).is_file(),(doc,ref)
for file in ROOT.glob('*.js'):
 assert not re.search(r'\b(fetch|XMLHttpRequest)\s*\(',file.read_text()),(file.name,'red en tiempo de ejecución')
 if shutil.which('node'):subprocess.run(['node','--check',str(file)],check=True,capture_output=True)
print('Tokens de seis paletas y preferencia del sistema completos; enlaces, ausencia de fetch y sintaxis JS correctos' if shutil.which('node') else 'Tokens, enlaces y ausencia de fetch correctos; Node no disponible: sintaxis JS no ejecutada')
registry=json.loads((ROOT/'registro.json').read_text())
recipes=dict(re.findall(r'<!-- nota:ejemplo ([\w-]+) -->\s*```html\n(.*?)\n```',(ROOT/'componentes.md').read_text(),re.S))
expected=set(recipes)-{'informe','multipagina'}
assert {item['id'] for item in registry['componentes']}==expected, 'Registro incompleto'
assert len(registry['componentes'])==len(expected), 'Registro duplicado'
for item in registry['componentes']:
 assert item['html']==recipes[item['id']] and item['criterio_y_limites'], ('Fuente de registro distinta',item['id'])
 assert all(dep==THREE or (ROOT/dep).is_file() for dep in item['dependencias']), ('Dependencia inexistente',item['id'])
print('Registro local: '+str(len(expected))+' recetas con HTML original, documentación y dependencias existentes')
print('Esto NO comprueba píxeles, audio, WebGL, foco real ni comportamiento del navegador.')
