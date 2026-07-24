# Timesfm Forecasting

[返回技能总览](../../../../README.md) · [English](en.md) · [查看原始 SKILL](../SKILL.md)

## 1. 技能简介

使用 Google TimesFM 基础模型进行零样本时间序列预测。适用于任何单变量时间序列（销售、传感器、能源、生命体征、天气），无需训练自定义模型。支持带有点预测和预测间隔的 CSV/DataFrame/array 输入。包括预检系统检查器脚本，用于在首次使用前验证 RAM/GPU。

它属于“机器学习与人工智能”类别，核心定位是：构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型。本说明把原始技能的技术内容整理为中文使用契约；涉及具体命令、参数或版本时，仍以[原始 `SKILL.md`](../SKILL.md)及随附文件为准。

## 2. 适合用它做什么

- 准备数据与建模流程
- 训练或调用机器学习模型
- 评估性能、偏差与复现条件
- 当你已有“数据、任务定义与计算约束”，并希望得到“模型、预测、指标或实验记录”时使用。
- 当任务需要围绕“构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型”形成可复核、可继续加工的中间产物时使用。

不建议仅因为技能名称相近就直接调用；先确认研究对象、输入格式和预期产出与本页描述一致。

## 3. 工作方式

本技能按“输入契约 → 执行 → 验证 → 交付”工作。原始指令的重点阅读路径为：`能力概览` → `适用场景` → `输入要求` → `安装与配置` → `专题说明` → `产出要求` → `参考资料` → `工作流程`。

1. **定义任务、预测目标、数据粒度、评价指标与基线。** 本技能至少需要：数据、任务定义与计算约束。
2. **划分数据并建立防止泄漏的预处理和验证流程。** 保留关键选择、参数、筛选条件和中间结果，便于复核。
3. **训练或调用模型，记录参数、版本、种子和计算环境。** 执行重点包括：准备数据与建模流程；训练或调用机器学习模型；评估性能、偏差与复现条件。
4. **评估泛化、校准、误差、偏倚和可解释性后交付模型产物。** 最终交付：模型、预测、指标或实验记录。
5. **交付前复核。** 检查结果是否回答原始问题，是否区分事实、推断和不确定性，是否留下足够的复现与交接信息。

## 4. 请求说明

你可以直接用自然语言提出任务。一个高质量请求最好同时写清目标、输入、约束、产出格式和验收标准。

### 推荐请求模板

> 请使用“Timesfm Forecasting”处理【数据、任务定义与计算约束】。目标是【写明研究目标】；请遵守【时间范围、对象范围、格式或方法约束】，输出【模型、预测、指标或实验记录】，并列出关键步骤、证据来源、不确定性和需要人工确认的事项。

### 可直接改写的请求

- “请用 Timesfm Forecasting 完成准备数据与建模流程。我的材料是【数据、任务定义与计算约束】，结果请整理为【模型、预测、指标或实验记录】。”
- “请先检查我提供的【数据、任务定义与计算约束】是否足够，再用 Timesfm Forecasting 执行评估性能、偏差与复现条件；不要补造缺失信息。”
- “请把 Timesfm Forecasting 的处理过程做成可复核记录，交付【模型、预测、指标或实验记录】，同时标出假设、限制和下一步建议。”

## 5. 示例预览

| 环节 | 示例内容 |
|---|---|
| 任务目标 | 使用 **Timesfm Forecasting** 完成“准备数据与建模流程” |
| 输入材料 | 数据、任务定义与计算约束 |
| 处理重点 | 准备数据与建模流程；训练或调用机器学习模型；评估性能、偏差与复现条件 |
| 预期产出 | 模型、预测、指标或实验记录 |
| 验收重点 | 结果可追溯、关键假设明确、与“构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型”的目标一致 |

示例只展示交付形态，不替代真实任务中的数据、参数、伦理审批、领域判断或人工复核。

## 6. 你需要提供

- **必需输入：**数据、任务定义与计算约束。
- **任务目标：**要回答的问题、使用场景和完成标准。
- **范围限制：**研究对象、时间范围、排除条件、语言、格式或目标期刊等。
- **已有材料：**原始数据、文献、代码、图表、协议或草稿；请说明版本及允许使用的范围。
- **交付偏好：**文件格式、字段结构、是否需要脚本、是否保留中间结果与审计记录。

如果上述信息不全，应先列出缺口并向用户确认；不能把猜测当作用户已提供的事实。

## 7. 产出

- 模型、预测、指标或实验记录。
- 一份简明的方法与参数说明，记录关键选择、版本、过滤或排除规则。
- 一份质量检查与未决问题清单，标出不能自动确认、需要领域专家复核的部分。
- 如任务产生文件，优先保留可编辑源文件，并将派生产物与用户原始材料分开。

## 8. 内置参考

- [原始 `SKILL.md`](../SKILL.md)：权威执行指令与完整技术细节。
- 随技能打包 **26** 个文件，按用途完整列出如下。

### 参考资料（3）

- [`references/api_reference.md`](../references/api_reference.md)：方法、规范或领域约束参考。
- [`references/data_preparation.md`](../references/data_preparation.md)：方法、规范或领域约束参考。
- [`references/system_requirements.md`](../references/system_requirements.md)：方法、规范或领域约束参考。

