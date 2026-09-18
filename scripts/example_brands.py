"""Tres identidades verificables y dos composiciones adicionales por caso de uso."""
from html import escape
from contract_artifact import ROOT, build, recipe
from brands import BRANDS, logo
from example_executive import document


def intro(id, title, text):
    return '<section id="'+id+'"><h2>'+title+'</h2><p>'+text+'</p></section>'


def generate():
    overview = intro('identidades', 'Tres marcas. La misma base de lectura.', 'Logos extraídos de los repositorios y paletas adaptadas a documentos. Cada identidad conserva Claro, Oscuro y Sistema, comentarios y ayudas de lectura. Las muestras de color muestran los valores originales; el texto y las gráficas usan variantes legibles.')
    for key, brand in BRANDS.items():
        overview += '<section class="ancho" id="marca-'+key+'"><h2>'+escape(brand['nombre'])+'</h2><a aria-label="Ver el artefacto '+escape(brand['nombre'])+'" href="'+key+'.html">'+logo(key)+'</a><div class="marca-muestras">'
        overview += ''.join('<span><i style="--muestra:'+value+'" aria-hidden="true"></i>'+escape(name)+' · '+value+'</span>' for name,value in brand['colores'].items())
        overview += '</div><p>'+escape(brand['criterio'])+'</p><p><a href="'+brand['fuente_color']+'">Tokens del repositorio</a> · <a href="'+brand['origen_logo']+'">Logo de origen</a> · <a href="'+key+'.html">Abrir el artefacto</a></p></section>'
    (ROOT/'examples/generated/brands.html').write_text(build('Margen · Identidades de marca', [{'id':'marcas','titulo':'Liftit, Tikin y Catabum','html':overview},{'id':'uso','titulo':'Uso y actualización','html':document('docs/brands.md','marcas-uso')}], description='Identidad trazable para documentos que se pueden compartir.', document_id='bottifact-marcas', theme='editorial', mode='system'))
    tikin = intro('lectura', 'Primero, entender el movimiento.', 'Propongo leer el corte financiero desde el saldo, sus movimientos y las excepciones que necesitan explicación. Esta composición es una muestra de la biblioteca: todas las cifras son ilustrativas y cada pieza tiene su propio conjunto de datos. No representa actividad de Tikin.')
    tikin += intro('movimientos', 'Del saldo al cambio', 'La cascada permite seguir entradas y salidas. Antes de usarla con información real, quiero confirmar moneda, período y qué partidas componen el cierre.')+recipe('cascada')
    tikin += recipe('apuntes')
    tikin += intro('conciliar', 'La diferencia debe poder explicarse', 'Una conciliación necesita dos fuentes comparables. Aquí la tabla permite explorar un ejemplo; una coincidencia en el total no prueba que cada registro sea correcto.')+recipe('conciliacion')
    tikin += intro('criterio', 'Conservar el razonamiento de la decisión', 'Una propuesta debe dejar visibles su fundamento, alternativas y condiciones de revisión. La siguiente ficha muestra la estructura con un ejemplo de producto, no una decisión aprobada en Tikin.')+recipe('decision')
    tikin += '<p class="procedencia">Identidad: blanco, negro y rojo; logo original de la landing. <a href="examples/generated/brands.html#marca-tikin">Ver colores originales, fuentes y límites</a>.</p>'
    catabum = intro('lectura', 'Entender qué trae de vuelta a la comunidad.', 'Quiero separar participación, avance y recurrencia antes de atribuir un cambio a una campaña. Esta composición usa datos ficticios de la biblioteca: las piezas son muestras independientes, no un único embudo ni resultados de Catabum.')
    catabum += intro('recurrencia', 'Volver importa tanto como llegar', 'Las cohortes permiten comparar grupos que comenzaron en momentos distintos. La lectura necesita población inicial, ventana de retorno y una definición estable de actividad.')+recipe('cohortes')
    catabum += recipe('apuntes')
    catabum += intro('conversion', 'Mirar en qué paso se pierde participación', 'El embudo conserva el número de casos por etapa. Las diferencias entre etapas muestran dónde investigar; no prueban la causa del abandono.')+recipe('embudo')
    catabum += intro('seguimiento', 'Una acción necesita contexto', 'La actividad registrada ayuda a narrar continuidad. No equivale a crecimiento ni calidad. Este calendario pertenece a un ejemplo separado de las cohortes anteriores.')+recipe('calendario')
    catabum += '<p class="procedencia">Identidad: tokens de la app y logo compartido. El modo claro es una adaptación para lectura. <a href="examples/generated/brands.html#marca-catabum">Ver la procedencia</a>.</p>'
    for key, title, content in [('tikin','Tikin · Lectura financiera',tikin),('catabum','Catabum · Lectura de comunidad',catabum)]:
        (ROOT/'examples/content'/('theme-'+key+'.html')).write_text(content+'\n')
        (ROOT/'examples/generated'/(key+'.html')).write_text(build(title,[{'id':'contenido','titulo':title,'html':content}],theme=key,marca=key,mode='system',style='sobrio',document_id='bottifact-'+key))
    print('Generados examples/generated/brands.html, examples/generated/tikin.html y examples/generated/catabum.html con logos incrustados.')
