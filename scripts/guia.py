"""Guía completa derivada del registro; conserva un único montaje de controles comunes."""
import re,json,html
from pathlib import Path
from contrato_artefacto import build,recipe,ROOT
from biblioteca import CHAPTERS

def inline(text):
 text=html.escape(text)
 text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
 text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
 return re.sub(r'\[([^]]+)\]\(([^)]+)\)',r'<a href="\2">\1</a>',text)

def prose(text):
 """Markdown acotado de estas guías: párrafos, listas, tablas y código; sin paquetes externos."""
 result=[]
 for block in text.strip().split('\n\n'):
  lines=block.splitlines()
  if not lines:continue
  if lines[0].startswith('|'):
   rows=[[inline(c.strip()) for c in line.strip('|').split('|')] for line in lines if not re.match(r'^\|[\s:|-]+\|$',line)]
   result.append('<div class="tabla-caja" tabindex="0" role="region" aria-label="Criterios de composición, tabla desplazable"><table><caption>Comparar opciones</caption><thead><tr>'+''.join('<th scope="col">'+c+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join(('<th scope="row">'+c+'</th>') if i==0 else '<td>'+c+'</td>' for i,c in enumerate(row))+'</tr>' for row in rows[1:])+'</tbody></table></div>')
  elif lines[0].startswith('```'):
   code='\n'.join(lines[1:-1]);result.append('<div class="codigo"><pre tabindex="0" aria-label="Comandos de ejemplo, desplazables"><code>'+html.escape(code)+'</code></pre></div>')
  elif re.match(r'^(?:- |\d+\. )',lines[0]):
   items=re.split(r'\n(?=- |\d+\. )',block);tag='ul' if lines[0].startswith('-') else 'ol'
   result.append('<'+tag+'>'+''.join('<li>'+inline(re.sub(r'^(?:- |\d+\. )','',item)).replace('\n',' ')+'</li>' for item in items)+'</'+tag+'>')
  else:result.append('<p>'+inline(block).replace('\n',' ')+'</p>')
 return ''.join(result)

def code_box(source,key,title):
 return f'<details class="receta-copia ancho"><summary>HTML completo · {html.escape(title)}</summary><div class="codigo codigo-editorial"><div class="cab"><span>{html.escape(title)}</span><button type="button" class="boton-icono-copia" data-copiar="guia-fuente-{key}" aria-label="Copiar HTML de {html.escape(title)}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 8h12v13H8zM16 8V3H4v13h4"/></svg></button><span class="copia-estado" role="status"></span></div><pre tabindex="0" aria-label="HTML de {html.escape(title)}, desplazable"><code id="guia-fuente-{key}" data-lenguaje="html">{html.escape(source)}</code></pre></div></details>'

