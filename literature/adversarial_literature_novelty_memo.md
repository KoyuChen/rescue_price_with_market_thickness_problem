# 第三轮对抗式临近文献审查与贡献边界

**项目：** *Announced Rescue Payments with Strategic Drivers: Commitment, Universal Rejection, and Latent Local Supply*
**检索截点：** 2026-08-27
**审查目标：** 优先寻找能够击穿贡献主张的文献，而不是扩充一份“相关文献清单”。
**证据原则：** 模型事实优先核对出版社全文/摘要、作者稿、arXiv、SSRN 正文；搜索摘要只用于发现，不单独支撑关键判断。

## 1. 执行结论

### 1.1 第三轮判定

**宽泛的机制贡献不成立；第二轮所保留的“筛选后 incumbents 与 fresh entrants 汇合”也不能单独作为创新；定理级贡献只能在更窄的制度交集内守住。**

第三轮最重要的新发现是 [Lee and Li (2023)](https://doi.org/10.1111/joie.12355)。该文在期初公告并承诺一列 reserve prices 与 bidder samples；long-lived bidders 在每期以对称 cutoff 决定 bid now 或 wait；等待可获得以后较低的 reserve price，但要面对更多新 bidders 的竞争。其正文更明确写出：进入后期 stage auction 的旧 bidders 已被上一期 cutoff 截断，而当期 newly solicited bidders 仍从原始分布抽取。把出售方的降价拍卖镜像成采购方的加价支付后，这正是“当前较低支付/较少竞争 versus 未来较高支付/更多竞争”，以及“第一轮失败后，已筛选 incumbents 与未筛选 fresh entrants 同池竞争”。因此，**strategic waiting、预告价格路径、screened incumbent pool、fresh entry 及二者的混合，不论单独还是作为这一四项组合，都已有直接理论先例。**

[Crémer, Spiegel, and Zheng (2007)](https://doi.org/10.1016/j.jet.2006.03.003) 提供了更早的 search-auction 基础：已联系 bidders 成为 incumbents，失败后再邀请 entrants；其两-bidder例子让第一位 bidder 拒绝 buy-now offer 后与第二期新 bidder 竞争。[McAfee and McMillan (1988)](https://doi.org/10.1016/0022-0531(88)90098-1) 则是逐期搜索并保留已接触候选人的机制源头。Lee–Li 不是只共享若干关键词，而是在 procurement dual 下直接复现本文供应侧的核心等待—竞争—筛选结构。

Lee–Li 仍未覆盖本文的全部对象：它使用 second-price auction 与 reserve prices，支付随竞争结果而非固定为匿名 \(p_j\)；搜索路径和 sample sizes 是公告的机制对象，而不是公开期望厚度 \(m\) 下隐藏的 Poisson realized supply；它没有 incumbent discount \(\delta\)、私有价值 rider 的 abandon/repeat/rescue，目标也是收入而非 same-request completion。故可防守边界必须建立在这些差异的**联合**上，而不能再把 survivor/entrant mixture 当作残余创新。

第三轮还找到两个 thickness 层面的直接约束。[Zhao, Papier, and Teo (2024)](https://doi.org/10.1287/msom.2021.0354) 已在外卖平台研究故意延迟匹配以创造更厚市场，证明总成本关于 thickness 的准凸性并得到中间厚度最优；[Loertscher, Muir, and Taylor (2022)](https://doi.org/10.1016/j.jet.2021.105383) 直接研究 optimal market thickness。因此不能把“中间厚度更有价值”或“存在内点最优 thickness”作为一般创新。本文的 \(V(m)\) 必须定义为**固定 \(m\) 下 rescue 相对 flat pricing 的完成率增量**，即 *the completion value of rescue pricing at thickness \(m\)*，而不是 *the value of market thickness*。

实证方面，[Zhang, Miao, Chu, and Png (2026)](https://doi.org/10.1287/mksc.2023.0561) 已用动态结构模型估计 ride-hailing 中战略司机的 acceptance 与 relocation，并把两侧市场均衡作为 fixed point 求解。故“首次结构估计司机接受行为”也不成立。本稿在没有身份关联 exposure logs、公告处理和 rider continuation 数据之前，只能保留 **DATA REQUIRED / planned empirical calibration**，不能写任何校准结果或把理论参数称为已估计。

### 1.2 第二轮基础判定（保留）

第二轮最重要的新发现不是 2026 年的 ride-hailing working paper，而是 [Li and Kuo (2013)](https://doi.org/10.1007/s10479-013-1331-6) 的离散荷兰式拍卖。该文在拍卖前设置有限价格时钟，上一价格无人接受才进入下一价格；竞标人数服从 Poisson 分布；同一价位多人接受时随机分配；拍卖人优化整条价格路径。把出售方的降价时钟镜像成采购方的加价时钟后，它已经覆盖了“同一标的、预先设定的低—高价格、全拒后进入下一 tick、随机 Poisson participation、接受时的分配竞争、优化价格路径”这一大块结构。商业采购系统也明确实施这种反向荷兰式时钟：买方从低价开始自动加价，第一位供应商接受即成交，等待意味着可能被竞争者抢走订单（[SAP Ariba 官方说明](https://help.sap.com/docs/strategic-sourcing/managing-events-with-guided-sourcing/about-dutch-auctions)）。因此，**公告式 rescue clock 本身不是新机制。**

更强的是，[Buchanan, Gjerstad, and Porter (2016)](https://doi.org/10.1002/soej.12145) 已在多单位离散 Dutch clock 中建立实现 group size 不公开、竞标者从连续无人接受的历史更新规模后验、并求对称 Bayesian-Nash bidding functions 的模型。[Carare and Rothkopf (2005)](https://doi.org/10.1287/mnsc.1040.0328) 求解带等待交易成本的 slow Dutch 均衡；[Shneyerov (2014)](https://doi.org/10.1007/s00199-014-0825-z) 则刻画买方比卖方更不耐心时的最优动态 clock。因而“隐藏人数 + 无接受历史 + 战略等待 + 折现/时钟优化”的宽组合也已有明确先例。

Li and Kuo 并未求解供应商在当前接受与等待更高支付之间的 Bayesian 均衡；它把估值跨越时的接受行为直接嵌入拍卖收入公式。Buchanan et al. 是多单位拍卖，Carare–Rothkopf 与 Shneyerov 通常也没有本文的单请求 rider continuation。上述 Dutch 文献都没有私有价值 rider 的 post/abandon/repeat/rescue、incumbent survival/fresh entry 或完成率目标。故仍可守的对象必须同时写入：

1. **固定匿名 posted payment 而非 auction-contingent payment；**
2. **公开 \(m\) 但隐藏 realized Poisson supply 所诱导的 failure posterior；**
3. **私有价值 rider 在全拒后的内生 abandon/repeat/rescue；**
4. **incumbent discount、随机 survival 与 fresh entry 同时存在时的 cutoff-WPBE；**
5. **完成率目标下优化 rescue-versus-flat 的定理。**

不能再把贡献概括成“事前承诺 + 同请求竞争 + 不可见人数 + 全拒信号”，也不能把“隐藏人数下由无接受历史更新信念”或“折现战略等待”补进去后宣称新颖。Li and Kuo、Buchanan et al. 及 slow-Dutch 文献已分别吞掉这些拍卖镜像。贡献必须落在**把单请求司机等待均衡嵌入 private rider continuation，并由此得到 failure posterior、survival/entry 与完成率设计定理**上。

### 1.3 2008 Aviv 文献的正确位置

[Aviv and Pazgal (2008)](https://doi.org/10.1287/msom.1070.0183) 仍然是很好的**方法镜像**：先固定公告政策，求前瞻主体的阈值反应，再评价/优化政策；消费者等待降价并承担缺货风险，与司机等待加价并承担失单风险方向相反。但它不是实质最近邻。制度/结构上更近的是 Li and Kuo、Wu、Sigg、Chen 和 Bai；字面上的两期 contingent preannouncement 也可由 [Correa, Montoya, and Thraves (2016)](https://doi.org/10.1287/opre.2015.1452) 补足。

### 1.4 最终新颖性结论

截至检索截点，我们**没有找到**一篇文献同时完成以下任务：在单一请求上事前公告两期固定匿名支付；让只知道公开 \(m\) 而不知道 realized Poisson competition 的私人成本 incumbents 在“立即竞争分配”与“折现等待同一请求”之间形成内生 cutoff-WPBE；让全拒后的私有价值 rider 内生选择 abandon/repeat/rescue；在随机 survival 与 fresh entry 下联合刻画人数后验和成本筛选；并以完成率为目标比较优化 flat 与 rescue menu。Lee–Li 已经覆盖战略等待、筛选后的 incumbents 与新 entrants 汇合，故残差不是 mixed pool 本身，而是上述更窄的 posted-payment、latent-supply、two-sided-continuation 与 completion-design 交集。

这是“未检索到完整先例”，不是数学意义的不存在证明。安全措辞应为 **“To our knowledge, among the models reviewed…”**，不能写无条件的 “first”。

## 2. 本轮的 novelty-kill test

### 2.1 九个判定维度

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
| K9 筛选 incumbents + fresh entrants | 失败后留下的 incumbents 已由一期 cutoff 筛选，同时有未经历一期筛选的新司机进入 |

### 2.2 击穿规则

- 若已有文献覆盖 K1–K9，核心贡献死亡。
- 若文献覆盖 K1、K2、K4、K5，即使没有 K3 的均衡，也足以击穿“公告 rescue clock + latent competition”这一宽主张。
- 若文献覆盖 K3，则“司机/供应商首次在当前接受与未来高价之间权衡”死亡。
- 若文献覆盖 K4 和公告的 supply-contingent policy，则“不可见供给与公告政策的结合”死亡。
- 若文献覆盖 K3 和 K9，则“战略等待使旧池被筛选，并在下一期与 fresh entrants 竞争”死亡；Lee–Li 正好满足这一击穿条件。
- 真正可守的贡献必须对应本文已经证明的定理，而不是一组特征标签。

## 3. 最高威胁证据账本

### 3.1 Lee and Li (2023)：第三轮发现的最强直接威胁

**一手来源：** [Wiley / *Journal of Industrial Economics* 全文](https://onlinelibrary.wiley.com/doi/full/10.1111/joie.12355)，DOI `10.1111/joie.12355`。

**已核实的重叠：**

- seller 在 period 0 公告并承诺 reserve-price 与 bidder-sample 路径；
- long-lived bidders 一旦被邀请即留在交易中，后续每期与新邀请的 bidder samples 共同竞价；
- bidders 使用对称 cutoff strategy，类型高于 cutoff 者现在 bid，低于 cutoff 者 wait；
- 现在行动面对较不利价格但竞争较少，等待面对更有利价格但新增竞争者更多；
- 若上一期无人有效出价，下一期旧 bidders 的类型分布被上一期 cutoff 截断，而 newly solicited bidders 仍从原始分布抽取；
- 文中明确把 stage auction 写成旧的 truncated “weak bidders” 与新的 untruncated “strong bidders” 的竞争。

在 procurement dual 中，下降 reserve price 对应上升的最高采购支付；bid now versus wait 对应司机以低支付现在接受或等更高支付；上一轮失败后留下的旧供应者是 screened incumbents，而新增供应者是 fresh entrants。因此这不是松散类比，而是本文供应侧核心博弈的直接 auction counterpart。

**它杀死的表述：**

- “首次研究 screened incumbents 与 unscreened entrants 的混合池”；
- “首次把预告价格路径、战略等待与 fresh entry 结合”；
- “首次刻画当前低价/少竞争与未来高价/多竞争之间的 cutoff”；
- “surviving incumbents plus fresh drivers 是本文的独立创新”。

**仍有的关键缺口：** Lee–Li 支付由 second-price auction 结果决定，不是固定匿名 \(p_j\)；其 search schedule/sample sizes 是公告并由卖方选择的，不是公开 \(m\) 下隐藏的 Poisson realized supply；它抽象掉时间折现，没有私有价值 rider continuation，也不以请求完成率为目标。本文只能在这些差异的联合上定位贡献。

**威胁等级：4（最高；必须在引言和文献综述中正面区分）。**

### 3.2 Crémer–Spiegel–Zheng (2007) 与 McAfee–McMillan (1988)：search-auction 源头

**一手来源：** [Crémer, Spiegel, and Zheng (2007), *Journal of Economic Theory*](https://doi.org/10.1016/j.jet.2006.03.003)；[McAfee and McMillan (1988), *Journal of Economic Theory*](https://doi.org/10.1016/0022-0531(88)90098-1)。

Crémer et al. 把已接触的 bidders 称为 incumbents，并允许机制继续邀请新 entrants。其两-bidder例子可实施为：period 1 向 bidder 1 提供 buy-now price；若其拒绝，bidder 1 与 period-2 entrant bidder 2 在第二期拍卖中共同竞争。论文使用 PBE/incentive-feasible search mechanism，明确说明 incumbents 可以保留到后续分配。McAfee–McMillan 更早研究逐期搜索 long-lived suppliers/bidders 的 optimal search mechanism，是这一文献链的基础。

这两篇使 mixed incumbent/entrant pool 不能被描述成全新问题；Lee–Li 又进一步内生化 cutoff waiting 并明确写出旧池截断。因此本文应把三篇作为同一组最邻近理论先例，而不是只引用一般的 dynamic auction 文献。

**威胁等级：3+（直接理论先例）。**

### 3.3 Li and Kuo (2013)：离散 Poisson clock 的结构攻击

**一手来源：** [Springer / *Annals of Operations Research*](https://link.springer.com/article/10.1007/s10479-013-1331-6)，DOI `10.1007/s10479-013-1331-6`。

**已核实的重叠：**

- 在事件开始前设定有限的离散价格 levels；
- 只有更高价格未被任何 bidder 接受，时钟才进入下一价位；
- bidder 私有 valuation；人数服从 Poisson 分布；
- 同 tick 多人接受时随机选中一人；
- 拍卖人把整条价格路径写成凹的非线性规划并求全局最优。

**证据边界：** 正式模型没有清楚写明每个 bidder 都观察不到实现的 \(N\)，也没有形式化完整价格向量对 bidder 的期初公开与共同知识；接受规则又不依赖人数或历史。因此该文证明的是随机 Poisson 人数与预设离散路径的设计先例，不能单独用来证明“隐藏人数后验学习”。这一更强先例由 Buchanan et al. 提供。

**它杀死的表述：**

- “首次研究预先公告的同标的低—高价格时钟”；
- “首次把 Poisson-random participation 与离散 contingent price path 结合”；
- “随机分配竞争使 waiting 有失单风险是新的机制”；
- “policy–threshold–optimization 顺序本身是贡献”。

**仍有的关键缺口：** 该文是出售方 Dutch clock；采购方向是其镜像。更重要的是，它没有求解由未来价格诱发的内生 strategic-delay equilibrium，没有 rider continuation、survival/entry 或 completion-vs-flat 定理。因此它把本文从“机制创新”压缩为“带双边 continuation 的均衡微观基础和完成率定理”。

**威胁等级：3+（必须重写贡献）。**

### 3.4 Buchanan–Gjerstad–Porter、Carare–Rothkopf 与 Shneyerov：Dutch 均衡攻击

**一手来源：** [Buchanan, Gjerstad, and Porter (2016), Wiley](https://onlinelibrary.wiley.com/doi/10.1002/soej.12145)；[Carare and Rothkopf (2005), INFORMS](https://pubsonline.informs.org/doi/10.1287/mnsc.1040.0328)；[Shneyerov (2014), DOI](https://doi.org/10.1007/s00199-014-0825-z)。

- Buchanan et al. 的竞标者只知道 group size 属于两个可能值，并根据 clock 上持续没有接受更新后验；剩余单位信息只在其 disclosure treatment 中公开，不能当作所有处理共有的信息。论文推导对称 Bayesian-Nash bidding functions。它直接击穿“隐藏实现人数 + 非接受历史 + 战略等待/学习的组合首次出现”。但它是 uniform-price multi-unit Dutch auction、到第 $m$ 次接受才停止，不是单请求 first-accept，也没有 rider continuation。
- Carare and Rothkopf 在 slow Dutch auction 中加入随等待累积的 transaction cost，并求对称博弈均衡；“等待的真实成本改变抢先时点”不是本文新机制。
- Shneyerov 假定 buyers 比 seller 更不耐心，刻画 revenue-maximizing slow clock，并证明最优 clock 真正动态且包含延迟；“异质耐心 + 动态 clock 优化”也不能作为宽贡献。

三篇一起表明，本文不能通过给 Li–Kuo 补上“均衡、隐藏人数后验、折现”来重新恢复机制新颖性。残差仍是单请求采购镜像中 rider 的私有 continuation、survival/entry 及 completion-vs-flat 的特定定理包。

**威胁等级：3+（直接占据 strategic clock 的理论核心）。**

### 3.5 Wu et al. (2022)：最接近的实际多阶段订单奖金

**一手来源：** [作者公开全文](https://arxiv.org/abs/2202.10695)，KDD 正确 DOI 为 [`10.1145/3534678.3539202`](https://doi.org/10.1145/3534678.3539202)。旧备忘录中的 `3539042` 是错误 DOI。

**已核实的重叠：** 同一外卖订单同时推送给附近多名司机；未接单且未取消的订单进入下一阶段；bonus 可在 10、20 分钟等节点上升；平台在预算内最大化被接受的订单数量，A/B test 报告取消显著下降。

**最危险的反证：** 论文假设阶段接受率只依赖当前价格，并做了一个“10 分钟后固定 bonus”的消融实验；作者报告前 10 分钟接受率几乎不变，并明确解释为没有观察到司机等 bonus。

**为什么没有直接否证本文：** Wu 的在线算法在每个阶段实时计算并展示当期 bonus；正文没有说明完整未来 bonus path 在第一阶段被公开并承诺。因此这是真实制度下对 anticipatory waiting 的不利证据，但不是对“已知的事前承诺菜单”的干净检验。最安全的写法是“does not specify an ex-ante announcement of the full future path”，不能武断写成 “nonannounced”。

**论文必须承担的外部效度负担：** 解释在哪种制度中 future rescue schedule 会被司机事前知道并相信；否则理论中的 K3 可能并不是运营上重要的边际。

**威胁等级：3（运营与经验反证）。**

### 3.6 Sigg, Hardt, and Mendler-Dünner (2025)：最接近的行为机制

**一手来源：** [arXiv 全文](https://arxiv.org/abs/2410.12633)，CHI DOI [`10.1145/3706598.3713966`](https://doi.org/10.1145/3706598.3713966)。

模型中固定的 \(N\) 名 workers 服务连续订单；平台把同一订单随机给一名 idle worker，每次拒绝后支付增加 \(\Delta\) 并重新随机派发，包括刚拒绝者。collective participants 使用外生共同阈值，nonparticipants 在任何价格接受。论文证明集体平均收益为正，并刻画 labor oversupply 如何损害参与者收益。

它已经吞掉“拒绝同单—涨价重派—可能失单—市场厚度影响等待收益”。本文剩余差异是：个体私人成本与内生 cutoff、同时广播而非顺序单播、rider continuation、潜在人数、平台完成率设计。

**威胁等级：3（行为近邻）。**

### 3.7 Bai, Heese, and Tripathy (2023)：不可见供给与公告政策的强攻击

**一手来源：** [出版社开放全文](https://journals.sagepub.com/doi/10.1111/poms.14064)。

平台先公告随显示在线供给 \(m\) 变化的价格/补偿规则 \((p(m),w(m))\)；真实本地供给 \(M\) 是随机变量且平台不可见；providers 随后协调隐藏一部分在线人数，以诱发更高 compensation。论文求 subgame-perfect equilibrium 并设计 bonus/optimal policy 以消除 withholding。

这意味着以下表述都不成立：

- “首次研究事前政策、随机不可见供给和 strategic withholding”；
- “latent supply 使公告 compensation policy 产生操纵激励是新的”；
- “平台用 bonus 对抗供应商等待/隐藏供给是新的”。

它与本文不同之处是集体选择显示在线人数，而不是匿名司机基于私人成本同时决定同一请求 accept/wait；平台观察的是操纵后的 \(m\)，没有全拒后的 rider continuation 或同单 failure posterior。

**威胁等级：3（潜在供给/承诺组件）。**

### 3.8 Chen (2012)：竞争供应商等待更高报价

**一手来源：** [*Review of Economic Studies*](https://academic.oup.com/restud/article/79/4/1341/1573679)。

一名 buyer 在多轮向固定、已知数量的私人成本 sellers 报价；第一个接受者成交；sellers 具有阈值策略并可等待更高报价。它直接杀死“首次研究竞争供应商 accept-now versus wait-for-more”。差异是 buyer 不事前承诺、卖家数固定已知、无 platform–rider 分离、Poisson/Palm、survival/entry 和完成率设计。

**威胁等级：3（博弈结构）。**

### 3.9 Zhao–Papier–Teo 与 Loertscher–Muir–Taylor：中间厚度不是新结论

**一手来源：** [Zhao, Papier, and Teo (2024), *M&SOM*](https://doi.org/10.1287/msom.2021.0354)；[Loertscher, Muir, and Taylor (2022), *Journal of Economic Theory*](https://doi.org/10.1016/j.jet.2021.105383)。

Zhao et al. 在 online food delivery 中让平台故意延迟 driver assignment，以增加可用 drivers 与 orders 并形成更厚的 marketplace；其 \(k\)-level thickening policy 在真实 Meituan 数据上做数值评价，理论上得到总成本关于 market thickness 的 quasi-convexity 和 intermediate optimal thickness。Loertscher et al. 直接研究 planner 如何选择 market thickness，并量化储存少量 traders 所创造的 matching gains。

**它们杀死的表述：** “首次证明中间厚度最优”“首次表明 thickness 的价值在中间市场最大”“market thickness 本身具有驼峰价值”。本文只能研究固定 \(m\) 下 rescue 相对 flat pricing 的政策增量 \(V(m)\)，并把任何单峰性严格限定为本文模型中的 theorem、numerical evidence 或 conjecture。

**威胁等级：3（thickness framing 必须重写）。**

### 3.10 Ride-hailing 接受/拒绝、广播、两阶段设计与结构估计

- [Feng and Wang (2023)](https://doi.org/10.1016/j.tre.2023.103175) 已在竞争环境中求司机 acceptance/rejection 的 Nash 与 cognitive-hierarchy 行为；它是跨地区无限期系统，不是同单未来工资。
- [Meskar, Aslani, and Modarres (2023)](https://doi.org/10.1016/j.trc.2023.104200) 联合优化 fare、driver compensation 和 matching rate，并允许司机拒单、迁移及动态 fleet；没有失败后的同单公告加价。
- [Guda and Subramanian (2019)](https://doi.org/10.1287/mnsc.2018.3050) 与 [Afèche, Liu, and Maglaras (2023)](https://doi.org/10.1287/msom.2023.1221) 已研究战略司机、竞争、relocation、forecast/controls 和 worker incentives；不是同请求 rescue。
- [Horner, Pazour, and Mitchell (2021)](https://doi.org/10.1016/j.tre.2021.102419) 与 [Ausseil, Pazour, and Ulmer (2022)](https://doi.org/10.1287/trsc.2022.1133) 优化多供应商通知/菜单并处理随机拒绝与 duplicate selection；接受是 stochastic response，不是跨期战略等待。
- [Qin, Yang, and Liu (2025)](https://doi.org/10.1016/j.trc.2025.105318) 在无人响应后扩大第二轮广播半径，并优化半径和等待时间；接受是异质概率反应，不是对未来工资的战略等待。
- [Feng, Niazadeh, and Saberi (2023)](https://doi.org/10.1287/opre.2022.2398) 的 two-stage 是为即将到来的未来需求 batching 并设计竞争算法，不是同一请求 rescue。
- [Wang et al. (2026)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7240784) 在 broadcasting 静态均衡中让司机按距离/时间价值内生接单，平台联合选 fare 与半径；无跨期同单加价。该文是 SSRN working paper，DOI `10.2139/ssrn.7240784`。
- [Ekbatani et al. (2026), Part I](https://arxiv.org/abs/2603.21533) 和 [Part II](https://arxiv.org/abs/2603.21531) 研究 Lyft non-exclusive notifications、notification set、First-Accept/Best-Accept 与长期 marketplace effects；接受是给定的 pair-specific probability，不是私人成本 strategic waiting。两篇均为 working papers。
- [Zhang, Miao, Chu, and Png (2026)](https://doi.org/10.1287/mksc.2023.0561) 用 Singapore taxi data 建立动态结构模型，让 strategic drivers 联合优化 acceptance 与 relocation，并让 riders 选择交通方式；两侧均衡以 fixed point 求解并用于 driver-accept versus auto-accept counterfactual。它直接杀死“首次结构估计战略司机接受行为”。

这些工作共同杀死“首次研究司机拒绝”“首次研究同时广播”“首次研究两轮无响应后再尝试”“首次研究平台在广播下联合价格和匹配”等表述。

## 4. 维度矩阵

符号：**●** 明确覆盖；**◐** 部分/镜像覆盖；**—** 未覆盖。矩阵只比较结构，不代表论文质量或总体相似度。

| 文献 | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 | K9 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **本文** | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| **Lee–Li 2023** | ● | ● | ● | — | ● | — | ◐ | ◐ | ● |
| Crémer–Spiegel–Zheng 2007 | ● | ◐ | ● | — | ● | — | ◐ | ◐ | ● |
| McAfee–McMillan 1988 | ◐ | ◐ | ◐ | — | ◐ | — | ◐ | ◐ | ◐ |
| Li–Kuo 2013 | ● | ● | — | ◐ | ● | — | ◐ | ◐ | — |
| Buchanan–Gjerstad–Porter 2016 | ● | ◐ | ● | ● | ◐ | — | ◐ | ◐ | — |
| Carare–Rothkopf 2005 | ● | ◐ | ● | — | ◐ | — | ◐ | ◐ | — |
| Shneyerov 2014 | ● | ◐ | ● | — | ◐ | — | ◐ | ◐ | — |
| Wu et al. 2022 | —/◐ | ● | — | ◐ | ◐ | ◐ | — | ◐ | ◐ |
| Sigg et al. 2025 | ◐ | ● | ◐ | — | ◐ | — | — | — | — |
| Bai et al. 2023 | ● | — | ◐ | ● | — | ● | — | ◐ | — |
| Chen 2012 | — | ◐ | ● | — | ◐ | — | — | — | — |
| Hu–Hu–Zhu 2022 | ◐ | — | ◐ | — | ◐ | ● | — | ◐ | — |
| Chen–Hu 2020 | ◐ | — | ● | ◐ | ◐ | ● | — | ◐ | — |
| Qin et al. 2025 | ◐ | ● | — | ◐ | ● | ◐ | — | ◐ | ◐ |
| Feng–Niazadeh–Saberi 2023 | ● | — | — | ◐ | ● | ◐ | — | ◐ | — |
| Wang et al. 2026 WP | — | — | ◐ | ◐ | ● | ● | — | ◐ | — |
| Ekbatani et al. 2026 WP | — | — | — | ◐ | ● | ◐ | — | ◐ | — |
| Aviv–Pazgal 2008 | ● | ◐ | ◐ | — | — | — | ◐ | ◐ | — |
| Correa et al. 2016 | ● | ● | ◐ | — | — | — | ◐ | ◐ | — |
| Zhao–Papier–Teo 2024 | — | — | — | ◐ | ● | — | — | ◐ | — |
| Loertscher–Muir–Taylor 2022 | — | — | — | — | ● | — | — | ◐ | — |
| Zhang–Miao–Chu–Png 2026 | — | — | ◐ | — | ● | ◐ | — | ◐ | — |

### 矩阵后的关键修正

前两轮把“K1–K8 的完整交集”作为安全贡献仍不够精确：K1、K2、K4、K5 的拍卖镜像已被 Li–Kuo 高度覆盖，Lee–Li 又直接覆盖 K1、K2、K3、K5、K9。最终贡献不能是勾选更多格子，而必须写成：**在已有 search-auction/clock architecture 中，本文研究固定匿名 posted payment、公开期望但隐藏实现的 Poisson supply、private rider continuation 与 completion design 的联合。**

## 5. 逐项杀死宽泛主张

以下表述应删除或主动否认：

- “本文首次提出失败后加价、多阶段奖金或 rescue pricing。”
- “本文首次研究供应商等待未来更高支付。”
- “本文首次研究失败后 screened incumbents 与 fresh entrants 在同一池中竞争。”
- “本文首次把战略等待、旧池筛选和新增竞争者结合。”
- “本文首次把事前 price clock、Poisson 人数和 first acceptance 结合。”
- “本文首次研究同一订单被拒后涨价重派及厚度影响。”
- “本文首次研究不可见真实供给下的公告 compensation rule。”
- “本文首次把隐藏实现人数、无接受历史的后验更新与战略等待结合。”
- “本文首次把司机/供应商折现与最优动态 price clock 结合。”
- “本文首次研究两轮 broadcast、first-response 或无响应后的第二次尝试。”
- “本文首次得到 ride-hailing 的 low-then-high surge path。”
- “本文首次证明中间 market thickness 最优或最有价值。”Zhao et al. 和 Loertscher et al. 已分别覆盖平台 thickening 与 optimal thickness。
- “本文首次证明厚度价值单峰。”论文只证明连续性、两端速率和正的有限最优点；\(\beta<1/2\) 时严格单峰为假，\(\beta\ge1/2\) 尚未证明。
- “本文首次结构估计战略司机接受行为。”Zhang et al. 已建立并估计 driver acceptance/relocation 的动态结构模型。
- “承诺本身有价值。”论文没有与 unannounced/adaptive policy 做直接机制比较，不能把因果价值归给 announcement。

## 6. 当前可以守住的定理级贡献

### 6.1 一般模型：均衡微观基础，而非机制发明

在任意 survival \(\alpha\)、fresh entry \(\gamma\) 和 incumbent discount \(\delta\) 下，本文在**匿名、对称、纯 first-period driver cutoff WPBE** 类内刻画任意固定 posted-payment menu 的均衡 correspondence，包括 Palm rival distribution、全拒后的 Poisson splitting、隐藏 realized count 与成本筛选的联合 posterior、rider continuation、边界 cutoff 和 tie-breaking。该结论不覆盖所有 mixed/asymmetric PBE。Lee–Li 已有 screened incumbents 与 fresh entrants 的 cutoff competition，因此这里的贡献只能是上述 latent-count、fixed-payment 与 two-sided-continuation 的联合刻画。

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

在 no-entry benchmark 中，论文给出 thin/thick optimized rates、patience–thickness topology 和 public-\(n\) benchmark。在正 survival 与 interior first-payment 条件下，incumbent impatience \(\delta<1\) 产生纯 intertemporal-compensation 项；即使已知只有一个司机，局部 rescue 也可严格有效。assignment competition 在 \(n\ge2\) 时再增加一个项。因此 latent Poisson supply 影响后验和全局设计，但不是所有局部增益的必要条件。由于 Zhao et al. 与 Loertscher et al. 已有 intermediate/optimal thickness，本文必须把 \(V(m)\) 称为“固定 thickness 下 rescue pricing 相对 flat pricing 的 completion gain”，而不是 thickness 本身的价值。

## 7. 建议采用的贡献表述

### 7.1 中文

> 本文不以反向荷兰式加价时钟、失败后奖金或供应商等待高价本身为贡献。我们研究这类已知时钟在双边 continuation 与潜在本地供给下的均衡完成率设计：平台在司机行动前公告同一请求的两期支付；私人成本 incumbents 在不了解实现竞争人数时，同时权衡当前分配竞争与折现等待；全拒后，私有价值 rider 再选择 abandon、repeat 或 rescue。我们在匿名对称纯 cutoff-WPBE 类内刻画该均衡，并在 uniform no-entry benchmark 中解出两价格完成率问题，给出优化 flat dominance、patience threshold 和 thickness rates。

更完整的引言应在这段之前明确承认：Lee–Li 已研究预告价格/搜索路径下 long-lived incumbents 的 cutoff waiting、旧池截断和 fresh bidders 进入；本文不把 mixed pool 本身作为创新。

### 7.2 英文引言版

> We build on search auctions with long-lived incumbents and newly solicited bidders, reverse-Dutch-style procurement clocks, and multistage platform bonuses. We do not claim that strategic waiting, the screening of incumbents after failure, or their subsequent competition with fresh entrants is new. Our analysis focuses on a posted-payment, two-sided version in which the expected incumbent thickness is public but its Poisson realization is latent. Universal rejection therefore updates beliefs about both realized competition and incumbent costs, while a private-value rider chooses whether to abandon, repeat, or activate rescue. Within the anonymous symmetric pure-cutoff WPBE class, we characterize this interaction under arbitrary survival and entry. In the uniform no-entry benchmark, we solve the two-price completion problem and establish optimized-flat dominance under explicit patience conditions.

### 7.3 最短版本

> We provide a cutoff-WPBE and completion-design analysis of fixed rescue payments with private rider continuation and latent realized same-request competition.

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

### G. “screened incumbents 与 fresh entrants 不就是 Lee–Li 的 procurement dual？”

**答法：** 是，必须明确承认。本文不能把 mixed pool 或“未来新增竞争者约束当前等待”作为创新。可防守差异是固定匿名 posted payment、公开期望但隐藏实现的 Poisson competition、incumbent discount、private rider continuation 和 completion objective 的联合。

### H. “中间 thickness 的峰值不是 Zhao et al. 和 optimal-thickness 文献早已有了吗？”

**答法：** 是。本文不选择或创造 market thickness；它固定外生公开 \(m\)，比较同一环境中的优化 rescue 与优化 flat policy。\(V(m)\) 是 rescue pricing 的增量完成价值随 thickness 的变化，不是 thickness 的总价值或边际价值。

## 9. 实证扩展：`DATA REQUIRED` 与可识别边界

### 9.1 当前稿件状态

在真实数据和实验设计尚未核实前，正式稿只能保留如下声明：

> **Planned empirical calibration—DATA REQUIRED.** This section specifies the request-level variation and exposure logs required to discipline the model. The current draft reports no estimated structural parameter, calibrated treatment effect, or empirical counterfactual.

不能把人为指定的 \(\alpha,\beta,\gamma,\delta,F,G\) 称为 empirical calibration，也不能预写“模型拟合良好”“数据支持战略等待”或“中等厚度下增益最大”等结果句。

### 9.2 最低数据要求

1. **身份关联的 notification/exposure sets：** 每个请求在两轮中 eligible、notified、opened/viewed 的 driver IDs 及时间戳；仅有 completed-trip data 不够。
2. **司机实际看到的价格信息：** 第一轮界面显示的 \(p_1\)、未来 \(p_2\)、触发条件、等待时长以及是否标记为 committed。后台设置了 \(p_2\) 不等于司机事前知道 \(p_2\)。
3. **公开 thickness 信息与 realized pool：** 司机在行动前可见的区域供需、候选人数或其充分统计量，以及平台日志中的 realized eligible incumbent count。若 \(m\) 只是 econometrician forecast、并非司机共同知道的 public state，则并未校准本文的信息结构。
4. **司机动作：** accept、explicit reject、timeout、app disconnect、离开区域、被其他订单占用及最终 assignment。必须区分真实拒绝与未看到/无法响应。
5. **rider 动作：** 初始 post、一期失败后的 cancel、repeat \(p_1\)、activate rescue \(p_2\)，以及每一动作的时间和界面信息。
6. **外生价格变化：** 至少需要在固定 first-round request/candidate set 时改变 announced \(p_2\)；只随机化 contemporaneous \(p_1\) 不能识别 anticipation。

### 9.3 screened incumbents 与 entrants 的日志定义

令 \(I_1\) 为第一轮实际 exposed 且有机会响应的 incumbent IDs，\(I_2\) 为其中第一轮未接受且第二轮仍 eligible/exposed 的 IDs，\(E_2\) 为第二轮 exposed 但不在 \(I_1\) 中的 IDs。数据中应直接构造

\[
\text{survivors}=I_1\cap I_2,\qquad
\text{entrants}=E_2=\mathcal D_2\setminus I_1.
\]

没有跨轮 driver IDs 时，只能识别第二轮总 pool，不能分别识别 \(\alpha\) 与 \(\gamma\)。第一轮未接受的 incumbents 是经过行为选择的 screened pool，其成本分布应按均衡 cutoff 截断；fresh entrants 没有经历这一筛选。实证上还应先允许 entrant distribution \(F_E\) 与 incumbent primitive distribution \(F_I\) 不同，再把 \(F_E=F_I\) 作为可检验或敏感性限制，而不是无条件事实。

### 9.4 参数—数据映射

| 对象 | 可识别信息 | 不足数据下的边界 |
|---|---|---|
| \(m\) | 第一轮 eligible/exposed incumbent count 在公开状态下的条件均值 | nearby/online drivers 总数不是正确分母 |
| \(\alpha\) | 第一轮 rejector ID 在第二轮仍 eligible/exposed 的条件概率 | 无跨轮 ID 时不可与 entry 分开 |
| \(\gamma\) | 第二轮新增 exposed IDs 的条件强度 | 若 \(p_2\) 吸引司机上线/移入，\(\gamma\) 应依赖政策而非固定 |
| \(F_I,F_E\) | 分池的 acceptance/rejection moments 与价格实验 | 只观察中标司机会产生严重 selection |
| \(\delta\) | announced \(p_2\) 在固定 \(p_1\) 下对一期接受的影响 | 仅观察第二轮接受率不能识别战略等待 |
| \(\beta,G\) | rider-level continuation choices 对价格、等待和预期成功率的响应 | observed continuation rate 不是纯 \(\beta\) |
| \(V(m)\) | 同一 public-\(m\) state 下优化/实验 rescue 与 flat 的 completion difference | 跨区域简单比较混合了需求、空间与选择效应 |

[Miao et al. (2023)](https://doi.org/10.1002/joom.1223) 表明 surge 会吸引 part-time drivers 并造成竞争，故 \(\gamma\) 对 \(p_2\) 的外生性需要短窗口、固定 notification set 或显式 entry equation 支撑。[Zhang et al. (2026)](https://doi.org/10.1287/mksc.2023.0561) 已提供战略 acceptance/relocation 的动态结构估计先例；本文实证贡献若成立，必须来自 same-request announcement、failure screening 与 identity-linked mixed pool，而不是“估计司机接受行为”本身。

### 9.5 最有识别力的实验占位

理想实验至少包含三个 arms，并在请求特征、\(p_1\) 与第一轮 candidate set 上保持可比：

1. **announced rescue：** 第一轮明确展示并承诺 \((p_1,p_2)\)；
2. **surprise rescue：** 第一轮只展示 \(p_1\)，失败后给出相同 \(p_2\)；
3. **flat：** 两期维持 \(p_1\)。

announced 与 surprise 在第一轮接受率上的差异识别 announcement/anticipation channel；相同 \(p_2\) 下第二轮差异用于检查 selection 与 contemporaneous rescue response。Wu et al. 的“未来 bonus 不改变前十分钟接受率”应作为预先指定的 falsification benchmark，而不能省略。

若现有实验仅随机化当期价格，最安全的边界句是：

> The experiment disciplines contemporaneous acceptance and completion responses. The anticipation parameter and the strategic rescue channel remain theory-based sensitivity exercises.

## 10. 本轮发现的书目信息纠错

1. Wu et al. (2022) 的 KDD DOI 是 **`10.1145/3534678.3539202`**；旧备忘录的 `3539042` 指向别的论文。第一作者是 **Zhuolin Wu (Z. Wu)**，不是 “D. Wu”。
2. Qin et al. (2025) 的作者是 **Xiaoran Qin, Hai Yang, Yuhan Liu**，应写 `X. Qin, H. Yang, and Y. Liu`；完整题名是 *A two-round broadcasting matching mechanism in ride-sourcing markets: Implication and optimization*。
3. Wang et al. (2026) 仍是 SSRN working paper，DOI `10.2139/ssrn.7240784`。
4. Ekbatani et al. (2026) Part I–II 截至检索日仍按 arXiv/Chicago Booth working papers 处理，不写成正式期刊发表。

## 11. 建议的文献综述顺序

1. **search auction 与筛选后混合池：** Lee–Li；Crémer–Spiegel–Zheng；McAfee–McMillan。先承认 long-lived incumbents、cutoff waiting、旧池截断和 fresh entrants 已经存在。
2. **拍卖/采购时钟先例：** Li–Kuo；Buchanan–Gjerstad–Porter；Carare–Rothkopf；Shneyerov；反向荷兰式采购制度。承认 price clock、Poisson participation、hidden group-size learning、strategic delay、impatience 和 clock optimization 已存在。
3. **同单多阶段奖金与通知：** Wu；Qin；Feng–Niazadeh–Saberi；Wang；Ekbatani。承认 bonus escalation、two-stage matching 和 broadcast 已存在。
4. **战略拒绝与隐藏供给：** Sigg；Chen；Bai；Garg–Nazerzadeh；Feng–Wang；Meskar；Guda–Subramanian；Afèche–Liu–Maglaras。承认 supplier waiting、rejection、relocation 和 withholding 已存在。
5. **market thickness：** Zhao–Papier–Teo；Loertscher–Muir–Taylor。承认 strategic thickening、intermediate optimum 与 optimal thickness 已存在。
6. **双边动态定价、结构估计与公告式 contingent pricing：** Zhang–Miao–Chu–Png；Chen–Hu；Hu–Hu–Zhu；Aviv–Pazgal；Dasu–Tong；Correa–Montoya–Thraves。把 Aviv 明确放在方法镜像，而不是实质最近邻。
7. **最后才写本文残差：** fixed anonymous rescue payments + public expected/latent realized supply + private rider continuation + joint failure posterior + completion theorems。

## 12. 核心来源

- Lee, J., and D. Z. Li. 2023. [Seller Compound Search for Bidders](https://doi.org/10.1111/joie.12355). *Journal of Industrial Economics* 71(4):1004–1037.
- Crémer, J., Y. Spiegel, and C. Z. Zheng. 2007. [Optimal Search Auctions](https://doi.org/10.1016/j.jet.2006.03.003). *Journal of Economic Theory* 134(1):226–248.
- McAfee, R. P., and J. McMillan. 1988. [Search Mechanisms](https://doi.org/10.1016/0022-0531(88)90098-1). *Journal of Economic Theory* 44(1):99–123.
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
- Zhao, Y., F. Papier, and C.-P. Teo. 2024. [Market Thickness in Online Food Delivery Platforms: The Impact of Food Processing Times](https://doi.org/10.1287/msom.2021.0354). *M&SOM* 26(3):853–872.
- Loertscher, S., E. V. Muir, and P. G. Taylor. 2022. [Optimal Market Thickness](https://doi.org/10.1016/j.jet.2021.105383). *Journal of Economic Theory* 200:105383.
- Zhang, X., W. Miao, J. Chu, and I. Png. 2026. [The Design of Centralized Matching Systems on Two-Sided Platforms: Evidence from the Ride-Hailing Market](https://doi.org/10.1287/mksc.2023.0561). *Marketing Science* 45(4):816–843.
- Miao, W., Y. Deng, W. Wang, Y. Liu, and C. S. Tang. 2023. [The Effects of Surge Pricing on Driver Behavior in the Ride-Sharing Market: Evidence from a Quasi-Experiment](https://doi.org/10.1002/joom.1223). *Journal of Operations Management* 69(5):794–822.
- Aviv, Y., and A. Pazgal. 2008. [Optimal Pricing of Seasonal Products in the Presence of Forward-Looking Consumers](https://doi.org/10.1287/msom.1070.0183). *M&SOM* 10(3):339–359.
- Dasu, S., and C. Tong. 2010. [Dynamic Pricing When Consumers Are Strategic](https://doi.org/10.1016/j.ejor.2009.11.018). *European Journal of Operational Research* 204(3):662–671.
- Correa, J., R. Montoya, and C. Thraves. 2016. [Contingent Preannounced Pricing Policies with Strategic Consumers](https://doi.org/10.1287/opre.2015.1452). *Operations Research* 64(1):251–272.

## 13. 检索范围、负结果与保留意见

本轮交叉使用了以下词族及其镜像：announced/preannounced/contingent pricing；reverse Dutch/ascending procurement clock；dynamic procurement；same-order rejection/reoffer；failure-contingent reward；multistage delivery bonus；strategic driver acceptance/rejection；screened incumbents/fresh entrants；long-lived bidders/newly solicited bidders；compound search auctions；supply withholding/log-off；broadcast/non-exclusive notification；two-stage stochastic matching；unknown/stochastic/Poisson number of bidders；first acceptance/tie allocation；forward-looking buyers/sellers；market thickness；structural driver acceptance；ride-hailing calibration。

我们专门尝试寻找同时包含“事前同单固定加价 + 私人成本战略等待 + 随机且实现后不可见的供应商人数 + 全拒后 private rider continuation + completion-vs-flat design”的论文，未找到完整命中。Lee and Li 是最强的直接供应侧反例：它已经包含预告路径、cutoff waiting、screened incumbents 与 fresh entrants，但缺少 fixed posted payment、latent Poisson realized count、rider continuation 和 completion objective。Li and Kuo 是最接近的 Poisson discrete-clock 反例；Bai 是最接近的 latent-supply/announced-policy 反例；Wu 是最接近的实际 bonus system；Zhao 是最接近的 platform-thickness 反例；Zhang 是最接近的 structural acceptance estimation 先例。

检索不能证明不存在遗漏。尤其是 2026 年 working papers、采购拍卖文献和平台内部机制会继续变化；投稿前应重新检索并核对版本。所有“未找到”的句子都必须保留时间截点、模型范围和知识限定。
