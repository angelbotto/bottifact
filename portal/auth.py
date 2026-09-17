"""Acceso propio: códigos por correo y Google OIDC con estado, nonce y PKCE."""
import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
import urllib.parse
import urllib.request

import jwt
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.concurrency import run_in_threadpool

AUTH_COOKIE = '__Host-bottifact-auth'


def target(value):
    return value if isinstance(value, str) and re.fullmatch(r'/(?:a/[a-f0-9]{32})?', value) else '/'


def remote_json(url, data, headers=None, form=False):
    body = urllib.parse.urlencode(data).encode() if form else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded' if form else 'application/json', 'User-Agent': 'Bottifact/1.0', **(headers or {})})
    # No reenviar credenciales a redirecciones de un proveedor.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs): return None
    with urllib.request.build_opener(NoRedirect).open(req, timeout=15) as response:
        return json.load(response)


def send_code(email, code):
    return remote_json(os.environ['BOTTIFACT_EMAIL_URL'].rstrip('/') + '/api/v1/emails', {
        'from': os.environ['BOTTIFACT_EMAIL_FROM'], 'to': email,
        'subject': 'Tu código de acceso a Bottifact',
        'text': f'Tu código de acceso es {code}. Vence en 10 minutos y solo sirve una vez.\n\nÚsalo en https://artifacts.botto.is. Si no lo pediste, ignora este mensaje. No compartas el código.'
    }, {'Authorization': 'Bearer ' + os.environ['BOTTIFACT_EMAIL_KEY']})


