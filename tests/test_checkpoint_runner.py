from dataclasses import asdict
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import numpy as np
from rescue_solver.core import ModelParams, Profile
from rescue_solver.storage import digest
import run_checkpointed_markets as runner


class RunnerTests(unittest.TestCase):
    def test_completed_failed_menus_reused_and_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            np.savez(root/'support.npz',c=[.2],fc=[1.],s=[1.],fs=[1.])
            request=dict(source_identity={'sha256':{}},support_sha256=digest(root/'support.npz'),
                         model=asdict(ModelParams(route_draws=10)),m=[6],seed=100)
            def fake(model,m,p1,p2,settings,*args):
                profile=Profile(np.zeros((1,1)),np.zeros((1,1)),np.zeros((2,1,1)),
                                np.array([p1,p2]),{})
                return profile,dict(m=m,p1=p1,p2=p2,settings=asdict(settings),
                                    numerical_checks_passed=False,status='validation_blocked')
            with patch.object(runner,'solve_checkpointed',side_effect=fake) as solve:
                first=runner.worker((str(root),6,request))
                self.assertEqual(solve.call_count,2)
                second=runner.worker((str(root),6,request))
                self.assertEqual(solve.call_count,2)
                self.assertEqual(first,second)
                self.assertEqual(len(second['rows']),2)
                result_path=root/'m6/menu_00000/result.json'
                result=json.loads(result_path.read_text());result['p1']=.99
                result_path.write_text(json.dumps(result))
                with self.assertRaisesRegex(ValueError,'order mismatch'):
                    runner.worker((str(root),6,request))


if __name__=='__main__': unittest.main()
