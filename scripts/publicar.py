#!/usr/bin/env python3
"""Publica HTML y recupera comentarios del portal Bottifact con una conexión personal."""
import argparse
import getpass
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONFIG=Path.home()/'.config/bottifact/portal.json'

def request(base, token, path, data=None):
    req=urllib.request.Request(base+path,data=json.dumps(data).encode() if data is not None else None,
        headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
    # No enviar la conexión a otro destino mediante una redirección.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*args,**kwargs):return None
    try:
        with urllib.request.build_opener(NoRedirect).open(req,timeout=60) as response:return json.load(response)
    except urllib.error.HTTPError as e:
        try:message=json.load(e).get('detail','Error del portal')
        except (ValueError,AttributeError):message='Error del portal'
        raise SystemExit(str(e.code)+': '+str(message)) from None
    except urllib.error.URLError:raise SystemExit('No se pudo conectar al portal. Revisa la dirección y la red.') from None

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--config',type=Path,default=CONFIG)
    sub=p.add_subparsers(dest='command',required=True)
    c=sub.add_parser('conectar');c.add_argument('--servidor',required=True);c.add_argument('--token-archivo',type=Path)
    c=sub.add_parser('publicar');c.add_argument('--archivo',type=Path,required=True);c.add_argument('--titulo',required=True);c.add_argument('--espacio',default='Personal');c.add_argument('--artefacto-id')
    c=sub.add_parser('comentarios');c.add_argument('--artefacto-id');c.add_argument('--abiertos',action='store_true');c.add_argument('--salida',type=Path)
    sub.add_parser('estado');sub.add_parser('listar');args=p.parse_args()
    if args.command=='conectar':
        base=args.servidor.rstrip('/');url=urllib.parse.urlparse(base)
        if url.scheme!='https' or not url.netloc or url.path or url.query or url.fragment or url.username:raise SystemExit('Usa el origen HTTPS del portal, sin rutas ni credenciales.')
        token=args.token_archivo.read_text().strip() if args.token_archivo else getpass.getpass('Token personal (oculto): ')
        user=request(base,token,'/api/session')['user']
        if not user or not user['verified']:raise SystemExit('La conexión requiere una cuenta verificada.')
        args.config.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        fd=os.open(args.config,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600);os.fchmod(fd,0o600)
        with os.fdopen(fd,'w') as f:json.dump({'server':base,'token':token},f)
        print('Conexión guardada para '+user['email']+'. No se incluye en el skill ni en los artefactos.');return
    if not args.config.exists():raise SystemExit('Primero conecta tu cuenta con: publicar.py conectar --servidor https://artifacts.botto.is')
    if args.config.stat().st_mode&0o077:raise SystemExit('La conexión debe ser privada: chmod 600 '+str(args.config))
    config=json.loads(args.config.read_text());base=config['server'];token=config['token']
    if args.command=='publicar':
        if args.archivo.stat().st_size>20*1024*1024:raise SystemExit('El HTML supera 20 MB.')
        aid=args.artefacto_id
        if aid and (len(aid)!=32 or any(x not in '0123456789abcdef' for x in aid)):raise SystemExit('ID de artefacto inválido.')
        result=request(base,token,'/api/artifacts'+('/'+aid+'/versions' if aid else ''),{'title':args.titulo,'space':args.espacio,'html':args.archivo.read_text()})
    elif args.command=='comentarios':
        params={'scope':'open' if args.abiertos else 'all'}
        if args.artefacto_id:params['artifact']=args.artefacto_id
        text=request(base,token,'/api/review/export?'+urllib.parse.urlencode(params))['text']
        if args.salida:args.salida.write_text(text+'\n');print(str(args.salida))
        else:print(text)
        return
    else:result=request(base,token,'/api/session' if args.command=='estado' else '/api/artifacts')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
