# 第二轮对抗式临近文献审查与贡献边界

**项目：** *Announced Rescue Payments with Strategic Drivers: Commitment, Universal Rejection, and Latent Local Supply*
**检索截点：** 2026-08-26
**审查目标：** 优先寻找能够击穿贡献主张的文献，而不是扩充一份“相关文献清单”。
**证据原则：** 模型事实优先核对出版社全文/摘要、作者稿、arXiv、SSRN 正文；搜索摘要只用于发现，不单独支撑关键判断。

## 1. 执行结论

### 1.1 第二轮判定

**宽泛的机制贡献不成立；第一轮所写的“四项结构交集”也仍然过宽；定理级贡献可以在更窄边界内守住。**

本轮最重要的新发现不是 2026 年的 ride-hailing working paper，而是 [Li and Kuo (2013)](https://doi.org/10.1007/s10479-013-1331-6) 的离散荷兰式拍卖。该文在拍卖前设置有限价格时钟，上一价格无人接受才进入下一价格；竞标人数服从 Poisson 分布；同一价位多人接受时随机分配；拍卖人优化整条价格路径。把出售方的降价时钟镜像成采购方的加价时钟后，它已经覆盖了“同一标的、预先设定的低—高价格、全拒后进入下一 tick、随机 Poisson participation、接受时的分配竞争、优化价格路径”这一大块结构。商业采购系统也明确实施这种反向荷兰式时钟：买方从低价开始自动加价，第一位供应商接受即成交，等待意味着可能被竞争者抢走订单（[SAP Ariba 官方说明](https://help.sap.com/docs/strategic-sourcing/managing-events-with-guided-sourcing/about-dutch-auctions)）。因此，**公告式 rescue clock 本身不是新机制。**

更强的是，[Buchanan, Gjerstad, and Porter (2016)](https://doi.org/10.1002/soej.12145) 已在多单位离散 Dutch clock 中建立实现 group size 不公开、竞标者从连续无人接受的历史更新规模后验、并求对称 Bayesian-Nash bidding functions 的模型。[Carare and Rothkopf (2005)](https://doi.org/10.1287/mnsc.1040.0328) 求解带等待交易成本的 slow Dutch 均衡；[Shneyerov (2014)](https://doi.org/10.1007/s00199-014-0825-z) 则刻画买方比卖方更不耐心时的最优动态 clock。因而“隐藏人数 + 无接受历史 + 战略等待 + 折现/时钟优化”的宽组合也已有明确先例。

Li and Kuo 并未求解供应商在当前接受与等待更高支付之间的 Bayesian 均衡；它把估值跨越时的接受行为直接嵌入拍卖收入公式。Buchanan et al. 是多单位拍卖，Carare–Rothkopf 与 Shneyerov 通常也没有本文的单请求 rider continuation。上述 Dutch 文献都没有私有价值 rider 的 post/abandon/repeat/rescue、incumbent survival/fresh entry 或完成率目标。故仍可守的对象必须同时写入：

1. **公告时钟下内生的 same-request 战略延迟；**
2. **私有价值 rider 在全拒后的内生 continuation；**
3. **全拒所诱导的供给后验以及 incumbent survival/fresh entry；**
4. **在明确 cutoff-WPBE 类内的完成率定理、优化 flat 比较与 no-entry 全局设计。**

不能再把贡献概括成“事前承诺 + 同请求竞争 + 不可见人数 + 全拒信号”，也不能把“隐藏人数下由无接受历史更新信念”或“折现战略等待”补进去后宣称新颖。Li and Kuo、Buchanan et al. 及 slow-Dutch 文献已分别吞掉这些拍卖镜像。贡献必须落在**把单请求司机等待均衡嵌入 private rider continuation，并由此得到 failure posterior、survival/entry 与完成率设计定理**上。

### 1.2 2008 Aviv 文献的正确位置

[Aviv and Pazgal (2008)](https://doi.org/10.1287/msom.1070.0183) 仍然是很好的**方法镜像**：先固定公告政策，求前瞻主体的阈值反应，再评价/优化政策；消费者等待降价并承担缺货风险，与司机等待加价并承担失单风险方向相反。但它不是实质最近邻。制度/结构上更近的是 Li and Kuo、Wu、Sigg、Chen 和 Bai；字面上的两期 contingent preannouncement 也可由 [Correa, Montoya, and Thraves (2016)](https://doi.org/10.1287/opre.2015.1452) 补足。

### 1.3 最终新颖性结论

截至检索截点，我们**没有找到**一篇文献同时完成以下任务：在单一请求上事前公告两期支付；让不知道实现竞争人数的私人成本 incumbents 在“立即竞争分配”与“折现等待同一请求”之间形成内生 cutoff-WPBE；让全拒后的私有价值 rider 内生选择 abandon/repeat/rescue；在 survival/fresh entry 下刻画供给后验；并以完成率为目标比较优化 flat 与 rescue menu。

这是“未检索到完整先例”，不是数学意义的不存在证明。安全措辞应为 **“To our knowledge, among the models reviewed…”**，不能写无条件的 “first”。

## 2. 本轮的 novelty-kill test

### 2.1 八个判定维度

| 维度 | 当前论文中的严格含义 |
|---|---|
| K1 事前时钟/菜单 | 私人行动前固定 \((p_1,p_2)\)，失败后不能重定第二笔支付 |
| K2 同请求失败触发 | 只有同一请求一期无人接受，第二期才可达 |
| K3 内生战略等待 | 私人成本 incumbent 因未来同单支付和竞争风险内生选择 accept/wait |
| K4 潜在实现人数 | 公开厚度已知，但实现的本地 incumbent 数对玩家不可见 |
| K5 同时分配竞争 | incumbents 同时响应；多人接受时存在随机分配份额 |
| K6 私有 rider continuation | rider 有私有价值，并在失败后选择 abandon/repeat/rescue |
| K7 失败后验 | universal rejection 同时触发 continuation 并改变对可用供给的公共信念 |
| K8 完成率设计定理 | 求指定均衡类，再比较优化 flat 与动态菜单的完成率 |

### 2.2 击穿规则

- 若已有文献覆盖 K1–K8，核心贡献死亡。
- 若文献覆盖 K1、K2、K4、K5，即使没有 K3 的均衡，也足以击穿“公告 rescue clock + latent competition”这一宽主张。
- 若文献覆盖 K3，则“司机/供应商首次在当前接受与未来高价之间权衡”死亡。
- 若文献覆盖 K4 和公告的 supply-contingent policy，则“不可见供给与公告政策的结合”死亡。
- 真正可守的贡献必须对应本文已经证明的定理，而不是一组特征标签。

## 3. 最高威胁证据账本

### 3.1 Li and Kuo (2013)：本轮发现的最强结构攻击

**一手来源：** [Springer / *Annals of Operations Research*](https://link.springer.com/article/10.1007/s10479-013-1331-6)，DOI `10.1007/s10479-013-1331-6`。

**已核实的重叠：**

- 在事件开始前设定有限的离散价格 levels；
- 只有更高价格未被任何 bidder 接受，时钟才进入下一价位；
- bidder 私有 valuation；人数服从 Poisson 分布；
- 同 tick 多人接受时随机选中一人；
- 拍卖人把整条价格路径写成凹的非线性规划并求全局最优。

**证据边界：** 正式模型没有清楚写明每个 bidder 都观察不到实现的 (N)，也没有形式化完整价格向量对 bidder 的期初公开与共同知识；接受规则又不依赖人数或历史。因此该文证明的是随机 Poisson 人数与预设离散路径的设计先例，不能单独用来证明“隐藏人数后验学习”。这一更强先例由 Buchanan et al. 提供。

**它杀死的表述：**

- “首次研究预先公告的同标的低—高价格时钟”；
- “首次把 Poisson-random participation 与离散 contingent price path 结合”；
- “随机分配竞争使 waiting 有失单风险是新的机制”；
- “policy–threshold–optimization 顺序本身是贡献”。

**仍有的关键缺口：** 该文是出售方 Dutch clock；采购方向是其镜像。更重要的是，它没有求解由未来价格诱发的内生 strategic-delay equilibrium，没有 rider continuation、survival/entry 或 completion-vs-flat 定理。因此它把本文从“机制创新”压缩为“带双边 continuation 的均衡微观基础和完成率定理”。

**威胁等级：3+（必须重写贡献）。**

### 3.2 Buchanan–Gjerstad–Porter、Carare–Rothkopf 与 Shneyerov：Dutch 均衡攻击

**一手来源：** [Buchanan, Gjerstad, and Porter (2016), Wiley](https://onlinelibrary.wiley.com/doi/10.1002/soej.12145)；[Carare and Rothkopf (2005), INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.1040.0328)；[Shneyerov (2014), DOI](https://doi.org/10.1007/s00199-014-0825-z)。

- Buchanan et al. 的竞标者只知道 group size 属于两个可能值，并根据 clock 上持续没有接受更新后验；剩余单位信息只在其 disclosure treatment 中公开，不能当作所有处理共有的信息。论文推导对称 Bayesian-Nash bidding functions。它直接击穿“隐藏实现人数 + 非接受历史 + 战略等待/学习的组合首次出现”。但它是 uniform-price multi-unit Dutch auction、到第 $m$ 次接受才停止，不是单请求 first-accept，也没有 rider continuation。
- Carare and Rothkopf 在 slow Dutch auction 中加入随等待累积的 transaction cost，并求对称博弈均衡；“等待的真实成本改变抢先时点”不是本文新机制。
- Shneyerov 假定 buyers 比 seller 更不耐心，刻画 revenue-maximizing slow clock，并证明最优 clock 真正动态且包含延迟；“异质耐心 + 动态 clock 优化”也不能作为宽贡献。

三篇一起表明，本文不能通过给 Li–Kuo 补上“均衡、隐藏人数后验、折现”来重新恢复机制新颖性。残差仍是单请求采购镜像中 rider 的私有 continuation、survival/entry 及 completion-vs-flat 的特定定理包。

**威胁等级：3+（直接占据 strategic clock 的理论核心）。**

### 3.3 Wu et al. (2022)：最接近的实际多阶段订单奖金

**一手来源：** [作者公开全文](https://arxiv.org/abs/2202.10695)，KDD 正确 DOI 为 [`10.1145/3534678.3539202`](https://doi.org/10.1145/3534678.3539202)。旧备忘录中的 `3539042` 是错误 DOI。

**已核实的重叠：** 同一外卖订单同时推送给附近多名司机；未接单且未取消的订单进入下一阶段；bonus 可在 10、20 分钟等节点上升；平台在预算内最大化被接受的订单数量，A/B test 报告取消显著下降。

**最危险的反证：** 论文假设阶段接受率只依赖当前价格，并做了一个“10 分钟后固定 bonus”的消融实验；作者报告前 10 分钟接受率几乎不变，并明确解释为没有观察到司机等 bonus。

**为什么没有直接否证本文：** Wu 的在线算法在每个阶段实时计算并展示当期 bonus；正文没有说明完整未来 bonus path 在第一阶段被公开并承诺。因此这是真实制度下对 anticipatory waiting 的不利证据，但不是对“已知的事前承诺菜单”的干净检验。最安全的写法是“does not specify an ex-ante announcement of the full future path”，不能武断写成 “nonannounced”。

**论文必须承担的外部效度负担：** 解释在哪种制度中 future rescue schedule 会被司机事前知道并相信；否则理论中的 K3 可能并不是运营上重要的边际。

**威胁等级：3（运营与经验反证）。**

### 3.4 Sigg, Hardt, and Mendler-Dünner (2025)：最接近的行为机制

**一手来源：** [arXiv 全文](https://arxiv.org/abs/2410.12633)，CHI DOI [`10.1145/3706598.3713966`](https://doi.org/10.1145/3706598.3713966)。

模型中固定的 \(N\) 名 workers 服务连续订单；平台把同一订单随机给一名 idle worker，每次拒绝后支付增加 \(\Delta\) 并重新随机派发，包括刚拒绝者。collective participants 使用外生共同阈值，nonparticipants 在任何价格接受。论文证明集体平均收益为正，并刻画 labor oversupply 如何损害参与者收益。

它已经吞掉“拒绝同单—涨价重派—可能失单—市场厚度影响等待收益”。本文剩余差异是：个体私人成本与内生 cutoff、同时广播而非顺序单播、rider continuation、潜在人数、平台完成率设计。

**威胁等级：3（行为近邻）。**

### 3.5 Bai, Heese, and Tripathy (2023)：不可见供给与公告政策的强攻击

**一手来源：** [出版社开放全文](https://journals.sagepub.com/doi/10.1111/poms.14064)。

平台先公告随显示在线供给 \(m\) 变化的价格/补偿规则 \((p(m),w(m))\)；真实本地供给 \(M\) 是随机变量且平台不可见；providers 随后协调隐藏一部分在线人数，以诱发更高 compensation。论文求 subgame-perfect equilibrium 并设计 bonus/optimal policy 以消除 withholding。

这意味着以下表述都不成立：

- “首次研究事前政策、随机不可见供给和 strategic withholding”；
- “latent supply 使公告 compensation policy 产生操纵激励是新的”；
- “平台用 bonus 对抗供应商等待/隐藏供给是新的”。

它与本文不同之处是集体选择显示在线人数，而不是匿名司机基于私人成本同时决定同一请求 accept/wait；平台观察的是操纵后的 \(m\)，没有全拒后的 rider continuation 或同单 failure posterior。

**威胁等级：3（潜在供给/承诺组件）。**

### 3.6 Chen (2012)：竞争供应商等待更高报价

**一手来源：** [*Review of Economic Studies*](https://academic.oup.com/restud/article/79/4/1341/1573679)。

一名 buyer 在多轮向固定、已知数量的私人成本 sellers 报价；第一个接受者成交；sellers 具有阈值策略并可等待更高报价。它直接杀死“首次研究竞争供应商 accept-now versus wait-for-more”。差异是 buyer 不事前承诺、卖家数固定已知、无 platform–rider 分离、Poisson/Palm、survival/entry 和完成率设计。

**威胁等级：3（博弈结构）。**

### 3.7 Ride-hailing 接受/拒绝、广播和两阶段设计

- [Feng and Wang (2023)](https://doi.org/10.1016/j.tre.2023.103175) 已在竞争环境中求司机 acceptance/rejection 的 Nash 与 cognitive-hierarchy 行为；它是跨地区无限期系统，不是同单未来工资。
- [Meskar, Aslani, and Modarres (2023)](https://doi.org/10.1016/j.trc.2023.104200) 联合优化 fare、driver compensation 和 matching rate，并允许司机拒单、迁移及动态 fleet；没有失败后的同单公告加价。
- [Guda and Subramanian (2019)](https://doi.org/10.1287/mnsc.2018.3050) 与 [Afèche, Liu, and Maglaras (2023)](https://doi.org/10.1287/msom.2023.1221) 已研究战略司机、竞争、relocation、forecast/controls 和 worker incentives；不是同请求 rescue。
- [Horner, Pazour, and Mitchell (2021)](https://doi.org/10.1016/j.tre.2021.102419) 与 [Ausseil, Pazour, and Ulmer (2022)](https://doi.org/10.1287/trsc.2022.1133) 优化多供应商通知/菜单并处理随机拒绝与 duplicate selection；接受是 stochastic response，不是跨期战略等待。
- [Qin, Yang, and Liu (2025)](https://doi.org/10.1016/j.trc.2025.105318) 在无人响应后扩大第二轮广播半径，并优化半径和等待时间；接受是异质概率反应，不是对未来工资的战略等待。
- [Feng, Niazadeh, and Saberi (2023)](https://doi.org/10.1287/opre.2022.2398) 的 two-stage 是为即将到来的未来需求 batching 并设计竞争算法，不是同一请求 rescue。
- [Wang et al. (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7240784) 在 broadcasting 静态均衡中让司机按距离/时间价值内生接单，平台联合选 fare 与半径；无跨期同单加价。该文是 SSRN working paper，DOI `10.2139/ssrn.7240784`。
- [Ekbatani et al. (2026), Part I](https://arxiv.org/abs/2603.21533) 和 [Part II](https://arxiv.org/abs/2603.21531) 研究 Lyft non-exclusive notifications、notification set、First-Accept/Best-Accept 与长期 marketplace effects；接受是给定的 pair-specific probability，不是私人成本 strategic waiting。两篇均为 working papers。

这些工作共同杀死“首次研究司机拒绝”“首次研究同时广播”“首次研究两轮无响应后再尝试”“首次研究平台在广播下联合价格和匹配”等表述。

## 4. 维度矩阵

符号：**●** 明确覆盖；**◐** 部分/镜像覆盖；**—** 未覆盖。矩阵只比较结构，不代表论文质量或总体相似度。

| 文献 | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **本文** | ● | ● | ● | ● | ● | ● | ● | ● |
| Li–Kuo 2013 | ● | ● | — | ◐ | ● | — | ◐ | ◐ |
| Buchanan–Gjerstad–Porter 2016 | ● | ◐ | ● | ● | ◐ | — | ◐ | ◐ |
| Carare–Rothkopf 2005 | ● | ◐ | ● | — | ◐ | — | ◐ | ◐ |
| Shneyerov 2014 | ● | ◐ | ● | — | ◐ | — | ◐ | ◐ |
| Wu et al. 2022 | —/◐ | ● | — | ◐ | ◐ | ◐ | — | ◐ |
| Sigg et al. 2025 | ◐ | ● | ◐ | — | ◐ | — | — | — |
| Bai et al. 2023 | ● | — | ◐ | ● | — | ● | — | ◐ |
| Chen 2012 | — | ◐ | ● | — | ◐ | — | — | — |
| Hu–Hu–Zhu 2022 | ◐ | — | ◐ | — | ◐ | ● | — | ◐ |
| Chen–Hu 2020 | ◐ | — | ● | ◐ | ◐ | ● | — | ◐ |
| Qin et al. 2025 | ◐ | ● | — | ◐ | ● | ◐ | — | ◐ |
| Feng–Niazadeh–Saberi 2023 | ● | — | — | ◐ | ● | ◐ | — | ◐ |
| Wang et al. 2026 WP | — | — | ◐ | ◐ | ● | ● | — | ◐ |
| Ekbatani et al. 2026 WP | — | — | — | ◐ | ● | ◐ | — | ◐ |
| Aviv–Pazgal 2008 | ● | ◐ | ◐ | — | — | — | ◐ | ◐ |
| Correa et al. 2016 | ● | ● | ◐ | — | — | — | ◐ | ◐ |

### 矩阵后的关键修正

第一轮把“C1–C8 的完整交集”作为安全贡献仍不够精确，因为 K1、K2、K4、K5 的拍卖镜像已经被 Li and Kuo 高度覆盖。最终贡献不能是勾选更多格子，而必须写成：**在这一已知 clock architecture 中，本文内生化 discounted supplier delay 与 private rider continuation，并得到指定均衡类中的完成率定理。**

## 5. 逐项杀死宽泛主张

以下表述应删除或主动否认：

- “本文首次提出失败后加价、多阶段奖金或 rescue pricing。”
- “本文首次研究供应商等待未来更高支付。”
- “本文首次把事前 price clock、Poisson 人数和 first acceptance 结合。”
- “本文首次研究同一订单被拒后涨价重派及厚度影响。”
- “本文首次研究不可见真实供给下的公告 compensation rule。”
- “本文首次把隐藏实现人数、无接受历史的后验更新与战略等待结合。”
- “本文首次把司机/供应商折现与最优动态 price clock 结合。”
- “本文首次研究两轮 broadcast、first-response 或无响应后的第二次尝试。”
- “本文首次得到 ride-hailing 的 low-then-high surge path。”
- “本文首次证明厚度价值单峰。”论文只证明连续性、两端速率和正的有限最优点；\(\beta<1/2\) 时严格单峰为假，\(\beta\ge1/2\) 尚未证明。
- “承诺本身有价值。”论文没有与 unannounced/adaptive policy 做直接机制比较，不能把因果价值归给 announcement。

## 6. 当前可以守住的定理级贡献

### 6.1 一般模型：均衡微观基础，而非机制发明

在任意 survival \(\alpha\)、fresh entry \(\gamma\) 和 incumbent discount \(\delta\) 下，本文在**匿名、对称、纯 first-period driver cutoff WPBE** 类内刻画任意菜单的均衡 correspondence，包括 Palm rival distribution、全拒后的 Poisson splitting、rider continuation、边界 cutoff 和 tie-breaking。该结论不覆盖所有 mixed/asymmetric PBE。

### 6.2 局部 rescue 定理

对任意**固定** fresh-entry rate \(\gamma\)，只要 active-rescue 条件成立，小幅公告 escalation 存在唯一邻近 cutoff，且完成率右导数严格为正。不能写成对无界 \(\gamma\) 共享一个统一邻域的 “uniform across entry rates”。

### 6.3 无新进入基准中的全局完成率设计

在 \(\gamma=0\)、uniform types、指定 cutoff equilibrium class 和 completion objective 下：

- 每个菜单有唯一 numeric cutoff；
- 固定 \(p_1\) 的最优 rescue 精确分成 reject-all、tangent-rescue、repeat-only；
- 二维菜单问题化为连续的一维最大化并证明 attainment；
- 若 \(\alpha>0\) 且 \(\beta\ge1/2\)，优化 dynamic menu 严格优于优化 flat menu；
- 更一般地，gain set 由内生 patience threshold \(\beta_c(m,\alpha,\delta)\) 精确刻画。

这才是最强可守贡献。不要写成不带条件的 “full platform policy problem”。

### 6.4 厚度与 incumbent discount

在 no-entry benchmark 中，论文给出 thin/thick optimized rates、patience–thickness topology 和 public-\(n\) benchmark。在正 survival 与 interior first-payment 条件下，incumbent impatience \(\delta<1\) 产生纯 intertemporal-compensation 项；即使已知只有一个司机，局部 rescue 也可严格有效。assignment competition 在 \(n\ge2\) 时再增加一个项。因此 latent Poisson supply 影响后验和全局设计，但不是所有局部增益的必要条件。

## 7. 建议采用的贡献表述

### 7.1 中文

> 本文不以反向荷兰式加价时钟、失败后奖金或供应商等待高价本身为贡献。我们研究这类已知时钟在双边 continuation 与潜在本地供给下的均衡完成率设计：平台在司机行动前公告同一请求的两期支付；私人成本 incumbents 在不了解实现竞争人数时，同时权衡当前分配竞争与折现等待；全拒后，私有价值 rider 再选择 abandon、repeat 或 rescue。我们在匿名对称纯 cutoff-WPBE 类内刻画该均衡，并在 uniform no-entry benchmark 中解出两价格完成率问题，给出优化 flat dominance、patience threshold 和 thickness rates。

### 7.2 英文引言版

> We do not claim to introduce a reverse-Dutch-style procurement clock, multistage bonuses, or supplier delay in anticipation of higher compensation. Our contribution is an equilibrium completion analysis of such a clock when continuation is two-sided and realized local supply is latent. Private-cost incumbents simultaneously trade off current assignment competition against a discounted option to wait, while a private-value rider chooses whether to post and, after universal rejection, whether to abandon, repeat, or activate rescue. Within the anonymous symmetric pure-cutoff WPBE class, we characterize this interaction under arbitrary survival and entry. In the uniform no-entry benchmark, we solve the two-price completion problem and establish optimized-flat dominance under explicit patience conditions.

### 7.3 最短版本

> We provide a cutoff-WPBE and completion-design analysis for a two-tick reverse-Dutch-like rescue clock with private rider continuation and latent same-request competition.

## 8. 最强审稿人攻击与需要正面回答的问题

### A. “这不就是两 tick 的 reverse Dutch procurement auction？”

**答法：** 制度骨架是，机制本身不新。差异必须落在 rider continuation、incumbent discount、failure posterior、survival/entry 和 completion-vs-flat 定理。论文应直接引用 Li and Kuo，并在制度范围中承认 reverse Dutch interpretation。

### B. “Wu 的现场实验没有发现等 bonus，为什么你的战略渠道重要？”

**答法：** Wu 没有说明完整未来 path 被第一阶段公告；其结果限制的是实际在线 bonus 机制。本文研究的是可信且事前可知的 schedule。若无法给出这种制度实例，理论应被定位为一个机制边界：announcement 何时会创造等待、以及该等待是否吃掉完成率收益。

### C. “Bai 已经有公告政策、随机不可见供给和 withholding。”

**答法：** 承认这一组件先例。本文研究的是独立私人成本 drivers 对同一请求的同时 accept/wait，不是 providers 协调隐藏上线人数；全拒还触发 rider continuation 并改变 terminal eligible pool。

### D. “为什么平台只最大化 completion，且 payment 由 rider 转给 driver？”

这更像 bidding、tipping/top-up、freight、task marketplace 或 rider-funded rescue，而不是标准 platform-funded surge。若以 ride-hailing 为主叙事，必须区分 rider fare、driver pay 和 platform-funded bonus；利润/预算目标下结论尚未建立。

### E. “广播通常 first-response-wins，不是同时接受后随机抽签。”

Qin、Wang 和 Lyft NED 文献使该攻击更强。uniform selection 只能解释为有限响应窗的 reduced form；不应声称等价于 response-time race。first-accept robustness 仍是重要扩展。

### F. “结果受限于 cutoff WPBE 和 no-entry global benchmark。”

必须始终把 equilibrium class 紧贴 characterization，把 \(\gamma=0\)、\(\alpha>0\)、\(\beta\) 条件紧贴 global dominance。保守选择不是对所有 PBE 的 worst-case guarantee。

## 9. 本轮发现的书目信息纠错

1. Wu et al. (2022) 的 KDD DOI 是 **`10.1145/3534678.3539202`**；旧备忘录的 `3539042` 指向别的论文。第一作者是 **Zhuolin Wu (Z. Wu)**，不是 “D. Wu”。
2. Qin et al. (2025) 的作者是 **Xiaoran Qin, Hai Yang, Yuhan Liu**，应写 `X. Qin, H. Yang, and Y. Liu`；完整题名是 *A two-round broadcasting matching mechanism in ride-sourcing markets: Implication and optimization*。
3. Wang et al. (2026) 仍是 SSRN working paper，DOI `10.2139/ssrn.7240784`。
4. Ekbatani et al. (2026) Part I–II 截至检索日仍按 arXiv/Chicago Booth working papers 处理，不写成正式期刊发表。

## 10. 建议的文献综述顺序

1. **拍卖/采购时钟先例：** Li–Kuo；Buchanan–Gjerstad–Porter；Carare–Rothkopf；Shneyerov；反向荷兰式采购制度。先承认 price clock、Poisson participation、hidden group-size learning、strategic delay、impatience 和 clock optimization 已存在。
2. **同单多阶段奖金与通知：** Wu；Qin；Feng–Niazadeh–Saberi；Wang；Ekbatani。承认 bonus escalation、two-stage matching 和 broadcast 已存在。
3. **战略拒绝与隐藏供给：** Sigg；Chen；Bai；Garg–Nazerzadeh；Feng–Wang；Meskar；Guda–Subramanian；Afèche–Liu–Maglaras。承认 supplier waiting、rejection、relocation 和 withholding 已存在。
4. **双边动态定价与公告式 contingent pricing：** Chen–Hu；Hu–Hu–Zhu；Aviv–Pazgal；Dasu–Tong；Correa–Montoya–Thraves。把 Aviv 明确放在方法镜像，而不是实质最近邻。
5. **最后才写本文残差：** endogenous same-request cutoff delay + private rider continuation + failure posterior + completion theorems。

## 11. 核心来源

- Li, Z., and C.-C. Kuo. 2013. [Design of Discrete Dutch Auctions with an Uncertain Number of Bidders](https://doi.org/10.1007/s10479-013-1331-6). *Annals of Operations Research* 211:255–272.
- Buchanan, J., S. Gjerstad, and D. Porter. 2016. [Information Effects in Uniform Price Multi-Unit Dutch Auctions](https://doi.org/10.1002/soej.12145). *Southern Economic Journal* 83(1):126–145.
- Carare, O., and M. Rothkopf. 2005. [Slow Dutch Auctions](https://doi.org/10.1287/mnsc.1040.0328). *Management Science* 51(3):365–373.
- Shneyerov, A. 2014. [An Optimal Slow Dutch Auction](https://doi.org/10.1007/s00199-014-0825-z). *Economic Theory* 57(3):577–602.
- Wu, Z. et al. 2022. [A Framework for Multi-stage Bonus Allocation in Meal Delivery Platform](https://arxiv.org/abs/2202.10695). *KDD 2022*:4195–4203. DOI `10.1145/3534678.3539202`.
- Sigg, D., M. Hardt, and C. Mendler-Dünner. 2025. [Decline Now](https://doi.org/10.1145/3706598.3713966). *CHI 2025*, Article 912.
- Bai, J., H. S. Heese, and M. Tripathy. 2023. [Hiding in Plain Sight](https://doi.org/10.1111/poms.14064). *Production and Operations Management* 32(12):3837–3855.
- Chen, C.-H. 2012. [Name Your Own Price at Priceline.com](https://doi.org/10.1093/restud/rds005). *Review of Economic Studies* 79(4):1341–1369.
- Guda, H., and U. Subramanian. 2019. [Your Uber Is Arriving](https://doi.org/10.1287/mnsc.2018.3050). *Management Science* 65(5):1995–2014.
- Chen, Y., and M. Hu. 2020. [Pricing and Matching with Forward-Looking Buyers and Sellers](https://doi.org/10.1287/msom.2018.0769). *M&SOM* 22(4):717–734.
- Hu, B., M. Hu, and H. Zhu. 2022. [Surge Pricing and Two-Sided Temporal Responses in Ride Hailing](https://doi.org/10.1287/msom.2020.0960). *M&SOM* 24(1):91–109.
- Feng, X., and M. Wang. 2023. [Strategic Driver’s Acceptance-or-Rejection Behavior and Cognitive Hierarchy in On-Demand Platforms](https://doi.org/10.1016/j.tre.2023.103175). *Transportation Research Part E* 176:103175.
- Meskar, M., S. Aslani, and M. Modarres. 2023. [Spatio-temporal Pricing Algorithm for Ride-Hailing Platforms Where Drivers Can Decline Ride Requests](https://doi.org/10.1016/j.trc.2023.104200). *Transportation Research Part C* 153:104200.
- Afèche, P., Z. Liu, and C. Maglaras. 2023. [Ride-Hailing Networks with Strategic Drivers](https://doi.org/10.1287/msom.2023.1221). *M&SOM* 25(5):1890–1908.
- Feng, Y., R. Niazadeh, and A. Saberi. 2023. [Two-Stage Stochastic Matching and Pricing with Applications to Ride Hailing](https://doi.org/10.1287/opre.2022.2398). *Operations Research* 72(4):1574–1594.
- Qin, X., H. Yang, and Y. Liu. 2025. [A Two-Round Broadcasting Matching Mechanism in Ride-Sourcing Markets: Implication and Optimization](https://doi.org/10.1016/j.trc.2025.105318). *Transportation Research Part C* 180:105318.
- Wang, C., K. Zhang, S. Feng, and J. Ke. 2026. [Pricing and Matching for Ride-Hailing Markets under the Broadcasting Mechanism](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7240784). SSRN working paper.
- Ekbatani, F. et al. 2026. [Non-Exclusive Notifications for Ride-Hailing at Lyft I](https://arxiv.org/abs/2603.21533) and [II](https://arxiv.org/abs/2603.21531). Working papers.
- Aviv, Y., and A. Pazgal. 2008. [Optimal Pricing of Seasonal Products in the Presence of Forward-Looking Consumers](https://doi.org/10.1287/msom.1070.0183). *M&SOM* 10(3):339–359.
- Dasu, S., and C. Tong. 2010. [Dynamic Pricing When Consumers Are Strategic](https://doi.org/10.1016/j.ejor.2009.11.018). *European Journal of Operational Research* 204(3):662–671.
- Correa, J., R. Montoya, and C. Thraves. 2016. [Contingent Preannounced Pricing Policies with Strategic Consumers](https://doi.org/10.1287/opre.2015.1452). *Operations Research* 64(1):251–272.

## 12. 检索范围、负结果与保留意见

本轮交叉使用了以下词族及其镜像：announced/preannounced/contingent pricing；reverse Dutch/ascending procurement clock；dynamic procurement；same-order rejection/reoffer；failure-contingent reward；multistage delivery bonus；strategic driver acceptance/rejection；supply withholding/log-off；broadcast/non-exclusive notification；two-stage stochastic matching；unknown/stochastic/Poisson number of bidders；first acceptance/tie allocation；forward-looking buyers/sellers；market thickness。

我们专门尝试寻找同时包含“事前同单加价 + 私人成本战略等待 + 随机且实现后不可见的供应商人数 + 全拒后 rider continuation + completion-vs-flat design”的论文，未找到完整命中。Li and Kuo 是最接近的结构反例，但缺少 endogenous strategic waiting 和 rider continuation；Bai 是最接近的 latent-supply/announced-policy 反例；Wu 是最接近的实际 bonus system；Sigg 是最接近的同单拒绝行为模型；Chen 是最接近的供应商等待博弈。

检索不能证明不存在遗漏。尤其是 2026 年 working papers、采购拍卖文献和平台内部机制会继续变化；投稿前应重新检索并核对版本。所有“未找到”的句子都必须保留时间截点、模型范围和知识限定。
