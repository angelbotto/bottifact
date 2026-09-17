#!/usr/bin/env python3
"""Create a private self-host configuration without printing secrets."""
import argparse
import os
from pathlib import Path
import re
import secrets
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from portal.settings import validate_origin
from urllib.parse import urlsplit


def configure(path, origin, admin):
    origin=validate_origin(origin)
    parsed=urlsplit(origin)
    if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password or parsed.path not in ('','/') or parsed.query or parsed.fragment:
        raise ValueError('Use an origin such as https://artifacts.example.com, without a path.')
    if parsed.scheme!='https' and parsed.hostname not in ('localhost','127.0.0.1','::1'):
        raise ValueError('HTTP is only supported on loopback for local development. Use HTTPS for remote access.')
    if not re.fullmatch(r'[^\s@,]+@[^\s@,]+\.[^\s@,]+',admin):raise ValueError('Use one valid administrator email.')
    template=(Path(__file__).resolve().parents[1]/'.env.example').read_text()
    values={'BOTTIFACT_ORIGIN':origin.rstrip('/'),'BOTTIFACT_DOMAIN':parsed.hostname,
            'BOTTIFACT_ADMIN_EMAILS':admin.lower(),'BOTTIFACT_AUTH_SECRET':secrets.token_urlsafe(48)}
    for key,value in values.items():
        if any(c in value for c in ('\n','\r','$','#','"',"'",'`')):raise ValueError('Invalid configuration character.')
        template=re.sub(r'^'+key+r'=.*$',key+'='+value,template,flags=re.M)
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:f.write(template)

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--origin',required=True);p.add_argument('--admin',required=True);p.add_argument('--output',type=Path,default=Path('.env'));a=p.parse_args()
    try:configure(a.output,a.origin,a.admin)
    except (ValueError,OSError) as e:p.exit(1,str(e)+'\n')
    print('Created '+str(a.output)+' (private). Configure Google or email, or use the one-time administrator bootstrap.')
