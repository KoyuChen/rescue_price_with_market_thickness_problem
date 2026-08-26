# 当前版本的 Theory Foundation

下面这套可以作为新稿的理论主干。核心变化是：

公共状态是 market thickness m,N∼Pois⁡(m) 的实现不是公共状态。\boxed{\text{公共状态是 market thickness }m,\quad N\sim\operatorname{Pois}(m)\text{ 的实现不是公共状态。}} 

因此，平台菜单、司机策略和乘客决策都依赖 mm，而不依赖 realized NN。原稿中“nn publicly observed”以及 n↦(p1(n),p2(n))n\mapsto(p\_1(n),p\_2(n)) 的 state-contingent mechanism 应整体删除。 

保留的 primitives 是：

-  rider type v∼U[0,1]v\sim U[0,1]； 
-  period-2 value βv\beta v； 
-  driver cost c∼U[0,1]c\sim U[0,1]； 
-  incumbent survival probability α\alpha； 
-  fresh-supply intensity γm\gamma m； 
-  平台最大化一张**潜在请求**的无条件完成概率。 

---

# 1. Model

## 1.1 Public market state and latent supply

市场厚度

m>0m>0 

是公共信息。平台、rider 和所有司机都知道 mm，但具体的初始司机数量

NI∼Pois⁡(m)N^I\sim\operatorname{Pois}(m) 

不是公共状态，菜单不能依赖其实现。

一名收到订单的司机知道：

-  自己存在并收到了订单； 
-  自己的成本 cc； 
-  公共参数 m,α,γ,βm,\alpha,\gamma,\beta； 
-  平台承诺的菜单 (p1,p2)(p\_1,p\_2)； 
-  其他司机的均衡策略； 

但不知道还有多少名其他司机。

第二期 fresh drivers 数量为

NE∼Pois⁡(γm),N^E\sim\operatorname{Pois}(\gamma m), 

独立于初始司机池。每名 fresh driver 的成本仍为独立的 U[0,1]U[0,1]。

这里的 γ\gamma 是：

fresh-supply intensity relative to initial market thickness.\text{fresh-supply intensity relative to initial market thickness}. 

---

## 1.2 Rider and payments

一名潜在 rider 的价值为

v∼U[0,1].v\sim U[0,1]. 

-  第一期完成的价值为 vv； 
- 第二期完成的价值为 βv\beta v，其中

  β∈(0,1).\beta\in(0,1). 

平台承诺

0≤p1≤p2≤1.0\le p\_1\le p\_2\le1. 

支付由 rider 向被选中的司机支付，平台将其视为纯转移，目标是最大化无条件 completion probability。

这意味着模型研究的是：

completion-maximizing payment protocol,\text{completion-maximizing payment protocol}, 

不是利润最大化或福利最大化。

---

## 1.3 Timing

1.  公共观察 mm，平台承诺 (p1,p2)(p\_1,p\_2)。 
2.  rider 观察 vv，决定是否发单。 
3.  初始司机数 NI∼Pois⁡(m)N^I\sim\operatorname{Pois}(m) 实现，但不是公共状态。 
4.  每名初始司机观察自己的成本，同时接受或拒绝 p1p\_1。 
5.  若至少一人接受，平台在接受者中均匀随机选择一人，订单完成。 
6. 若无人接受，rider 在以下三项中选择：

   abandon,repeat p1,activate p2.\text{abandon},\qquad \text{repeat }p\_1,\qquad \text{activate }p\_2. 
7.  incumbent survival 和 fresh entry 实现。 
8.  所有愿意接受当前支付的司机中均匀随机选择一人；若无人愿意，订单失败。 

rider 在第 6 步只观察“一期未完成”，不观察：

-  原来究竟有多少司机； 
-  有多少人是主动拒绝； 
-  有多少 incumbent survive； 
-  有多少 fresh driver 到达。 

---

# 2. Poisson supply objects

定义

