"""Equivalent array kernels: same types, count draws, quadrature and tolerances.

Only reusable price/profile coefficients and matrix operations change.
Floating-point reduction order can differ; equivalence is numerical, not bitwise.
Original running sources remain unchanged.
"""
import numpy as np
from rescue_solver.core import FixedSupportRescueModel
from history_envelope import EnvelopeHistoryEvaluator


class VectorizedTieModel(FixedSupportRescueModel):
    def _tie_factor(self, counts, equal_old_mask, old_r, lambda_equal_new):
        if not np.any(equal_old_mask) and lambda_equal_new <= 1e-14:
            return np.ones(len(counts))
        n_equal=counts[:,equal_old_mask]
        r_equal=old_r[equal_old_mask]
        log_g=np.broadcast_to(lambda_equal_new*(self.tie_t-1),
                              (len(counts),len(self.tie_t))).copy()
        if n_equal.shape[1]:
            bases=np.clip(1-r_equal[:,None]+r_equal[:,None]*self.tie_t,1e-14,1.)
            log_g += n_equal @ np.log(bases)
        return np.exp(log_g) @ self.tie_w


class CachedEnvelopeEvaluator(EnvelopeHistoryEvaluator):
    def value_intervals(self, counts, p1, q_values, old_r, lambda_new):
        model=self.model; beta=model.par.beta
        key=(float(p1),np.asarray(q_values).tobytes(),
             np.asarray(old_r).tobytes(),np.asarray(lambda_new).tobytes())
        if getattr(self,'_kernel_key',None) != key:
            thresholds=[0.,1.]
            thresholds.extend(p1+model.par.ell*(1-model.s))
            for q in q_values: thresholds.extend((q+model.beta_detour)/beta)
            edges=np.unique(np.clip(thresholds,0.,1.))
            left,right=edges[:-1],edges[1:];mid=(left+right)/2
            kernels=[]
            for iq,q in enumerate(q_values):
                go,gn=p1+model.beta_detour,q+model.beta_detour
                levels=np.unique(np.round(np.r_[go,gn],12))
                log_no=np.log(np.clip(1-old_r[iq],1e-14,1.))
                old_mask=go[:,None]<=levels[None,:]+1e-11
                new_mask=gn[:,None]<=levels[None,:]+1e-11
                # Sum the same nonnegative intensities once per profile.
                new_cumulative=np.array([lambda_new[iq][new_mask[:,j]].sum()
                                         for j in range(len(levels))])
                kernels.append((levels,log_no[:,None]*old_mask,new_cumulative,
                                beta*mid[:,None]>levels[None,:]))
            self._kernel_key=key;self._kernel=(left,right,mid,kernels)
        left,right,mid,kernels=self._kernel
        n,B,A=len(counts),len(mid),1+len(q_values)
        slope,bias=np.zeros((n,B,A)),np.zeros((n,B,A))
        best=model.S-1-np.argmax(counts[:,::-1]>0,axis=1)
        threshold=p1+model.par.ell*(1-model.s[best])
        active=(counts.sum(axis=1)>0)[:,None]&(mid[None,:]>threshold[:,None])
        slope[:,:,0]=active;bias[:,:,0]=-active.astype(float)*threshold[:,None]
        for iq,(levels,log_weights,new_cumulative,enabled) in enumerate(kernels):
            log_none=counts@log_weights-new_cumulative
            cdf=1-np.exp(np.minimum(log_none,0))
            mass=np.diff(np.column_stack([np.zeros(n),cdf]),axis=1)
            slope[:,:,iq+1]=beta*(mass@enabled.T)
            bias[:,:,iq+1]=-(mass*levels)@enabled.T
        cuts=[np.broadcast_to(left,(n,B)),np.broadcast_to(right,(n,B))]
        for a in range(A):
            for b in range(a+1,A):
                den=slope[:,:,a]-slope[:,:,b]
                cross=np.divide(bias[:,:,b]-bias[:,:,a],den,
                    out=np.broadcast_to(left,(n,B)).copy(),where=np.abs(den)>1e-15)
                cuts.append(np.clip(cross,left,right))
        for a in range(A):
            cross=np.divide(1e-12-bias[:,:,a],slope[:,:,a],
                out=np.broadcast_to(left,(n,B)).copy(),where=slope[:,:,a]>0)
            cuts.append(np.clip(cross,left,right))
        cuts=np.sort(np.stack(cuts,axis=-1),axis=-1)
        widths=np.diff(cuts,axis=-1);centers=(cuts[:,:,:-1]+cuts[:,:,1:])/2
        values=slope[:,:,None,:]*centers[:,:,:,None]+bias[:,:,None,:]
        action=np.argmax(values,axis=-1)
        action[np.max(values,axis=-1)<=1e-12]=-1
        lengths=np.stack([np.sum(widths*(action==a),axis=-1) for a in range(A)],axis=1)
        return lengths,mid
