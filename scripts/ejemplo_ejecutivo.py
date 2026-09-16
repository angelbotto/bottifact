"""Memo con hechos del registro y perfil editorial compartido por los agentes."""
import json
import re
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
    body = f'''<section id="lectura-ejecutiva"><p class="ceja">Bottifact / memo de trabajo / 15 sep 2026</p>
<h2>Una base común para compartir criterio.</h2>
<p class="bajada">Propongo que cada artefacto permita entender qué cambió, contrastar la evidencia y decidir qué sigue.</p>
<p>Bottifact reúne {count} recetas y {families} familias visuales. Mi prioridad es aprovechar esa biblioteca con una voz consistente: una lectura ejecutiva al inicio, profundidad disponible y una propuesta que se pueda discutir.</p>
<p>El catálogo describe capacidad disponible. Todavía falta demostrar, con encargos comparables por agente, la calidad editorial y el ahorro de trabajo. Esa es la siguiente prueba que propongo.</p>
<p class="procedencia">Corte del catálogo: versión {escape(version['version'])}. Fuentes: <a href="registro.json">registro de componentes</a> y <a href="VERSION.json">versión del sistema</a>. Propuesta de trabajo; no registra aprobación ni asignaciones.</p></section>
<section class="ancho" id="balance"><h2>Highlights y lowlights</h2>
<div class="cards-trazadas cards-abiertas marco-difuso">
<a href="#evidencia" data-audio-hover><h3>{count} recetas disponibles</h3><p>El registro reúne piezas de lectura, evidencia y revisión. La guía permite consultar su HTML y sus límites.</p><span class="procedencia">HIGHLIGHT · inventario verificable</span></a>
<a href="temas.html" data-audio-hover><h3>{families} familias, {version['paletas']} paletas</h3><p>La identidad visual y el modo claro, oscuro o sistema se eligen por separado.</p><span class="procedencia">HIGHLIGHT · VERSION.json</span></a>
<a href="instalacion.md" data-audio-hover><h3>Una entrada para tres agentes</h3><p>Claude, Codex y Hermes pueden usar el mismo paquete y las mismas instrucciones.</p><span class="procedencia">HIGHLIGHT · compatibilidad de formato</span></a>
<a href="colaboracion.md" data-audio-hover><h3>Revisión todavía local</h3><p>Los comentarios se intercambian por archivo. No hay sincronización entre equipos ni identidad autenticada.</p><span class="procedencia">LOWLIGHT · límite de colaboración</span></a>
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
