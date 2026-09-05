"""Independent no-hidden equilibrium branch; diagnostic, NEVER price selection.

This branch exists for flat AND off-diagonal menus. Choosing it just for flat
while selecting a different rescue branch would change the comparison rule.
"""
import numpy as np
from rescue_solver.core import Profile


def all_early_profile(model, p1, p2):
    q=np.unique(np.round([p1,p2],12))
    return Profile((model.a<=p1).astype(float),np.zeros_like(model.a),
                   np.zeros((len(q),model.C,model.S)),q,{})


def no_hidden_completion(model, m, p1, continuous_cost=False):
    if not np.isfinite(m) or m<=0 or not 0<=p1<=model.par.p_bar:
        raise ValueError('Invalid thickness or first price')
    if continuous_cost:
        participation=np.clip(p1-model.par.kappa*(1-model.s),0,1)
    else:
        participation=np.sum(model.fc[:,None]*(model.a<=p1),axis=0)
    lam=m*model.fs*participation
    higher=np.cumsum(lam[::-1])[::-1]-lam
    demand=np.maximum(1-p1-model.par.ell*(1-model.s),0)
    return float(np.sum(np.exp(-higher)*(-np.expm1(-lam))*demand))
