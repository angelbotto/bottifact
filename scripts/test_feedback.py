"""Feedback must preserve evidence without sending or overwriting private data."""
import json
import os
from pathlib import Path
import tempfile
import unittest
from feedback import write_handoff

class FeedbackTests(unittest.TestCase):
    def response(self):
        return {'text': 'Artifact sample · version v1 · selected quote · comment', 'items': [
            {'body': 'Please explain this total', 'context': {'artifact': 'sample', 'version': 'v1',
             'version_sha256': 'abc', 'quote': 'total', 'source': {'agent': 'codex', 'session': 'session-example', 'device': 'demo-device'}}}]}

    def test_private_bundle_preserves_context_without_execution(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'handoff'
            response = self.response()
            result = write_handoff(response, target)
            context = json.loads((target / 'context.json').read_text())
            self.assertEqual(context['items'], response['items'])
            self.assertEqual(result['target']['session'], 'session-example')
            self.assertFalse(context['executed'])
            self.assertIn(response['text'], (target / 'feedback.md').read_text())
            if os.name == 'posix':
                self.assertEqual(target.stat().st_mode & 0o777, 0o700)
                self.assertEqual((target / 'context.json').stat().st_mode & 0o777, 0o600)
            with self.assertRaises(FileExistsError): write_handoff(response, target)

    def test_ambiguous_or_missing_origin_requires_explicit_target(self):
        response = self.response()
        response['items'].append({'context': {'source': {'agent': 'hermes', 'session': 'second'}}})
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'handoff'
            with self.assertRaises(ValueError): write_handoff(response, target)
            self.assertFalse(target.exists())
            result = write_handoff(response, target, 'claude', 'chosen-session')
            self.assertEqual(result['target']['session'], 'chosen-session')
            self.assertEqual(len(json.loads((target/'context.json').read_text())['origins']), 2)

    def test_empty_export_does_not_create_a_folder(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'handoff'
            with self.assertRaises(ValueError): write_handoff({'items': []}, target)
            self.assertFalse(target.exists())

if __name__ == '__main__': unittest.main()
