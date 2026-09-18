"""Synthetic operational scenarios for the unified table and reader controls."""

from pathlib import Path
from html import escape
import base64
from contract_artifact import build

ROOT = Path(__file__).resolve().parents[1]


def rich_cell(key, row, column, value, index):
    """Synthetic rich content; scalar attributes remain authoritative for queries."""
    text = escape(str(value))
    if key != "liftit-deliveries":
        return text
    names = ["Ana Rivera", "Daniel Torres", "Lucía Gómez"]
    colors = ["amber", "violet", "mint"]
    def image(name):
        data = (ROOT / "packages/core/assets/table-fixtures" / name).read_bytes()
        return "data:image/svg+xml;base64," + base64.b64encode(data).decode()
    if column == 0:
        return (f'<strong>{text}</strong><span class="bf-record-subtitle">{escape(row[1])} · distribución</span>'
                f'<details class="bf-inline-detail"><summary>Ver entrega</summary><div class="bf-detail-grid">'
                f'<section class="bf-detail-card"><h4>Recorrido</h4><p>{escape(row[1])} · circuito de distribución.</p><small>Ejemplo sin GPS ni conexión operativa.</small></section>'
                f'<section class="bf-detail-card"><h4>Seguimiento</h4><p>Responsable: {names[index % 3]}.</p><p>Validar la evidencia antes de cerrar la entrega.</p></section></div></details>')
    if column == 2:
        tone = {"Entregado": "success", "En ruta": "info", "Excepción": "danger"}[value]
        return f'<span class="bf-status" data-tone="{tone}"><span aria-hidden="true"></span>{text}</span>'
    if column == 4:
        return f'<span class="bf-person"><span class="bf-avatar"><img src="{image("avatar-" + colors[index % 3] + ".svg")}" alt="" width="30" height="30"></span><span><strong>{text}</strong><small>Operación · persona ficticia</small></span></span>'
    if column == 5:
        return f'<span class="bf-media"><img src="{image("cargo.svg")}" alt="Ilustración de una caja" width="64" height="44"><span><strong>{text}</strong><small>Manifiesto ilustrativo</small></span></span>'
    return text


def table(key, title, headers, rows, unit):
    head = "".join(
        '<th scope="col" data-tipo="'
        + ("numero" if i == 3 else "texto")
        + '"><button type="button" data-orden-col="'
        + str(i)
        + '" data-direccion="1">'
        + escape(h)
        + " <span data-indicador-orden>↕</span></button></th>"
        for i, h in enumerate(headers)
    )
    body = "".join(
        '<tr id="'
        + key
        + "-"
        + str(i + 1)
        + '" data-row-id="'
        + key
        + "-"
        + str(i + 1)
        + '">'
        + "".join(
            "<td"
            + (' data-valor="' + escape(str(v), quote=True) + '"')
            + ">"
            + rich_cell(key, row, j, v, i)
            + "</td>"
            for j, v in enumerate(row)
        )
        + "</tr>"
        for i, row in enumerate(rows)
    )
    return (
        '<section class="pieza amplio" id="'
        + key
        + '" data-explorador data-unidad="'
        + unit
        + '"><h3>'
        + title
        + '</h3><form class="tabla-herramientas"><label>Buscar<input type="search" name="buscar"></label><label>Agrupar<select name="grupo"><option value="">Sin grupo</option><option value="1">'
        + headers[1]
        + '</option><option value="2">'
        + headers[2]
        + "</option></select></label><details><summary>Columnas</summary>"
        + "".join(
            '<label><input type="checkbox" data-columna="'
            + str(i)
            + '" checked>'
            + escape(h)
            + "</label>"
            for i, h in enumerate(headers)
        )
        + '</details><button type="reset">Restablecer</button></form><p data-explorador-estado role="status"></p><div class="tabla-caja" tabindex="0" role="region" aria-label="'
        + title
        + '"><table><caption>Seis registros ilustrativos · sin conexión a operación real</caption><thead><tr>'
        + head
        + "</tr></thead><tbody>"
        + body
        + '</tbody></table></div><p class="procedencia">Fuente: fixture público de Margen. Los totales corresponden al filtro completo; la selección puede incluir registros ocultos.</p></section>'
    )