ϕ(x):={1−e−xx,x>0,1,x=0.\phi(x):= \begin{cases} \dfrac{1-e^{-x}}{x},&x>0,\\\\[6pt] 1,&x=0. \end{cases} 

该函数将同时给出一期和二期的 expected assignment share。

---

## 2.1 Symmetric cutoff

考虑匿名对称策略：

accept p1⟺c≤a,\text{accept }p\_1 \quad\Longleftrightarrow\quad c\le a, 

其中

a∈[0,p1].a\in[0,p\_1]. 

由于初始司机池是 Poisson，接受者数满足

K1∼Pois⁡(ma).K\_1\sim\operatorname{Pois}(ma). 

因此一期覆盖概率为

A1(m,a)=1−e−ma.\boxed{ A\_1(m,a)=1-e^{-ma}. } 

---

## 2.2 First-period assignment share

从一名 focal driver 的角度，其他初始司机数仍服从

N−iI∼Pois⁡(m).N^I\_{-i}\sim\operatorname{Pois}(m). 

若她接受，其他接受者数为

K−i1∼Pois⁡(ma).K\_{-i}^1\sim\operatorname{Pois}(ma). 

所以她的 expected assignment share 为

σm(a)=E[11+K−i1]=ϕ(ma)=1−e−mama.\boxed{ \sigma\_m(a) = \mathbb E\left[\frac1{1+K\_{-i}^1}\right] = \phi(ma) = \frac{1-e^{-ma}}{ma}. } 

---

## 2.3 Posterior after universal rejection

Poisson splitting 给出：

\#{c≤a}∼Pois⁡(ma),\\#\\{c\le a\\}\sim\operatorname{Pois}(ma), #{a\<c≤pj}∼Pois⁡(m(pj−a)),\\#\\{a\<c\le p\_j\\} \sim \operatorname{Pois}\bigl(m(p\_j-a)\bigr), 

且二者独立。

因此，观察到一期无人接受，只说明第一类计数为零；第二类计数的分布不变。

经过 survival thinning，二期愿意接受 pjp\_j 的 incumbent 数量为

Pois⁡(mα(pj−a)).\operatorname{Pois}\bigl(m\alpha(p\_j-a)\bigr). 

愿意接受 pjp\_j 的 fresh-driver 数量为

Pois⁡(γmpj).\operatorname{Pois}(\gamma mp\_j). 

定义

λj(m,a)=m[α(pj−a)+γpj].\boxed{ \lambda\_j(m,a) = m\left[\alpha(p\_j-a)+\gamma p\_j\right]. } 

则二期愿意接受 pjp\_j 的总司机数服从

Pois⁡(λj(m,a)).\operatorname{Pois}\bigl(\lambda\_j(m,a)\bigr). 

对应 coverage probability 为

Cj(m,a)=1−e−λj(m,a)=1−exp⁡{−m[α(pj−a)+γpj]}.\boxed{ C\_j(m,a) = 1-e^{-\lambda\_j(m,a)} = 1-\exp\left\\{ -m[\alpha(p\_j-a)+\gamma p\_j] \right\\}. } 

---

## 2.4 Second-period assignment share

给定 focal incumbent：

-  已经拒绝一期支付； 
-  survive； 
-  愿意接受 pjp\_j； 

她面对的其他 willing drivers 数量为

Pois⁡(λj(m,a)).\operatorname{Pois}\bigl(\lambda\_j(m,a)\bigr). 

因此其 expected assignment share 是

s\~j,m(a)=ϕ(λj(m,a)).\boxed{ \widetilde s\_{j,m}(a) = \phi\bigl(\lambda\_j(m,a)\bigr). } 

所以一期和二期 assignment shares 具有统一形式：

σm(a)=ϕ(ma),s\~j,m(a)=ϕ(m[α(pj−a)+γpj]).\sigma\_m(a)=\phi(ma), \qquad \widetilde s\_{j,m}(a) = \phi\left( m[\alpha(p\_j-a)+\gamma p\_j] \right). 

---

# 3. Rider’s optimal continuation

## 3.1 Posting decision

若 v\<p1v\<p\_1，则：

v−p1<0,v-p\_1<0, 

而且由于 β<1\beta<1 和 p2≥p1p\_2\ge p\_1，

βv−p1<0,βv−p2<0.\beta v-p\_1<0, \qquad \beta v-p\_2<0. 

所以 rider 不会发单。

若 v≥p1v\ge p\_1，一期成交至少给出非负效用，而且 rider 可以在失败后 abandon。因此：

post⟺v≥p1.\boxed{ \text{post} \quad\Longleftrightarrow\quad v\ge p\_1. } 

发单概率为

1−p1.1-p\_1. 

---

## 3.2 Period-2 choice

一期失败后，rider 比较

0,0, C1(m,a)(βv−p1),C\_1(m,a)(\beta v-p\_1), C2(m,a)(βv−p2).C\_2(m,a)(\beta v-p\_2). 

当 C2>C1C\_2>C\_1 时，repeat 与 escalate 的无差异类型为

vmM(a)=C2(m,a)p2−C1(m,a)p1β[C2(m,a)−C1(m,a)].\boxed{ v\_m^M(a) = \frac{ C\_2(m,a)p\_2-C\_1(m,a)p\_1 }{ \beta[C\_2(m,a)-C\_1(m,a)] }. } 

若 C2=C1C\_2=C\_1，定义

vmM(a)=+∞.v\_m^M(a)=+\infty. 

可以直接验证

vmM(a)≥p2β≥p1β.v\_m^M(a)\ge \frac{p\_2}{\beta} \ge\frac{p\_1}{\beta}. 

因此 rider 的 continuation strategy 是

{abandon,v\<p1/β,repeat p1,p1/β≤v\<vmM(a),activate p2,v≥vmM(a).\begin{cases} \text{abandon}, & v\<p\_1/\beta,\\\\[3pt] \text{repeat }p\_1, & p\_1/\beta\le v\<v\_m^M(a),\\\\[3pt] \text{activate }p\_2, & v\ge v\_m^M(a). \end{cases} 

这一 threshold structure 与原稿保留，但 coverage 现在直接依赖公共厚度 mm，而不是公开 realization nn。

---

## 3.3 Activation masses

条件于订单已经发出，即 v≥p1v\ge p\_1，定义

ηmR(a)=[min⁡{vmM(a),1}−p1/β]+1−p1,\boxed{ \eta\_m^R(a) = \frac{ \left[ \min\\{v\_m^M(a),1\\} -p\_1/\beta \right]^+ }{ 1-p\_1 }, } ηm(a)=[1−vmM(a)]+1−p1.\boxed{ \eta\_m(a) = \frac{ [1-v\_m^M(a)]^+ }{ 1-p\_1 }. } 

两者满足

ηmR(a)+ηm(a)=ρ(p1):=[1−p1/β]+1−p1.\boxed{ \eta\_m^R(a)+\eta\_m(a) = \rho(p\_1) := \frac{[1-p\_1/\beta]^+}{1-p\_1}. } 

该总 continuation mass 不依赖：

-  cutoff aa； 
- mm； 
- p2p\_2； 
- α,γ\alpha,\gamma。 

它只取决于一期支付和 rider patience。

---

# 4. Driver’s Bayesian problem

考虑一名成本

c≤p1c\le p\_1 

的 focal incumbent。

---

## 4.1 Accept now

若她接受一期支付，其 expected payoff 为

UmA(c;a)=σm(a)(p1−c)=ϕ(ma)(p1−c).\boxed{ U^A\_m(c;a) = \sigma\_m(a)(p\_1-c) = \phi(ma)(p\_1-c). } 

---

## 4.2 Reject and wait

若她拒绝：

- 其他司机全部拒绝的概率为

  e−ma;e^{-ma}; 
- 她自己 survive 的概率为

  α;\alpha; 
- rider repeat 或 escalate 的概率分别为

  ηmR(a),ηm(a);\eta\_m^R(a),\qquad\eta\_m(a); 
- 二期 assignment shares 为

  s\~1,m(a),s\~2,m(a).\widetilde s\_{1,m}(a),\qquad \widetilde s\_{2,m}(a). 

因此

UmW(c;a)=e−maα[ηmR(a)s\~1,m(a)(p1−c)+ηm(a)s\~2,m(a)(p2−c)].\boxed{ \begin{aligned} U^W\_m(c;a) ={}& e^{-ma}\alpha \Big[ \eta\_m^R(a)\widetilde s\_{1,m}(a)(p\_1-c)\\\ &\hspace{27mm} + \eta\_m(a)\widetilde s\_{2,m}(a)(p\_2-c) \Big]. \end{aligned} } 

定义 accept-minus-wait difference：

Ψm(c;a)=ϕ(ma)(p1−c)−e−maα[ηmR(a)ϕ(λ1(m,a))(p1−c)+ηm(a)ϕ(λ2(m,a))(p2−c)].\boxed{ \begin{aligned} \Psi\_m(c;a) ={}& \phi(ma)(p\_1-c)\\\ &- e^{-ma}\alpha \Big[ \eta\_m^R(a)\phi(\lambda\_1(m,a))(p\_1-c)\\\ &\hspace{22mm} + \eta\_m(a)\phi(\lambda\_2(m,a))(p\_2-c) \Big]. \end{aligned} } 

---

# 5. PBE characterization

## Lemma 1. Cutoff best responses

对 cc 求导：

∂Ψm(c;a)∂c=−ϕ(ma)+e−maα[ηmR(a)ϕ(λ1)+ηm(a)ϕ(λ2)].\frac{\partial\Psi\_m(c;a)}{\partial c} = -\phi(ma) + e^{-ma}\alpha \left[ \eta\_m^R(a)\phi(\lambda\_1) + \eta\_m(a)\phi(\lambda\_2) \right]. 

由于

ϕ(λj)≤1,ηmR+ηm=ρ≤1,α≤1,\phi(\lambda\_j)\le1, \qquad \eta\_m^R+\eta\_m=\rho\le1, \qquad \alpha\le1, 

有

∂Ψm(c;a)∂c≤−ϕ(ma)+e−ma.\frac{\partial\Psi\_m(c;a)}{\partial c} \le -\phi(ma)+e^{-ma}. 

而

ϕ(x)≥e−x\phi(x)\ge e^{-x} 

等价于

ex≥1+x.e^x\ge1+x. 

因此

∂Ψm(c;a)∂c≤0.\boxed{ \frac{\partial\Psi\_m(c;a)}{\partial c}\le0. } 

所以每个匿名纯策略 best response 都可以表示为 cutoff。

---

## Proposition 1. Bayesian cutoff PBE

定义

fm(a;p1,p2):=Ψm(a;a).f\_m(a;p\_1,p\_2) := \Psi\_m(a;a). 

显式地，

fm(a;p1,p2)=ϕ(ma)(p1−a)−e−maα[ηmR(a)ϕ(λ1(m,a))(p1−a)+ηm(a)ϕ(λ2(m,a))(p2−a)].\boxed{ \begin{aligned} f\_m(a;p\_1,p\_2) ={}& \phi(ma)(p\_1-a)\\\ &- e^{-ma}\alpha \Big[ \eta\_m^R(a)\phi(\lambda\_1(m,a))(p\_1-a)\\\ &\hspace{22mm} + \eta\_m(a)\phi(\lambda\_2(m,a))(p\_2-a) \Big]. \end{aligned} } 

cutoff a∈[0,p1]a\in[0,p\_1] 构成匿名纯策略 PBE，当且仅当

{fm(0;p1,p2)≤0,a=0,fm(a;p1,p2)=0,0\<a\<p1,fm(p1;p1,p2)≥0,a=p1.\boxed{ \begin{cases} f\_m(0;p\_1,p\_2)\le0, & a=0,\\\\[3pt] f\_m(a;p\_1,p\_2)=0, &0\<a\<p\_1,\\\\[3pt] f\_m(p\_1;p\_1,p\_2)\ge0, &a=p\_1. \end{cases} } 

定义 equilibrium correspondence：

Emα,γ(p1,p2)={a∈[0,p1]\:a 满足上述条件}.\boxed{ \mathcal E\_m^{\alpha,\gamma}(p\_1,p\_2) = \left\\{ a\in[0,p\_1]: a\text{ 满足上述条件} \right\\}. } 

---

## Proposition 2. PBE existence

有

fm(p1;p1,p2)=−e−mp1αηm(p1)ϕ(λ2(m,p1))(p2−p1)≤0.f\_m(p\_1;p\_1,p\_2) = - e^{-mp\_1}\alpha\eta\_m(p\_1) \phi(\lambda\_2(m,p\_1))(p\_2-p\_1) \le0. 

于是：

-  若 fm(0)≤0f\_m(0)\le0，则 a=0a=0 是 PBE； 
- 若 fm(0)>0f\_m(0)>0，连续性和

  fm(p1)≤0f\_m(p\_1)\le0 

  保证存在一个内部根。

所以：

Emα,γ(p1,p2)≠∅.\boxed{ \mathcal E\_m^{\alpha,\gamma}(p\_1,p\_2)\neq\varnothing. } 

equilibrium set 也是闭且有界的，因此 compact。

当前尚未证明每个菜单下 PBE 全局唯一；平台设计应保留 equilibrium correspondence。

---

# 6. Completion probability and best menu

给定 cutoff PBE aa，总 completion probability 为

Mmα,γ(p1,p2;a)=(1−p1){1−e−ma[1−ηmR(a)C1(m,a)−ηm(a)C2(m,a)]}.\boxed{ \begin{aligned} M\_m^{\alpha,\gamma}(p\_1,p\_2;a) = (1-p\_1) \Big\\{ 1-e^{-ma} \big[ 1-\eta\_m^R(a)C\_1(m,a) -\eta\_m(a)C\_2(m,a) \big] \Big\\}. \end{aligned} } 

解释为：

1−p1⏟rider posts×[1−e−ma⏟period-1 completion+e−ma(ηmRC1+ηmC2)⏟period-2 rescue].\underbrace{1-p\_1}\_{\text{rider posts}} \times \left[ \underbrace{1-e^{-ma}}\_{\text{period-1 completion}} + \underbrace{ e^{-ma} \bigl(\eta\_m^RC\_1+\eta\_mC\_2\bigr) }\_{\text{period-2 rescue}} \right]. 

原稿中的 completion decomposition 保留，但固定 nn 的 (1−a)n(1-a)^n 被 Poisson failure probability e−mae^{-ma} 替代。

---

## Robust menu value

若存在多个 cutoff PBE，定义

M‾mα,γ(p1,p2)=min⁡a∈Emα,γ(p1,p2)Mmα,γ(p1,p2;a).\boxed{ \underline M\_m^{\alpha,\gamma}(p\_1,p\_2) = \min\_{a\in\mathcal E\_m^{\alpha,\gamma}(p\_1,p\_2)} M\_m^{\alpha,\gamma}(p\_1,p\_2;a). } 

平台的 dynamic-menu value 是

Dα,γ∗(m)=sup⁡0≤p1≤p2≤1M‾mα,γ(p1,p2).\boxed{ D\_{\alpha,\gamma}^\*(m) = \sup\_{0\le p\_1\le p\_2\le1} \underline M\_m^{\alpha,\gamma}(p\_1,p\_2). } 

若 supremum 被某个 pair 实现，则

(p1∗(m),p2∗(m))(p\_1^\*(m),p\_2^\*(m)) 

是 best menu。

关键是：

(p1∗,p2∗) 是 m 的函数，而不是 realized N 的函数。\boxed{ (p\_1^\*,p\_2^\*)\text{ 是 }m\text{ 的函数，而不是 realized }N\text{ 的函数。} } 

---

# 7. Flat benchmark

令

p1=p2=p.p\_1=p\_2=p. 

## Proposition 3. Unique flat PBE

当 a\<pa\<p 时，

fm(a;p,p)=(p−a)[ϕ(ma)−e−maαρ(p)ϕ(m[α(p−a)+γp])].f\_m(a;p,p) = (p-a) \left[ \phi(ma) - e^{-ma}\alpha\rho(p) \phi\bigl(m[\alpha(p-a)+\gamma p]\bigr) \right]. 

由于

ϕ(ma)≥e−ma,\phi(ma)\ge e^{-ma}, 

而

αρ(p)ϕ(⋅)<1(p>0),\alpha\rho(p)\phi(\cdot)<1 \qquad(p>0), 

括号严格为正。因此没有 a\<pa\<p 可以构成 PBE。

于是：

Emα,γ(p,p)={p}.\boxed{ \mathcal E\_m^{\alpha,\gamma}(p,p)=\\{p\\}. } 

flat payment 下拒绝者成本高于 pp，所以 surviving incumbents 不会在第二期接受相同支付；二期 flat completion 只能来自 fresh entrants。

---

## Flat completion

QγF(m,p)=(1−p)(1−e−mp)+e−mp[1−pβ]+(1−e−γmp).\boxed{ Q\_\gamma^F(m,p) = (1-p)(1-e^{-mp}) + e^{-mp} \left[1-\frac p\beta\right]^+ (1-e^{-\gamma mp}). } 

因此

Fα,γ∗(m)=sup⁡p∈[0,1]QγF(m,p).\boxed{ F\_{\alpha,\gamma}^\*(m) = \sup\_{p\in[0,1]}Q\_\gamma^F(m,p). } 

实际上 QγFQ\_\gamma^F 不依赖 α\alpha，所以也可写成

Fγ∗(m).F\_\gamma^\*(m). 

动态菜单价值为

Vα,γ(m)=Dα,γ∗(m)−Fγ∗(m)≥0.\boxed{ V\_{\alpha,\gamma}(m) = D\_{\alpha,\gamma}^\*(m)-F\_\gamma^\*(m) \ge0. } 

---

# 8. Local escalation theorem

这是当前版本最重要的理论工具。

固定一个 flat payment p∈(0,β)p\in(0,\beta)，考虑

p1=p,p2=p+ε,ε↓0.p\_1=p, \qquad p\_2=p+\varepsilon, \qquad \varepsilon\downarrow0. 

定义

u=1−p,R=e−mp,E=e−γmp,u=1-p, \qquad R=e^{-mp}, \qquad E=e^{-\gamma mp}, h=1−E,σ=ϕ(mp),ℓ=ϕ(γmp),h=1-E, \qquad \sigma=\phi(mp), \qquad \ell=\phi(\gamma mp), ρ=1−p/β1−p.\rho=\frac{1-p/\beta}{1-p}. 

定义 limiting escalation threshold

vˉm=1β[p+hmE(α+γ)],\boxed{ \bar v\_m = \frac1\beta \left[ p+ \frac{h}{mE(\alpha+\gamma)} \right], } 

其中假设 α+γ>0\alpha+\gamma>0，并定义

ηm0=[1−vˉm]+1−p.\boxed{ \eta\_m^0 = \frac{[1-\bar v\_m]^+}{1-p}. } 

---

## Theorem 1. Local PBE response

假设

p<β,vˉm≠1.p<\beta, \qquad \bar v\_m\neq1. 

则对所有足够小的 ε>0\varepsilon>0，small-escalation menu 在 flat cutoff 附近具有唯一 PBE：

aε=p−κmε+o(ε),a\_\varepsilon = p-\kappa\_m\varepsilon+o(\varepsilon), 

其中

κm=Rαℓ ηm0σ−Rαℓρ.\boxed{ \kappa\_m = \frac{ R\alpha\ell\\,\eta\_m^0 }{ \sigma-R\alpha\ell\rho }. } 

而且所有 cutoff PBE 都满足 localization bound

0≤p−a≤αρ1−αρε.\boxed{ 0\le p-a \le \frac{\alpha\rho}{1-\alpha\rho}\varepsilon. } 

因此 small escalation 下不能出现离 flat cutoff 很远的另一支 equilibrium。

---

## Theorem 2. Exact local completion coefficient

定义

Bm=1−ρ[1−(1−α)E].B\_m = 1-\rho\left[1-(1-\alpha)E\right]. 

则

Lmα,γ(p):=lim⁡ε↓0M‾mα,γ(p,p+ε)−QγF(m,p)ε=muR[E(α+γ)ηm0−κmBm].\boxed{ \begin{aligned} L\_m^{\alpha,\gamma}(p) &:= \lim\_{\varepsilon\downarrow0} \frac{ \underline M\_m^{\alpha,\gamma}(p,p+\varepsilon) - Q\_\gamma^F(m,p) }{ \varepsilon }\\\\[3pt] &= muR \left[ E(\alpha+\gamma)\eta\_m^0 - \kappa\_m B\_m \right]. \end{aligned} } 

这个系数分成：

muRE(α+γ)ηm0⏟marginal rescue gain−muRκmBm⏟strategic-delay loss.\underbrace{ muR E(\alpha+\gamma)\eta\_m^0 }\_{\text{marginal rescue gain}} - \underbrace{ muR\kappa\_m B\_m }\_{\text{strategic-delay loss}}. 

因此：

-  第一项是提高 p2p\_2 后新增的二期 coverage； 
-  第二项是司机预期未来高支付后降低一期 cutoff 的损失。 

---

# 9. No-entry benchmark theorem

当

γ=0\gamma=0 

时：

E=1,h=0,ℓ=1,ηm0=ρ.E=1,\qquad h=0,\qquad\ell=1, \qquad\eta\_m^0=\rho. 

局部系数化简为

Lmα,0(p)=mue−mpαρ[ϕ(mp)−e−mp]ϕ(mp)−e−mpαρ.\boxed{ L\_m^{\alpha,0}(p) = \frac{ mu e^{-mp}\alpha\rho \left[ \phi(mp)-e^{-mp} \right] }{ \phi(mp)-e^{-mp}\alpha\rho }. } 

由于

ϕ(mp)>e−mp(m>0,p>0),\phi(mp)>e^{-mp} \qquad(m>0,p>0), 

得到：

Lmα,0(p)>0\boxed{ L\_m^{\alpha,0}(p)>0 } 

只要

m>0,α>0,0\<p<β.m>0,\qquad \alpha>0,\qquad 0\<p<\beta. 

这取代旧稿的：

n=1 neutrality,n≥2 preemption.n=1\text{ neutrality},\qquad n\ge2\text{ preemption}. 

新结论是：

> 只要公共 thickness m>0m>0，司机就认为存在竞争者的正概率；latent competition 已足以使小幅升级严格提高 completion。

旧 one-driver neutrality 只在极薄市场极限中留下二阶残余。

---

## Thin-market expansion of the local coefficient

当 m↓0m\downarrow0：

ϕ(mp)−e−mp=mp2+O(m2).\phi(mp)-e^{-mp} = \frac{mp}{2}+O(m^2). 

因此

Lmα,0(p)=αρ p(1−p)2(1−αρ)m2+O(m3).\boxed{ L\_m^{\alpha,0}(p) = \frac{ \alpha\rho\\,p(1-p) }{ 2(1-\alpha\rho) } m^2 + O(m^3). } 

所以无 fresh entry 时：

marginal value of escalation=O(m2).\text{marginal value of escalation} = O(m^2). 

若 γ>0\gamma>0 且 limiting activation region 非空，则

Lmα,γ(p)=m(1−p)γηm0+O(m2),L\_m^{\alpha,\gamma}(p) = m(1-p)\gamma\eta\_m^0+O(m^2), 

即 fresh entry 可以将局部 gain 提升为一阶 O(m)O(m)。

这里需要明确：

> 这些是 local coefficient LmL\_m 的 asymptotics；optimized global value V(m)V(m) 的精确阶数仍需单独证明。

---

# 10. Optimal flat payment without entry

当 γ=0\gamma=0 时，

Q0F(m,p)=(1−p)(1−e−mp).Q\_0^F(m,p) = (1-p)(1-e^{-mp}). 

其唯一 interior maximizer pF(m)p\_F(m) 满足

empF(m)=1+m[1−pF(m)].\boxed{ e^{mp\_F(m)} = 1+m[1-p\_F(m)]. } 

等价地，

pF(m)=m+1−W(em+1)m,\boxed{ p\_F(m) = \frac{ m+1-W(e^{m+1}) }{ m }, } 

其中 WW 是 Lambert WW function。

并且

0\<pF(m)<12∀m>0.\boxed{ 0\<p\_F(m)<\frac12 \qquad\forall m>0. } 

因此，当

β>12,α>0,γ=0,\beta>\frac12,\qquad \alpha>0,\qquad \gamma=0, 

最优 flat payment 必有

pF(m)<β,p\_F(m)<\beta, 

从而

Lmα,0(pF(m))>0.L\_m^{\alpha,0}(p\_F(m))>0. 

于是：

Dα,0∗(m)>F0∗(m)∀m>0.\boxed{ D\_{\alpha,0}^\*(m)>F\_0^\*(m) \qquad\forall m>0. } 

这已经是一个完整且有力的 strict-value theorem。

---

# 11. Thickness endpoints

## Proposition 4. Thin-market endpoint

任何 completion 都要求初始或 fresh pool 中至少出现一名司机，因此

Dα,γ∗(m)≤1−e−(1+γ)m.D\_{\alpha,\gamma}^\*(m) \le 1-e^{-(1+\gamma)m}. 

所以

lim⁡m↓0Dα,γ∗(m)=lim⁡m↓0Fγ∗(m)=lim⁡m↓0Vα,γ(m)=0.\boxed{ \lim\_{m\downarrow0} D\_{\alpha,\gamma}^\*(m) = \lim\_{m\downarrow0} F\_\gamma^\*(m) = \lim\_{m\downarrow0} V\_{\alpha,\gamma}(m) = 0. } 

---

## Proposition 5. Thick-market endpoint

选择 flat payment

p=m−1/2.p=m^{-1/2}. 

仅一期 completion 就满足

Fγ∗(m)≥(1−m−1/2)(1−e−m)⟶1.F\_\gamma^\*(m) \ge (1-m^{-1/2})(1-e^{-\sqrt m}) \longrightarrow1. 

因此

Dα,γ∗(m)≥Fγ∗(m)→1,D\_{\alpha,\gamma}^\*(m)\ge F\_\gamma^\*(m)\to1, 

同时 D∗≤1D^\*\le1，所以

lim⁡m→∞Fγ∗(m)=lim⁡m→∞Dα,γ∗(m)=1.\boxed{ \lim\_{m\to\infty} F\_\gamma^\*(m) = \lim\_{m\to\infty} D\_{\alpha,\gamma}^\*(m) = 1. } 

进而

lim⁡m→∞Vα,γ(m)=0.\boxed{ \lim\_{m\to\infty} V\_{\alpha,\gamma}(m)=0. } 

---

## Intermediate-thickness implication

理论上已经得到：

Vα,γ(m)→0as m↓0,V\_{\alpha,\gamma}(m)\to0 \quad\text{as }m\downarrow0, 

以及

Vα,γ(m)→0as m→∞.V\_{\alpha,\gamma}(m)\to0 \quad\text{as }m\to\infty. 

在无进入、α>0,β>12\alpha>0,\beta>\frac12 时，还有

Vα,0(m)>0∀m>0.V\_{\alpha,0}(m)>0 \qquad\forall m>0. 

因此，只差一个关于 robust design value 的 continuity/attainment lemma，就能正式推出：

Vα,0(m) 在某个有限且严格为正的 m∗ 处达到全局最大值。\boxed{ V\_{\alpha,0}(m) \text{ 在某个有限且严格为正的 } m^\* \text{ 处达到全局最大值。} } 

目前：

-  interior-peak logic 已经闭合； 
-  peak existence 还需要 value-continuity lemma； 
-  peak uniqueness 和 single-peakedness 仍未证明。 

---

# 12. 当前 theorem status

## 已经闭合或可直接写出完整证明

1. **Poisson posterior decomposition**

   Cj=1−e−m[α(pj−a)+γpj].C\_j=1-e^{-m[\alpha(p\_j-a)+\gamma p\_j]}. 
2. **Assignment-share formulas**

   σm(a)=ϕ(ma),s\~j,m(a)=ϕ(λj).\sigma\_m(a)=\phi(ma), \qquad \widetilde s\_{j,m}(a)=\phi(\lambda\_j). 
3. **Rider threshold strategy**

   p1,p1/β,vmM(a).p\_1,\quad p\_1/\beta,\quad v\_m^M(a). 
4. **Cutoff best responses**。 
5. **匿名 cutoff PBE 存在性**。 
6. **Flat policy 唯一 PBE**

   a=p.a=p. 
7. **Flat completion formula**。 
8. **Small-escalation localization and local uniqueness**。 
9. **Exact local coefficient Lmα,γ(p)L\_m^{\alpha,\gamma}(p)**。 
10. **No-entry strict positivity**

    Lmα,0(p)>0.L\_m^{\alpha,0}(p)>0. 
11. **No-entry optimal-flat strict improvement**

    Dα,0∗(m)>F0∗(m).D\_{\alpha,0}^\*(m)>F\_0^\*(m). 
12. **Thin- and thick-market endpoint limits**。 

---

## 尚需证明

1.  每个任意菜单下 cutoff PBE 是否全局唯一； 
2.  worst-equilibrium value 对 (m,p1,p2)(m,p\_1,p\_2) 的连续性； 
3.  best menu 的 supremum 是否总被实现； 
4. V(m)V(m) 是否严格 single-peaked； 
5. m∗m^\* 是否唯一； 
6. m∗m^\* 对 α,γ,β\alpha,\gamma,\beta 的比较静态； 
7. 一般 γ>0\gamma>0 下

   Lmα,γ(p)L\_m^{\alpha,\gamma}(p) 

   的全局符号；
8.  optimized value V(m)V(m) 在 m↓0m\downarrow0 时的精确阶数； 
9.  uniform distributions 之外的推广。 

---

# 13. 论文的理论主线

现在最干净的逻辑不再是“条件于 nn 的一个司机 versus 多个司机”，而是：

Public thickness m, latent realized supply⇓Representative driver faces Poisson competition⇓Failure-contingent escalation creates a waiting option⇓PBE cutoff solves a scalar Bayesian fixed point⇓Latent competition makes escalation strictly valuable⇓The value vanishes in both very thin and very thick markets\boxed{ \begin{array}{c} \text{Public thickness }m,\text{ latent realized supply}\\\ \Downarrow\\\ \text{Representative driver faces Poisson competition}\\\ \Downarrow\\\ \text{Failure-contingent escalation creates a waiting option}\\\ \Downarrow\\\ \text{PBE cutoff solves a scalar Bayesian fixed point}\\\ \Downarrow\\\ \text{Latent competition makes escalation strictly valuable}\\\ \Downarrow\\\ \text{The value vanishes in both very thin and very thick markets} \end{array} } 

最核心的经济 wedge 是

ϕ(mp)−e−mp>0.\boxed{ \phi(mp)-e^{-mp}>0. } 

其中：

- ϕ(mp)\phi(mp) 是司机现在接受后，在潜在竞争中被选中的 expected share； 
- e−mpe^{-mp} 是她拒绝后，所有其他司机也拒绝、订单进入第二期的概率。 

二者之差在 m>0m>0 时严格为正，并在 m↓0m\downarrow0 时收敛到零。这是新模型里取代

σn−(1−p)n−1\sigma\_n-(1-p)^{n-1} 

的连续-thickness competition wedge。

因此目前最准确的 punchline 是：

> **A platform that knows market thickness but not realized supply can use a precommitted rescue payment to improve completion. The option is valuable because a driver who accepts now competes for assignment, whereas a driver who waits is paid only if every rival also waits. This latent-competition wedge disappears in very thin markets, while optimized flat pricing eliminates the remaining headroom in very thick markets.**