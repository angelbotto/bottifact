"""Administración mediante SSH. Nunca imprime tokens ni enlaces de acceso."""
import argparse
import json
import os
import shutil
import sqlite3
import time
from pathlib import Path
from .app import Store


def secret_file(path, value):
    target=Path(path);target.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f: f.write(value+'\n')
    print('Guardado en '+str(target))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',default=os.environ.get('BOTTIFACT_DATA','/data'))
    sub=p.add_subparsers(dest='command',required=True)
    for command in ['token','login']:
        c=sub.add_parser(command);c.add_argument('--email',required=True);c.add_argument('--name',required=True);c.add_argument('--output',required=True)
        if command=='token':c.add_argument('--label',default='Agente')
    c=sub.add_parser('backup');c.add_argument('--output',required=True)
    args=p.parse_args();store=Store(args.data)
    if args.command=='backup':
        out=Path(args.output);out.mkdir(parents=True,exist_ok=False,mode=0o700)
        # SQLite backup toma una instantánea coherente aunque el servidor siga activo.
        with store.db() as source:
            with sqlite3.connect(out/'bottifact.sqlite3') as dest:source.backup(dest)
        with sqlite3.connect(out/'bottifact.sqlite3') as snap:
            assert snap.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
            hashes=[x[0] for x in snap.execute('SELECT DISTINCT sha FROM versions')]
            versions=[x[0] for x in snap.execute('SELECT id FROM versions')]
        (out/'files').mkdir(mode=0o700)
        for sha in hashes:shutil.copy2(store.files/(sha+'.html'),out/'files'/(sha+'.html'))
        for version in versions:
            attachments=store.files/'attachments'/version
            if attachments.is_dir():shutil.copytree(attachments,out/'files'/'attachments'/version)
        (out/'backup.json').write_text(json.dumps({'created':int(time.time()),'files':len(hashes),'schema':1}))
        print('Respaldo íntegro: '+str(out));return
    user=store.user(args.email,args.name)
    value=store.token(user['id'],args.label) if args.command=='token' else os.environ.get('BOTTIFACT_ORIGIN','https://artifacts.botto.is')+'/auth/bootstrap?code='+store.login_once(user['id'])
    secret_file(args.output,value)

if __name__=='__main__':main()