### 执行脚本（2）

- [`scripts/check_system.py`](../scripts/check_system.py)：可复用执行或验证脚本。
- [`scripts/forecast_csv.py`](../scripts/forecast_csv.py)：可复用执行或验证脚本。

### 其他随附文件（21）

- [`examples/anomaly-detection/detect_anomalies.py`](../examples/anomaly-detection/detect_anomalies.py)：技能运行或说明所需的随附文件。
- [`examples/anomaly-detection/output/anomaly_detection.json`](../examples/anomaly-detection/output/anomaly_detection.json)：技能运行或说明所需的随附文件。
- [`examples/anomaly-detection/output/anomaly_detection.png`](../examples/anomaly-detection/output/anomaly_detection.png)：技能运行或说明所需的随附文件。
- [`examples/covariates-forecasting/demo_covariates.py`](../examples/covariates-forecasting/demo_covariates.py)：技能运行或说明所需的随附文件。
- [`examples/covariates-forecasting/output/covariates_data.png`](../examples/covariates-forecasting/output/covariates_data.png)：技能运行或说明所需的随附文件。
- [`examples/covariates-forecasting/output/covariates_metadata.json`](../examples/covariates-forecasting/output/covariates_metadata.json)：技能运行或说明所需的随附文件。
- [`examples/covariates-forecasting/output/sales_with_covariates.csv`](../examples/covariates-forecasting/output/sales_with_covariates.csv)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/generate_animation_data.py`](../examples/global-temperature/generate_animation_data.py)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/generate_gif.py`](../examples/global-temperature/generate_gif.py)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/generate_html.py`](../examples/global-temperature/generate_html.py)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/animation_data.json`](../examples/global-temperature/output/animation_data.json)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/forecast_animation.gif`](../examples/global-temperature/output/forecast_animation.gif)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/forecast_output.csv`](../examples/global-temperature/output/forecast_output.csv)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/forecast_output.json`](../examples/global-temperature/output/forecast_output.json)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/forecast_visualization.png`](../examples/global-temperature/output/forecast_visualization.png)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/output/interactive_forecast.html`](../examples/global-temperature/output/interactive_forecast.html)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/README.md`](../examples/global-temperature/README.md)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/run_example.sh`](../examples/global-temperature/run_example.sh)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/run_forecast.py`](../examples/global-temperature/run_forecast.py)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/temperature_anomaly.csv`](../examples/global-temperature/temperature_anomaly.csv)：技能运行或说明所需的随附文件。
- [`examples/global-temperature/visualize_forecast.py`](../examples/global-temperature/visualize_forecast.py)：技能运行或说明所需的随附文件。

仅在相关步骤需要时读取相应参考或脚本；运行脚本前应检查参数、输入路径、输出路径及是否会修改文件。

## 9. 边界

- 测试集、未来信息或同源样本泄漏会使性能失真。
- 单一指标不能代表模型的稳健性、公平性和实际效用。
- 生成或预测结果必须标注模型来源、置信度和人工复核要求。
- 本技能的职责是“构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型”，不能替代与任务相关的伦理、临床、法律、安全或领域专家审查。
- 外部数据、接口和模型的内容可能变化；重要结论应保存来源、访问时间和稳定标识。

## 10. 相关技能

- [Aeon](../../aeon/locales/zh-CN.md)：该技能应用于时间序列机器学习任务，包括分类、回归、聚类、预测、异常检测、分割和相似性搜索。当处理时态数据、顺序模式或时间索引观察需要标准 ML 方法之外的专用算法时使用。特别适合使用 scikit-learn 兼容 API 进行单变量和多变量时间序列分析。
- [Torch Geometric](../../torch-geometric/locales/zh-CN.md)：图神经网络（PyG）。节点/图分类、链接预测、GCN、GAT、GraphSAGE、异构图、分子属性预测、用于几何深度学习。
- [Stable Baselines3](../../stable-baselines3/locales/zh-CN.md)：具有类似 scikit-learn 的 API 的可用于生产的强化学习算法（PPO、SAC、DQN、TD3、DDPG、A2C）。用于标准 RL 实验、快速原型设计和记录良好的算法实现。最适合在 Gymnasium 环境中进行单智能体强化学习。对于高性能并行训练、多代理系统或自定义矢量化环境，请改用 pufferlib。

这些技能与本技能处于相近任务域。组合使用前先划分每个技能的输入、输出和责任边界，避免重复处理或相互覆盖。

## 11. 与其他技能的关系

- **上游准备：**[Exploratory Data Analysis](../../../data-analysis-statistics/exploratory-data-analysis/locales/zh-CN.md)可用于准备或核对本技能所需的“数据、任务定义与计算约束”。
- **本技能职责：**Timesfm Forecasting 聚焦于“构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型”，负责完成“准备数据与建模流程；训练或调用机器学习模型；评估性能、偏差与复现条件”。
- **下游承接：**[Scientific Visualization](../../../presentation-visualization/scientific-visualization/locales/zh-CN.md)可继续使用本技能产生的“模型、预测、指标或实验记录”开展后续分析、表达或交付。
- **分工原则：**若任务重点已经从“构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型”转移到其他领域，应把本技能的可追溯产出作为交接材料，而不是让一个技能包办全部科研流程。
