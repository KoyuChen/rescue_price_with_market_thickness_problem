# Rescue pricing solver

一个可独立运行、可复审的有限类型双层求解器：内层求司机与乘客的策略响应，
外层分别搜索 rescue 菜单 `(p1,p2)` 与 flat 价格 `p`，目标为最终成交概率。
经济设定采用 v1.1.1；不是旧版本结果复现器，不读取 v1.2 候选或历史缓存。

**当前是数值原型与诊断工具，不是连续类型 WPBE 或连续价格全局最优性的证明器。**
小 regret、退出码 0、软件测试通过，均不等于理论认证。未解决的条件后验会保留为
`insufficient_evidence`。不会为了得到单峰而改变结果。
旧探索入口 `python -m rescue_solver` 的统一 Hoeffding 界在常用大模型预算下过于保守。
新入口 `run_research.py` 使用直接收益差的经验 Bernstein 界、结构性离轨历史证明和
零温度支持清理；它先运行高预算验证门，未通过就不展开厚度搜索。
具体范围和限制见 [docs/RESEARCH_RERUN.md](docs/RESEARCH_RERUN.md) 与
[docs/PRECISION.md](docs/PRECISION.md)。

最新实际结果见 [docs/RESULTS_STATUS.md](docs/RESULTS_STATUS.md)：m=1 同精度固定菜单的
千万配对市场增益为 +0.17967 个百分点；尚不是外层优化结果或多厚度单峰结论。

## 本轮高预算重跑

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python run_research.py \
  --workers 2 --output runs/research_gate_20260905
```

统一 17 个成本点、24 个顺路点；120 万 OD 抽样；10000 个训练计数样本；
两组各 100000 个独立审计计数样本；32 点并列积分。验证门使用固定菜单，
不是外层最优价格，不输出认证的 `V(m)`。审计失败及其完整策略同样保存。

## 安装与测试

Python 3.10+；唯一运行依赖是 NumPy。无需 Gurobi/CPLEX 或旧发布包。

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

不安装本项目也可以在仓库根目录运行 `python -m rescue_solver` 或 `python run_solver.py`。
安装后的命令是 `rescue-solver`。为避免小矩阵计算的线程开销，运行长实验前可设置：

```bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
```

## 1. 先检查随机路线

```bash
python -m rescue_solver routes --route-seed 42 --route-draws 10000 --output runs/routes_42
```

生成 `routes.npz`：随机起点、长度、方向和实际顺路度；`summary.json` 记录种子和统计。
换种子得到新 OD 样本；固定种子可复现。顺路度不是统一常数，也不是为某个峰形拟合的。
求均衡时将随机 OD 分布离散化；市场评价继续随机抽取每位司机的顺路类型。

## 2. 给定菜单求内层策略

快速软件检查（小类型支撑与低预算，不能当研究结果）：

```bash
python -m rescue_solver menu --m 1 --p1 .425 --p2 .490 \
  --config configs/small.json --route-seed 42 --smoke \
  --selection-markets 1000 --report-markets 2000 --output runs/menu_smoke
```

原 15×22 配置，较高求解预算示例：

```bash
python -m rescue_solver menu --m 1 --p1 .425 --p2 .490 \
  --route-seed 20260904 --seed 2026090501 \
  --train-counts 10000 --audit-counts 100000 --iteration-multiplier 2 \
  --selection-markets 200000 --output runs/menu_m1
```

例子价格仅展示 API，不宣称其最优。高预算仍可能不收敛或无法解决稀有信息集。
`--iteration-multiplier` 只增加各温度阶段的迭代次数，不放宽 regret 门槛。
默认路线构造使用 800000 次 OD 抽样，15 个成本点、至多 22 个顺路点。

## 3. 外层选择价格：六个厚度

```bash
python -m rescue_solver grid --m 1 3 6 12 24 48 --step .05 \
  --workers 6 \
  --route-seed 20260904 --seed 2026090501 \
  --train-counts 10000 --audit-counts 100000 \
  --selection-markets 200000 --report-markets 1000000 \
  --output runs/six_m_grid
```

步长 .05 时，每个厚度完整求解 231 个菜单，总计 1386 个，不是只比较旧表中的价格。
flat 单独在全部对角菜单上优化；对角策略与 rescue 完全相同。
先用选择样本冻结两个菜单，再打开独立报告样本；报告结果不能触发重新选价。
`V_estimate` 是所选候选在报告样本中的差值；只要内层或外层尚未验证，就不是认证的
`V*(m)`。未决候选不会从网格中消失，负的报告增益也不会被截断。

三个以上厚度点会得到 `shape_diagnostic`：相邻差分、近似误差区间、原始网格是否单峰。
它不平滑、不插值，不证明连续 m 的单峰；若输入策略未认证，该限制会明确标注。
`thickness_diagnostic` 另外逐点检验 `p1 <= p_flat <= p2`、三条价格是否随厚度不增，
以及观测到的内部峰值是否高于两端。内部峰值比较使用全点两两差值的同时正态区间，
避免先挑最高点再把它当预先指定的比较；这些区间只覆盖报告样本误差。
“中间比两端高”和“整条曲线先升后降”是不同的检查。程序不将任何价格关系写成约束。

`--workers` 按厚度并行，不改变初始化、抽样种子、选择规则或结果；可用不同 worker
数量恢复同一个请求。六个厚度共享同一随机 OD 支撑，独立报告种子按厚度索引固定。

完整粗网格探索命令（不是烟雾测试，也不是高精度研究结论）：

```bash
python -m rescue_solver grid --m 1 3 6 12 24 48 --step .1 --workers 6 \
  --route-seed 20260904 --seed 2026090501 \
  --train-counts 128 --audit-counts 2000 \
  --selection-markets 50000 --report-markets 1000000 \
  --output runs/relationship_grid_01
