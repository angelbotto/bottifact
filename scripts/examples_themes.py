"""Tres composiciones ilustrativas, con presentación inicial y base canónica."""
from contract_artifact import ROOT,build,recipe

def intro(id,title,text):return '<section id="'+id+'"><h2>'+title+'</h2><p>'+text+'</p></section>'
def generate():
 liftit=intro('operacion','Primero, entender el servicio.','Una lectura de operación conecta tres preguntas: dónde se mueven los pedidos, qué registros conviene revisar y qué capacidad queda. Esta composición usa datos ficticios y componentes de ejemplo; no representa una operación real de Liftit.')
 liftit+='<p>Liftit combina tecnología para transporte, asignación y trazabilidad de entregas. <a href="https://liftit.co/es/index.html">Conocer el servicio de Liftit</a>.</p>'
 liftit+=intro('cobertura','Dónde mirar','Selecciona un vehículo, alterna Colombia y el globo, y reproduce el corte de ejemplo. Las ciudades tienen nombres y las rutas son esquemáticas; la animación no representa GPS ni velocidad real.')+recipe('globo-flota')+recipe('ficha-entrega')
 liftit+=intro('registros','Del territorio al registro','Busca, filtra, agrupa u ordena la tabla. Los controles ayudan a explorar una muestra; no conectan un sistema de producción.')+recipe('cola-novedades')
 liftit+=intro('capacidad','La capacidad necesita un denominador','La escena permite comparar capacidad y ocupación con su tabla textual. Usa siempre la misma unidad y fecha de corte.')+recipe('almacen')
 liftit+=intro('mapa-plano','El corte también se puede leer en plano','La misma familia conserva una vista SVG para comparar volumen. Aquí los viajes pertenecen a otro ejemplo de agregados; no equivalen a los tres vehículos anteriores.')+recipe('mapa-rutas')
 liftit+=intro('limite','Qué decidir después','Antes de atribuir una mejora al servicio, confirma el período, la fuente y si los intentos fallidos están incluidos. El tema usa Ribbon #465EFF y Bay #2B3492 del frontend LMS, con su isotipo original. Las combinaciones tipográficas siguen siendo las de Bottifact. <a href="examples/generated/brands.html#marca-liftit">Ver fuentes y colores de marca</a>.')
 blue=intro('plano','Un plano para entender la confirmación.','Especificación conceptual: crear, revisar y confirmar. La cuadrícula da carácter al documento; las distancias del dibujo no representan duración ni cantidad. Las notas numeradas expresan el contrato de cada paso.')+recipe('anotaciones')
 blue+=intro('contrato','Las decisiones del diseño','Compara el estado anterior y el propuesto. La existencia de una interfaz no demuestra que la tarea sea más fácil.')+recipe('antes-despues')
 blue+=intro('recorrido','La propuesta se puede probar','El visor admite HTML declarativo local. Alterna tamaño, proporción y orientación; la vista conserva sus píxeles CSS y sus límites están escritos.')+recipe('visor')
 blue+=intro('historia','Cómo llegamos aquí','Una cronología comunica hitos; no usa la distancia vertical como escala temporal.')+recipe('trayectoria')
 hack=intro('runbook','Leer el contrato antes de ejecutar.','Runbook ilustrativo para revisar un resumen de registros. El código explica una función; la terminal es evidencia estática. Los ejemplos no ejecutan comandos sobre tu equipo.')
 hack+=intro('implementacion','La implementación mínima','Las líneas destacadas nombran el total y el promedio. Una entrada vacía conserva total cero y promedio ausente; no fabrica una observación.')+recipe('codigo-lineas')
 hack+=intro('salida','Una salida que se puede copiar','Usa la terminal para mostrar texto exacto, unidades y contexto. El botón copia la salida sin añadir números de línea.')+recipe('terminal')
 hack+=intro('variantes','El mismo argumento, varios lenguajes','Las pestañas agrupan ejemplos relacionados. No sustituyen capítulos con preguntas distintas.')+recipe('codigo-poliglota')
 hack+=intro('recuperar','Fallos y límites visibles','Un aviso tiene significado escrito y un icono; el color acompaña el estado. La animación se cancela con movimiento reducido.')+recipe('avisos-animados')
 for key,title,style,content in [('liftit','Liftit · Lectura de operación','sobrio',liftit),('blueprint','Blueprint · Plano de una confirmación','tecnico',blue),('hacker','Hacker · Contrato, código y evidencia','tecnico',hack)]:
  (ROOT/'examples/content'/('theme-'+key+'.html')).write_text(content+'\n')
  (ROOT/'examples/generated'/(key+'.html')).write_text(build(title,[{'id':'contenido','titulo':title,'html':content}],brand='nota',theme=key,style=style))
 print('Generados examples/generated/liftit.html, examples/generated/blueprint.html y examples/generated/hacker.html')
if __name__=='__main__':generate()