def generate():
    intro = """<section id="decision"><p class="ceja">Margen / guía de trabajo</p><h2>Leer, contrastar y devolver contexto.</h2><p>La prioridad es reducir el trabajo entre encontrar un documento y preparar su siguiente versión. Esta guía permite probar las tablas con datos ficticios y entender qué queda guardado en el archivo, en el navegador o en la cuenta.</p><p>La barra inferior reúne Apariencia, Comentar, Comentarios y Compartir. Pasa el cursor o enfoca un icono para identificarlo; también puedes recorrer las herramientas con las flechas del teclado. El contador muestra los hilos abiertos. Al escribir eliges si el comentario es compartido o privado. Comentarios reúne las referencias y la búsqueda; Compartir reúne enlace, acceso y gestión. El tema elegido por un lector conserva el diseño publicado.</p></section>"""
    scenarios = [
        (
            "liftit-deliveries",
            "Liftit · entregas y excepciones",
            ["Entrega", "Ciudad", "Estado", "Viajes"],
            [
                ["L-101", "Bogotá", "Entregado", 18],
                ["L-102", "Medellín", "En ruta", 12],
                ["L-103", "Cali", "Excepción", 4],
                ["L-104", "Bogotá", "En ruta", 11],
                ["L-105", "Cali", "Entregado", 9],
                ["L-106", "Medellín", "Excepción", 2],
            ],
            "viajes",
        ),
        (
            "tikin-reconciliation",
            "Tikin · conciliación financiera",
            ["Registro", "Cuenta", "Estado", "Importe COP"],
            [
                ["T-101", "Recaudo", "Conciliado", 1200000],
                ["T-102", "Operación", "Pendiente", 420000],
                ["T-103", "Recaudo", "Diferencia", 80000],
                ["T-104", "Operación", "Conciliado", 620000],
                ["T-105", "Recaudo", "Pendiente", 210000],
                ["T-106", "Operación", "Diferencia", -30000],
            ],
            "COP",
        ),
        (
            "catabum-decisions",
            "Catabum · decisiones y capacidad",
            ["Decisión", "Proyecto", "Estado", "Horas"],
            [
                ["C-101", "Descubrimiento", "Aprobada", 12],
                ["C-102", "Prototipo", "Por revisar", 8],
                ["C-103", "Entrega", "Bloqueada", 5],
                ["C-104", "Prototipo", "Aprobada", 16],
                ["C-105", "Entrega", "Por revisar", 10],
                ["C-106", "Descubrimiento", "Bloqueada", 3],
            ],
            "horas",
        ),
    ]
    body = intro
    for key, title, headers, rows, unit in scenarios:
        if key == "liftit-deliveries":
            headers = headers + ["Responsable", "Carga"]
            rows = [row + [["Ana Rivera", "Daniel Torres", "Lucía Gómez"][i % 3], "Mercancía embalada"] for i, row in enumerate(rows)]
        body += (
            '<section id="probar-'
            + key
            + '"><h2>'
            + title
            + "</h2><p>Elige Tabla para comparar columnas, Lista para recorrer registros, Fichas para leer cada uno y Tablero para revisar estados o categorías. En Filtros puedes elegir varios valores, combinar condiciones y quitar cada filtro por separado. En Diseño puedes arrastrar las columnas o moverlas con las flechas, ocultarlas, fijarlas y ajustar su ancho. Guarda la configuración en Vistas. En las entregas, Ver entrega abre tarjetas con contexto; las personas e imágenes son ilustrativas.</p></section>"
            + table(key, title, headers, rows, unit)
        )
    body += """<section id="devolver"><h2>De la revisión a la siguiente versión.</h2><ol><li>Dejo el comentario sobre el fragmento que necesita cambiar.</li><li>Abro Revisión → Preparar contexto para IA.</li><li>Elijo hilos y, sólo si hace falta, mis notas privadas y las referencias.</li><li>Reviso el prompt con artefacto, versión, cita, sesión y dispositivo registrados.</li><li>Lo copio a mi agente. Publico la revisión como borrador y comparo antes de reemplazar la versión compartida.</li></ol><p>Copiar no envía instrucciones a una sesión ni resuelve comentarios automáticamente.</p></section><section id="conectar"><h2>Conocimiento que se puede explicar.</h2><p>En la biblioteca, las entidades distinguen empresas, proyectos y temas. Los alias ayudan a buscar; no fusionan empresas. Las relaciones explícitas conservan una cita de la versión que las respalda. Las mesas y tableros son privados: juntar documentos no cambia su audiencia.</p><p>La vista de sesiones agrupa salidas por agente, sesión y dispositivo. No contiene transcripciones importadas.</p></section>"""
    (ROOT / "examples/generated/workbench.html").write_text(
        build(
            "Margen · Trabajar con contexto",
            [{"id": "guia", "titulo": "Trabajar con contexto", "html": body}],
            "Tablas, referencias y revisión con datos sintéticos.",
            theme="linear",
            mode="light",
            document_id="bottifact-workbench-guide",
        )
    )
