"""Importación administrativa e idempotente de un inventario local revisado.

No rastrea URLs ni modifica archivos originales. El manifiesto queda fuera de Git.
Cada entrada declara source, file, title, space, attachments y optional legacy_url.
"""
import argparse, hashlib, html as html_module, json, os, re, shutil, time, uuid
from pathlib import Path
from portal.app import Store, admin_emails


def import_archive(store, entries):
    owner=store.user(admin_emails()[0],'Angel Botto')
    with store.db() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS imports(source TEXT PRIMARY KEY,artifact TEXT NOT NULL REFERENCES artifacts(id),sha TEXT NOT NULL,at INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS bookmark_migrations(bookmark TEXT PRIMARY KEY,artifact TEXT NOT NULL REFERENCES artifacts(id));''')
    results=[]
    # IDs se reservan primero para convertir vínculos entre documentos del inventario.
    mapping={}; sha_ids={}
    for e in entries:
        raw=Path(e['file']).read_bytes(); original_sha=hashlib.sha256(raw).hexdigest()
        with store.db() as db:
            old=db.execute('SELECT artifact,sha FROM imports WHERE source=?',(e['source'],)).fetchone()
            same=db.execute('SELECT artifact,sha FROM imports WHERE sha=?',(original_sha,)).fetchone()
            native=db.execute('SELECT artifact,sha FROM versions WHERE sha=?',(original_sha,)).fetchone()
            row=old or same or native
        e['_aid']=row['artifact'] if row else sha_ids.get(original_sha,uuid.uuid4().hex);e['_sha']=original_sha;sha_ids[original_sha]=e['_aid']
        mapping[str(Path(e['file']).resolve())]=e['_aid']
        if e.get('legacy_url'):mapping[e['legacy_url'].rstrip('/')+'/']=e['_aid']
    for e in entries:
        aid=e['_aid'];source=Path(e['file']);html=source.read_text(); original_sha=e['_sha']
        with store.db() as db:
            existing=db.execute('SELECT artifact FROM imports WHERE source=? AND sha=?',(e['source'],original_sha)).fetchone()
            same=db.execute('SELECT artifact FROM imports WHERE sha=?',(original_sha,)).fetchone()
            native=db.execute('SELECT artifact,sha FROM versions WHERE sha=?',(original_sha,)).fetchone()
            if existing or same or native:
                aid=(existing or same or native)['artifact'];db.execute('INSERT OR REPLACE INTO imports VALUES(?,?,?,?)',(e['source'],aid,original_sha,int(time.time())))
                if e.get('legacy_url'):db.execute('INSERT OR REPLACE INTO bookmark_migrations SELECT id,? FROM bookmarks WHERE url=?',(aid,e['legacy_url']))
                results.append({'source':e['source'],'id':aid,'status':'existing'});continue
            doc=re.search(r'<meta\s+name=[\"\']nota-documento[\"\']\s+content=[\"\']([a-zA-Z0-9_-]{1,120})',html)
            docid=doc[1] if doc else 'import-'+hashlib.sha256(e['source'].encode()).hexdigest()[:24]
            if not doc:
                meta='<meta name="nota-documento" content="'+docid+'">'
                head=re.search(r'<head(?:\s[^>]*)?>',html,re.I)
                doctype=re.match(r'\s*<!doctype[^>]*>',html,re.I)
                pos=head.end() if head else doctype.end() if doctype else 0
                html=html[:pos]+meta+html[pos:]
            vid=uuid.uuid4().hex
            from urllib.parse import urlsplit,unquote,quote
            def links(m):
                tag,href=m.group(1),m.group(3);u=urlsplit(href)
                target=(source.parent/unquote(u.path)).resolve() if not u.scheme and not u.netloc else None
                to=mapping.get(str(target)) if target else mapping.get(href.rstrip('/')+'/')
                if to:return tag+' data-bottifact-link href="/a/'+to+('#'+html_module.escape(u.fragment,quote=True) if u.fragment else '')+'"'
                attachments=e.get('attachments',{})
                if href in attachments:return tag+' data-bottifact-link href="/api/artifacts/'+aid+'/attachments/'+vid+'/'+quote(href,safe='/')+'"'
                return m.group(0)
            html=re.sub(r'(<a\b[^>]*?)\s+href=([\"\'])(.*?)\2',links,html,flags=re.I)
            # También cubre enlaces que los documentos antiguos dibujan con JavaScript.
            routes={}
            for path,target_aid in mapping.items():
                if path.startswith('https://'):
                    if path.rstrip('/') not in html:continue
                elif not Path(path).is_relative_to(source.parent):continue
                key=path if path.startswith('https://') else os.path.relpath(path,source.parent)
                routes[key]='/a/'+target_aid
            for relative in e.get('attachments',{}):
                routes[relative]='/api/artifacts/'+aid+'/attachments/'+vid+'/'+quote(relative,safe='/')
            config='<script>window.BottifactArchiveLinks='+json.dumps(routes).replace('<','\\u003c')+';</script>'
            head=re.search(r'<head(?:\s[^>]*)?>',html,re.I)
            doctype=re.match(r'\s*<!doctype[^>]*>',html,re.I)
            pos=head.end() if head else doctype.end() if doctype else 0
            html=html[:pos]+config+html[pos:]
            data=html.encode();sha=hashlib.sha256(data).hexdigest()
            if len(data)>20*1024*1024:raise ValueError('Documento supera 20 MB: '+e['source'])
            file=store.files/(sha+'.html')
            if not file.exists():file.write_bytes(data);file.chmod(0o600)
            for relative,path in e.get('attachments',{}).items():
                root=(store.files/'attachments'/vid).resolve();dest=(root/relative).resolve()
                if not dest.is_relative_to(root):raise ValueError('Adjunto fuera de carpeta')
                dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest);dest.chmod(0o600)
            now=int(time.time());title=e['title'].strip()[:200];space=e['space'][:60]
            if db.execute('SELECT 1 FROM artifacts WHERE id=?',(aid,)).fetchone():
                db.execute('UPDATE artifacts SET title=?,space=?,current_version=?,updated=? WHERE id=?',(title,space,vid,now,aid))
            else:
                db.execute('INSERT INTO artifacts(id,owner,title,space,document_id,visibility,current_version,updated) VALUES(?,?,?,?,?,?,?,?)',(aid,owner['id'],title,space,docid,'private',vid,now))
            db.execute('INSERT INTO versions VALUES(?,?,?,?)',(vid,aid,sha,now))
            db.execute('INSERT OR REPLACE INTO imports VALUES(?,?,?,?)',(e['source'],aid,original_sha,now))
            if e.get('legacy_url'):db.execute('INSERT OR REPLACE INTO bookmark_migrations SELECT id,? FROM bookmarks WHERE url=?',(aid,e['legacy_url']))
            db.execute('INSERT INTO audit(actor,action,artifact,at) VALUES(?,?,?,?)',(owner['id'],'import-private',aid,now))
            results.append({'source':e['source'],'id':aid,'version':vid,'status':'imported'})
    return results

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest',required=True,type=Path);p.add_argument('--data',required=True);p.add_argument('--result',required=True,type=Path);args=p.parse_args()
    if not admin_emails():p.error('Configura BOTTIFACT_ADMIN_EMAILS con el propietario verificado.')
    result=import_archive(Store(args.data),json.loads(args.manifest.read_text()))
    args.result.write_text(json.dumps(result,ensure_ascii=False,indent=2));args.result.chmod(0o600)
    print('Importados:',sum(r['status']=='imported' for r in result),'existentes:',sum(r['status']=='existing' for r in result))
