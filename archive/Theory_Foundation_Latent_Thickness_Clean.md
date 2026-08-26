# Theory Foundation: Latent Market Thickness and Failure-Contingent Escalation

## 0. 当前版本的核心结论

平台只观察公共市场厚度 $m$，不能观察或依赖 realized supply。平台在一期之前承诺菜单 $(p_1,p_2)$；一期失败后，rider 可以 abandon、repeat $p_1$，或 activate $p_2$。

当前最干净的 baseline 是无新增供给：

$$
\gamma=0,\qquad \alpha>0.
$$

在任意 $m>0$ 和 $p\in(0,\beta)$ 下，从 flat menu $(p,p)$ 出发加入足够小的 rescue premium $(p,p+\varepsilon)$，都会严格提高 completion。进一步，当 $\beta>1/2$ 时，它严格优于最优 flat payment：

$$
D_{\alpha,0}^*(m)>F_0^*(m)
\qquad \forall m>0,\ \alpha>0.
$$

增益在 $m\downarrow0$ 与 $m\to\infty$ 时都趋于零。因此，目前能够严格声称的是：

> The dynamic menu is strictly valuable at every finite thickness in the no-entry baseline, but its value vanishes at both thickness extremes.

这给出 intermediate-thickness mechanism，但尚未证明 strict single-peakedness 或唯一 peak。

---

## 1. Primitives、信息结构与 timing

### 1.1 Public thickness and latent supply

公共市场厚度为 $m>0$。在 rider 的概率测度下，初始司机数为

$$
N^I\sim\operatorname{Pois}(m).
$$

Realized $N^I$ 不进入平台菜单，也不被 rider 或其他司机观察。平台在 $N^I$ 实现之前承诺

$$
0\le p_1\le p_2\le1.
$$

因此，菜单只能是

$$
(p_1,p_2)=(p_1(m),p_2(m)),
$$

而不能是 state-contingent pair $(p_1(N^I),p_2(N^I))$。

必须正式加入 Poisson-game/Palm information structure。在一名 focal driver 条件于自己存在的 Palm 测度下，

$$
N_{-i}^I\mid i\text{ is present}\sim\operatorname{Pois}(m).
$$

这不是普通的 $N^I-1\mid N^I\ge1$。仅由总数服从 Poisson，并不能自动推出 focal driver 面对的 rivals 数也服从同一 Poisson；后者需要 Palm/Slivnyak 结构。

### 1.2 Rider、driver 与第二期供给

Rider type 与 driver cost 相互独立：

$$
v\sim U[0,1],\qquad c\sim U[0,1].
$$

一期完成时 rider value 为 $v$；二期完成时为

$$
\beta v,\qquad \beta\in(0,1).
$$

一期 incumbent 以概率

$$
\alpha\in[0,1]
$$

留到第二期。第二期 fresh drivers 数量为

$$
N^E\sim\operatorname{Pois}(\gamma m),\qquad \gamma\ge0,
$$

且独立于初始司机池。

$p_j$ 同时是 rider 的支付和被匹配 driver 的收入；平台将其视为纯转移，只最大化每名潜在 rider 的无条件 completion probability。只有最终被随机选中的司机才获得 $p_j-c$；accept 但未被选中的司机没有成本或收益。

### 1.3 Timing

1. 公共观察 $m$，平台承诺 $(p_1,p_2)$。
2. Rider 观察 $v$，决定是否发单。
3. 初始司机池实现；每名司机观察自己的存在、成本、公共参数与菜单，但不知道 rivals 数量。
4. 所有初始司机同时接受或拒绝 $p_1$。
5. 若至少一人接受，平台在接受者中均匀选择一人，订单完成。
6. 若一期失败，rider 只观察 failure，并选择 abandon、repeat $p_1$ 或 activate $p_2$。
7. Incumbent survival 与 fresh entry 实现。
8. 第二期为终局；愿意接受当前支付的司机中随机选择一人，否则订单失败。

平台不能在失败后重新优化 $p_2$。这是一个 ex ante committed protocol；$p_2$ 不是自动 surge，而是 rider 可主动启用的 rescue option。

### 1.4 Tie-breaking 必须成为 primitive

采用以下规则：

- posting 的期望收益为零时，$v\ge p_1$ 的 rider 发单，$v<p_1$ 的 rider 不发单；
- continuation 的最大收益为零，且 repeat 与 abandon 无差异时，选择 repeat；
- $p_2=p_1$ 时，repeat 优先于名义上的 activate；
- cutoff type 的 driver 按后文的边界约定行动。

