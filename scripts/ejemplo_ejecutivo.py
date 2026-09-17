"""Memo con hechos del registro y perfil editorial compartido por los agentes."""
import json
import re
from collections import Counter
from html import escape
from contrato_artefacto import ROOT, build, recipe
from guia import prose


def document(filename, prefix):
    source = (ROOT / filename).read_text().split('\n', 1)[1]
    parts = re.split(r'^## (.+)\n', source, flags=re.M)
    body = prose(parts[0])
    for n in range(1, len(parts), 2):
        body += f'<section id="{prefix}-{n}"><h2>{escape(parts[n])}</h2></section>'
        for block in parts[n + 1].strip().split('\n\n'):
            rendered = prose(block)
            if block.startswith('|'):
                rendered = '<figure class="ancho marco-difuso">' + rendered + '</figure>'
            body += rendered
    return body


def generate():
    version = json.loads((ROOT / 'VERSION.json').read_text())
    registry = json.loads((ROOT / 'registro.json').read_text())['componentes']
    count, families = len(registry), len(version['temas'])
    chapters = Counter(item['capitulo'] for item in registry)
    labels = {'graficas': 'Gráficas', 'lectura': 'Lectura', 'reportes': 'Reportes', 'publicaciones': 'Publicaciones', 'configuracion': 'Configuración', 'expresion': 'Expresión', 'tablas': 'Tablas', 'prototipos': 'Prototipos'}
    body = f'''<section id="lectura-ejecutiva"><p class="ceja">Bottifact / memo de trabajo / 15 sep 2026</p>
<h2>Una base común para compartir criterio.</h2>
<p class="bajada">Propongo que cada artefacto permita entender qué cambió, contrastar la evidencia y decidir qué sigue.</p>
<p>Bottifact reúne {count} recetas y {families} familias visuales. Mi prioridad es aprovechar esa biblioteca con una voz consistente: una lectura ejecutiva al inicio, profundidad disponible y una propuesta que se pueda discutir.</p>
<p>El catálogo describe capacidad disponible. Todavía falta demostrar, con encargos comparables por agente, la calidad editorial y el ahorro de trabajo. Esa es la siguiente prueba que propongo.</p>
<p class="procedencia">Corte del catálogo: versión {escape(version['version'])}. Fuentes: <a href="registro.json">registro de componentes</a> y <a href="VERSION.json">versión del sistema</a>. Propuesta de trabajo; no registra aprobación ni asignaciones.</p></section>
<section class="ancho" id="balance"><h2>Highlights y lowlights</h2>
<div class="cards-trazadas cards-abiertas">
<a href="#evidencia" data-audio-hover><h3>{count} recetas disponibles</h3><p>El registro reúne piezas de lectura, evidencia y revisión. La guía permite consultar su HTML y sus límites.</p><span class="procedencia">HIGHLIGHT · inventario verificable</span></a>
<a href="temas.html" data-audio-hover><h3>{families} familias, {version['paletas']} paletas</h3><p>La identidad visual y el modo claro, oscuro o sistema se eligen por separado.</p><span class="procedencia">HIGHLIGHT · VERSION.json</span></a>
<a href="instalacion.md" data-audio-hover><h3>Una entrada para tres agentes</h3><p>Claude, Codex y Hermes pueden usar el mismo paquete y las mismas instrucciones.</p><span class="procedencia">HIGHLIGHT · compatibilidad de formato</span></a>
<a href="colaboracion.md" data-audio-hover><h3>Ingreso de invitados por verificar</h3><p>El dominio público ya está activo y la revisión conectada reside en el NAS. Falta probar la recepción real del código de acceso con otra persona.</p><span class="procedencia">LOWLIGHT · verificación externa pendiente</span></a>
<a href="evaluacion-skill.md" data-audio-hover><h3>Falta evaluar la voz por agente</h3><p>Una instalación válida no demuestra que los tres agentes entreguen textos equivalentes.</p><span class="procedencia">LOWLIGHT · prueba pendiente</span></a>
<a href="#metodo" data-audio-hover><h3>Impacto aún sin medir</h3><p>No hay aquí una medición de adopción, tiempo ahorrado o calidad de decisiones.</p><span class="procedencia">LOWLIGHT · vacío de evidencia</span></a>
</div></section>'''
    notes = recipe('apuntes')
    for key in ['apuntes-ejemplo', 'apunte-izquierdo', 'apunte-derecho']:
        notes = notes.replace(key, 'ejecutivo-' + key)
    notes = notes.replace('Una decisión necesita contexto.', 'La amplitud necesita intención.')
    notes = notes.replace('La evidencia sirve cuando nos ayuda a <span data-subrayar="referencia">decidir mejor</span>. Un reporte puede dejar una pregunta breve al margen sin interrumpir el argumento.', 'Quiero usar más piezas donde ayuden a <span data-subrayar="referencia">decidir mejor</span>. El catálogo completo está disponible; cada documento necesita su propia selección.')
    notes = notes.replace('menos ruido, más criterio.', '¿qué decisión facilita?')
    notes = notes.replace('Explicar también es editar.', 'La cifra necesita un límite.')
    notes = notes.replace('Antes de agregar otra gráfica, prueba a <span data-subrayar="referencia">quitar lo que sobra</span>. La anotación acompaña al párrafo; el subrayado se dibuja cuando aparece.', 'El número de recetas indica <span data-subrayar="referencia">capacidad disponible</span>. No permite concluir que un equipo decide mejor o produce más rápido.')
    notes = re.sub(r'<p>Corrección ilustrativa:.*?</p>', '', notes)
    notes = notes.replace('¿se entiende sin explicarlo?', 'falta medir el resultado.')
    body += notes
    body += '<section id="catalogo-visual"><h2>La evidencia tiene más de una forma.</h2><p>El capítulo de gráficas reúne '+str(chapters['graficas'])+' recetas. Quiero aprovechar esa variedad cuando exista una pregunta que se pueda responder visualmente. El inventario permite ver dónde hay más opciones; no expresa prioridad ni tiempo invertido.</p></section>'
    def chart(key, attr, title, rows, caption):
        source = recipe(key)
        source = re.sub(r' id="[^"]+"', ' id="ejecutivo-'+attr+'"', source, count=1)
        source = re.sub(r'data-unidad="[^"]+"', 'data-unidad="recetas"', source)
        source = re.sub(r'<caption>.*?</caption>', '<caption>'+escape(title)+'</caption>', source)
        source = re.sub(r'<summary>.*?</summary>', '<summary>Consultar los datos del catálogo</summary>', source)
        source = re.sub(r'aria-label="[^"]+"', 'aria-label="Datos del catálogo, tabla desplazable"', source)
        source = re.sub(r'<thead>.*?</thead>', '<thead><tr><th scope="col">Categoría</th><th scope="col">Recetas</th></tr></thead>', source, flags=re.S)
        cells = ''.join('<tr><th scope="row">'+escape(label)+'</th><td data-valor="'+str(value)+'">'+str(value)+'</td></tr>' for label,value in rows)
        source = re.sub(r'<tbody>.*?</tbody>', '<tbody>'+cells+'</tbody>', source, flags=re.S)
        source = re.sub(r'<figcaption>.*?</figcaption>', '<figcaption>'+caption+'</figcaption>', source, flags=re.S)
        return source
    body += chart('barras', 'capitulos', 'Recetas por capítulo', [(labels[key], value) for key,value in chapters.most_common()], 'Fuente: <a href="registro.json">registro.json</a>. '+str(count)+' recetas, una entrada por ID; corte de esta versión. Unidad: recetas. La longitud compara cantidades por capítulo.')
    groups = [('Gráficas, reportes y tablas',sum(chapters[k] for k in ['graficas','reportes','tablas'])),('Lectura y expresión',chapters['lectura']+chapters['expresion']),('Publicaciones',chapters['publicaciones']),('Configuración',chapters['configuracion']),('Prototipos',chapters['prototipos'])]
    data_count = groups[0][1]
    body += '<section id="peso-evidencia"><h2>'+str(data_count)+' de '+str(count)+' recetas para explorar evidencia.</h2><p>Gráficas, reportes y tablas suman '+str(data_count)+' entradas: '+format(100*data_count/count,'.1f').replace('.',',')+' % del inventario. Es una agrupación editorial de tres capítulos; cada receta se cuenta una sola vez. Las piezas de lectura y expresión ayudan a conectar esa evidencia con el argumento.</p></section>'
    body += chart('torta', 'composicion', 'Composición del catálogo', groups, 'Fuente: <a href="registro.json">registro.json</a>. Denominador: '+str(count)+' recetas. Agrupación: gráficas + reportes + tablas; lectura + expresión; los demás capítulos conservan su categoría. Cambia entre torta y donut para consultar las mismas cantidades.')
    more_notes = notes.replace('ejecutivo-apunt', 'ejecutivo-datos-apunt')
    for old,new in [
        ('La amplitud necesita intención.','Comparar antes de concluir.'),
        ('Quiero usar más piezas donde ayuden a <span data-subrayar="referencia">decidir mejor</span>. El catálogo completo está disponible; cada documento necesita su propia selección.','Las barras me permiten comparar capítulos. La torta responde cuánto representa una agrupación dentro del <span data-subrayar="referencia">mismo total</span>. Ambas parten del registro; la pregunta cambia.'),
        ('¿qué decisión facilita?','mismo dato, otra pregunta.'),
        ('La cifra necesita un límite.','La excepción merece contexto.'),
        ('El número de recetas indica <span data-subrayar="referencia">capacidad disponible</span>. No permite concluir que un equipo decide mejor o produce más rápido.','Quiero que la revisión permita <span data-subrayar="referencia">discutir una afirmación</span>. Un comentario sobre una cifra debe conservar la fuente, el fragmento y la pregunta pendiente, para que el equipo sepa qué contrastar.'),
        ('falta medir el resultado.','¿qué cambiaría mi lectura?')]: more_notes=more_notes.replace(old,new)
    body += more_notes
    # La tabla conserva filtros, agrupación y ordenación del contrato existente.
    table = recipe('explorador').replace('explorador-ejemplo', 'evidencia')
    table = table.replace('Explorar el registro', 'Qué está disponible y qué falta demostrar')
    table = table.replace('Seis registros ficticios. Ordena por encabezado, filtra y agrupa sin perder el detalle.', 'Seis observaciones sobre el sistema. Filtra por estado o agrupa por ámbito para separar capacidad y validación.')
    for old, new in [('Equipo', 'Ámbito'), ('Importe COP', 'Fuente'), ('En revisión', 'Pendiente'), ('Confirmado', 'Disponible'), ('6 registros de ejemplo.', '6 observaciones del sistema.'), ('Movimientos ilustrativos · importes en COP', 'Estado de Bottifact · corte de esta versión')]:
        table = table.replace(old, new)
    rows = [
        ('Recetas', 'Biblioteca', 'Disponible', 'registro.json'),
        ('Familias y modos', 'Biblioteca', 'Disponible', 'temas.md'),
        ('Formato de tres agentes', 'Distribución', 'Disponible', 'instalacion.md'),
        ('Calidad editorial por agente', 'Evaluación', 'Pendiente', 'evaluacion-skill.md'),
        ('Sincronización de comentarios', 'Colaboración', 'Pendiente', 'colaboracion.md'),
        ('Impacto en trabajo del equipo', 'Evaluación', 'Pendiente', 'voz-ejecutiva.md'),
    ]
    tbody = ''.join('<tr><th scope="row">' + escape(a) + '</th><td>' + escape(b) + '</td><td>' + escape(c) + '</td><td><a href="' + d + '">' + d + '</a></td></tr>' for a, b, c, d in rows)
    table = re.sub(r'<tbody>.*?</tbody>', '<tbody>' + tbody + '</tbody>', table, flags=re.S)
    body += table
    team_notes = notes.replace('ejecutivo-apunt','ejecutivo-equipo-apunt')
    for old,new in [
        ('La amplitud necesita intención.','Que el equipo encuentre su contexto.'),
        ('Quiero usar más piezas donde ayuden a <span data-subrayar="referencia">decidir mejor</span>. El catálogo completo está disponible; cada documento necesita su propia selección.','De la lectura de <em>Scaling People</em> tomo un criterio: reunir <span data-subrayar="referencia">propósito y responsabilidades</span> con métricas, riesgos y dependencias. El acuerdo necesita ser consultable. <a href="https://stripe.com/guides/atlas/creating-your-founding-documents">Extracto de Claire Hughes Johnson</a>.'),
        ('¿qué decisión facilita?','¿qué espera el equipo?'),
        ('La cifra necesita un límite.','Probar también cambia el documento.'),
        ('El número de recetas indica <span data-subrayar="referencia">capacidad disponible</span>. No permite concluir que un equipo decide mejor o produce más rápido.','Quiero recoger los ajustes junto al contenido y <span data-subrayar="referencia">volver a comprobar</span> los puntos corregidos. La base conserva el mismo ID del documento para mantener el contexto de la revisión.'),
        ('falta medir el resultado.','conservar el hilo.')]: team_notes=team_notes.replace(old,new)
    body += team_notes
    body += '''<section id="propuesta"><h2>Propongo estandarizar la voz y comprobar el resultado.</h2></section>
<aside class="pieza ficha-decision" aria-labelledby="decision-voz"><p class="ceja">Propuesta / pendiente de evaluación</p><h3 id="decision-voz">Una guía compartida, con ejemplos y criterios observables</h3><dl>
<div><dt>Por qué</dt><dd>El mismo perfil editorial puede acompañar la biblioteca en los tres agentes sin mantener instrucciones divergentes.</dd></div>
<div><dt>Alternativa</dt><dd>Personalizar instrucciones separadas por agente. Permite ajustes particulares, pero multiplica las versiones que hay que mantener.</dd></div>
<div><dt>Qué falta comprobar</dt><dd>Que cada agente use evidencia real, escriba desde la voz del autor y aproveche las piezas pertinentes sin perder los controles estándar.</dd></div>
<div><dt>Cuándo revisarla</dt><dd>Si un encargo real necesita reglas incompatibles con el perfil común o produce omisiones recurrentes.</dd></div>
</dl></aside>
<aside class="aviso"><span class="num" aria-hidden="true">!</span><div><p class="titulo">Una propuesta no es un acuerdo.</p><p>Los próximos pasos no tienen responsable ni fecha asignados. Quiero definirlos con el contexto de ejecución, sin dar por aprobado un compromiso.</p></div></aside>
<section id="pasos"><h2>La siguiente comprobación</h2><ol>
<li><strong>Preparar un encargo común.</strong> Mismos datos de entrada, destinatario y decisión esperada para los tres agentes.</li>
<li><strong>Generar y revisar.</strong> Contrastar fuentes, voz, cobertura útil de componentes, comentarios y apariencia. Registrar agente, versión y salida.</li>
<li><strong>Corregir la guía con los fallos observados.</strong> Una mejora se acepta cuando el caso vuelve a producir un documento correcto.</li>
</ol><p>Responsable y fecha: por definir. Criterios de revisión: <a href="evaluacion-skill.md">evaluación del skill</a>.</p></section>
<section id="metodo"><h2>Alcance de esta lectura</h2><details class="metodologia"><summary>Fuentes, método y exclusiones</summary><dl class="nota-glosario">
<div><dt>Inventario</dt><dd>Conteo de entradas en registro.json; familias y paletas declaradas en VERSION.json. No son métricas de productividad.</dd></div>
<div><dt>Capacidades y límites</dt><dd>Instalación y colaboración documentadas en esta versión. La evaluación con cada agente se registra por separado.</dd></div>
<div><dt>Interpretación</dt><dd>Priorizar una voz común y una prueba comparativa es una propuesta editorial, no un efecto demostrado.</dd></div>
<div><dt>Exclusiones</dt><dd>No hay cifras de negocio, resultados de clientes, calendario comprometido ni ejecución remota en otro equipo.</dd></div>
</dl></details></section>
<nav class="biblioteca-rutas ancho" aria-label="Continuar"><a href="#perfil"><strong>Cómo quiero comunicar</strong><small>Voz, estructura, datos y componentes.</small></a><a href="#fuentes"><strong>Lecturas y alcance</strong><small>Fuentes primarias y adaptación del criterio.</small></a><a href="guia.html"><strong>Biblioteca completa</strong><small>Consultar todas las recetas.</small></a></nav>'''
    pages = [
        {'id': 'memo', 'titulo': 'Mi lectura', 'html': body},
        {'id': 'perfil', 'titulo': 'Guía de comunicación', 'html': document('voz-ejecutiva.md', 'perfil')},
        {'id': 'fuentes', 'titulo': 'Referencias', 'html': document('referencias-comunicacion.md', 'fuentes')},
    ]
    (ROOT / 'ejecutivo.html').write_text(build('Bottifact · Comunicar para decidir', pages, description='Voz ejecutiva, evidencia y una biblioteca al servicio del argumento.', theme='editorial', mode='system', document_id='bottifact-voz-ejecutiva'))


if __name__ == '__main__':
    generate()
