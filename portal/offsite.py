"""Copia privada fuera del NAS, verificada antes de informar éxito. Para launchd/cron."""
import argparse
import json
import os
import re
import shutil
import subprocess
import tarfile
import tempfile
import time
from pathlib import Path
from backup import verify


def main():
    p=argparse.ArgumentParser();p.add_argument('--host',required=True);p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    if not re.fullmatch(r'[\w.@-]+',args.host):raise SystemExit('Host SSH inválido.')
    base=['/usr/bin/ssh','-o','BatchMode=yes','-o','ConnectTimeout=15',args.host]
    docker='sudo -n /usr/local/bin/docker exec bottifact-worker '
    get="python -c 'from pathlib import Path;p=sorted(Path(\"/backups\").glob(\"snapshot-*\"));print(p[-1].name if p else \"\")'"
    name=subprocess.check_output(base+[docker+get],text=True).strip()
    if not re.fullmatch(r'snapshot-\d{8}-\d{6}-[a-f0-9]{6}',name):raise SystemExit('No hay un respaldo completo disponible.')
    args.output.mkdir(parents=True,exist_ok=True,mode=0o700);os.chmod(args.output,0o700);final=args.output/name
    if not final.exists():
        with tempfile.TemporaryDirectory(prefix='.download-',dir=args.output) as tmp:
            tmp=Path(tmp);archive=tmp/'backup.tgz'
            with archive.open('wb') as stream:subprocess.run(base+[docker+'tar czf - -C /backups '+name],stdout=stream,check=True)
            with tarfile.open(archive) as tar:
                for m in tar:
                    if m.issym() or m.islnk() or not (m.isfile() or m.isdir()) or not (tmp/m.name).resolve().is_relative_to(tmp.resolve()):raise ValueError('Archivo de respaldo inválido.')
                tar.extractall(tmp,filter='data')
            verify(tmp/name);(tmp/name).rename(final)
    proof=verify(final)
    state={'ok':True,'at':int(time.time()),'detail':'Copia verificada fuera del NAS, en Mac mini. '+str(proof['files'])+' archivos.'}
    code="python -c 'import sys,json;from portal.backup import status;status(\"/data\",\"external\",json.load(sys.stdin))'"
    subprocess.run(base+[docker.replace('exec ','exec -i ')+code],input=json.dumps(state).encode(),check=True)
    for old in sorted(args.output.glob('snapshot-*'),reverse=True)[7:]:
        if old.is_dir() and not old.is_symlink():shutil.rmtree(old)
    print(json.dumps(state,ensure_ascii=False))

if __name__=='__main__':main()
