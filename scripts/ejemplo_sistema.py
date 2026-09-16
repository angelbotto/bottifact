"""Informe del stack y el skill, publicado con la misma base que evalúa."""
import re
from html import escape
from contrato_artefacto import ROOT,build
from guia import prose

def generate():
 source=(ROOT/'arquitectura.md').read_text().split('\n',1)[1]
 parts=re.split(r'^## (.+)\n',source,flags=re.M)
 body='<section id="bottifact"><p class="ceja">Bottico + artifact / revisión del sistema</p><h2>Una biblioteca. Un skill. Tu artefacto.</h2>'+prose(parts[0])+'</section>'
 for n in range(1,len(parts),2):
  heading=parts[n];body+='<section id="sistema-'+str(n)+'"><h2>'+escape(heading)+'</h2></section>'
  for block in parts[n+1].strip().split('\n\n'):
   html=prose(block)
   if block.startswith('|'):html='<figure class="ancho">'+html.replace('<caption>Comparar opciones</caption>','<caption>'+escape(heading)+'</caption>')+'</figure>'
   body+=html
 body+='<nav class="biblioteca-rutas ancho" aria-label="Seguir explorando"><a href="guia.html"><strong>Biblioteca y recetas</strong><small>Elegir piezas por intención.</small></a><a href="temas.html"><strong>Familias y modos</strong><small>Encontrar la voz del documento.</small></a><a href="https://github.com/angelbotto/bottifact"><strong>Repositorio Bottifact</strong><small>Código, skill y versiones.</small></a></nav>'
 (ROOT/'sistema.html').write_text(build('Bottifact · El sistema y su evolución',[{'id':'sistema','titulo':'El sistema','html':body}],description='Biblioteca, generador y skill portable. Qué funciona hoy y qué conviene construir después.',theme='linear',mode='system',document_id='bottifact-sistema'))
