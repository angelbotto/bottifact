"""Un proceso: respaldo diario y resúmenes optativos. Reintentos sin duplicar avisos."""
import json
import os
import time
import uuid
from pathlib import Path
from portal.auth import remote_json
from portal.backup import backup,status


def send_digest(email,text,key):
    provider=os.environ.get('BOTTIFACT_EMAIL_PROVIDER','resend')
    suffix='/emails' if provider=='resend' else '/api/v1/emails'
    return remote_json(os.environ['BOTTIFACT_EMAIL_URL'].rstrip('/')+suffix,{
        'from':os.environ['BOTTIFACT_EMAIL_FROM'],'to':[email] if provider=='resend' else email,
        'subject':'Bottifact · revisión pendiente','text':text},
        {'Authorization':'Bearer '+os.environ['BOTTIFACT_EMAIL_KEY'],'Idempotency-Key':'bottifact-digest/'+key})


def digests(store,origin,permissions,send=send_digest):
    now=int(time.time())
    with store.db() as db:users=[dict(r) for r in db.execute("SELECT u.*,s.last_sent FROM users u JOIN notification_settings s ON s.user=u.id WHERE s.frequency='daily' AND u.verified=1 AND s.last_sent<?",(now-86400,))]
    for user in users:
        with store.db() as db:
            batch=db.execute('SELECT * FROM delivery_batches WHERE user=? AND sent=0 ORDER BY created LIMIT 1',(user['id'],)).fetchone()
            if batch and batch['created']<now-23*3600:
                # Do not retry an expired provider idempotency key: delivery may have succeeded.
                db.execute('UPDATE delivery_batches SET sent=-1 WHERE id=?',(batch['id'],));db.execute('UPDATE notification_settings SET last_sent=? WHERE user=?',(now,user['id']));continue
            rows=[]
            for n in db.execute('SELECT * FROM notifications WHERE user=? AND seen=0 AND mailed=0 ORDER BY id LIMIT 100',(user['id'],)):
                a=db.execute('SELECT * FROM artifacts WHERE id=?',(n['artifact'],)).fetchone()
                e=db.execute('SELECT event FROM events WHERE id=?',(n['event'],)).fetchone()
                if not a or not e:continue
                from portal.workflows import version_state
                p=permissions(db,a,user)
                if not p['review'] or (version_state(db,json.loads(e['event'])['version'])=='draft' and not p['edit']):continue
                rows.append((dict(n),dict(a)))
            if batch:
                ids=json.loads(batch['items'])
                # Recheck permissions and unseen state immediately before sending.
                allowed={n['id'] for n,a in rows}
                if not set(ids)<=allowed:
                    db.execute('UPDATE delivery_batches SET sent=-1 WHERE id=?',(batch['id'],));continue
                record=dict(batch)
            elif rows:
                ids=[n['id'] for n,a in rows];bid=uuid.uuid4().hex
                lines=['Tienes revisiones pendientes en Bottifact.','']
                for n,a in rows:lines.extend([a['title'],origin+'/a/'+a['id']+'?thread='+n['thread'],''])
                lines+=['Puedes desactivar este resumen en Avisos → Resumen por correo. No respondas a este mensaje para modificar un artefacto.']
                record={'id':bid,'items':json.dumps(ids),'body':'\n'.join(lines)}
                db.execute('INSERT INTO delivery_batches(id,user,items,body,created) VALUES(?,?,?,?,?)',(bid,user['id'],record['items'],record['body'],now))
            else:continue
        try:send(user['email'],record['body'],record['id'])
        except Exception:
            status(store.root,'mail',{'ok':False,'at':now,'detail':'Resumen pendiente de reintento; no se muestran credenciales.'});continue
        with store.db() as db:
            db.execute('UPDATE delivery_batches SET sent=? WHERE id=?',(now,record['id']))
            db.executemany('UPDATE notifications SET mailed=1 WHERE id=?',[(i,) for i in json.loads(record['items'])])
            db.execute('UPDATE notification_settings SET last_sent=? WHERE user=?',(now,user['id']))
        status(store.root,'mail',{'ok':True,'at':now,'detail':'Resumen aceptado por el proveedor. La aceptación no acredita entrega.'})


def main():
    from portal.app import Store,permissions
    store=Store(os.environ.get('BOTTIFACT_DATA','/data'));root=store.root
    while True:
        try:
            with store.db() as db:r=db.execute("SELECT value FROM operation_status WHERE key='backup'").fetchone()
            last=json.loads(r['value']) if r else {}
            if not last.get('ok') or time.time()-last.get('at',0)>86400:
                backup(root,os.environ.get('BOTTIFACT_BACKUPS','/backups'),os.environ.get('BOTTIFACT_BACKUP_CONFIG'))
            if os.environ.get('BOTTIFACT_EMAIL_KEY'):digests(store,os.environ.get('BOTTIFACT_ORIGIN','http://localhost:8788'),permissions)
            status(root,'worker',{'ok':True,'at':int(time.time()),'detail':'Respaldo diario · avisos optativos cada minuto.'})
        except Exception:
            status(root,'worker',{'ok':False,'at':int(time.time()),'detail':'Hay una tarea pendiente de reintento.'})
        time.sleep(60)

if __name__=='__main__':main()
