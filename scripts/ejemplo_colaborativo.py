"""Laboratorio de revisión, tabla ampliada y temas Linear; todo ilustrativo."""
import re
from contrato_artefacto import ROOT,recipe,build

def generate():
 table=recipe('explorador').replace('id="explorador-ejemplo" data-explorador','id="explorador-ejemplo" data-explorador data-pagina-tamano="10"').replace('Seis registros ficticios. Ordena por encabezado, filtra y agrupa sin perder el detalle.','Treinta y seis registros ficticios. Busca, filtra por columna, selecciona y exporta. Mayús permite agregar otro criterio de orden.').replace('6 registros de ejemplo.','36 registros de ejemplo.')
 rows=[]
 for i in range(36):
  amount=f"{(i+1)*10000:,}".replace(",", ".")
  rows.append(f'<tr><th scope="row">Entrega de ejemplo {i+1:02}</th><td>{["Bogotá","Medellín","Cali"][i%3]}</td><td>{["En revisión","Confirmado"][i%2]}</td><td data-valor="{(i+1)*10000}">{amount}</td><td>2026-09-{i%28+1:02}</td><td>{["Ana","Luis","Camila"][i%3]}</td></tr>')
 table=re.sub(r'<tbody>[\s\S]*?</tbody>','<tbody>'+''.join(rows)+'</tbody>',table)
 extra=''
 for i,name,kind in [(4,'Fecha','fecha'),(5,'Responsable','texto')]:
  extra+=f'<th scope="col" data-tipo="{kind}"><button type="button" data-orden-col="{i}" data-direccion="1">{name} <span data-indicador-orden aria-hidden="true">↕</span></button></th>'
 table=table.replace('</tr></thead>',extra+'</tr></thead>').replace('data-columna="3" checked> Importe COP</label>','data-columna="3" checked> Importe COP</label><label><input type="checkbox" data-columna="4" checked> Fecha</label><label><input type="checkbox" data-columna="5" checked> Responsable</label>')
 content='''<section id="revision-juntos"><p class="ceja">Laboratorio · revisión y datos</p><h2>Una conversación junto a la evidencia.</h2><p id="cita-revision">Antes de cerrar una decisión, conviene revisar la fuente, el alcance y quién se encarga del siguiente paso.</p><p>Activa la burbuja, deja un comentario sobre esta frase y abre la lista: puedes responder, asignar, resolver y exportar la revisión. Se guarda en este navegador. Para otra persona, comparte el HTML y el archivo de revisión; importar reúne los eventos.</p><p>Los nombres son declarados. Esta muestra no tiene cuentas ni sincronización remota.</p></section><section id="tabla-trabajo"><h2>Una tabla para trabajar.</h2><p>El total corresponde a las filas filtradas; la selección se mantiene al cambiar de página. Los grupos cuentan sólo las filas de su página.</p></section>'''+table+'''<section id="siguiente-capa"><h2>Lo que viene después.</h2><p>Presencia, seguir la lectura de otra persona, decisiones verificadas y comentarios por versión requieren una aplicación conectada. El documento portable seguirá siendo una instantánea que puedas guardar.</p><p><a href="arquitectura.md">Evaluación del stack</a> · <a href="colaboracion.md">Contrato de colaboración</a> · <a href="linear-light.html">Linear Light</a> · <a href="linear-dark.html">Linear Dark</a></p></section>'''
 (ROOT/'ejemplos/colaborativo-contenido.html').write_text(content)
 for theme,name in [('linear-light','colaborativo'),('linear-light','linear-light'),('linear-dark','linear-dark')]:
  (ROOT/(name+'.html')).write_text(build('Nota Tikin · Revisión compartida',[{'id':'contenido','titulo':'Revisión','html':content}],theme=theme,style='sobrio',document_id='nota-laboratorio-colaborativo'))
if __name__=='__main__':generate()