def mount_auth(app, store, origin, set_session, payload, clean, email_pattern):
    sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
    with store.db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS auth_challenges(id TEXT PRIMARY KEY,kind TEXT,email TEXT,proof TEXT,binding TEXT,expires INTEGER,attempts INTEGER DEFAULT 0,next TEXT,extra TEXT);
        CREATE TABLE IF NOT EXISTS auth_limits(bucket TEXT PRIMARY KEY,count INTEGER,expires INTEGER);
        ''')
    google_keys = jwt.PyJWKClient('https://www.googleapis.com/oauth2/v3/certs', cache_keys=True)
    email_ready = lambda: all(os.environ.get(k) for k in ['BOTTIFACT_EMAIL_URL', 'BOTTIFACT_EMAIL_KEY', 'BOTTIFACT_EMAIL_FROM', 'BOTTIFACT_AUTH_SECRET'])
    google_ready = lambda: all(os.environ.get(k) for k in ['BOTTIFACT_GOOGLE_ID', 'BOTTIFACT_GOOGLE_SECRET']) and os.environ.get('BOTTIFACT_GOOGLE_ENABLED') == '1'

    def limited(key, maximum, seconds):
        now = int(time.time())
        with store.db() as db:
            db.execute('DELETE FROM auth_limits WHERE expires<=?', (now,))
            row = db.execute('SELECT * FROM auth_limits WHERE bucket=?', (sha(key),)).fetchone()
            if row and row['count'] >= maximum:
                raise HTTPException(429, 'Espera unos minutos antes de volver a intentarlo.', headers={'Retry-After': str(row['expires'] - now)})
            db.execute('INSERT INTO auth_limits VALUES(?,1,?) ON CONFLICT(bucket) DO UPDATE SET count=count+1', (sha(key), now + seconds))

    def binding(response, value):
        response.set_cookie(AUTH_COOKIE, value, secure=True, httponly=True, samesite='lax', max_age=600, path='/')
        return response

    def finish(uid, destination):
        response = set_session(RedirectResponse(destination, status_code=303), uid)
        response.delete_cookie(AUTH_COOKIE, secure=True, httponly=True, samesite='lax', path='/')
        return response

    @app.get('/api/auth/options')
    def options():
        return {'email': email_ready(), 'google': google_ready()}

    @app.post('/api/auth/email')
    async def email_start(request: Request):
        if not email_ready(): raise HTTPException(503, 'El acceso por correo aún no está configurado.')
        body = await payload(request)
        email = clean(body.get('email'), 254).lower()
        if not email_pattern.fullmatch(email): raise HTTPException(422, 'Revisa tu correo.')
        ip = request.headers.get('cf-connecting-ip') or request.client.host
        limited('send-ip:' + ip, 20, 3600)
        limited('send-email-hour:' + email, 5, 3600)
        limited('send-email-minute:' + email, 1, 60)
        cid, browser = secrets.token_urlsafe(32), secrets.token_urlsafe(32)
        code = f'{secrets.randbelow(1000000):06d}'
        proof = hmac.new(os.environ['BOTTIFACT_AUTH_SECRET'].encode(), (cid + ':' + code).encode(), hashlib.sha256).hexdigest()
        with store.db() as db:
            db.execute('DELETE FROM auth_challenges WHERE expires<=? OR (kind=? AND email=?)', (int(time.time()), 'email', email))
            db.execute('INSERT INTO auth_challenges VALUES(?,?,?,?,?,?,0,?,?)', (cid, 'email', email, proof, sha(browser), int(time.time()) + 600, target(body.get('next')), '{}'))
        try:
            await run_in_threadpool(send_code, email, code)
        except Exception:
            with store.db() as db: db.execute('DELETE FROM auth_challenges WHERE id=?', (cid,))
            raise HTTPException(503, 'No pudimos enviar el código. Intenta de nuevo en un minuto.') from None
        return binding(JSONResponse({'challenge': cid, 'expires_in': 600}), browser)

    @app.post('/api/auth/email/verify')
    async def email_verify(request: Request):
        body = await payload(request)
        cid, code = clean(body.get('challenge'), 100), clean(body.get('code'), 6)
        valid = False
        with store.db() as db:
            row = db.execute('SELECT * FROM auth_challenges WHERE id=? AND kind=?', (cid, 'email')).fetchone()
            if row and row['expires'] > time.time() and row['attempts'] < 5 and hmac.compare_digest(row['binding'], sha(request.cookies.get(AUTH_COOKIE, ''))):
                proof = hmac.new(os.environ.get('BOTTIFACT_AUTH_SECRET', '').encode(), (cid + ':' + code).encode(), hashlib.sha256).hexdigest()
                valid = bool(re.fullmatch(r'[0-9]{6}', code)) and hmac.compare_digest(proof, row['proof'])
                db.execute('UPDATE auth_challenges SET attempts=attempts+1 WHERE id=?', (cid,))
                if valid: db.execute('DELETE FROM auth_challenges WHERE id=?', (cid,))
        # Los intentos se confirman incluso cuando falla la verificación.
        if not valid: raise HTTPException(401, 'Código incorrecto, vencido o utilizado. Puedes solicitar otro.')
        u = store.user(row['email'], row['email'].split('@')[0])
        response = set_session(JSONResponse({'next': row['next']}), u['id'])
        response.delete_cookie(AUTH_COOKIE, secure=True, httponly=True, samesite='lax', path='/')
        return response

    @app.get('/auth/google')
    def google_start(request: Request):
        if not google_ready(): return RedirectResponse('/login?error=google_setup', status_code=303)
        state, browser, nonce, verifier = [secrets.token_urlsafe(32) for _ in range(4)]
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
        limited('google:' + (request.headers.get('cf-connecting-ip') or request.client.host), 30, 600)
        with store.db() as db:
            db.execute('DELETE FROM auth_challenges WHERE expires<=?', (int(time.time()),))
            db.execute('INSERT INTO auth_challenges VALUES(?,?,?,?,?,?,0,?,?)', (sha(state), 'google', '', nonce, sha(browser), int(time.time()) + 600, target(request.query_params.get('next')), json.dumps({'verifier': verifier})))
        params = dict(client_id=os.environ['BOTTIFACT_GOOGLE_ID'], redirect_uri=origin + '/auth/google/callback', response_type='code', scope='openid email profile', state=state, nonce=nonce, code_challenge=challenge, code_challenge_method='S256', prompt='select_account')
        return binding(RedirectResponse('https://accounts.google.com/o/oauth2/v2/auth?' + urllib.parse.urlencode(params), status_code=303), browser)

    @app.get('/auth/google/callback')
    def google_finish(request: Request):
        state = request.query_params.get('state', '')
        with store.db() as db:
            row = db.execute('SELECT * FROM auth_challenges WHERE id=? AND kind=?', (sha(state), 'google')).fetchone()
            if not row or row['expires'] <= time.time() or not hmac.compare_digest(row['binding'], sha(request.cookies.get(AUTH_COOKIE, ''))):
                return RedirectResponse('/login?error=google_session', status_code=303)
            db.execute('DELETE FROM auth_challenges WHERE id=?', (sha(state),))
        try:
            if request.query_params.get('error'): raise ValueError('Cancelled')
            token = remote_json('https://oauth2.googleapis.com/token', dict(client_id=os.environ['BOTTIFACT_GOOGLE_ID'], client_secret=os.environ['BOTTIFACT_GOOGLE_SECRET'], code=request.query_params.get('code', ''), code_verifier=json.loads(row['extra'])['verifier'], grant_type='authorization_code', redirect_uri=origin + '/auth/google/callback'), form=True)['id_token']
            claims = jwt.decode(token, google_keys.get_signing_key_from_jwt(token).key, algorithms=['RS256'], audience=os.environ['BOTTIFACT_GOOGLE_ID'], issuer=['https://accounts.google.com', 'accounts.google.com'], options={'require': ['exp', 'iat', 'sub', 'iss', 'aud', 'email', 'nonce']})
            if claims.get('email_verified') is not True or not hmac.compare_digest(claims['nonce'], row['proof']): raise ValueError('Unverified')
            if claims.get('azp', os.environ['BOTTIFACT_GOOGLE_ID']) != os.environ['BOTTIFACT_GOOGLE_ID']: raise ValueError('Wrong client')
            u = store.user(claims['email'], claims.get('name') or claims['email'].split('@')[0])
        except Exception:
            return RedirectResponse('/login?error=google_session', status_code=303)
        return finish(u['id'], row['next'])
