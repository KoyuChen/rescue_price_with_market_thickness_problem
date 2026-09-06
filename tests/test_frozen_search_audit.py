import math
import tempfile
import unittest
from pathlib import Path
from audit_frozen_search_menu import audit_plan, validate_output, verify_hashes
from rescue_solver.storage import digest


class FrozenSearchAuditTests(unittest.TestCase):
    def test_plan_fixed_and_error_spending(self):
        a = audit_plan(3,164)
        self.assertEqual(a, audit_plan(3,164))
        self.assertEqual(a['count_draws'],5000000)
        self.assertNotEqual(*a['seeds'])
        self.assertAlmostEqual(audit_plan(1,0)['alpha_per_replicate']*6*2*math.pi**2/6,.001)

    def test_refuses_source_overlap(self):
        for output in ('/tmp/search','/tmp/search/audit','/tmp'):
            with self.assertRaises(ValueError): validate_output('/tmp/search',output)
        validate_output('/tmp/search','/tmp/audit')

    def test_hash_verification_detects_wrong_digest(self):
        # Use this immutable test source rather than writing test fixtures.
        path = Path(__file__)
        verify_hashes(path.parent,{path.name:digest(path)})
        with self.assertRaises(ValueError): verify_hashes(path.parent,{path.name:'0'*64})
