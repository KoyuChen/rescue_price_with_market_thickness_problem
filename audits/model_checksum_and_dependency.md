# Model checksum and dependency DAG

Status: frozen baseline for the long-run audit.

## Primitives

- One potential request, two periods, public thickness $m>0$.
- Platform commits before private information to $(p_1,p_2)$ with
  $0\le p_1\le p_2\le1$; $p_2$ is failure-contingent and cannot be revised.
- Rider value $v\sim U[0,1]$; period-2 service value is $\beta v$,
  $\beta\in(0,1)$.
- Request-perspective incumbent population $N^I\sim\operatorname{Pois}(m)$.
  Realized $N^I$ is latent to platform, rider, and each driver.
- Conditional on a focal incumbent, the rival count is
  $\operatorname{Pois}(m)$ (Palm/Slivnyak), not
  $N^I-1\mid N^I\ge1$.
- Incumbent costs $c_i\sim U[0,1]$, fixed across periods.
- First-period drivers move simultaneously; multiple acceptors are uniformly
  rationed. Only the selected driver receives payment and incurs cost.
- After universal rejection, the rider observes failure only and chooses
  abandon, repeat $p_1$, or activate $p_2$.
- Each incumbent survives independently with probability $\alpha$.
  Fresh supply is $\operatorname{Pois}(\gamma m)$ with iid uniform costs.
- Payment is a rider-to-selected-driver transfer. Platform objective is
  unconditional completion per potential request.
- Baseline equilibrium scope: anonymous symmetric pure-cutoff WPBE.
- Conservative policy value minimizes only over that cutoff-WPBE
  correspondence, not over every mixed/asymmetric WPBE.

## Tie-breaking primitives

- A rider with $v\ge p_1$ posts when indifferent; a type below $p_1$ does not.
- Whenever the maximal continuation payoff is zero, repeat is chosen when
  $\beta v-p_1\ge0$ and abandon otherwise. This includes a positive-measure
  abandon/repeat tie when repeat has zero coverage.
- If $p_2=p_1$, repeat is selected over nominal escalation.
- If repeat and strict rescue tie at a positive payoff, rescue is selected.
- At an interior driver cutoff the cutoff type accepts; at $a=0$ the zero-cost
  cutoff type rejects; at $a=p_1$ the cutoff type accepts.
- At $p_1=0$, use the lower-boundary reject condition only. At $(1,1)$ define
  the natural zero-demand extension $\mathcal E(1,1)=\{1\}$ and $M=0$.

## Forbidden silent changes

- No policy or strategy may condition on realized $N^I$.
- No replacement of Palm rivals by ordinary truncation.
- No switch from WPBE to SPE.
- No profit/welfare objective in the baseline.
- No automatic rescue in place of the rider's continuation decision.
- No first-response-wins rule in the baseline.
- No claim that a symmetric-cutoff minimum is a worst-PBE value.

## Dependency DAG

1. Primitives and timing.
2. Information sets and Bayes/Palm beliefs.
3. Terminal acceptance and post-failure supply laws.
4. Rider posting and continuation strategy.
5. Focal driver accept/wait payoffs.
6. Single crossing and cutoff best responses.
7. Equilibrium correspondence $\mathcal E$.
8. Branch completion $M$ and conservative menu value.
9. Flat benchmark.
10. Local perturbation around flat.
11. Global menu design and attainment.
12. Thickness regularity, endpoints, and shape.
13. Contribution and managerial interpretation.

Any correction at level $k$ reopens every downstream level.
