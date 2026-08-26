"""Deterministic regression tests for the numerical falsification engine."""

from __future__ import annotations

import math
import unittest

import numpy as np

from equilibria import find_equilibria_fast, isolate_equilibria_mp, pessimistic_completion_fast
from geometry import (
    certify_geometry_optimum_mp,
    geometry_point,
    optimize_geometry,
    zero_plateau_threshold,
)
from model import (
    Params,
    cutoff_residual,
    cutoff_residual_array,
    flat_completion,
    local_coefficient,
    phi,
)
from noentry import identity_error, lower_p_branch, q_first_order_residual
from optimize import Settings, optimize_announced


class EngineTests(unittest.TestCase):
    def test_phi_at_zero(self) -> None:
        self.assertEqual(phi(0.0), 1.0)
        self.assertAlmostEqual(phi(1e-10), 1 - 0.5e-10, places=15)

    def test_vectorized_residual_matches_scalar(self) -> None:
        rng = np.random.default_rng(20260825)
        for _ in range(100):
            par = Params(10 ** rng.uniform(-2, 2), rng.random(), rng.uniform(0.1, 0.95), rng.random())
            p1 = rng.uniform(0.0, 0.9)
            p2 = rng.uniform(p1, 1.0)
            aa = np.linspace(0.0, p1, 21)
            vec = cutoff_residual_array(aa, p1, p2, par)
            scalar = np.array([cutoff_residual(float(a), p1, p2, par) for a in aa])
            self.assertLess(np.max(np.abs(vec - scalar)), 3e-15)

    def test_flat_unique_and_completion(self) -> None:
        for par in [Params(2, 0.8, 0.7, 0), Params(2, 0.8, 0.7, 0.4)]:
            p = 0.3
            val, eq, _ = pessimistic_completion_fast(p, p, par, grid_size=129)
            self.assertEqual(eq.cutoffs, (p,))
            self.assertAlmostEqual(val, flat_completion(p, par), places=15)

    def test_noentry_reduction_identity(self) -> None:
        par = Params(2, 0.8, 0.7, 0)
        for a in np.linspace(0, 0.3, 31):
            self.assertLess(abs(identity_error(float(a), 0.3, 0.5, par)), 2e-15)

    def test_fast_and_mp_roots(self) -> None:
        par = Params(2, 0.8, 0.7, 0)
        fast = find_equilibria_fast(0.3, 0.5, par, grid_size=129)
        high = isolate_equilibria_mp("0.3", "0.5", par, dps=65, box_tol="1e-18")
        self.assertFalse(high.unresolved)
        self.assertEqual(len(fast.cutoffs), len(high.cutoffs))
        self.assertLess(abs(fast.cutoffs[0] - float(high.cutoffs[0])), 2e-14)

    def test_geometry_matches_nested_optimizer(self) -> None:
        par = Params(2, 0.8, 0.7, 0)
        g = optimize_geometry(par, grid_size=121)
        nested = optimize_announced(
            par,
            Settings(p1_grid=13, p2_grid=17, root_grid=65, local_refinements=1,
                     xatol=1e-7, diagnostics=False),
        )
        self.assertLess(abs(g.dynamic_value - nested.best.value), 2e-13)
        self.assertLess(abs(q_first_order_residual(g.point.a, g.point.q, par)), 2e-13)

    def test_PQJ_implements_cutoff(self) -> None:
        par = Params(10, 1, 0.9, 0)
        for a in np.linspace(0.01, 0.89, 30):
            z = geometry_point(float(a), par)
            self.assertLess(a, z.p)
            self.assertLess(z.p, z.q)
            self.assertLess(z.q, par.beta)
            self.assertLess(abs(cutoff_residual(float(a), z.p, z.q, par)), 2e-14)

    def test_P0_equals_pz(self) -> None:
        par = Params(2, 0.8, 0.7, 0)
        pz, _, _ = zero_plateau_threshold(par)
        self.assertLess(abs(geometry_point(0.0, par).p - pz), 2e-15)

    def test_local_derivative(self) -> None:
        par, p, eps = Params(2, 0.8, 0.7, 0), 0.3, 1e-7
        val, _, _ = pessimistic_completion_fast(p, p + eps, par, grid_size=161)
        quotient = (val - flat_completion(p, par)) / eps
        self.assertLess(abs(quotient / local_coefficient(p, par) - 1), 1e-5)

    def test_endpoint_cloud_not_multiple_J_maxima(self) -> None:
        for par in [Params(0.3, 1, 0.9, 0), Params(1e-5, 1, 0.5, 0)]:
            out = optimize_geometry(par, grid_size=161)
            self.assertEqual(len(out.local_maxima), 1)

    def test_high_precision_critical_gain(self) -> None:
        par = Params(1e-5, 1, 0.5, 0)
        g = optimize_geometry(par)
        cert = certify_geometry_optimum_mp(par, g.point.a, dps=70)
        ratio = float(cert.escalation_value / (1e-5 ** 4))
        self.assertLess(abs(ratio - 1 / 2048), 5e-9)


if __name__ == "__main__":
    unittest.main()

