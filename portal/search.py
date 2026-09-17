"""Índice local de texto HTML; no ejecuta documentos ni indexa su código oculto."""
import base64
import hashlib
import json
import re
import unicodedata
from html.parser import HTMLParser


class DocumentText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip=[]; self.parts=[]; self.size=0

    def handle_starttag(self, tag, attrs):
        if tag in ('script','style','nav','button','dialog','select','textarea','template'):
            self.skip.append(tag)
        elif tag=='img' and not self.skip:
            self.handle_data(dict(attrs).get('alt',''))

    def handle_endtag(self, tag):
        if self.skip and tag==self.skip[-1]:self.skip.pop()

    def handle_data(self, data):
        if not self.skip and self.size<1000000:
            text=' '.join(data.split())
            if text:self.parts.append(text);self.size+=len(text)+1


def extract_text(source):
    parser=DocumentText();parser.feed(source)
    return ' '.join(parser.parts)[:1000000]


def index_document(db, artifact, content):
    db.execute('DELETE FROM artifact_fts WHERE artifact=?',(artifact['id'],))
    db.execute('INSERT INTO artifact_fts(artifact,version,title,space,body) VALUES(?,?,?,?,?)',
               (artifact['id'],artifact['current_version'],artifact['title'],artifact['space'],extract_text(content)))


def match_query(query):
    words=re.findall(r'\w+',query,flags=re.UNICODE)[:16]
    return ' AND '.join('"'+word[:80]+'"*' for word in words)


def normalized(text):
    return ''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))


def window(rows, params):
    """Cursor por clave estable; las altas nuevas no desplazan páginas existentes."""
    sort=params.get('sort','recent')
    def key(a):
        if sort=='title':return (normalized(a['title']),a['id'])
        if sort=='comments':return (-a['open_comments'],-a['updated'],a['id'])
        return (-a['updated'],a['id'])
    rows=sorted(rows,key=key)
    if 'limit' not in params:return rows,None
    limit=int(params['limit'])
    if not 1<=limit<=60:raise ValueError('Límite inválido.')
    signature=hashlib.sha256(json.dumps({k:params.get(k,'') for k in ['q','view','space','access','sort','document_id']},sort_keys=True).encode()).hexdigest()[:16]
    if params.get('cursor'):
        if len(params['cursor'])>2048:raise ValueError('Cursor inválido.')
        cursor=json.loads(base64.urlsafe_b64decode(params['cursor']).decode())
        if cursor['scope']!=signature:raise ValueError('La búsqueda cambió. Vuelve a empezar.')
        after=tuple(cursor['after'])
        rows=[a for a in rows if key(a)>after]
    selected=rows[:limit]
    cursor=None
    if len(rows)>limit:
        cursor=base64.urlsafe_b64encode(json.dumps({'scope':signature,'after':key(selected[-1])}).encode()).decode()
    return selected,cursor