def generate():
 registry=json.loads((ROOT/'registro.json').read_text())['componentes'];by_id={r['id']:r for r in registry}
 cases=json.loads((ROOT/'casos-uso.json').read_text())['casos']
 sections={};parts=re.split(r'^## (.+)$',(ROOT/'guia-uso.md').read_text(),flags=re.M)
 for i in range(1,len(parts),2):sections[parts[i]]=parts[i+1]
 def section(title,id):return '<section class="seccion" id="'+id+'"><h2>'+title+'</h2></section>'+prose(sections[title]).replace('class="tabla-caja"','class="tabla-caja ancho"')
 links=''.join('<li><a href="#guia-'+r['id']+'">'+html.escape(r['nombre'])+'</a></li>' for r in registry)
 routes=''.join('<article class="card-editorial"><p class="ceja">'+c['id']+'</p><h3>'+c['nombre']+'</h3><p>'+c['pregunta']+'</p><p>'+', '.join('<a href="#guia-'+k+'">'+by_id[k]['nombre']+'</a>' for k in c['componentes'])+'</p></article>' for c in cases)
 intro='''<section class="seccion" id="guia-empezar"><p class="ceja">Manual de uso / edición 04</p><h2>Una biblioteca para pensar con ella.</h2><p>Elige una pregunta. Construye el argumento. Dale a cada pieza una tarea.</p><p>Esta guía reúne <strong>{component_count} componentes, 13 familias con claro y oscuro y ocho recorridos de composición</strong>. Cada receta se puede ver y copiar; la base siempre incluye apariencia, sonido optativo, comentarios y ayudas de lectura.</p><p>Los ejemplos son ilustrativos: ninguna cifra de las muestras describe resultados reales de Liftit o Tikin.</p></section><nav class="biblioteca-rutas ancho" aria-label="Entradas a la guía"><a href="#componer"><strong>01 / Encontrar la forma</strong><small>Del objetivo a la combinación de componentes.</small></a><a href="#voz"><strong>02 / Escribir entre líneas</strong><small>Notas izquierda y derecha, subrayado, audio y ayudas.</small></a><a href="#ambientes"><strong>03 / Probar los temas</strong><small>Familias, modo claro/oscuro/sistema y documentos completos.</small></a><a href="#entrega"><strong>04 / Llevarla a tu agente</strong><small>Generar, validar e instalar en Hermes, Claude o Codex.</small></a></nav>'''
 intro=intro.replace('{component_count}',str(len(registry)))
 intro+='<section id="guia-inventario"><h2>Todas las piezas, a mano.</h2><p>Selecciona un nombre para ir al ejemplo, sus límites y el HTML completo. Apariencia y comentarios se usan desde los controles comunes del documento.</p><nav aria-label="Todos los componentes"><ul class="catalogo-indice">'+links+'</ul></nav></section>'
 compose=section('Antes de escoger piezas','guia-pregunta')+section('Recorridos que se pueden adaptar','guia-recorridos')+'<div class="cards-editoriales ancho">'+routes+'</div>'+section('Dar escala a la evidencia','guia-escala')+section('Logística: del territorio a la acción','guia-logistica')
 voice=section('Dos voces: argumento y nota al margen','guia-voces')
 # IDs separados de la receta del catálogo: la muestra de composición es un documento distinto.
 sample=recipe('apuntes')
 for id in ['apuntes-ejemplo','apunte-izquierdo','apunte-derecho']:sample=sample.replace(id,'guia-demo-'+id)
 sample=sample.replace('Una decisión necesita contexto.','El denominador cambia la lectura.').replace('La evidencia sirve cuando nos ayuda a <span data-subrayar="referencia">decidir mejor</span>. Un reporte puede dejar una pregunta breve al margen sin interrumpir el argumento.','Antes de afirmar que el servicio mejoró, define si estás midiendo <span data-subrayar="referencia">entregas completadas</span> o todos los intentos. La cifra necesita ese contexto.').replace('menos ruido, más criterio.','¿incluye devoluciones?').replace('Explicar también es editar.','Una propuesta todavía es una pregunta.').replace('Antes de agregar otra gráfica, prueba a <span data-subrayar="referencia">quitar lo que sobra</span>. La anotación acompaña al párrafo; el subrayado se dibuja cuando aparece.','Un prototipo permite <span data-subrayar="referencia">observar una tarea</span>. Hasta hacer la prueba no sabemos si la interfaz ayuda a completarla.').replace('¿se entiende sin explicarlo?','primero, ver a alguien usarlo.')
 voice+=sample+code_box(sample,'composicion-notas','Composición de notas izquierda y derecha')+section('Barras que ayudan a leer y revisar','guia-ayudas')
 themes=section('Elegir una voz visual','guia-temas')+'<p><a href="temas.html">Explorar las 13 familias y los modos Claro, Oscuro y Sistema</a>.</p>'+'''<nav class="biblioteca-rutas ancho" aria-label="Ejemplos de temas"><a href="liftit.html"><span class="paleta-mini liftit" aria-hidden="true"><i></i><b></b></span><strong>Liftit / operación</strong><small>Rutas, datos y capacidad. Adaptación del azul medido en la web oficial.</small></a><a href="blueprint.html"><span class="paleta-mini blueprint" aria-hidden="true"><i></i><b></b></span><strong>Blueprint / sistema</strong><small>Plano azul, cuadrícula blanca y explicación de una confirmación.</small></a><a href="hacker.html"><span class="paleta-mini hacker" aria-hidden="true"><i></i><b></b></span><strong>Hacker / runbook</strong><small>Contrato, código destacado, terminal y recuperación.</small></a></nav><aside class="aviso"><span class="num">i</span><div><p class="titulo">Prueba la guía entera en cada tema.</p><p>Abre la llave sol/luna de la cabecera. Las paletas se aplican también a tablas, gráficas, mapas, notas y comentarios. El sonido está habilitado y espera el primer clic real. Puedes apagarlo en la pestaña Sonido; esa elección se recuerda. En Letras prueba Libro, Revista y Bitácora.</p></div></aside>'''
 pages=[{'id':id,'titulo':title,'html':body} for id,title,body in [('manual','Guía de la biblioteca',intro),('componer','Componer',compose),('voz','Voz y lectura',voice),('ambientes','Temas',themes)]]
 for chapter,label,_,desc,keys in CHAPTERS:
  body='<p class="bajada">'+desc+'</p>'
  for key in keys:
   r=by_id[key];body+='<section id="guia-'+key+'" data-guia-componente="'+key+'"><p class="ceja">'+chapter+' / '+key+'</p><h2>'+html.escape(r['nombre'])+'</h2></section>'
   if key in ['apariencia','revision']:body+='<p>Este componente ya está activo en la base: '+('abre la llave sol/luna de la cabecera.' if key=='apariencia' else 'usa la burbuja flotante para dejar y copiar un comentario.')+'</p>'
   else:body+=r['html']
   body+='<div class="receta-guia">'+prose(r['criterio_y_limites'])+'<p class="procedencia">Dependencias: '+html.escape(', '.join(r['dependencias']))+'</p></div>'+code_box(r['html'],key,r['nombre'])
  pages.append({'id':'piezas-'+chapter,'titulo':label,'html':body})
 install=(ROOT/'instalacion.md').read_text();installparts=re.split(r'^## (.+)$',install,flags=re.M)
 delivery=section('Copiar, componer y comprobar','guia-generar')
 for i in range(1,len(installparts),2):delivery+='<section id="guia-instalar-'+str(i)+'"><h2>'+html.escape(installparts[i])+'</h2>'+prose(installparts[i+1])+'</section>'
 pages.append({'id':'entrega','titulo':'Usar el skill','html':delivery})
 (ROOT/'guia.html').write_text(build('Nota Tikin · Guía de uso y componentes',pages,'Cómo construir documentos que se leen, se exploran y se revisan.'))
 (ROOT/'auditoria/guia-cobertura.json').write_text(json.dumps({'paginas':[p['id'] for p in pages],'componentes':[r['id'] for r in registry],'casos':cases},ensure_ascii=False,indent=2)+'\n')
 print('Generada guia.html: '+str(len(pages))+' páginas y '+str(len(registry))+' recetas completas')

if __name__=='__main__':generate()
