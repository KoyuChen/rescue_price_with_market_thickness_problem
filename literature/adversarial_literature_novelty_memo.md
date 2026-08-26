# 对抗式临近文献检索与贡献边界备忘录

**项目：** *Announced Escalation with Strategic Drivers: A Two-Period Model with Latent Market Thickness*  
**检索截点：** 2026-08-25  
**判定目标：** 不是寻找“可以引用的相关文献”，而是主动寻找足以推翻本文首创性表述的最近邻。

## 1. 执行结论

### 总判定

**宽泛贡献不成立；精确交集贡献可以守住。**

Aviv and Pazgal (2008) 不是检索后最接近的实质文献。它仍适合解释“先承诺政策、再解前瞻主体阈值反应、最后优化”的分析架构，以及“等待降价并承担缺货风险”与“等待加价并承担被别人抢单风险”的镜像关系；但引言不能再把它当作唯一或首要的经济近邻。

真正需要在引言正面交锋的四篇是：

1. [Wu et al. (2022), *A Framework for Multi-stage Bonus Allocation in Meal Delivery Platform*](https://arxiv.org/abs/2202.10695)：已经研究同一订单未被接受后进入下一阶段、增加奖金并最大化接单量；
2. [Sigg, Hardt, and Mendler-Dünner (2025), *Decline Now*](https://doi.org/10.1145/3706598.3713966)：已经研究司机拒绝同一订单、平台加价重派，以及劳动力过剩如何改变拒单运动的个体收益；
3. [Chen (2012), *Name Your Own Price at Priceline.com*](https://doi.org/10.1093/restud/rds005)：已经内生化多个私人成本供应商在“现在接受”和“等待更高报价”之间的阈值策略；
4. [Hu, Hu, and Zhu (2022), *Surge Pricing and Two-Sided Temporal Responses in Ride Hailing*](https://pubsonline.informs.org/doi/10.1287/msom.2020.0960)：已经得到前瞻乘客和司机下的两期低—高价格路径及其匹配优势。

检索中**没有发现**一篇同时包含以下结构：平台在任何司机行动前承诺单一请求的失败触发救援支付；同一批私人成本 incumbent 在不知道已实现 Poisson 竞争人数时同时选择 accept-now/wait；首轮全拒既触发下一轮又形成公共信号；乘客以私有价值决定发布及失败后的 abandon/repeat/rescue；平台在内生 cutoff-WPBE 上比较完成率与优化 flat benchmark。

因此，论文不应声称“发明失败后加价”或“首次研究司机等待更高工资”，而应把贡献写成：**为已有的多阶段订单奖金与拒单后加价制度，提供一个包含事前承诺、潜在竞争和内生全拒信号的 Bayesian 均衡微观基础，并证明战略延迟存在时救援加价仍能严格提高完成率。**

## 2. 对抗式判定标准

本文潜在贡献被拆成八个原子维度。单个维度已有文献并不构成贡献；可守的是它们的交集以及由交集产生的定理。

| 维度 | 本文的精确定义 |
|---|---|
| C1 事前承诺 | 在 rider/driver 行动和私有信息实现前公告 \((p_1,p_2)\)，失败后不能重定 \(p_2\) |
| C2 内生失败触发 | 只有首轮无人接受同一请求时，rescue option 才可达 |
| C3 同请求战略等待 | incumbent 为保留同一请求的高价机会而拒绝 \(p_1\)，而非等待未来别的订单或迁移到别的区域 |
| C4 潜在竞争人数 | 所有人只知道公开厚度 \(m\)，不知道已实现的 \(N^I\sim\mathrm{Pois}(m)\) |
| C5 同时广播竞争 | drivers 同时 accept/wait；多人接受时随机选一人，因此立即接受有 assignment competition |
| C6 双边私有决策 | rider 有私有 \(v\)，driver 有私有 \(c\)；rider 决定 post 及失败后的 abandon/repeat/rescue |
| C7 内生公共信号 | “全体拒绝”同时揭示低成本 incumbent 不存在，并决定存活者与新进入者面对的第二轮供给 |
| C8 完成率设计定理 | 解匿名对称纯 cutoff WPBE correspondence，再进行 flat 与 escalation 的完成率比较 |

**击穿标准。** 若已有文献同时覆盖 C1–C8，主贡献不成立；若覆盖“同一请求拒绝—加价—再分配”或“竞争供应商等待更高报价”，则相应的宽泛首创表述已经死亡，即使 C1–C8 的完整交集尚未出现。

## 3. 最近邻威胁矩阵

威胁等级：**3 = 必须改写贡献；2 = 吞掉重要组件；1 = 背景或方法近邻。**

| 文献 | 最危险的重叠 | 它否证的宽泛表述 | 本文仍可守的差异 | 威胁 |
|---|---|---|---|---:|
| [Wu et al. 2022](https://doi.org/10.1145/3534678.3539042) | 同一配送订单多阶段流转；未接后追加 order-specific bonus；平台在预算内最大化接单数 | “首次研究失败后多阶段加价以提高完成率” | 阶段接受率只依赖当期 bonus；未来 bonus 不作为公告菜单进入司机决策；无私人成本 Bayes 博弈、潜在竞争人数、乘客 continuation | **3** |
| [Sigg et al. 2025](https://arxiv.org/abs/2410.12633) | DoorDash 同一订单每次被拒后加 \(\delta\) 并重派；拒单者权衡涨价与错失订单；供给过剩决定参与收益 | “首次刻画拒单后加价、#DeclineNow 或厚度约束等待” | 固定已知 \(N\)；顺序单播；参与比例与共同阈值外生；无私人成本 cutoff 均衡、平台设计、rider 或公共全拒信号 | **3** |
| [Chen 2012](https://academic.oup.com/restud/article/79/4/1341/1573679) | 一名买方向固定 \(N\) 个私人成本卖家多轮报价；首个接受者成交；卖家可等更高报价 | “首次研究竞争供应商在现在接受与等待递增报价间权衡” | \(N\) 固定已知；买方拒绝后再报价且不预先承诺；无平台—rider 分离、Poisson/Palm、存活/进入和完成率设计 | **3** |
| [Hu, Hu, and Zhu 2022](https://pubsonline.informs.org/doi/10.1287/msom.2020.0960) | ride-hailing 两期、前瞻乘客和司机、随机匹配、低—高 penetration surge | “首次研究两期 low-then-high surge 或双边前瞻反应” | 司机的慢反应是区域进入/追涨，不是 incumbent 对同一订单拒绝等待；连续公开供需；\(p_2\) 非事前失败菜单 | **3** |
| [Chen and Hu 2020](https://pubsonline.informs.org/doi/10.1287/msom.2018.0769) | 买卖双方以 Poisson 过程到达，均有私有类型并可等待；中介动态定 bid/ask 和匹配 | “首次研究 Poisson 双边私有类型、前瞻等待和动态支付” | 多主体连续到达的大市场；没有单请求、潜在已实现 rival pool、全拒公共信号或精确两期 flat 比较 | **3** |
| [Qin, Yang, and Liu 2025](https://doi.org/10.1016/j.trc.2025.105318) | 第一轮小半径广播；无人响应后第二轮扩半径；空间 Poisson 供需；优化两轮机制 | “首次研究两轮、失败触发、Poisson 广播 matching” | 操作杠杆是半径和等待时间而非公告工资；接受是概率反应；没有司机为第二轮而战略性拒绝 | **3**（结构） |
| [Sun et al. 2020](https://doi.org/10.1016/j.trb.2020.10.001) | 比较向半径内多司机广播且 first response 获单的 Inform 机制与直接派单；司机内生选择系统 | “首次研究 broadcast、first response 与司机内生选择” | 无失败后第二轮、工资变化、公告菜单或同请求等待；司机选择机制而非基于私人成本抢同一订单 | **2** |
| [Acemoglu, Mostagir, and Ozdaglar 2014](https://www.nber.org/papers/w19852) | 任务每次尝试但未完成后提高奖励；workers 战略选择参与时点；动态价格实施技能层级 | “首次研究 failure-contingent reward escalation” | 失败来自尝试后不能完成，而非所有供应商战略拒绝；技能筛选而非同请求成本竞争；无 rider、Poisson rival pool | **3** |
| [Garg and Nazerzadeh 2022](https://pubsonline.informs.org/doi/10.1287/mnsc.2021.4058) | 司机因 trip duration 的机会成本和未来 surge 拒绝当前行程；设计 IC driver payment | “首次研究司机因预期未来高价而拒单” | 单司机跨任务动态决策；不是同一请求的失败重投；无 rival competition、rider rescue 或全拒后验 | **2–3** |
| [Bai, Heese, and Tripathy 2023](https://journals.sagepub.com/doi/full/10.1111/poms.14064) | 平台看不见实际供给；providers 隐藏上线人数以触发 surge；平台用 bonus 消除 withholding | “首次研究隐藏供给与战略 withholding 触发涨价” | 集体可协调的 availability manipulation；非单请求上独立私人成本 accept/wait；无失败菜单和 Palm assignment wedge | **2–3** |
| [Wang et al. 2026 working paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7240784) | broadcasting 下司机内生接单；平台联合选择价格和匹配半径 | “首次在广播中联合研究价格、匹配与司机内生选择” | 静态市场均衡；无失败重投、公告后续工资、同请求等待和公共失败信号 | **2** |
| [Ekbatani et al. 2026, Part I](https://arxiv.org/abs/2603.21533)；[Part II](https://arxiv.org/abs/2603.21531) | Lyft 的 non-exclusive notification 同时向多名司机广播；比较 First Acceptance 与 Best Acceptance，并分析 marketplace effects | “首次研究同时广播、first-accept 分配或其完成率作用” | 单周期；接受概率外生；无工资菜单、战略等待或失败后重发 | **2–3（广播）** |
| [Dasu and Tong 2010](https://doi.org/10.1016/j.ejor.2009.11.018); [Correa, Montoya, and Thraves 2016](https://pubsonline.informs.org/doi/10.1287/opre.2015.1452) | 期初公告 posted/contingent 价格；战略消费者等待；价格可依销售或剩余库存状态 | “首次研究事前公告的状态依赖价格菜单” | 需求侧等待降价；库存状态而非供应商全拒；无双边私有类型和同请求 assignment competition | **2** |
| [Aviv and Pazgal 2008](https://doi.org/10.1287/msom.1070.0183) | 固定公告政策后解战略消费者阈值，再评价/优化政策；等待与可得性风险 | “政策—均衡—优化的分析顺序本身是新贡献” | 需求侧 markdown/stockout，是本文机制的镜像而非同一市场；没有供应侧等待、失败触发和潜在 Poisson 竞争 | **2（方法）** |

### 检索后的“最近”应如何理解

- **制度/运营最近：Wu et al. (2022)。** 同一订单、多阶段、失败后 bonus、完成量目标都重合。本文最重要的差异是把 Wu et al. 明确排除的跨阶段战略反应内生化。
- **行为机制最近：Sigg et al. (2025)。** “拒绝—同单涨价—重派—过度供给约束收益”几乎贴脸。本文的增量是从外生集体阈值转向私人成本个体 Bayes 均衡和平台完成率设计。
- **博弈结构最近：Chen (2012)。** 竞争供应商等待更高报价、首个接受者获胜和 cutoff strategy 都已存在。本文的增量是事前承诺、潜在人数、同时广播及失败信号。
- **平台市场最近：Hu et al. (2022) 与 Chen and Hu (2020)。** 它们已经覆盖双边前瞻反应、Poisson 到达和动态平台价格，但不是单请求的 failure-triggered commitment。
- **方法镜像最近：Aviv and Pazgal (2008)。** 可保留，但应降为一组 announced/contingent pricing 文献中的方法锚点。

## 4. 已被否证、可守与有条件可守的主张

### 4.1 应删除或明确否认的主张

以下任何表述都会被上述文献直接击穿：

- “本文首次研究失败后的递增支付或多阶段奖金。”
- “本文首次发现司机会拒绝当前订单以等待更高支付。”
- “本文首次研究同一订单拒单后加价及市场厚度的作用。”
- “本文首次得到 ride-hailing 的两期低—高 surge path。”
- “本文首次研究 Poisson 双边市场中前瞻买卖双方与动态定价。”
- “本文首次研究不可见供给下 providers withholding 以触发 surge。”
- “本文首次提出事前公告的 contingent pricing menu。”
- “本文首先证明厚度对动态定价价值呈单峰关系。”目前只证明两端消失，不能推出全局单峰。

### 4.2 可以作为主贡献的精确交集

**贡献 1：单请求公告式救援的均衡微观基础。** 平台在所有私人信息和司机行动之前承诺 \((p_1,p_2)\)；潜在 incumbent 对同一请求同时决定立即接受还是保留失败后的救援选择权。该问题区别于平台逐阶段在线重算 bonus、司机等待未来其他订单或司机迁移追逐系统级 surge。

**贡献 2：潜在竞争下的内生失败信号。** 已实现的 \(N^I\) 对平台、rider 和 driver 均不可见。全体拒绝不仅是进入第二期的触发器，也揭示不存在首轮低成本接受者。Poisson/Palm 结构把“立即接受时的随机分配份额”与“所有 rivals 都等待时才可达的救援概率”分开，形成

\[
\phi(ma)-e^{-ma}>0.
\]

这条式子本身是技术工具，不宜单独声称为贡献；贡献在于它如何改变公告菜单的均衡设计。

**贡献 3：战略延迟下的完成率改进定理。** 在匿名对称纯 cutoff WPBE 类内，刻画任意公告菜单的均衡 correspondence，并证明：从 active flat payment 出发，只要正质量 riders 会启用救援，小幅公告 escalation 即使诱发首轮等待仍严格提高完成率；在 \(\gamma=0,\alpha>0,\beta>1/2\) 的条件下，它严格优于优化后的 flat benchmark。

**贡献 4：厚度与 fresh entry 的边界规律。** escalation value 在有限正厚度下可严格为正，但在 \(m\to0\) 和 \(m\to\infty\) 时消失；fresh entry 改变薄市场中救援价值的来源和阶数。除非进一步证明，不应把两端消失写成全局单峰。

### 4.3 必须加限定词的主张

- “equilibrium robust” 只能指**匿名、对称、纯 cutoff WPBE 类内**及文中采用的保守选择，不能写成对所有 PBE 的 worst-case guarantee。
- “escalation outperforms flat” 必须附上 active rescue、survival、\(\beta\)、entry 等相应条件。
- 目前证明的是**局部小幅 escalation 的价值**，不是全局最优 dynamic menu，也没有一般的最优菜单存在性结论。
- “latent thickness” 必须通过已知 \(N\) 或公开供给 benchmark 证明其经济作用，不能只依赖 Poisson 计算便利。

## 5. 建议采用的贡献表述

### 中文核心表述

> 本文不以失败后加价或多阶段奖金本身为贡献。我们研究的是一个此前尚未被刻画的单请求承诺问题：平台在司机行动前公告失败触发的救援支付；已实现的本地供给人数不可见，私人成本 incumbent 同时权衡立即抢单与等待同一请求的更高支付。全体拒绝既决定救援是否可达，又形成关于潜在竞争的公共信号。我们刻画该博弈的对称 cutoff-WPBE correspondence，并证明在明确条件下，小幅救援加价尽管诱发战略延迟，仍能严格提高完成率并优于优化的 flat benchmark。

### 可直接用于英文引言的贡献段

> We do not claim to introduce multistage bonuses or failure-contingent pay increases. Instead, we provide an equilibrium microfoundation for an announced order-level rescue policy. Before any supplier acts, the platform commits to a payment that becomes available only after universal rejection. Private-cost incumbents simultaneously trade off current assignment competition against the option to wait for a higher payment, while neither they nor the platform observe the realized Poisson rival pool. Universal rejection therefore both activates rescue and generates a public signal about available supply. We characterize the anonymous symmetric pure-cutoff WPBE correspondence and show that, under stated conditions, a small committed rescue step raises completion despite the strategic delay it creates and can strictly outperform the optimized flat-payment benchmark.

### 可直接用于英文文献定位的段落

> The closest operational work studies multistage, order-specific bonuses while modeling each stage's acceptance probability as a function of the current bonus (Wu et al. 2022). The closest behavioral model studies workers who collectively reject an order so that it is reoffered at a higher payment, but takes the participation rate and rejection threshold as primitives (Sigg et al. 2025). Chen (2012) endogenizes private-cost sellers' willingness to wait for higher offers, whereas the buyer does not precommit and the number of sellers is fixed and known. Relative to these studies, our focus is the interaction of ex ante commitment, simultaneous same-request competition, and an unobserved realized supplier pool. This interaction makes universal rejection an endogenous public signal and yields a completion-design result that is absent from the neighboring models.

### 一句话版本

> We isolate the Bayesian commitment mechanism behind an announced, failure-triggered rescue payment: latent same-request competition disciplines strategic supplier delay strongly enough that a small rescue step can increase completion.

## 6. 建议重构文献综述的顺序

不要再用 Aviv (2008) 单篇统领。建议改成三组，并在三组之后明确交集：

1. **同单多阶段奖金与广播机制：** Wu et al. (2022), Qin et al. (2025), Wang et al. (2026)。先承认制度和运营问题已有；指出它们未内生化对公告后续奖金的等待。
2. **供应商拒绝、递增采购与战略供给：** Sigg et al. (2025), Chen (2012), Acemoglu et al. (2014), Garg and Nazerzadeh (2022), Bai et al. (2023)。先承认拒单、等待和隐藏供给机制已有；指出本文同时引入个体私人成本、潜在竞争人数和单请求失败信号。
3. **双边平台动态定价与公告式 contingent pricing：** Chen and Hu (2020), Hu et al. (2022), Aviv and Pazgal (2008), Dasu and Tong (2010), Correa et al. (2016)。把 Aviv 放在“承诺与阈值分析的镜像文献”中，而不是最近的 ride-hailing 近邻。

三组之后用一句话收口：**现有研究分别覆盖多阶段奖金、拒单后加价、竞争供应商等待、双边前瞻反应和公告式 contingent pricing；本文研究这些机制在潜在 Poisson 同请求竞争中的交集。**

## 7. 最可能的审稿人攻击及应对

### A. “Wu 的现场实验没有发现司机等 bonus；你的战略渠道是否制度上不存在？”

这是第一优先级问题。Wu et al. 在每一阶段在线重算并展示当前 bonus；论文既未建模也未记录对未来 bonus path 的期初公开承诺，并假定第 \(t\) 阶段接受率仅取决于当前价格。其实验中“10 分钟后固定 bonus 未降低前 10 分钟接单率”支持的是**该实际机制下没有明显 anticipatory waiting**，不能直接否证公告式救援。论文必须明确公告发生在哪里：算法公开规则、平台保证的 rescue schedule，或 rider 事前可见的 top-up option。更好的定位不是“所有多阶段奖金都会诱发等待”，而是“平台若选择以公告换取可信承诺，何时等待成本仍小于救援收益”。

### B. “谁支付，为什么平台只最大化完成率？”

当前设定由 rider 向选中 driver 支付，平台把支付视为 transfer。这更接近 rider-bid、tip/top-up、货运或任务平台，而不是标准 Uber fare/surge。需要明确制度对象；否则应区分 rider fare 与 platform-funded bonus，并检验利润/预算目标下结论是否保留。

### C. “你只在受限均衡类和局部扰动中得到结果。”

必须避免把 pessimistic symmetric-cutoff value 写成所有 PBE 的最坏值。最好给出唯一性区域、局部所有分支上的方向性，或对混合/非对称策略的讨论。若不能求全局最优菜单，就把论文标题和摘要聚焦为“local value of committed rescue”。

### D. “Poisson/Palm 只是算得方便。”

增加公开/已知 \(N\) benchmark，展示 \(\phi(ma)-e^{-ma}\) 的哪一部分来自随机分配竞争、哪一部分来自人数潜在及失败后验。若去掉 latent \(N\) 后主要定理仍完全相同，“latent thickness”不宜放在标题核心位置。

### E. “广播订单通常先响应先得，而不是同时接受后均匀抽取。”

Qin et al. (2025)、Wang et al. (2026) 以及 Lyft 的 non-exclusive notification 研究（Ekbatani et al. 2026 I–II）使这个问题更尖锐。应解释 uniform selection 是 reduced-form simultaneous response，或增加 response-time/first-accept robustness。

### F. “厚度结果是否真的新且强？”

两端消失不是单峰。厚度应作为机制比较静态而非独立主贡献，除非能证明内部唯一峰值、已知供给对照或可检验预测。

## 8. 论文修改优先级

### 必须在下一版完成

1. 把 Wu (2022)、Sigg (2025)、Chen (2012)、Hu–Hu–Zhu (2022)、Chen–Hu (2020)、Qin (2025) 加入引言和文献综述，并主动说明各自已经覆盖什么。
2. 删除所有宽泛的 first/novel 表述；摘要聚焦“announced single-request commitment + latent rival pool + endogenous universal rejection signal + completion theorem”。
3. 将 Aviv (2008) 从“最接近的实质文献”降为方法镜像，并改用三组文献结构。
4. 解释公告的制度基础，以及为何 Wu 的 nonannounced bonus 结果不构成反例。
5. 严格限定 equilibrium class、局部结果和 optimized-flat 优越性的参数条件。

### 最能增加论文说服力的理论扩展

1. 已知 \(N\)/公开本地供给 benchmark；
2. first-response-wins 而非 uniform random assignment 的稳健性；
3. platform-funded bonus、预算或利润目标的稳健性；
4. equilibrium uniqueness/selection 区域；
5. 公告与不公告的直接机制比较。

## 9. 建议引用的核心来源

- Aviv, Y., and A. Pazgal. 2008. [Optimal Pricing of Seasonal Products in the Presence of Forward-Looking Consumers](https://doi.org/10.1287/msom.1070.0183). *M&SOM* 10(3): 339–359.
- Chen, C.-H. 2012. [Name Your Own Price at Priceline.com: Strategic Bidding and Lockout Periods](https://doi.org/10.1093/restud/rds005). *Review of Economic Studies* 79(4): 1341–1369.
- Chen, Y., and M. Hu. 2020. [Pricing and Matching with Forward-Looking Buyers and Sellers](https://pubsonline.informs.org/doi/10.1287/msom.2018.0769). *M&SOM* 22(4): 717–734.
- Hu, B., M. Hu, and H. Zhu. 2022. [Surge Pricing and Two-Sided Temporal Responses in Ride Hailing](https://pubsonline.informs.org/doi/10.1287/msom.2020.0960). *M&SOM* 24(1): 91–109.
- Wu, D. et al. 2022. [A Framework for Multi-stage Bonus Allocation in Meal Delivery Platform](https://arxiv.org/abs/2202.10695). *KDD 2022*: 4195–4203.
- Sigg, D., M. Hardt, and C. Mendler-Dünner. 2025. [Decline Now: A Combinatorial Model for Algorithmic Collective Action](https://doi.org/10.1145/3706598.3713966). *CHI 2025*, Article 912.
- Qin, Y., H. Yang, and R. Liu. 2025. [A Two-Round Broadcasting Matching Mechanism in Ride-Sourcing Markets](https://doi.org/10.1016/j.trc.2025.105318). *Transportation Research Part C*.
- Sun, H., R. Teunter, G. Hua, and T. Wu. 2020. [Taxi-Hailing Platforms: Inform or Assign Drivers?](https://doi.org/10.1016/j.trb.2020.10.001). *Transportation Research Part B* 142: 197–212.
- Garg, N., and H. Nazerzadeh. 2022. [Driver Surge Pricing](https://pubsonline.informs.org/doi/10.1287/mnsc.2021.4058). *Management Science* 68(5): 3219–3235.
- Acemoglu, D., M. Mostagir, and A. Ozdaglar. 2014. [Managing Innovation in a Crowd](https://www.nber.org/papers/w19852). NBER Working Paper 19852.
- Bai, J., H. S. Heese, and A. Tripathy. 2023. [Hiding in Plain Sight: Surge Pricing and Strategic Providers](https://journals.sagepub.com/doi/full/10.1111/poms.14064). *Production and Operations Management* 32(12).
- Dasu, S., and C. Tong. 2010. [Dynamic Pricing When Consumers Are Strategic](https://doi.org/10.1016/j.ejor.2009.11.018). *European Journal of Operational Research* 204(3): 662–671.
- Correa, J., R. Montoya, and C. Thraves. 2016. [Contingent Preannounced Pricing Policies with Strategic Consumers](https://pubsonline.informs.org/doi/10.1287/opre.2015.1452). *Operations Research* 64(1): 251–272.
- Ekbatani et al. 2026. [Non-Exclusive Notifications for Ride-Hailing at Lyft I: Single-Cycle Approximation Algorithms](https://arxiv.org/abs/2603.21533); [Part II: Simulations and Marketplace Analysis](https://arxiv.org/abs/2603.21531). Working papers.

## 10. 检索范围与保留意见

对抗检索覆盖了 announced/contingent strategic pricing、dynamic procurement、failure-contingent rewards、ride-hailing surge、strategic driver rejection/withholding、broadcast matching、Poisson two-sided matching 等词族，并优先核对出版社页面、DOI 页面、作者稿和会议正式记录。检索目标是寻找反例而非证明不存在，因此最稳妥的措辞仍应是：**“To our knowledge, we do not find a model combining …”**，而不是无条件的 “the first paper to …”。2026 年的 Wang et al. 仍是 SSRN working paper，发表状态和版本需在投稿前再次核验。
