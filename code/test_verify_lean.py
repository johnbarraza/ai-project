"""Regressions for source receipts on Windows and Linux checkouts."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import unittest

from verify_lean import source_sha256, check_official_snapshot


class SourceReceiptTests(unittest.TestCase):
    def test_recorded_acceptance_requires_unchanged_successful_validation(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'docs').mkdir()
            (root/'lean').mkdir()
            receipt = root/'lean/FINAL_CLOSURE_RECEIPT.md'
            receipt.write_text('Synthetic receipt fixture\n',encoding='utf-8')
            output = root/'docs/closure-check.txt'
            output.write_text('Synthetic validator output fixture\n',encoding='utf-8')
            validation = {'exit_code':0,'output':'docs/closure-check.txt'}
            manifest = {
                'hash_format':'sha256-utf8-lf-for-text',
                'artifacts':{'lean/FINAL_CLOSURE_RECEIPT.md':source_sha256(receipt)},
                'supplementary_artifacts':{'docs/closure-check.txt':source_sha256(output)},
                'checks':[validation],'status':'accepted',
                'official_contribution_workflow_complete':True,
                'accepted_closure_receipt_present':True,'closure_validation':validation,
            }
            path = root/'docs/lean-workflow.json'
            path.write_text(json.dumps(manifest),encoding='utf-8')
            self.assertTrue(check_official_snapshot(root)['official_contribution_workflow_complete'])
            validation['exit_code'] = 1
            path.write_text(json.dumps(manifest),encoding='utf-8')
            with self.assertRaises(AssertionError):
                check_official_snapshot(root)
            validation['exit_code'] = 0
            path.write_text(json.dumps(manifest),encoding='utf-8')
            output.write_text('Changed output\n',encoding='utf-8')
            with self.assertRaisesRegex(AssertionError,'check output changed'):
                check_official_snapshot(root)

    def test_binary_artifact_preserves_exact_bytes(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'docs').mkdir()
            (root/'lean').mkdir()
            path = root/'lean/diagram.pdf'
            path.write_bytes(b'%PDF-test\x00\r\nraw bytes\n')
            manifest = {
                'hash_format':'sha256-utf8-lf-text-and-raw-binary',
                'artifacts':{'lean/diagram.pdf':hashlib.sha256(path.read_bytes()).hexdigest()},
                'binary_artifacts':['lean/diagram.pdf'],'checks':[],
                'status':'open','official_contribution_workflow_complete':False,
                'accepted_closure_receipt_present':False,
            }
            (root/'docs/lean-workflow.json').write_text(json.dumps(manifest),encoding='utf-8')
            self.assertEqual(check_official_snapshot(root)['status'],'open')
            manifest['status'] = 'accepted'
            manifest['official_contribution_workflow_complete'] = True
            manifest['accepted_closure_receipt_present'] = True
            (root/'docs/lean-workflow.json').write_text(json.dumps(manifest),encoding='utf-8')
            with self.assertRaises(AssertionError):
                check_official_snapshot(root)
            manifest['status'] = 'open'
            manifest['official_contribution_workflow_complete'] = False
            manifest['accepted_closure_receipt_present'] = False
            (root/'docs/lean-workflow.json').write_text(json.dumps(manifest),encoding='utf-8')
            path.write_bytes(path.read_bytes().replace(b'\r\n',b'\n'))
            with self.assertRaisesRegex(AssertionError,'snapshot changed'):
                check_official_snapshot(root)

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
