"""Scheduler contracts; never touches the real user's scheduler."""
import json
from pathlib import Path
import plistlib
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from automatic_updates import configure
import update

class AutomaticUpdateTests(unittest.TestCase):
    def test_mac_keeps_paths_as_arguments_and_can_disable(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp);dest=home/'Library with spaces'
            calls=[]
            def run(args,**kwargs):
                calls.append(args);return subprocess.CompletedProcess(args,0,'','')
            result=configure('enable',dest,home,'darwin',run)
            data=plistlib.loads(Path(result['definition']).read_bytes())
            self.assertEqual(data['ProgramArguments'][-3:],[ '--destination',str(dest),'--if-changed'])
            self.assertEqual(data['StartInterval'],21600)
            self.assertNotIn('--server',data['ProgramArguments'])
            self.assertTrue(configure('status',dest,home,'darwin',run)['configured'])
            configure('disable',dest,home,'darwin',run)
            self.assertFalse(configure('status',dest,home,'darwin',run)['configured'])
    def test_linux_timer_is_per_user_and_escapes_unit_expansion(self):
        with tempfile.TemporaryDirectory() as temp:
            home=Path(temp);dest=home/'Library % $ space'
            def run(args,**kwargs):return subprocess.CompletedProcess(args,0,'','')
            result=configure('enable',dest,home,'linux',run)
            service=Path(result['definition']).with_suffix('.service').read_text()
            self.assertIn('%% $$ space',service);self.assertIn('--if-changed',service)
            self.assertIn('OnUnitActiveSec=6h',Path(result['definition']).read_text())
            configure('disable',dest,home,'linux',run)
            self.assertFalse(Path(result['definition']).exists())
    def test_unchanged_package_skips_installer_and_preserves_server(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'library';dest.mkdir();(dest/'VERSION.json').write_text('{}')
            settings=dest.parent/'.library-update.json';settings.write_text(json.dumps({'servidor':'https://docs.example.org','sha256':'a'*64}))
            with patch.object(sys,'argv',['update','--destination',str(dest),'--if-changed']),patch.object(update,'fetch',return_value=('a'*64).encode()) as fetch,patch.object(update.subprocess,'run') as run:
                update.main();run.assert_not_called();self.assertEqual(fetch.call_count,1)
                self.assertEqual(update.ORIGIN,'https://docs.example.org')
            self.assertEqual(json.loads(settings.read_text())['servidor'],'https://docs.example.org')
    def test_local_installation_cannot_silently_enable_network_updates(self):
        with tempfile.TemporaryDirectory() as temp:
            dest=Path(temp)/'library';dest.mkdir();(dest.parent/'.library-update.json').write_text('{"local":true}')
            with patch.object(sys,'argv',['update','--destination',str(dest),'--auto','enable']):
                with self.assertRaisesRegex(ValueError,'local'):update.main()
            with patch.object(sys,'argv',['update','--destination',str(dest),'--auto','status']),patch('automatic_updates.configure',return_value={'configured':False}) as configure_mock:
                update.main();configure_mock.assert_called_once()

if __name__=='__main__':unittest.main()
