import unittest
from run_m1_rare_posterior_repairs import CASES,validate_case


class M1RarePosteriorRepairTests(unittest.TestCase):
    def test_cases_are_fixed_and_unique(self):
        self.assertEqual(CASES,(193,194,195));self.assertEqual(len(CASES),len(set(CASES)))

    def test_rejects_passed_or_wrong_case(self):
        validate_case(194,{'m':1,'numerical_checks_passed':False})
        for ordinal,row in [(192,{'m':1,'numerical_checks_passed':False}),
                            (194,{'m':3,'numerical_checks_passed':False}),
                            (194,{'m':1,'numerical_checks_passed':True})]:
            with self.assertRaises(ValueError):validate_case(ordinal,row)