第二条不是无关紧要的零测度约定。当 $\gamma=0$ 且 $a=p_1$ 时，失败后的 repeat 与 abandon 对一个正测度的 rider-type 区间都给出零收益；该选择会影响偏离司机的等待收益。

---

## 2. Poisson competition calculus

定义

$$
\phi(x)=
\begin{cases}
\dfrac{1-e^{-x}}{x},&x>0,\\[5pt]
1,&x=0.
\end{cases}
$$

考虑一期匿名对称 cutoff 策略：成本低于 $a\in[0,p_1]$ 的司机接受一期支付。

### Lemma 1. Coverage and assignment shares

一期接受者数为 $\operatorname{Pois}(ma)$，所以

$$
A_1(m,a)=1-e^{-ma}.
$$

若 focal driver 接受，她面对的其他接受者数也为 $\operatorname{Pois}(ma)$，故 expected assignment share 为

$$
\sigma_m(a)
=\mathbb E\left[\frac{1}{1+K_{-i}}\right]
=\phi(ma).
$$

一期失败后，Poisson splitting 保留成本区间计数的独立性。若 rider 在第二期提供 $p_j$，愿意接受的 incumbent 与 fresh-driver 总数为

$$
\operatorname{Pois}(\lambda_j(m,a)),
\qquad
\lambda_j(m,a)
=m\left[\alpha(p_j-a)+\gamma p_j\right].
$$

因此

$$
C_j(m,a)=1-e^{-\lambda_j(m,a)},
\qquad
\widetilde s_{j,m}(a)=\phi(\lambda_j(m,a)).
$$

$C_j$ 是 rider 在一期失败后的二期 coverage probability；$\widetilde s_{j,m}$ 是一名等待且存活的 focal incumbent 在愿意接受 $p_j$ 时的 expected assignment share。

---

## 3. Rider strategy

### 3.1 Posting decision

给定 cutoff $a$，rider 发单的期望收益为

$$
\Pi(v;a)
=(1-e^{-ma})(v-p_1)
+e^{-ma}\max\left\{
0,\ C_1(\beta v-p_1),\ C_2(\beta v-p_2)
\right\}.
$$

在固定 tie-breaking 下，

$$
\text{post}\quad\Longleftrightarrow\quad v\ge p_1,
$$

故发单概率为 $1-p_1$。正文中的 conditional rider masses 先限定于 $p_1<1$；当 $p_1=1$ 时单独定义 completion 为零。

### 3.2 Failure-node choice

若 $C_2>C_1$，repeat 与 activate 的无差异类型为

$$
v_m^M(a)
=\frac{C_2(m,a)p_2-C_1(m,a)p_1}
{\beta[C_2(m,a)-C_1(m,a)]}.
$$

若 $C_2=C_1$，定义 $v_m^M(a)=+\infty$。因为

$$
v_m^M(a)\ge\frac{p_2}{\beta}\ge\frac{p_1}{\beta},
$$

failure-node strategy 为

$$
\begin{cases}
\text{abandon},&v<p_1/\beta,\\
\text{repeat }p_1,&p_1/\beta\le v<v_m^M(a),\\
\text{activate }p_2,&v\ge v_m^M(a).
\end{cases}
$$

条件于已经发单，定义

$$
\eta_m^R(a)
=\frac{[\min\{v_m^M(a),1\}-p_1/\beta]^+}{1-p_1},
$$

$$
\eta_m(a)
=\frac{[1-v_m^M(a)]^+}{1-p_1}.
$$

二者满足

$$
\eta_m^R(a)+\eta_m(a)
=\rho(p_1)
:=\frac{[1-p_1/\beta]^+}{1-p_1}.
$$

---

## 4. Symmetric Bayesian cutoff PBE

### 4.1 Driver payoffs and single crossing

对任意 $c\in[0,1]$，等待收益应写成

$$
U_m^W(c;a)
=e^{-ma}\alpha\left[
\eta_m^R(a)\phi(\lambda_1)[p_1-c]^+
+\eta_m(a)\phi(\lambda_2)[p_2-c]^+
\right].
$$

对 $c\le p_1$，一期接受收益为

$$
U_m^A(c;a)=\phi(ma)(p_1-c).
$$

于是 accept-minus-wait difference 为

