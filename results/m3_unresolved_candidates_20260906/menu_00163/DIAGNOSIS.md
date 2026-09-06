# m=3, (p1,p2)=(0.20,0.55): not a sampling-only failure

Original complete failed output, strategy and checkpoint copied without
modifying the active search. Parent `request.json` and `support.npz` are the
same frozen search inputs as the previously archived cases in this directory.

Training finished at 700 iterations, unknown histories 0. Maximum retention
regret is 0.0012275670362209487, and retention supported-action gap is
0.0187100599942227. Both exceed their unchanged tolerances (0.00075, 0.0015).
The two independent audits have zero unresolved checks but retention regret
upper bounds 0.0012329662934530204 and 0.0012333234204227215.

In the last 30 logged zero-temperature iterations, maximum regret ranged
from 0.00004869719124744876 to 0.003974438803987922. It repeatedly fell then
jumped, rather than converging. This describes observed iteration behavior,
not a proven dynamical period or a proof that no equilibrium exists.

Do not repair this by simply increasing reporting samples or applying the
zero-retention rule: high-price retention is already zero. A subsequent
algorithmic repair must preserve the model and explicitly document a common
equilibrium selection rule; this archive itself makes no acceptance claim.
