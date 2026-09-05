"""Feasibility-preserving lifts between cost probability partitions."""
import numpy as np
from rescue_solver.core import Profile


def lift_profile(model,original_edges,profile,p1,p2):
    edges=np.asarray(original_edges)
    indices=np.minimum(np.searchsorted(edges,model.c,side='right')-1,len(edges)-2)
    e=profile.sigma_e[indices].copy();h=profile.sigma_h[indices].copy()
    r=profile.retain[:,indices].copy()
    e[model.a>p1+1e-12]=0
    h[model.a>p2+1e-12]=0
    r[:,model.par.delta*p1-model.a<=0]=0
    return Profile(e,h,r,profile.q_values.copy(),{})