$$
\begin{aligned}
\Psi_m(c;a)
={}&\phi(ma)(p_1-c)\\
&-e^{-ma}\alpha\left[
\eta_m^R(a)\phi(\lambda_1)(p_1-c)
+\eta_m(a)\phi(\lambda_2)(p_2-c)
\right].
\end{aligned}
$$

当 $p_1>0$ 时，

$$
\frac{\partial\Psi_m(c;a)}{\partial c}
\le-\phi(ma)+e^{-ma}\alpha\rho(p_1)<0,
$$

因为 $\beta<1$ 蕴含 $\rho(p_1)<1$。因此一期决策满足严格 single crossing。$c>p_1$ 的司机接受一期会产生负收益，而等待收益非负，故必然拒绝。

### Proposition 1. Characterization and existence

定义

$$
f_m(a;p_1,p_2):=\Psi_m(a;a).
$$

匿名对称纯策略 cutoff PBE 的边界条件为

$$
\begin{cases}
f_m(0;p_1,p_2)\le0,&a=0,\\
f_m(a;p_1,p_2)=0,&0<a<p_1,\\
f_m(p_1;p_1,p_2)\ge0,&a=p_1.
\end{cases}
$$

字面策略约定为：

- $a=0$ 时所有类型拒绝；
- $0<a<p_1$ 时 $c<a$ 接受、$c>a$ 拒绝；
- $a=p_1$ 时 $c\le p_1$ 接受。

同时，

$$
f_m(p_1;p_1,p_2)
=-e^{-mp_1}\alpha\eta_m(p_1)
\phi(\lambda_2(m,p_1))(p_2-p_1)
\le0.
$$

所以：若 $f_m(0)\le0$，reject-all 是 equilibrium；若 $f_m(0)>0$，连续性与 $f_m(p_1)\le0$ 给出内部根，或在等号情形给出 $a=p_1$。

因此 symmetric cutoff equilibrium correspondence

$$
\mathcal E_m^{\alpha,\gamma}(p_1,p_2)
$$

对每个 $p_1<1$ 非空且 compact。

该命题只刻画 anonymous、symmetric、pure cutoff PBE，不应写成对所有 mixed 或 asymmetric PBE 的无条件刻画。

---

## 5. Implementable outcomes and platform design

给定菜单与 cutoff equilibrium $a$，无条件 completion probability 为

$$
\begin{aligned}
M_m^{\alpha,\gamma}(p_1,p_2;a)
=(1-p_1)\Big[
1-e^{-ma}
+e^{-ma}\{
\eta_m^R(a)C_1(m,a)+\eta_m(a)C_2(m,a)
\}
\Big].
\end{aligned}
$$

其结构是

$$
\text{posting mass}
\times
\bigl(\text{period-1 completion}+\text{period-2 rescue}\bigr).
$$

在未证明任意菜单的 equilibrium uniqueness 之前，应先定义 implementable outcome set：

$$
\mathcal I_m(p_1,p_2)
=\left\{
M_m^{\alpha,\gamma}(p_1,p_2;a):
a\in\mathcal E_m^{\alpha,\gamma}(p_1,p_2)
\right\}.
$$

进一步区分

$$
\underline M_m(p_1,p_2)
=\min_{a\in\mathcal E_m(p_1,p_2)}
M_m(p_1,p_2;a),
$$

$$
\overline M_m(p_1,p_2)
=\max_{a\in\mathcal E_m(p_1,p_2)}
M_m(p_1,p_2;a).
$$

若采用保守设计准则，则

$$
D_{\alpha,\gamma}^{-,*}(m)
=\sup_{0\le p_1\le p_2\le1}
\underline M_m(p_1,p_2).
$$

这应称为 worst symmetric-cutoff equilibrium value，而不是未经限定的 worst-PBE value。若采用 optimistic implementation，则相应定义 $D^{+,*}$。没有 equilibrium selection 或 attainment 结果时，“best menu”应理解为 design correspondence 或 supremum，而不是已经存在且唯一的 pair。

以下沿用保守值，并简写为 $D^*$。

---

## 6. Flat benchmark

### Proposition 2. Unique symmetric cutoff under a flat payment

令 $p_1=p_2=p>0$。对任意 $a<p$，

$$
f_m(a;p,p)
=(p-a)\left[
\phi(ma)-e^{-ma}\alpha\rho(p)
\phi\bigl(m[\alpha(p-a)+\gamma p]\bigr)
\right]>0.
$$

因此

$$
\mathcal E_m^{\alpha,\gamma}(p,p)=\{p\}.
$$

