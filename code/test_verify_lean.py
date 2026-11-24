"""Regressions for source receipts on Windows and Linux checkouts."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from verify_lean import source_sha256


class SourceReceiptTests(unittest.TestCase):
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
