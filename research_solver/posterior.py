"""Additional structural certificates using the actual hidden route support."""
import numpy as np


def supported_hidden_offpath(model,p1,q_values,new_lam):
    """If even the best POSSIBLE hidden offer cannot improve immediate trade.

    This is a proof over all rival counts, not a cutoff on small probabilities.
    Positive hidden intensity, however tiny, stays in the support.
    """
    answer=np.zeros((model.S,len(q_values)),dtype=bool)
    for iq,q in enumerate(q_values):
        active=np.asarray(new_lam[iq])>0
        if not active.any():
            answer[:,iq]=True
            continue
        best_hidden_cost=float(q+np.min(model.beta_detour[active]))
        if best_hidden_cost>=model.par.beta+1e-12:
            answer[:,iq]=True
        else:
            answer[:,iq]=best_hidden_cost>=model.par.beta*(p1+model.par.ell*(1-model.s))+1e-12
    return answer


def old_win_zero_certificates(model,p1,q_values,new_lam):
    """Prove an old offer is never acceptable WHEN continuation is chosen.

    Let g_s=p1+beta*d_s and B_s=E[(g_s-G_hidden_min)_+]. Give all observed
    early drivers free, certain retention to upper-bound waiting utility.
    For v >= p1/beta+d_s, waiting minus immediate is at most
    B_s-(1-beta)*(v-d_s), maximized at that lower endpoint.
    Therefore B_s < (1-beta)*p1/beta proves zero old win probability at q,
    even when the q history itself has positive probability. This must NOT
    be confused with a zero-probability history or a zero entry intensity.
    """
    old_cost=p1+model.beta_detour
    margin=(1-model.par.beta)*p1/model.par.beta
    result=np.zeros((model.S,len(q_values)),dtype=bool)
    for iq,q in enumerate(q_values):
        lam=np.asarray(new_lam[iq])
        higher=np.cumsum(lam[::-1])[::-1]-lam
        min_mass=np.exp(-higher)*(-np.expm1(-lam))
        gains=np.maximum(old_cost[:,None]-(q+model.beta_detour)[None,:],0) @ min_mass
        result[:,iq]=(gains+1e-12<margin)|(old_cost>=model.par.beta+1e-12)
    return result
