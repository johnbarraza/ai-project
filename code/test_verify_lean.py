"""Regressions for source receipts on Windows and Linux checkouts."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest

from verify_lean import source_sha256, check_official_snapshot


class SourceReceiptTests(unittest.TestCase):
    def test_snapshot_rejects_modified_file(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'docs').mkdir()
            (root/'lean').mkdir()
            source = root/'lean/build.txt'
            source.write_text('Build completed successfully.\n',encoding='utf-8')
            manifest = {
                'hash_format':'sha256-utf8-lf-for-text',
                'artifacts':{'lean/build.txt':source_sha256(source)},
                'checks':[{'exit_code':0,'output':'lean/build.txt'}],
                'status':'open','official_contribution_workflow_complete':False,
                'accepted_closure_receipt_present':False,
            }
            (root/'docs/lean-workflow.json').write_text(json.dumps(manifest),encoding='utf-8')
            self.assertEqual(check_official_snapshot(root)['status'],'open')
            source.write_text('A different result.\n',encoding='utf-8')
            with self.assertRaisesRegex(AssertionError,'snapshot changed'):
                check_official_snapshot(root)

    def test_checkout_line_endings_preserve_receipt(self):
        with TemporaryDirectory() as folder:
            a, b = Path(folder)/'a.lean', Path(folder)/'b.lean'
            a.write_bytes('theorem identity (x : ℝ) : x = x := by\n  rfl\n'.encode())
            b.write_bytes(a.read_bytes().replace(b'\n', b'\r\n'))
            self.assertEqual(source_sha256(a), source_sha256(b))
            b.write_bytes(a.read_bytes().replace(b'x = x', b'x = 0'))
            self.assertNotEqual(source_sha256(a), source_sha256(b))


if __name__ == '__main__':
    unittest.main()
