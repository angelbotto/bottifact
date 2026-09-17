"""Portal del NAS: autorización en cada lectura/escritura y HTML aislado.

SQLite reside en disco local del NAS, nunca en un montaje SMB/NFS. Un proceso
de aplicación; transacciones y bloqueo cubren cambios de permisos y comentarios.
"""
import hashlib
import json
import os
import re
import secrets
import sqlite3
import threading
import time
import uuid
from urllib.parse import urlsplit
from contextlib import contextmanager
from pathlib import Path

import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response, FileResponse
from portal.auth import mount_auth
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).parent
COOKIE = '__Host-bottifact'
MAX_BODY = 22 * 1024 * 1024
EMAIL = re.compile(r'^[^\s@]{1,64}@[^\s@.]+(?:\.[^\s@.]+)+$')
ID = re.compile(r'^[a-zA-Z0-9_-]{1,120}$')


def admin_emails():
    return [e.strip().lower() for e in os.environ.get("BOTTIFACT_ADMIN_EMAILS", "").split(",") if e.strip()]


def is_admin(user):
    return bool(user and user["verified"] and user.get("email") in admin_emails())


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def clean(value, maximum=200, empty=False):
    if not isinstance(value, str) or len(value) > maximum or (not empty and not value.strip()):
        raise HTTPException(422, 'Texto ausente o demasiado largo.')
    return value.strip()


async def payload(request):
    try:
        value = await request.json()
    except (ValueError, UnicodeError):
        raise HTTPException(422, 'JSON inválido.') from None
    if not isinstance(value, dict):
        raise HTTPException(422, 'Se esperaba un objeto JSON.')
    return value