```

每个厚度 66 个菜单，总计 396 个。该预算主要定位问题与候选区域。训练不收敛或
审计不通过时，不能拿高精度报告模拟来弥补；应先解决内层，再检验价格/类型加密稳定性。

先检查成本/流程可用以下命令，但不得用其价格和曲线作研究结论：

```bash
python -m rescue_solver grid --m 1 3 6 12 24 48 --step .5 --smoke \
  --route-seed 42 --selection-markets 1000 --report-markets 2000 \
  --output runs/grid_smoke
```

## 4. 断点恢复与独立复审

重发完全相同的 `menu`/`grid` 命令，追加 `--resume`，即可复用本次运行完成的菜单。
恢复是菜单级的；中断时尚未完成的菜单会重新求解，不声称恢复到每一步内层迭代。
源码、NumPy/Python 版本、请求、随机种子、模型、支撑或策略身份不一致时拒绝恢复。
新实验必须使用新的输出目录。结果不应手工修改成“通过”。

对已保存策略重新审计，不重新求策略、不重新选价：

```bash
python -m rescue_solver audit \
  --menu-dir runs/menu_smoke/thickness_000/menu_00000 \
  --audit-counts 100000 --audit-seed 314159 \
  --output runs/menu_smoke_independent_audit.json
```

复审继承原实验的计数积分模式；必须提供未用于原训练/审计的新种子。
`--count-cap` 和 `--max-states` 可控制枚举复审预算。

## 配置与 Python API

配置 JSON 只有一个顶层键 `model`，例如 `configs/small.json`。省略参数时使用默认值。
未知参数、无效概率、无效支撑或隐藏的旧求解预算会被拒绝；实际算法预算全部写入请求。

```python
from rescue_solver import ModelParams, RescueModel, Settings, solve_menu

model = RescueModel(ModelParams(seed=42, route_draws=10000))
profile, evidence = solve_menu(
    model, m=3, p1=.365, p2=.535,
    settings=Settings(train_counts=1024, audit_counts=20000),
    init="homotopy",
)
print(evidence["status"], evidence["training_regrets"])
```

`init=early|hidden` 用于独立分支敏感性实验；不在初值之间按平台收益挑选均衡。
`Settings(mode="enumerate")` 可枚举小模型的 Poisson 计数，保留尾概率不归一化。
状态数超预算时明确停止，不自动缩小模型；完整 22 路线支撑通常应使用 sample 模式。

## 输出如何解读

| 字段/状态 | 含义 |
|---|---|
| `not_converged` | 返回策略在训练评价中未同时通过偏离收益与支持差距门槛 |
| `insufficient_evidence` | 训练检查通过，但独立审计上界仍不能通过 |
| `numerical_checks_passed` | 当前数值规则下，训练及保守计数误差审计通过 |
| `max_regret_upper` | 包含计数抽样/截断误差的偏离收益上界；不是完整数值误差界 |
| `bounded_support_check_pass` | 支持集收益差的保守上界是否通过，独立于小概率加权 regret |
| `complementarity` | 期初与留存互补残差，单位为效用 |
| `unresolved_indices` | 未通过内层数值检查的所有菜单，不删去 |
| `sampling_rank_separated` | 固定策略的选择样本区间是否足以区分领先价格 |
| `V_is_certified_optimized_value` | 当前固定为 false |
| `wpbe_certified` | 当前固定为 false |

退出码 0 表示相应操作完成且数值检查通过；2 表示计算完成但仍有未决证据。
程序异常另给错误信息，不能因没有成功标志而默认通过。
Hoeffding 条件概率界较保守，稀有信息集即使有较小的样本 regret，也可能长期不能通过。

默认 regret 门槛为 `0.00075`，支持集收益差门槛为 `0.0015`（检查行动概率大于
`0.001` 的支持）；二者均为效用单位，不是价格小数位或成交率误差。训练停止与最终
独立审计必须同时满足这两类条件。支持阈值和预算均不是连续类型精度的保证。
15×22 是类型离散分辨率；价格步长是搜索分辨率；100 万报告市场只降低固定策略的
成交率/增益 Monte Carlo 误差。这三者不可互相替代。

## 数学与实现边界

完整时序、信息集、收益、Bayes 比率、互补条件、Poisson 计数与平台目标见
[docs/MODEL.md](docs/MODEL.md)。来源和验证范围见 [docs/PROVENANCE.md](docs/PROVENANCE.md)。
价格关系与薄/厚端极限的条件推导见 [docs/PRICE_AND_THICKNESS.md](docs/PRICE_AND_THICKNESS.md)：
本模型的两端增益趋零提供内部峰值的可能性，但不等于单峰证明。

本问题是非凸均衡约束的双层随机优化，不是 LP/MIP。当前采用温度延拓、阻尼最优反应、
零温度阶段和独立审计，未保证找到均衡或找到所有均衡。
尚未完整解决离轨信念构造、连续类型误差、并列数值积分误差和连续价格全局最优性。
因此不能将本仓库版本号或测试数量当作研究结论。

本仓库当前只保留求解器、配置、测试和说明。旧论文、图表、结果和历史算法已移出
当前文件树，但仍可从 Git 历史恢复。运行生成的数据默认放在 `runs/`，不提交到仓库。