$p=0$ 作为零完成率边界单独处理。Flat payment 下，一期拒绝者的成本高于 $p$，所以 surviving incumbents 不会在第二期接受相同支付；二期完成只能来自 fresh entrants。

Flat completion 为

$$
Q_\gamma^F(m,p)
=(1-p)(1-e^{-mp})
+e^{-mp}[1-p/\beta]^+(1-e^{-\gamma mp}),
$$

故

$$
F_\gamma^*(m)=\sup_{p\in[0,1]}Q_\gamma^F(m,p).
$$

---

## 7. Local escalation theorem

固定 $m>0$ 与 $p\in(0,\beta)$，考虑

$$
p_1=p,\qquad p_2=p+\varepsilon,\qquad \varepsilon\downarrow0.
$$

定义

$$
u=1-p,\quad
R=e^{-mp},\quad
E=e^{-\gamma mp},\quad
\sigma=\phi(mp),\quad
\ell=\phi(\gamma mp),\quad
\rho=\frac{1-p/\beta}{1-p}.
$$

若 $\alpha+\gamma>0$，再定义

$$
\bar v_m
=\frac1\beta\left[
p+\frac{1-E}{mE(\alpha+\gamma)}
\right],
\qquad
\eta_m^0
=\frac{[1-\bar v_m]^+}{1-p}.
$$

### Theorem 1. Equilibrium localization and response

假设 $\bar v_m\ne1$。对所有充分小的 $\varepsilon>0$，small-escalation menu 具有唯一 symmetric cutoff PBE，且

$$
a_\varepsilon
=p-\kappa_m\varepsilon+o(\varepsilon),
$$

其中

$$
\kappa_m
=\frac{R\alpha\ell\,\eta_m^0}
{\sigma-R\alpha\ell\rho}.
$$

所有 symmetric cutoff PBE 都满足

$$
0\le p-a
\le\frac{\alpha\rho}{1-\alpha\rho}\varepsilon.
$$

因此不存在离 flat cutoff 很远的另一支 equilibrium。

证明不能在奇异点 $(a,\varepsilon)=(p,0)$ 直接套 ordinary implicit-function theorem，因为 $v_m^M$ 在 flat menu 上是 $0/0$ 型极限。正确方法是先做 localization，再令

$$
k=\frac{p-a}{\varepsilon},
$$

并证明 rescaled equilibrium equation 一致收敛到严格递增的 affine equation。

### Theorem 2. Exact local completion coefficient and its sign

定义

$$
B_m=1-\rho[1-(1-\alpha)E].
$$

则

$$
\boxed{
L_m^{\alpha,\gamma}(p)
:=\lim_{\varepsilon\downarrow0}
\frac{
\underline M_m(p,p+\varepsilon)-Q_\gamma^F(m,p)
}{\varepsilon}
=m(1-p)R
\left[
E(\alpha+\gamma)\eta_m^0-\kappa_mB_m
\right].
}
$$

第一项是 marginal rescue gain；第二项是战略等待降低一期 cutoff 的 delay loss。

更强地，

$$
\boxed{
\bar v_m<1
\quad\Longrightarrow\quad
L_m^{\alpha,\gamma}(p)>0.
}
$$

若 $\bar v_m>1$，则 $\eta_m^0=\kappa_m=0$，所以 $L_m^{\alpha,\gamma}(p)=0$：无正质量 rider 在边际上启用 rescue payment，菜单的一阶变化自然没有价值。Kink case $\bar v_m=1$ 需要单独做 one-sided expansion。

因此，一般 fresh-entry case 的 local sign 也可以闭合：

> Whenever a marginal rescue premium is activated by a positive mass of riders, it strictly improves completion.

一个简洁的证明路线如下。令

$$
D=\sigma-R\alpha\ell\rho>0.
$$

将 $\kappa_m$ 代入可写成

$$
L_m^{\alpha,\gamma}(p)
=m(1-p)R\eta_m^0\frac{T_m}{D},
$$

其中

$$
T_m
=E(\alpha+\gamma)\sigma
-R\alpha\ell\left[1-\rho+\rho E(1+\gamma)\right].
$$

Activation condition $\bar v_m<1$ 蕴含一个严格 lower bound on $\rho$；结合 $\sigma/R=(e^{mp}-1)/(mp)$ 与 $\ell=\phi(\gamma mp)$，可证明 $T_m>0$。完整 inequality proof 放 appendix。

---

