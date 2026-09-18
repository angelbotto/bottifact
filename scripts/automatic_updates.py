"""Opt-in per-user background updates for managed Margen libraries."""
import hashlib
import json
import os
from pathlib import Path
import plistlib
import subprocess
import sys


def configure(action, destination, home=None, platform=None, run=subprocess.run):
    home=Path(home or Path.home());platform=platform or sys.platform
    destination=Path(destination).absolute()
    label='is.botto.bottifact.updates.'+hashlib.sha256(str(destination).encode()).hexdigest()[:10]
    command=[sys.executable,str(destination/'scripts/update.py'),'--destination',str(destination),'--if-changed']
    logs=home/'.local/state/bottifact';logs.mkdir(parents=True,exist_ok=True);logs.chmod(0o700)
    if platform=='darwin':
        directory=home/'Library/LaunchAgents';path=directory/(label+'.plist')
        if action=='status':return {'configured':path.exists(),'scheduler':'launchd','interval_hours':6,'definition':str(path)}
        run(['launchctl','bootout','gui/'+str(os.getuid())+'/'+label],capture_output=True,check=False)
        if action=='disable':path.unlink(missing_ok=True);return {'configured':False,'scheduler':'launchd'}
        directory.mkdir(parents=True,exist_ok=True)
        for name in ['updates.log','updates-error.log']:
            log=logs/name;log.touch(exist_ok=True);log.chmod(0o600)
        data={'Label':label,'ProgramArguments':command,'RunAtLoad':True,'StartInterval':21600,
              'StandardOutPath':str(logs/'updates.log'),'StandardErrorPath':str(logs/'updates-error.log')}
        path.write_bytes(plistlib.dumps(data));path.chmod(0o600)
        result=run(['launchctl','bootstrap','gui/'+str(os.getuid()),str(path)],capture_output=True,text=True,check=False)
        if result.returncode:raise ValueError('La tarea está escrita, pero launchd no la activó. Ejecuta el comando desde una sesión de usuario abierta. '+result.stderr.strip())
        return {'configured':True,'scheduler':'launchd','interval_hours':6,'definition':str(path)}
    if platform.startswith('linux'):
        directory=home/'.config/systemd/user';service=directory/(label+'.service');timer=directory/(label+'.timer')
        if action=='status':return {'configured':timer.exists(),'scheduler':'systemd-user','interval_hours':6,'definition':str(timer)}
        if action=='disable':
            run(['systemctl','--user','disable','--now',label+'.timer'],capture_output=True,check=False)
            timer.unlink(missing_ok=True);service.unlink(missing_ok=True)
            run(['systemctl','--user','daemon-reload'],check=True);return {'configured':False,'scheduler':'systemd-user'}
        directory.mkdir(parents=True,exist_ok=True)
        if any('\n' in arg or '\r' in arg for arg in command):raise ValueError('Ruta de comando no válida.')
        quoted=' '.join('"'+arg.replace('\\','\\\\').replace('"','\\"').replace('%','%%').replace('$','$$')+'"' for arg in command)
        service.write_text('[Unit]\nDescription=Update the managed Margen skill\n[Service]\nType=oneshot\nExecStart='+quoted+'\n')
        timer.write_text('[Unit]\nDescription=Check Margen every six hours\n[Timer]\nOnStartupSec=5m\nOnUnitActiveSec=6h\nRandomizedDelaySec=5m\n[Install]\nWantedBy=timers.target\n')
        run(['systemctl','--user','daemon-reload'],check=True);run(['systemctl','--user','enable','--now',label+'.timer'],check=True)
        return {'configured':True,'scheduler':'systemd-user','interval_hours':6,'definition':str(timer)}
    raise ValueError('Programación automática disponible en macOS y Linux con systemd de usuario. Usa update manualmente en otros entornos.')
