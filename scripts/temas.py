"""Registro de familias/modos y generación determinista, sin recursos de red."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'temas.json').read_text())
FAMILIES=tuple(f['id'] for f in DATA['familias'])
MODES=tuple(DATA['modos'])
ALIASES=DATA['alias_anteriores']
THEMES=tuple(dict.fromkeys([*FAMILIES,*ALIASES]))
MARK='/* TEMAS GENERADOS — scripts/temas.py; editar temas.json. */'
def normalize(theme=None,mode=None):
 if theme is not None and theme not in THEMES:raise ValueError('Tema desconocido: '+str(theme))
 if mode is not None and mode not in MODES:raise ValueError('Modo desconocido: '+str(mode))
 family,legacy=ALIASES.get(theme,[theme or 'editorial','system'])
 return family,mode or legacy

def mix(a,b,weight):
 return '#'+''.join(f'{round(int(a[i:i+2],16)*(1-weight)+int(b[i:i+2],16)*weight):02x}' for i in (1,3,5))
def tokens(seed,mode):
 p={**seed}
 p.update({'linea':mix(p['panel'],p['tinta'],.17),'linea-fuerte':mix(p['panel'],p['tinta'],.48),'naranja-suave':mix(p['papel'],p['naranja'],.10),
 'verde-suave':p['panel'],'rojo-suave':p['panel'],'azul-suave':p['panel'],'marcador':p['naranja'],'foco':p['naranja'],
 'globo-base':p['panel-2'],'globo-arco':p['tinta-3'],'globo-punto':p['naranja'],'globo-glow':p['panel-2'],'globo-dark':'.6' if mode=='dark' else '0','globo-brillo':'10' if mode=='dark' else '2.4',
 'grafica-1':p['naranja'],'grafica-2':p['verde'],'grafica-3':p['rojo'],'grafica-4':p['azul'],'grafica-papel':p['papel'],'grafica-tinta':p['tinta-2'],
 'calor-tinta':p['tinta'],'calor-ausente':p['panel-2'],'tabla-total':p['panel'],
 'escena-1':p['naranja'],'escena-2':p['verde'],'escena-3':p['rojo'],'escena-tinta':p['tinta-2'],
 'sonido-papel':p['panel'],'sonido-activo':p['verde'],'sonido-tinta':p['tinta'],'escritura-trazo':p['naranja'],'escritura-papel':p['panel']})
 for key,target in {'grafica-linea':'linea','tabla-elegida':'naranja-suave','escena-linea':'linea-fuerte','pieza-papel':'panel','pieza-tinta':'tinta','pieza-secundaria':'tinta-2','pieza-linea':'linea-fuerte','pieza-acento':'naranja','pieza-suave':'naranja-suave','pieza-sube':'verde','pieza-baja':'azul','apariencia-papel':'papel','apariencia-tinta':'tinta','apariencia-secundaria':'tinta-2','apariencia-linea':'linea-fuerte','apariencia-suave':'panel','papel-trama':'linea','sintaxis-numero':'azul','sintaxis-funcion':'naranja'}.items():p[key]='var(--'+target+')'
 for n,amount in enumerate([.02,.09,.17,.25,.33]):p['calor-'+str(n)]=mix(p['papel'],p['naranja'],amount)
 p.update({'plano-rejilla':'#ffffff0c' if mode=='dark' else '#1853a00b','plano-rejilla-mayor':'#ffffff18' if mode=='dark' else '#1853a016','foto-fondo':'#101114','foto-tinta':'#f4f9ff','foto-borde':'#ffffff20','foto-sombra':'#00000033'})
 return p

def original(css,id):
 rules=re.findall(r'(:root[^{}]*)\{([^{}]*)\}',css)
 p={}
 for selector,body in rules:
  if selector.strip()==':root':p.update({k:v for k,v in re.findall(r'--([\w-]+):\s*([^;]+);',body) if '!important' not in v})
 for selector,body in rules:
  if selector.strip() in {f":root[data-theme='{id}']",f':root[data-theme={id}]'}:p.update({k:v for k,v in re.findall(r'--([\w-]+):\s*([^;]+);',body) if '!important' not in v})
 def resolve(v):
  for _ in range(8):
   new=re.sub(r'var\(--([\w-]+)\)',lambda m:p.get(m[1],m[0]),v)
   if new==v:break
   v=new
  return v
 return {k:resolve(v) for k,v in p.items()}

def generate():
 css=(ROOT/'estilo.css').read_text().split(MARK)[0].rstrip()+'\n'
 out=[MARK];runtime={'familias':[],'aliases':ALIASES}
 for f in DATA['familias']:
  item={k:f[k] for k in ['id','nombre','grupo','descripcion']}
  for mode in ['light','dark']:
   config=f[mode];id=config if isinstance(config,str) else f['id']+'-'+mode
   p=original(css,id) if isinstance(config,str) else tokens(config,mode)
   if not isinstance(config,str):out.append(':root[data-theme="'+id+'"] {\n  color-scheme:'+mode+';\n'+''.join('  --'+k+': '+v+';\n' for k,v in p.items())+'}')
   out.append(':root[data-color-mode="'+mode+'"] .paleta-mini[data-muestra-tema="'+f['id']+'"] { --vista-papel:'+p['papel']+'; --vista-tinta:'+p['tinta']+'; --vista-acento:'+p['naranja']+'; }')
   item[mode]=id
  runtime['familias'].append(item)
 (ROOT/'estilo.css').write_text(css+'\n'+'\n'.join(out)+'\n')
 js=(ROOT/'interacciones.js').read_text()
 js=re.sub(r'  /\* REGISTRO TEMAS \*/.*?/\* FIN REGISTRO TEMAS \*/',lambda _: '  /* REGISTRO TEMAS */ const themeRegistry = '+json.dumps(runtime,ensure_ascii=False,separators=(',',':'))+'; /* FIN REGISTRO TEMAS */',js,flags=re.S)
 (ROOT/'interacciones.js').write_text(js)
 md=(ROOT/'componentes.md').read_text()
 def menu(match):
  s=match[0];name=re.search(r'name="color-([^"]+)"',s)[1]
  s=re.sub(r'<fieldset class="apariencia-modos"[\s\S]*?</fieldset>','',s)
  modes='<fieldset class="apariencia-modos"><legend>Modo</legend><div>'+''.join('<label><input type="radio" name="modo-'+name+'" value="'+m+'" data-elegir-modo'+(' checked' if m=='system' else '')+'><span>'+n+'</span></label>' for m,n in [('light','Claro'),('dark','Oscuro'),('system','Sistema')])+'</div><p data-modo-estado>Se adapta a la apariencia del dispositivo.</p></fieldset>'
  s=s.replace('<div class="apariencia-filtros">',modes+'<div class="apariencia-filtros">')
  s=re.sub(r'(<select data-familia-tema>).*?(</select>)',r'\1<option value="">Todas</option><option value="editorial">Editoriales</option><option value="marca">Marcas</option><option value="tecnico">Técnicos</option><option value="producto">Producto</option><option value="editor">Editores</option>\2',s,flags=re.S)
  s=s.replace('<label>Familia<select data-familia-tema>','<label>Categoría<select data-familia-tema>')
  cards='\n'.join('<label data-tema-familia="'+f['grupo']+'"><input type="radio" name="color-'+name+'" value="'+f['id']+'" data-elegir-tema'+(' checked' if f['id']=='editorial' else '')+'><span class="paleta-mini" data-muestra-tema="'+f['id']+'" aria-hidden="true"><i></i><b></b></span><span>'+escape(f['nombre'])+'<small>'+escape(f['descripcion'])+'</small></span></label>' for f in DATA['familias'])
  s=re.sub(r'(<div class="apariencia-colores"[^>]*>).*?(</div></fieldset>)',lambda m:m[1]+cards+m[2],s,flags=re.S)
  s=re.sub(r'(data-temas-resultados role="status">).*?(</p>)',lambda m:m[1]+str(len(FAMILIES))+' temas · claro y oscuro'+m[2],s)
  return s
 md=re.sub(r'<details class="apariencia-menu[^>]*>[\s\S]*?</details>',menu,md)
 (ROOT/'componentes.md').write_text(md)
if __name__=='__main__':generate()
