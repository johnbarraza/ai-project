"""Reject a positive curvature, altered model identity or inflated theorem claim."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from numerical_validation import check_native_report

DATA = Path(__file__).resolve().parent/'data'


class NativeAuditRegression(unittest.TestCase):
    def setUp(self):
        self.report = json.loads((DATA/'matlab_value_equilibrium_audit.json').read_text())
        self.experiments = json.loads((DATA/'paper_ge_experiments.json').read_text())

    def test_positive_curvature_rejected_despite_success_flags(self):
        changed = deepcopy(self.report)
        changed['cases'][0]['shape']['maximum_value_curvature'] = .001
        with self.assertRaises(AssertionError):
            check_native_report(changed,self.experiments)

    def test_different_saved_model_rejected(self):
        self.report['cases'][0]['mat_sha256'] = '0'*64
        with self.assertRaises(AssertionError):
            check_native_report(self.report,self.experiments)

    def test_numerical_audit_cannot_become_global_theorem(self):
        self.report['continuous_model_global_existence_proved'] = True
        with self.assertRaises(AssertionError):
            check_native_report(self.report,self.experiments)


if __name__ == '__main__':
    unittest.main()
