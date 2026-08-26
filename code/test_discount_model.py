"""Regression tests for the incumbent-discount falsification engine."""

from __future__ import annotations

import math
import unittest

from discount_model import (
    DiscountParams,
    completion,
    corrected_local_coefficient,
    cutoff_residual,
    find_equilibria,
    flat_completion,
    geometry_point,
    isolate_equilibria_mp,
    mp,
    mp_cover,
    mp_geometry_point,
    mpf,
    pessimistic_value,
)
from model import Params, completion as baseline_completion, cutoff_residual as baseline_residual


class DiscountModelTests(unittest.TestCase):
    def test_delta_one_recovers_baseline(self) -> None:
        old = Params(2.3, 0.7, 0.8, 0.4)
        new = DiscountParams(2.3, 0.7, 0.8, 0.4, 1.0)
        for a in (0.0, 0.1, 0.27):
            self.assertAlmostEqual(
                cutoff_residual(a, 0.3, 0.6, new),
                baseline_residual(a, 0.3, 0.6, old),
                places=14,
            )
            self.assertAlmostEqual(
                completion(a, 0.3, 0.6, new),
                baseline_completion(a, 0.3, 0.6, old),
                places=14,
            )

    def test_completion_is_not_directly_discounted(self) -> None:
        low = DiscountParams(1.7, 0.8, 0.75, 0.2, 0.1)
        high = DiscountParams(1.7, 0.8, 0.75, 0.2, 0.9)
        self.assertEqual(completion(0.2, 0.3, 0.6, low), completion(0.2, 0.3, 0.6, high))
        self.assertNotEqual(cutoff_residual(0.2, 0.3, 0.6, low), cutoff_residual(0.2, 0.3, 0.6, high))

    def test_flat_cutoff_survives_discount(self) -> None:
        for delta in (1.0, 0.5, 0.01, 1e-8):
            par = DiscountParams(8, 0.9, 0.7, 0.3, delta)
            eq = find_equilibria(0.35, 0.35, par)
            self.assertEqual(eq.cutoffs, (0.35,))
            value, _, _ = pessimistic_value(0.35, 0.35, par)
            self.assertAlmostEqual(value, flat_completion(0.35, par), places=14)

    def test_noentry_geometry_independently_satisfies_follower_model(self) -> None:
        par = DiscountParams(2, 0.8, 0.7, 0, 0.5)
        for a in (0.0, 0.1, 0.3, 0.69):
            point = geometry_point(a, par)
            self.assertLessEqual(a, point.p)
            self.assertLess(point.p, point.q)
            self.assertLess(point.q, par.beta)
            if a > 0:
                self.assertAlmostEqual(cutoff_residual(a, point.p, point.q, par), 0.0, places=13)
            self.assertAlmostEqual(completion(a, point.p, point.q, par), point.value, places=13)

    def test_corrected_local_coefficient(self) -> None:
        par = DiscountParams(2, 0.8, 0.7, 0, 0.5)
        p, eps = 0.3, 1e-7
        value, _, _ = pessimistic_value(p, p + eps, par, grid_size=201)
        quotient = (value - flat_completion(p, par)) / eps
        claimed = corrected_local_coefficient(p, par)
        self.assertLess(abs(quotient / claimed - 1), 1e-6)

    def test_mp_root_bracket(self) -> None:
        par = DiscountParams(2, 0.8, 0.7, 0, 0.5)
        eq = isolate_equilibria_mp("0.3", "0.5", par, dps=70, box_tol="1e-20")
        self.assertEqual(len(eq.roots), 1)
        self.assertFalse(eq.unresolved)
        box = eq.roots[0]
        self.assertLess(box.f_lo * box.f_hi, 0)
        self.assertLess(box.hi - box.lo, mpf("1e-20"))

    def test_patient_thin_exact_candidate(self) -> None:
        with mp.workdps(70):
            m = mpf("1e-5")
            par = DiscountParams(float(m), 1, 0.9, 0, 0.5)
            _, _, value, _ = mp_geometry_point("0.3", par)
            x = mp.findroot(lambda z: mp.expm1(z) + z - m, m / 2)
            flat = (1 - x / m) * mp_cover(x)
            ratio = (value - flat) / m
            target = (3 * mp.sqrt(29) - 9) / 200
            self.assertLess(abs(ratio - target), mpf("3e-8"))

    def test_critical_thin_m_cubed_candidate(self) -> None:
        with mp.workdps(80):
            m = mpf("1e-5")
            par = DiscountParams(float(m), 1, 0.5, 0, 0.5)
            _, _, value, _ = mp_geometry_point(mpf("0.5") - m / 12, par)
            x = mp.findroot(lambda z: mp.expm1(z) + z - m, m / 2)
            flat = (1 - x / m) * mp_cover(x)
            ratio = (value - flat) / m**3
            self.assertLess(abs(ratio - mp.mpf(1) / 768), mpf("5e-9"))

    def test_delta_validation(self) -> None:
        with self.assertRaises(ValueError):
            DiscountParams(1, 1, 0.5, 0, 0).validate()


if __name__ == "__main__":
    unittest.main()

