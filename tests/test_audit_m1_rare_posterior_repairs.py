import unittest

from audit_m1_rare_posterior_repairs import CASES, fresh_seed


class M1RarePosteriorFreshAuditTests(unittest.TestCase):
    def test_seeds_are_fixed_unique_and_disjoint_from_original_audits(self):
        seeds = {fresh_seed(i, j) for i in CASES for j in (1, 2)}
        self.assertEqual(len(seeds), 6)
        originals = {
            4417508447802535971, 4417508447802640700,
            5214898762111280937, 5214898762111385666,
            7899570428069614170, 7899570428069718899,
        }
        self.assertTrue(seeds.isdisjoint(originals))

    def test_seed_rejects_unplanned_cases(self):
        for args in ((192, 1), (193, 0), (195, 3)):
            with self.assertRaises(ValueError):
                fresh_seed(*args)
