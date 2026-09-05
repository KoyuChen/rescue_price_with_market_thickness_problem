import unittest
import numpy as np
from rescue_solver.core import FixedSupportRescueModel,ModelParams
from rescue_solver.solver import Settings
from research_solver.high_precision import solve_high
from run_thick_markets import global_menus,local_menus,refined_route_edges


class ThickTests(unittest.TestCase):
    def test_global_grid_keeps_fine_flat_diagonals(self):
        menus=global_menus()
        self.assertEqual(len(menus),611)
        self.assertIn((.2125,.2125),menus)
        self.assertIn((.15,.35),menus)
        self.assertTrue(all(0<=a<=b<=1 for a,b in menus))

    def test_refined_routes_preserve_tail_edges(self):
        original=ModelParams().route_positive_quantile_edges
        new=refined_route_edges(original,48)
        self.assertEqual(len(new),48)
        self.assertTrue(set(original)<=set(new))
        self.assertTrue(np.all(np.diff(new)>0))

    def test_local_prices_respect_order(self):
        prices=local_menus([dict(p1=.15,p2=.35)],.0025,.005)
        self.assertEqual(len(prices),25)
        self.assertIn((.15,.35),prices)

    def test_high_solver_small_zero_price_case(self):
        model=FixedSupportRescueModel(ModelParams(route_draws=10),np.array([.2]),
            np.array([1.]),np.array([1.]),np.array([1.]))
        settings=Settings(train_counts=100,audit_counts=1000,schedule=((0.,30,.5),))
        _,result=solve_high(model,6,0,0,settings)
        self.assertTrue(result['numerical_checks_passed'])
        self.assertFalse(result['external_price_optimized'])


if __name__=='__main__':unittest.main()
