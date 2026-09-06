"""Replay the inline read-only diagnostic; run from repo root with PYTHONPATH=."""
import json,numpy as np
from pathlib import Path
from accelerated_evaluator import VectorizedTieModel
from rescue_solver.config import build_model_params
from rescue_solver.storage import load_profile
from rescue_solver.solver import Settings
from rare_history_evaluator import RareHistoryEvaluator
root=Path('results/m3_unresolved_candidates_20260906')
request=json.loads((root/'request.json').read_text())
with np.load(root/'support.npz') as z:
    model=VectorizedTieModel(build_model_params(request['model']),*[z[k] for k in ('c','fc','s','fs')])
x,w=np.polynomial.legendre.leggauss(64);model.tie_t=(x+1)/2;model.tie_w=w/2
profile=load_profile('results/zero_retention_m3_menu157_20260906/m3_menu_00157/profile.npz')
ev=RareHistoryEvaluator(model,Settings()).evaluate(3,.2,.25,profile,50000,202609061034)
print(json.dumps(dict(unknown=ev['unknown_feasible_history_count'],records=ev['rare_history_resolution'])))