## 8. No-entry main theorem

令

$$
\gamma=0.
$$

此时 $\bar v_m=p/\beta<1$，所以所有 $p\in(0,\beta)$ 都处于 active-rescue region。并且

$$
E=\ell=1,\qquad
\eta_m^0=\rho,
$$

$$
\kappa_m
=\frac{e^{-mp}\alpha\rho}
{\phi(mp)-e^{-mp}\alpha\rho}.
$$

Theorem 2 化简为

$$
\boxed{
L_m^{\alpha,0}(p)
=
\frac{
m(1-p)e^{-mp}\alpha\rho
[\phi(mp)-e^{-mp}]
}{
\phi(mp)-e^{-mp}\alpha\rho
}>0.
}
$$

严格正性的核心 competition wedge 是

$$
\phi(mp)-e^{-mp}>0.
$$

- $\phi(mp)$ 是司机现在接受后，在 latent competition 中的 expected assignment share；
- $e^{-mp}$ 是她拒绝后，所有 rival 也拒绝、订单进入第二期的概率。

现在接受并不保证被选中，但等待只有在所有 rival 同时等待时才有价值。这一 wedge 取代 fixed-$n$ 模型中的 one-driver versus many-driver comparison。

### Corollary 1. Strict dominance over the optimal flat payment

当 $\gamma=0$ 时，

$$
Q_0^F(m,p)=(1-p)(1-e^{-mp}).
$$

其唯一最优解满足

$$
e^{mp_F(m)}=1+m[1-p_F(m)]
$$

并且

$$
0<p_F(m)<\frac12.
$$

因此若 $\beta>1/2$（事实上 $\beta=1/2$ 也足够），则 $p_F(m)<\beta$，从而

$$
\boxed{
D_{\alpha,0}^*(m)>F_0^*(m)
\qquad
\forall m>0,\ \alpha>0.
}
$$

Lambert-$W$ 闭式

$$
p_F(m)
=\frac{m+1-W_0(e^{m+1})}{m}
$$

可放 appendix。

---

## 9. Market thickness

定义

$$
V_{\alpha,\gamma}(m)
=D_{\alpha,\gamma}^*(m)-F_\gamma^*(m).
$$

### Thin-market endpoint

任何完成都要求初始池或 fresh pool 中至少有一名司机，因此

$$
D_{\alpha,\gamma}^*(m)
\le1-e^{-(1+\gamma)m}.
$$

所以

$$
\lim_{m\downarrow0}D_{\alpha,\gamma}^*(m)
=\lim_{m\downarrow0}F_\gamma^*(m)
=\lim_{m\downarrow0}V_{\alpha,\gamma}(m)=0.
$$

### Thick-market endpoint

选择 flat payment $p=m^{-1/2}$。仅一期 completion 就满足

$$
F_\gamma^*(m)
\ge(1-m^{-1/2})(1-e^{-\sqrt m})
\longrightarrow1.
$$

因此

$$
\lim_{m\to\infty}F_\gamma^*(m)
=\lim_{m\to\infty}D_{\alpha,\gamma}^*(m)=1
$$

以及

$$
\lim_{m\to\infty}V_{\alpha,\gamma}(m)=0.
$$

### 当前 thickness theorem 的准确边界

在 $\gamma=0,\alpha>0,\beta>1/2$ 下，

$$
V_{\alpha,0}(m)>0\qquad\forall m>0,
$$

且

$$
\lim_{m\downarrow0}V_{\alpha,0}(m)
=\lim_{m\to\infty}V_{\alpha,0}(m)=0.
$$

这足以支持 “intermediate-thickness value” 的经济叙事，但不足以声称 single-peakedness。

若进一步证明 $V_{\alpha,0}$ 的 continuity 与 design-value attainment，才能推出至少存在一个有限的 interior maximizer $m^*>0$。即便如此，也只能得到 peak existence，不能自动得到 peak uniqueness。

---

## 10. Thin-market orders and fresh entry

无 fresh entry 时，

$$
L_m^{\alpha,0}(p)
=\frac{\alpha\rho\,p(1-p)}
{2(1-\alpha\rho)}m^2
+O(m^3).
$$

所以 incumbent competition 在极薄市场只产生二阶 local gain。

当 $\gamma>0$ 时，定义

$$
\bar v_0
=\frac{p(\alpha+2\gamma)}
{\beta(\alpha+\gamma)},
\qquad
\eta_0^0
=\frac{[1-\bar v_0]^+}{1-p}.
$$