class Store:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.files = self.root / 'files'
        self.files.mkdir(exist_ok=True, mode=0o700)
        self.lock = threading.RLock()
        with self.db() as db:
            db.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,email TEXT UNIQUE,name TEXT NOT NULL,verified INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS sessions(hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS tokens(hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),label TEXT NOT NULL,created INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS logins(hash TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS artifacts(id TEXT PRIMARY KEY,owner TEXT NOT NULL REFERENCES users(id),title TEXT NOT NULL,
              space TEXT NOT NULL,document_id TEXT NOT NULL,visibility TEXT NOT NULL DEFAULT 'private',
              comments TEXT NOT NULL DEFAULT 'reviewers',guests INTEGER NOT NULL DEFAULT 0,current_version TEXT,updated INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS versions(id TEXT PRIMARY KEY,artifact TEXT NOT NULL REFERENCES artifacts(id),sha TEXT NOT NULL,created INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS grants(artifact TEXT NOT NULL REFERENCES artifacts(id),email TEXT NOT NULL,role TEXT NOT NULL,PRIMARY KEY(artifact,email));
            CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY,artifact TEXT NOT NULL REFERENCES artifacts(id),version TEXT NOT NULL REFERENCES versions(id),
              actor TEXT NOT NULL REFERENCES users(id),request_hash TEXT NOT NULL,event TEXT NOT NULL,time INTEGER NOT NULL);
            CREATE INDEX IF NOT EXISTS events_artifact ON events(artifact,time);
            CREATE TABLE IF NOT EXISTS bookmarks(id TEXT PRIMARY KEY,owner TEXT NOT NULL REFERENCES users(id),title TEXT NOT NULL,url TEXT NOT NULL,space TEXT NOT NULL,created INTEGER NOT NULL,UNIQUE(owner,url));
            CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,actor TEXT NOT NULL,action TEXT NOT NULL,artifact TEXT,at INTEGER NOT NULL);
            ''')

    @contextmanager
    def db(self):
        with self.lock:
            db = sqlite3.connect(self.root / 'bottifact.sqlite3', timeout=30)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA foreign_keys=ON')
            try:
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise
            finally:
                db.close()

    def user(self, email, name):
        email = clean(email, 254).lower()
        aliases = admin_emails()
        if email in aliases: email = aliases[0]
        if not EMAIL.fullmatch(email):
            raise HTTPException(422, 'Correo inválido.')
        with self.db() as db:
            found = db.execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
            if found:
                return dict(found)
            uid = uuid.uuid4().hex
            db.execute('INSERT INTO users VALUES(?,?,?,1)', (uid, email, clean(name, 80)))
            return dict(db.execute('SELECT * FROM users WHERE id=?', (uid,)).fetchone())

    def session(self, user_id):
        token = secrets.token_urlsafe(32)
        with self.db() as db:
            db.execute('DELETE FROM sessions WHERE expires<?', (int(time.time()),))
            db.execute('INSERT INTO sessions VALUES(?,?,?)', (digest(token), user_id, int(time.time()) + 86400 * 14))
        return token

    def token(self, user_id, label='Agente'):
        token = 'bf_' + secrets.token_urlsafe(40)
        with self.db() as db:
            if db.execute('SELECT count(*) FROM tokens WHERE user_id=?',(user_id,)).fetchone()[0]>=50: raise HTTPException(409,'Máximo 50 conexiones por cuenta.')
            db.execute('INSERT INTO tokens VALUES(?,?,?,?)', (digest(token), user_id, label, int(time.time())))
        return token

    def login_once(self, user_id):
        token = secrets.token_urlsafe(40)
        with self.db() as db:
            db.execute('DELETE FROM logins WHERE expires<?', (int(time.time()),))
            db.execute('INSERT INTO logins VALUES(?,?,?)', (digest(token), user_id, int(time.time()) + 300))
        return token


def role(db, artifact, user):
    if not user:
        return None
    if artifact['owner'] == user['id'] or is_admin(user):
        return 'owner'
    grant = db.execute('SELECT role FROM grants WHERE artifact=? AND email=?',
                       (artifact['id'], user.get('email') or '')).fetchone() if user['verified'] else None
    return grant['role'] if grant else None


def permissions(db, artifact, user):
    r = role(db, artifact, user)
    read = bool(r) or artifact['visibility'] in ('public', 'unlisted')
    review = read and (bool(r) or artifact['comments'] == 'readers')
    comment = review and bool(user) and (r in ('owner', 'editor', 'commenter') or
              (r is None and artifact['comments'] == 'readers' and (user['verified'] or artifact['guests'])))
    return {'read': read, 'review': review, 'comment': bool(comment), 'edit': r in ('owner', 'editor'), 'manage': r == 'owner', 'role': r}


def artifact_for(db, aid, user, capability='read'):
    a = db.execute('SELECT * FROM artifacts WHERE id=?', (aid,)).fetchone()
    if not a or not permissions(db, a, user)[capability]:
        raise HTTPException(404, 'Artefacto no disponible para esta cuenta.')
    return dict(a)


def snapshot(db, a):
    return {'format': 'nota-revision', 'version': 2, 'document': a['document_id'],
            'events': [json.loads(x['event']) for x in db.execute('SELECT event FROM events WHERE artifact=? ORDER BY time,id', (a['id'],))]}


def threads(events):
    result = {}
    for e in events:
        if e['kind'] == 'create':
            result[e['thread']] = {**e, 'replies': [], 'resolved': False, 'deleted': False, 'assignee': ''}
        t = result.get(e['thread'])
        if not t:
            continue
        if e['kind'] == 'reply': t['replies'].append(e)
        if e['kind'] == 'edit': t['text'] = e['text']
        if e['kind'] == 'resolve': t['resolved'] = e['resolved']
        if e['kind'] == 'assign': t['assignee'] = e['assignee']
        if e['kind'] == 'delete': t['deleted'] = True
    return [t for t in result.values() if not t['deleted']]


def create_app(data=None, origin=None, issuer=None, audience=None):
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    store = Store(data or os.environ.get('BOTTIFACT_DATA', '/tmp/bottifact-portal'))
    app.state.store = store
    origin = (origin or os.environ.get('BOTTIFACT_ORIGIN', 'https://artifacts.botto.is')).rstrip('/')
    origins = {origin, *filter(None, os.environ.get('BOTTIFACT_EXTRA_ORIGINS', '').split(','))}
    issuer = (issuer or os.environ.get('BOTTIFACT_ISSUER', 'https://bottico.cloudflareaccess.com')).rstrip('/')
    audience = audience or os.environ.get('BOTTIFACT_AUDIENCE', '')
    jwks = jwt.PyJWKClient(issuer + '/cdn-cgi/access/certs', cache_keys=True, lifespan=300)
    rate = {}
    rate_lock = threading.Lock()

    def who(request):
        auth = request.headers.get('authorization', '')
        with store.db() as db:
            if auth.startswith('Bearer '):
                row = db.execute('SELECT u.* FROM tokens t JOIN users u ON u.id=t.user_id WHERE t.hash=?', (digest(auth[7:]),)).fetchone()
                if not row: raise HTTPException(401, 'Conexión del agente inválida o revocada.')
                return {**dict(row), 'agent': True}
            session = request.cookies.get(COOKIE, '')
            row = db.execute('SELECT u.* FROM sessions s JOIN users u ON u.id=s.user_id WHERE s.hash=? AND s.expires>?',
                             (digest(session), int(time.time()))).fetchone() if session else None
            return {**dict(row), 'agent': False} if row else None

    def account(request, browser=False):
        u = who(request)
        if not u or not u['verified']: raise HTTPException(401, 'Inicia sesión con tu correo.')
        if browser and u['agent']: raise HTTPException(403, 'Esta acción requiere tu sesión en el portal.')
        return u

    def set_session(response, uid):
        response.set_cookie(COOKIE, store.session(uid), max_age=86400 * 14, secure=True, httponly=True, samesite='lax', path='/')
        return response

    @app.middleware('http')
    async def guard(request, call_next):
        # Cabeceras y Origin no se aceptan como prueba de identidad.
        if request.method in ('POST', 'PUT', 'DELETE', 'PATCH'):
            auth = request.headers.get('authorization', '')
            if not auth.startswith('Bearer ') and request.headers.get('origin') not in origins:
                return JSONResponse({'detail': 'Origen no permitido.'}, status_code=403)
            try: size = int(request.headers.get('content-length', '0'))
            except ValueError: size = -1
            if size < 0 or size > MAX_BODY: return JSONResponse({'detail':'Tamaño no permitido.'}, status_code=413)
            chunks=[];received=0
            async for chunk in request.stream():
                received+=len(chunk)
                if received>MAX_BODY: return JSONResponse({'detail':'Tamaño no permitido.'},status_code=413)
                chunks.append(chunk)
            request._body=b''.join(chunks)
            # Máximo 90 escrituras/minuto por conexión; sin guardar direcciones en disco.
            key = request.headers.get('cf-connecting-ip') or request.client.host
            now = int(time.time() // 60)
            with rate_lock:
                for old in [k for k, v in rate.items() if v[0] != now]: rate.pop(old, None)
                count = rate.get(key, (now, 0))[1] + 1
                if count > 90 or len(rate) > 10000:
                    return JSONResponse({'detail':'Demasiados cambios. Espera un minuto.'}, status_code=429, headers={'Retry-After':'60'})
                rate[key] = (now, count)
        response = await call_next(request)
        response.headers['Cache-Control'] = 'private, no-store'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['X-Robots-Tag'] = 'noindex, nofollow'
        if 'Content-Security-Policy' not in response.headers:
            response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self' data:; connect-src 'self'; frame-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'"
        return response

    mount_auth(app, store, origin, set_session, payload, clean, EMAIL)

    @app.get('/health')
    def health(): return {'service':'bottifact', 'status':'ok', 'storage':'nas-local'}

    @app.get('/api/session')
    def session(request: Request):
        u = who(request)
        return {'user': {**{k:u[k] for k in ('id','email','name','verified')}, 'admin':is_admin(u)} if u else None}

    @app.post('/api/guest')
    async def guest(request: Request):
        if who(request): raise HTTPException(409, 'Ya tienes una sesión. Ciérrala para cambiar de persona.')
        body = await payload(request)
        aid = clean(body.get('artifact'), 120)
        with store.db() as db:
            a = artifact_for(db, aid, None)
            if not a['guests'] or a['comments'] != 'readers': raise HTTPException(403, 'El autor requiere iniciar sesión para comentar.')
            uid = uuid.uuid4().hex
            db.execute('INSERT INTO users VALUES(?,NULL,?,0)', (uid, clean(body.get('name'), 80)))
        return set_session(JSONResponse({'ok':True}), uid)

    @app.post('/api/logout')
    def logout(request: Request):
        with store.db() as db: db.execute('DELETE FROM sessions WHERE hash=?', (digest(request.cookies.get(COOKIE, '')),))
        response = JSONResponse({'ok':True});response.delete_cookie(COOKIE, path='/', secure=True, httponly=True, samesite='lax')
        return response

    @app.get('/auth/login')
    def login(request: Request):
        if not audience: raise HTTPException(503, 'El acceso por correo está pendiente de configuración.')
        try:
            token = request.headers.get('cf-access-jwt-assertion', '')
            key = jwks.get_signing_key_from_jwt(token).key
            claims = jwt.decode(token, key, algorithms=['RS256'], audience=audience, issuer=issuer,
                                options={'require':['exp','iat','sub','email','iss','aud']}, leeway=15)
            if claims.get('type') != 'app': raise ValueError('Tipo de sesión inválido')
            u = store.user(claims['email'], claims.get('name') or claims['email'].split('@')[0])
        except Exception:
            raise HTTPException(401, 'No pudimos verificar la sesión de correo.') from None
        target = request.query_params.get('next', '/')
        if not re.fullmatch(r'/(?:a/[a-f0-9]{32})?', target): target = '/'
        return set_session(RedirectResponse(target, status_code=303), u['id'])

    @app.get('/auth/bootstrap')
    def bootstrap(request: Request):
        # Sólo puede emitir este enlace de un uso el administrador mediante SSH.
        token = request.query_params.get('code','')
        with store.db() as db:
            found = db.execute('SELECT * FROM logins WHERE hash=? AND expires>?', (digest(token), int(time.time()))).fetchone()
            if not found: raise HTTPException(401, 'Enlace vencido o utilizado.')
            db.execute('DELETE FROM logins WHERE hash=?', (digest(token),))
        return set_session(RedirectResponse('/', status_code=303), found['user_id'])

    @app.post('/api/tokens')
    async def new_token(request: Request):
        u = account(request, True);body = await payload(request)
        return {'token':store.token(u['id'], clean(body.get('label','Agente'),80))}

    @app.get('/api/tokens')
    def tokens(request: Request):
        u = account(request, True)
        with store.db() as db:
            return {'tokens':[dict(r) for r in db.execute('SELECT hash,label,created FROM tokens WHERE user_id=?', (u['id'],))]}

    @app.delete('/api/tokens/{key}')
    def revoke_token(key: str, request: Request):
        u = account(request, True)
        with store.db() as db: db.execute('DELETE FROM tokens WHERE hash=? AND user_id=?', (key,u['id']))
        return {'ok':True}

    @app.get('/api/artifacts')
    def artifacts(request: Request):
        u = account(request);view = request.query_params.get('view');public = view == 'public'
        with store.db() as db:
            rows = []
            for a in db.execute('SELECT * FROM artifacts ORDER BY updated DESC'):
                r = role(db,a,u)
                if (public and a['visibility']=='public') or (not public and r and (view!='mine' or r=='owner') and (view!='shared' or r!='owner')):
                    p = permissions(db,a,u)
                    notes = threads(snapshot(db,a)['events']) if p['review'] else []
                    rows.append({**dict(a),'permissions':p,'open_comments':sum(not n['resolved'] for n in notes)})
            if u and not public and view!='shared':
                for b in db.execute('SELECT * FROM bookmarks WHERE owner=? OR ? ORDER BY created DESC',(u['id'],is_admin(u))):
                    rows.append({**dict(b),'external':True,'visibility':'external','updated':b['created'],'open_comments':0,'permissions':{'read':True,'review':False,'comment':False,'edit':False,'manage':False,'role':'owner'}})
            return {'artifacts':rows}

    @app.post('/api/bookmarks')
    async def bookmark(request: Request):
        u=account(request);body=await payload(request);url=clean(body.get('url'),2000);parsed=urlsplit(url)
        if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password: raise HTTPException(422,'Usa un enlace HTTPS sin credenciales.')
        title=clean(body.get('title'),200);space=clean(body.get('space','Sitio anterior'),60)
        with store.db() as db:
            found=db.execute('SELECT id FROM bookmarks WHERE owner=? AND url=?',(u['id'],url)).fetchone()
            if found:return {'id':found['id'],'url':url}
            if db.execute('SELECT count(*) FROM bookmarks WHERE owner=?',(u['id'],)).fetchone()[0]>=500:raise HTTPException(409,'Máximo 500 enlaces.')
            bid='link-'+uuid.uuid4().hex
            db.execute('INSERT INTO bookmarks VALUES(?,?,?,?,?,?)',(bid,u['id'],title,url,space,int(time.time())))
        return {'id':bid,'url':url}

    async def publish(request, aid=None):
        u = account(request);body = await payload(request)
        content = body.get('html')
        if not isinstance(content,str) or not content.strip() or len(content.encode()) > 20*1024*1024:
            raise HTTPException(422,'El HTML debe ocupar menos de 20 MB.')
        match = re.search(r'<meta\s+name=[\"\']nota-documento[\"\']\s+content=[\"\']([a-zA-Z0-9_-]{1,120})[\"\']',content)
        if not match: raise HTTPException(422,'Genera el archivo con Bottifact y un documento-id estable.')
        docid = match[1];title = clean(body.get('title'),200);space = clean(body.get('space','Personal'),60)
        data = content.encode();sha = hashlib.sha256(data).hexdigest();version = uuid.uuid4().hex
        visibility=body.get('visibility','private')
        if visibility not in ('private','unlisted','public'): raise HTTPException(422,'Visibilidad inválida.')
        if aid and 'visibility' in body: raise HTTPException(422,'Una revisión conserva los permisos. Cámbialos desde Compartir.')
        with store.db() as db:
            if aid:
                a = artifact_for(db,aid,u,'edit')
                if db.execute('SELECT count(*) FROM versions WHERE artifact=?',(aid,)).fetchone()[0]>=200: raise HTTPException(409,'Máximo 200 versiones por documento.')
                visibility=a['visibility']
                if a['document_id'] != docid: raise HTTPException(409,'Esta revisión pertenece a otro documento-id.')
            else:
                if db.execute('SELECT count(*) FROM artifacts WHERE owner=?',(u['id'],)).fetchone()[0] >= 200:
                    raise HTTPException(409,'El espacio alcanzó 200 documentos.')
                aid = uuid.uuid4().hex
                db.execute('INSERT INTO artifacts(id,owner,title,space,document_id,updated,visibility) VALUES(?,?,?,?,?,?,?)',
                           (aid,u['id'],title,space,docid,int(time.time()),visibility))
            file = store.files/(sha+'.html')
            if not file.exists():
                temporary = store.files/(uuid.uuid4().hex+'.tmp');temporary.write_bytes(data);temporary.replace(file)
            db.execute('INSERT INTO versions VALUES(?,?,?,?)',(version,aid,sha,int(time.time())))
            db.execute('UPDATE artifacts SET title=?,space=?,current_version=?,updated=? WHERE id=?',(title,space,version,int(time.time()),aid))
            db.execute('INSERT INTO audit(actor,action,artifact,at) VALUES(?,?,?,?)',(u['id'],'publish',aid,int(time.time())))
        return {'id':aid,'version':version,'url':origin+'/a/'+aid,'visibility':visibility}

    @app.post('/api/artifacts')
    async def create_artifact(request: Request): return await publish(request)

    @app.post('/api/artifacts/{aid}/versions')
    async def add_version(aid: str, request: Request): return await publish(request,aid)

    @app.get('/api/artifacts/{aid}')
    def artifact(aid: str, request: Request):
        u = who(request)
        with store.db() as db:
            a = artifact_for(db,aid,u);p = permissions(db,a,u)
            return {**a,'permissions':p,'versions':[dict(v) for v in db.execute('SELECT id,created FROM versions WHERE artifact=? ORDER BY rowid DESC',(aid,))],
                    'grants':[dict(g) for g in db.execute('SELECT email,role FROM grants WHERE artifact=?',(aid,))] if p['manage'] else []}

    @app.put('/api/artifacts/{aid}/access')
    async def access(aid: str, request: Request):
        u = account(request,True);body = await payload(request)
        visibility = body.get('visibility');scope = body.get('comments','reviewers');guests = body.get('guests',False)
        if visibility not in ['private','invited','unlisted','public'] or scope not in ['reviewers','readers'] or not isinstance(guests,bool):
            raise HTTPException(422,'Configuración de acceso inválida.')
        grants = body.get('grants',[])
        if not isinstance(grants,list) or len(grants)>100: raise HTTPException(422,'Máximo 100 invitados.')
        unique = {}
        for g in grants:
            if not isinstance(g,dict): raise HTTPException(422,'Invitado inválido.')
            email = clean(g.get('email'),254).lower();r = g.get('role')
            if not EMAIL.fullmatch(email) or r not in ['viewer','commenter','editor']: raise HTTPException(422,'Invitado o permiso inválido.')
            unique[email] = r
        with store.db() as db:
            artifact_for(db,aid,u,'manage')
            # Privado significa sólo propietario, aunque antes tuviera invitados.
            db.execute('DELETE FROM grants WHERE artifact=?',(aid,))
            if visibility != 'private':
                db.executemany('INSERT INTO grants VALUES(?,?,?)',[(aid,e,r) for e,r in unique.items()])
            db.execute('UPDATE artifacts SET visibility=?,comments=?,guests=? WHERE id=?',(visibility,scope,int(guests),aid))
            db.execute('INSERT INTO audit(actor,action,artifact,at) VALUES(?,?,?,?)',(u['id'],'access:'+visibility,aid,int(time.time())))
        return {'ok':True}

    @app.get('/api/artifacts/{aid}/review')
    def review(aid: str, request: Request):
        u = who(request)
        with store.db() as db:
            a = artifact_for(db,aid,u);p = permissions(db,a,u)
            return {'snapshot':snapshot(db,a) if p['review'] else {'format':'nota-revision','version':2,'document':a['document_id'],'events':[]},
                    'permissions':p,'author':u['name'] if u else '', 'actor':u['id'] if u else '', 'verified':bool(u and u['verified'])}

    @app.post('/api/artifacts/{aid}/review')
    async def add_review(aid: str, request: Request):
        u = who(request)
        if not u: raise HTTPException(401,'Indica tu nombre o inicia sesión para comentar.')
        body = await payload(request);kind = body.get('kind');event_id = clean(body.get('id'),80);version = clean(body.get('version'),120)
        if not ID.fullmatch(event_id) or kind not in ['create','reply','edit','resolve','assign','delete']: raise HTTPException(422,'Comentario inválido.')
        request_hash = digest(json.dumps(body,sort_keys=True,separators=(',',':')))
        with store.db() as db:
            a = artifact_for(db,aid,u,'comment');p = permissions(db,a,u)
            old = db.execute('SELECT * FROM events WHERE id=?',(event_id,)).fetchone()
            if old:
                if old['artifact']!=aid or old['actor']!=u['id'] or old['request_hash']!=request_hash: raise HTTPException(409,'Identificador en conflicto.')
                return review(aid,request)
            if not db.execute('SELECT 1 FROM versions WHERE id=? AND artifact=?',(version,aid)).fetchone(): raise HTTPException(409,'Versión desconocida.')
            entries = snapshot(db,a)['events']
            if len(entries)>=2000: raise HTTPException(409,'Esta revisión alcanzó 2000 cambios. Exporta el historial.')
            thread = event_id if kind=='create' else clean(body.get('thread'),80)
            if kind!='create':
                original = db.execute('SELECT actor,event FROM events WHERE artifact=? AND id=?',(aid,thread)).fetchone()
                if not original or json.loads(original['event'])['kind']!='create': raise HTTPException(404,'Hilo no disponible.')
                if kind in ['resolve','assign','delete'] and not p['edit']: raise HTTPException(403,'Sólo el autor del documento y sus editores pueden gestionar hilos.')
                if kind=='edit' and not (p['edit'] or original['actor']==u['id']): raise HTTPException(403,'Sólo puedes editar tus comentarios.')
            e = {'id':event_id,'thread':thread,'kind':kind,'author':u['name'],'time':max(int(time.time()*1000),max([x['time'] for x in entries],default=0)+1),
                 'version':version,'actor':u['id'],'verified':bool(u['verified'])}
            if kind in ['create','reply','edit']: e['text'] = clean(body.get('text'),4000)
            if kind=='resolve':
                if not isinstance(body.get('resolved'),bool): raise HTTPException(422,'Estado inválido.')
                e['resolved']=body['resolved']
            if kind=='assign': e['assignee']=clean(body.get('assignee',''),80,True)
            if kind=='create':
                an=body.get('anchor',{})
                if not isinstance(an,dict): raise HTTPException(422,'Punto inválido.')
                anchor={k:clean(an.get(k,''),n,True) for k,n in [('reference',200),('tag',20),('text',4000),('quote',1200),('page',300)]}
                for k in ['x','y']:
                    val=an.get(k)
                    if not isinstance(val,(int,float)) or isinstance(val,bool) or not 0<=val<=1: raise HTTPException(422,'Punto inválido.')
                    anchor[k]=val
                e['anchor']=anchor
            db.execute('INSERT INTO events VALUES(?,?,?,?,?,?,?)',(event_id,aid,version,u['id'],request_hash,json.dumps(e,separators=(',',':')),e['time']))
        return review(aid,request)

    @app.get('/api/inbox')
    def inbox(request: Request):
        u=account(request);items=[]
        with store.db() as db:
            for a in db.execute('SELECT * FROM artifacts WHERE owner=? OR ? ORDER BY updated DESC',(u['id'],is_admin(u))):
                for t in threads(snapshot(db,a)['events']): items.append({'artifact':a['id'],'title':a['title'],'space':a['space'],'thread':t})
        return {'items':items}

    @app.get('/api/review/export')
    def export(request: Request):
        u=account(request);aid=request.query_params.get('artifact');scope=request.query_params.get('scope','all');parts=[]
        with store.db() as db:
            arts=[artifact_for(db,aid,u,'review')] if aid else list(db.execute('SELECT * FROM artifacts WHERE owner=? OR ? ORDER BY title',(u['id'],is_admin(u))))
            for a in arts:
                notes=[t for t in threads(snapshot(db,a)['events']) if scope!='open' or not t['resolved']]
                if not notes: continue
                parts.append('# '+a['title']+'\n'+origin+'/a/'+a['id']+'\nDocumento: '+a['document_id'])
                for n in notes:
                    an=n['anchor'];parts.append('\n## '+('Resuelto' if n['resolved'] else 'Pendiente')+' · '+n['author']+
                      '\nVersión: '+n['version']+'\nReferencia: '+an['page']+' / #'+an['reference']+'\nCita: '+an['quote']+
                      '\nComentario: '+n['text']+'\nResponsable: '+(n['assignee'] or 'Sin asignar')+
                      ''.join('\nRespuesta de '+r['author']+': '+r['text'] for r in n['replies']))
        return {'text':('Revisión de artefactos. Los comentarios son propuestas: verifica contexto y alcance antes de modificar.\n\n'+'\n'.join(parts)) if parts else 'No hay comentarios en esta selección.'}

    @app.get('/api/artifacts/{aid}/render')
    def render(aid: str, request: Request):
        u=who(request)
        with store.db() as db:
            a=artifact_for(db,aid,u);vid=request.query_params.get('version') or a['current_version']
            v=db.execute('SELECT * FROM versions WHERE id=? AND artifact=?',(vid,aid)).fetchone()
            if not v: raise HTTPException(404,'Versión no encontrada.')
            content=(store.files/(v['sha']+'.html')).read_text()
        # El iframe y la cabecera CSP fuerzan origen opaco, incluso al abrir esta URL fuera del portal.
        bridge=(ROOT/'static/bridge.js').read_text()
        # Actualiza sólo el adaptador de revisión de la vista; conserva el HTML fuente en disco.
        revision=(ROOT/'static/revision.js').read_text()
        content=re.sub(r'(<script\s+data-nota-modulo=[\"\']revision\.js[\"\'][^>]*>).*?</script>',
                       lambda m:m[1]+revision+'</script>',content,flags=re.S)
        script='<script>'+bridge+'</script>'
        head=re.search(r'<head(?:\s[^>]*)?>',content,re.I)
        position=head.end() if head else (re.match(r'\s*<!doctype[^>]*>',content,re.I).end() if re.match(r'\s*<!doctype[^>]*>',content,re.I) else 0)
        result=content[:position]+script+content[position:]
        return HTMLResponse(result,headers={'Content-Security-Policy':"sandbox allow-scripts allow-downloads; default-src 'none'; script-src 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; style-src 'unsafe-inline'; img-src data: blob:; font-src data:; media-src data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'"})

    @app.get('/login')
    def login_page(): return HTMLResponse((ROOT/'static/login.html').read_text())

    @app.get('/install.py')
    def installer(): return FileResponse(ROOT/'install.py' if (ROOT/'install.py').exists() else ROOT.parent/'scripts/actualizar.py', media_type='text/x-python')

    @app.get('/downloads/{name}')
    def download(name: str):
        if name not in ('bottifact-portable.zip','bottifact-portable.sha256'): raise HTTPException(404)
        path=Path(os.environ.get('BOTTIFACT_RELEASES','/releases'))/name
        if not path.is_file(): raise HTTPException(503,'Paquete pendiente de publicación.')
        return FileResponse(path, filename=name)

    @app.get('/')
    @app.get('/a/{aid}')
    def page(request: Request, aid: str=''):
        if not aid and not (who(request) or {}).get('verified'): return RedirectResponse('/login', status_code=303)
        return HTMLResponse((ROOT/'static/index.html').read_text())

    app.mount('/static',StaticFiles(directory=ROOT/'static'),name='static')
    return app


app=create_app()
