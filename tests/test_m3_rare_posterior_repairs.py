import unittest

from run_m3_rare_posterior_repairs import CASES, MARKET, validate_case


class M3RarePosteriorRepairTests(unittest.TestCase):
    def test_plan_is_fixed_and_unique(self):
        self.assertEqual(MARKET, 3)
        self.assertEqual(CASES, (157, 158, 159))
        self.assertEqual(len(CASES), len(set(CASES)))

    def test_validator_rejects_wrong_or_passed_result(self):
        validate_case(157, {'m': 3, 'numerical_checks_passed': False})
        for ordinal, row in (
            (156, {'m': 3, 'numerical_checks_passed': False}),
            (157, {'m': 1, 'numerical_checks_passed': False}),
            (157, {'m': 3, 'numerical_checks_passed': True}),
        ):
            with self.assertRaises(ValueError):
                validate_case(ordinal, row)