若严格满足

$$
\bar v_0<1
\quad\Longleftrightarrow\quad
p<\frac{\beta(\alpha+\gamma)}
{\alpha+2\gamma},
$$

则 limiting activation mass 为正，并且

$$
L_m^{\alpha,\gamma}(p)
=m(1-p)\gamma\eta_0^0+O(m^2).
$$

因此 fresh supply 可以把 local gain 从 $O(m^2)$ 提升为 $O(m)$。这只是 local coefficient 的阶数，不是 optimized global value $V(m)$ 的阶数。

---

## 11. 三个嵌套模型

### Case I. Closed pool, no exit

$$
\alpha=1,\qquad \gamma=0.
$$

失败后没有新司机，但所有 incumbent 都留在市场。Local escalation 的价值完全来自 latent competition。

### Case II. Exit only

$$
0<\alpha<1,\qquad \gamma=0.
$$

退出削弱 rescue capacity，但只要 $\alpha>0$，

$$
L_m^{\alpha,0}(p)>0.
$$

因此 survival 不需要等于一；正的 continuation probability 已经足够。

### Case III. Exit and replenishment

$$
\alpha\in[0,1],\qquad \gamma>0.
$$

Fresh supply 同时改变 rider activation threshold、司机等待收益和二期 coverage。只要 $\bar v_m<1$，small escalation 仍严格提高 completion；该 case 还承载 $O(m)$ versus $O(m^2)$ 的薄市场比较。

---

## 12. Theorem status

### 已闭合、可写成完整证明

1. Palm information structure 下的 Poisson posterior decomposition。
2. 一期与二期 assignment-share identities。
3. 固定 tie-breaking 下的 rider posting 与 continuation thresholds。
4. Driver single crossing 与 symmetric cutoff PBE characterization。
5. Symmetric cutoff PBE existence 与 compactness。
6. Flat policy 的唯一 symmetric cutoff equilibrium。
7. Flat completion formula。
8. Small-escalation localization、rescaled local uniqueness 与 exact coefficient。
9. Active-rescue region $\bar v_m<1$ 内一般 $\gamma\ge0$ 的 local strict positivity。
10. No-entry optimal-flat strict improvement。
11. Thin- and thick-market endpoint limits。

### 尚未闭合、不能写成现有 theorem

1. 任意 dynamic menu 下所有 PBE 的全局唯一性。
2. Mixed 或 asymmetric PBE 的完整刻画。
3. Worst symmetric-cutoff value 对 $(m,p_1,p_2)$ 的 continuity。
4. Dynamic design supremum 的一般 attainment。
5. Optimized gain $V(m)$ 在 $m\downarrow0$ 时的精确阶数。
6. $V(m)$ 的 strict single-peakedness 与唯一 $m^*$。
7. $m^*$ 对 $\alpha,\gamma,\beta$ 的比较静态。
8. Uniform distributions 之外的推广。
9. Kink case $\bar v_m=1$ 的高阶 one-sided expansion。

---

## 13. 推荐的主文 hierarchy

正文只保留六个标题级结果：

1. **Symmetric Bayesian Cutoff Equilibrium**
2. **Unique Flat Benchmark**
3. **Local Escalation under Latent Competition**
4. **Strict Dominance over the Optimal Flat Payment**
5. **The Value Vanishes at Both Thickness Extremes**
6. **Fresh-Entry Extension**

主文以 $\gamma=0$ 的干净 strict-value theorem 为核心；一般 $\gamma$ 的 activation theorem 与 $O(m)$ versus $O(m^2)$ 作为扩展。Palm/Poisson 推导、完整边界条件、localization proof、一般系数的 positivity proof、Lambert-$W$ 表达式和 endpoint proofs 放 appendix。

---

## 14. Final punchline

> A platform observes market thickness but not realized supply. A precommitted rescue payment is valuable because a driver who accepts immediately competes for assignment, whereas a driver who waits is paid only when every rival also waits. Whenever a positive mass of riders activates the rescue option, this latent-competition mechanism strictly raises completion. In the no-entry baseline, the gain is positive at every finite thickness but vanishes in both very thin and very thick markets.

最简数学表达是

$$
\underbrace{\phi(mp)}_{\text{accept-now assignment share}}
-
\underbrace{e^{-mp}}_{\text{all rivals wait}}
>0.
$$

这就是 latent-$N$ 模型中取代 fixed-$n$ comparison 的核心 competition wedge。
