"""Clasificación local explicable y relaciones limitadas a documentos autorizados.

No interpreta comentarios, código ni instrucciones de documentos. Las reglas no
son un modelo semántico: cada etiqueta indica los términos que la originaron.
"""
from functools import lru_cache
import json
import re
from portal.search import normalized

RULES = {
    'logística': ('Operaciones', ('logistica','entregas','flota','despacho','ultima milla','rutas')),
    'finanzas': ('Finanzas', ('finanzas','ingresos','margen','costos','flujo de caja','presupuesto','facturacion')),
    'ingeniería': ('Tecnología', ('arquitectura','ingenieria','repositorio','despliegue','api','backend','frontend')),
    'producto': ('Producto', ('producto','prototipo','experiencia de usuario','usabilidad','roadmap')),
    'estrategia': ('Dirección', ('estrategia','prioridades','objetivos','decision','decisiones','plan de trabajo')),
    'personas': ('Equipo', ('contratacion','equipo','liderazgo','desempeno','organizacion','onboarding')),
    'datos': ('Datos', ('analitica','metricas','indicadores','dataset','sql','dashboard')),
    'seguridad': ('Tecnología', ('autenticacion','permisos','seguridad','vulnerabilidad','credenciales')),
    'diseño': ('Diseño', ('tipografia','paleta','componentes','sistema de diseno','interfaz')),
    'investigación': ('Investigación', ('investigacion','hipotesis','experimento','hallazgos','entrevistas')),
}


def migrate(db):
    db.execute("CREATE TABLE IF NOT EXISTS knowledge_overrides(artifact TEXT PRIMARY KEY REFERENCES artifacts(id),category TEXT,automatic INTEGER NOT NULL DEFAULT 1)")


@lru_cache(maxsize=512)
def classify(title, body):
    title=normalized(title);body=normalized(body[:150000]);matches=[]
    for tag,(category,terms) in RULES.items():
        evidence=[term for term in terms if re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',body)]
        strong=[term for term in terms if re.search(r'(?<!\w)'+re.escape(term)+r'(?!\w)',title)]
        if strong or len(evidence)>=2:
            matches.append({'tag':tag,'category':category,'evidence':list(dict.fromkeys(strong+evidence)),'score':len(strong)*4+len(evidence)})
    matches.sort(key=lambda m:(-m['score'],m['tag']))
    return matches[:5]


def enrich(db,a,user):
    index=db.execute('SELECT body FROM artifact_fts WHERE artifact=?',(a['id'],)).fetchone()
    body=index['body'] if index else ''
    matches=classify(a['title'],body[:150000])
    override=db.execute('SELECT * FROM knowledge_overrides WHERE artifact=?',(a['id'],)).fetchone()
    automatic=not override or bool(override['automatic'])
    format_category='Biblioteca' if any(w in normalized(a['title']) for w in ('biblioteca','guia de componentes','guia de uso')) else None
    category=(override['category'] if override else None) or (format_category if automatic and format_category else None) or (matches[0]['category'] if automatic and matches else 'Sin clasificar')
    source={}
    if user and a['owner']==user['id']:
        row=db.execute('SELECT source FROM version_meta WHERE version=?',(a['current_version'],)).fetchone()
        source=json.loads(row['source']) if row else {}
    return {'category':category,'category_manual':bool(override and override['category']),
            'automatic':automatic,'auto_tags':[m['tag'] for m in matches] if automatic else [],
            'classification':matches,'source':source,'description':body[:260],
            'reading_minutes':max(1,round(len(body.split())/220))}


def connections(rows):
    """Only caller-authorized rows. Explain every edge; no category-only links."""
    candidates=[]
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            shared=sorted(set(a.get('tags',[])+a.get('auto_tags',[])) & set(b.get('tags',[])+b.get('auto_tags',[])))
            collections=sorted(set(a.get('collections',[])) & set(b.get('collections',[])))
            if not shared and not collections:continue
            reasons=['Colección: '+c for c in collections]+['Tema: '+t for t in shared]
            candidates.append({'source':a['id'],'target':b['id'],'reasons':reasons,'weight':len(collections)*3+len(shared)})
    candidates.sort(key=lambda e:(-e['weight'],e['source'],e['target']))
    # Keep the graph readable: bounded degree, disclosed truncation.
    degree={};selected=[]
    for e in candidates:
        if degree.get(e['source'],0)>=4 or degree.get(e['target'],0)>=4:continue
        selected.append(e)
        for key in ('source','target'):degree[e[key]]=degree.get(e[key],0)+1
    return selected
