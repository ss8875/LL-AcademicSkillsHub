# Clinical Decision Support

[返回技能总览](../../../../README.md) · [English](en.md) · [查看原始 SKILL](../SKILL.md)

## 1. 技能简介

为制药和临床研究环境生成专业的临床决策支持 (CDS) 文件，包括患者队列分析（根据结果进行生物标志物分层）和治疗推荐报告（带有决策算法的循证指南）。支持 GRADE 证据分级、统计分析（风险比、生存曲线、瀑布图）、生物标志物集成和法规遵从性。输出针对药物开发、临床研究和证据合成进行优化的可发布 LaTeX/PDF 格式。

它属于“临床医学与精准医疗”类别，核心定位是：组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持。本说明把原始技能的技术内容整理为中文使用契约；涉及具体命令、参数或版本时，仍以[原始 `SKILL.md`](../SKILL.md)及随附文件为准。

## 2. 适合用它做什么

- 整理临床与精准医学证据
- 处理受控医学数据
- 标注适用边界与风险
- 当你已有“临床问题、医学数据或证据资料”，并希望得到“证据摘要、分析结果或结构化记录”时使用。
- 当任务需要围绕“组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持”形成可复核、可继续加工的中间产物时使用。

不建议仅因为技能名称相近就直接调用；先确认研究对象、输入格式和预期产出与本页描述一致。

## 3. 工作方式

本技能按“输入契约 → 执行 → 验证 → 交付”工作。原始指令的重点阅读路径为：`脚本与接口` → `核心能力与原则` → `常见用法` → `适用场景` → `专题说明` → `任务结构` → `产出要求` → `协同与集成`。

1. **确认研究或病例范围、数据来源、终点与人群定义。** 本技能至少需要：临床问题、医学数据或证据资料。
2. **完成脱敏、质量控制、特征提取和证据分级。** 保留关键选择、参数、筛选条件和中间结果，便于复核。
3. **执行统计、影像或精准医学分析并标注不确定性。** 执行重点包括：整理临床与精准医学证据；处理受控医学数据；标注适用边界与风险。
4. **输出供临床或研究团队复核的结构化报告。** 最终交付：证据摘要、分析结果或结构化记录。
5. **交付前复核。** 检查结果是否回答原始问题，是否区分事实、推断和不确定性，是否留下足够的复现与交接信息。

## 4. 请求说明

你可以直接用自然语言提出任务。一个高质量请求最好同时写清目标、输入、约束、产出格式和验收标准。

### 推荐请求模板

> 请使用“Clinical Decision Support”处理【临床问题、医学数据或证据资料】。目标是【写明研究目标】；请遵守【时间范围、对象范围、格式或方法约束】，输出【证据摘要、分析结果或结构化记录】，并列出关键步骤、证据来源、不确定性和需要人工确认的事项。

### 可直接改写的请求

- “请用 Clinical Decision Support 完成整理临床与精准医学证据。我的材料是【临床问题、医学数据或证据资料】，结果请整理为【证据摘要、分析结果或结构化记录】。”
- “请先检查我提供的【临床问题、医学数据或证据资料】是否足够，再用 Clinical Decision Support 执行标注适用边界与风险；不要补造缺失信息。”
- “请把 Clinical Decision Support 的处理过程做成可复核记录，交付【证据摘要、分析结果或结构化记录】，同时标出假设、限制和下一步建议。”

## 5. 示例预览

| 环节 | 示例内容 |
|---|---|
| 任务目标 | 使用 **Clinical Decision Support** 完成“整理临床与精准医学证据” |
| 输入材料 | 临床问题、医学数据或证据资料 |
| 处理重点 | 整理临床与精准医学证据；处理受控医学数据；标注适用边界与风险 |
| 预期产出 | 证据摘要、分析结果或结构化记录 |
| 验收重点 | 结果可追溯、关键假设明确、与“组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持”的目标一致 |

示例只展示交付形态，不替代真实任务中的数据、参数、伦理审批、领域判断或人工复核。

## 6. 你需要提供

- **必需输入：**临床问题、医学数据或证据资料。
- **任务目标：**要回答的问题、使用场景和完成标准。
- **范围限制：**研究对象、时间范围、排除条件、语言、格式或目标期刊等。
- **已有材料：**原始数据、文献、代码、图表、协议或草稿；请说明版本及允许使用的范围。
- **交付偏好：**文件格式、字段结构、是否需要脚本、是否保留中间结果与审计记录。

如果上述信息不全，应先列出缺口并向用户确认；不能把猜测当作用户已提供的事实。

## 7. 产出

- 证据摘要、分析结果或结构化记录。
- 一份简明的方法与参数说明，记录关键选择、版本、过滤或排除规则。
- 一份质量检查与未决问题清单，标出不能自动确认、需要领域专家复核的部分。
- 如任务产生文件，优先保留可编辑源文件，并将派生产物与用户原始材料分开。

## 8. 内置参考

- [原始 `SKILL.md`](../SKILL.md)：权威执行指令与完整技术细节。
- 随技能打包 **19** 个文件，按用途完整列出如下。

### 参考资料（7）

- [`references/biomarker_classification.md`](../references/biomarker_classification.md)：方法、规范或领域约束参考。
- [`references/clinical_decision_algorithms.md`](../references/clinical_decision_algorithms.md)：方法、规范或领域约束参考。
- [`references/evidence_synthesis.md`](../references/evidence_synthesis.md)：方法、规范或领域约束参考。
- [`references/outcome_analysis.md`](../references/outcome_analysis.md)：方法、规范或领域约束参考。
- [`references/patient_cohort_analysis.md`](../references/patient_cohort_analysis.md)：方法、规范或领域约束参考。
- [`references/README.md`](../references/README.md)：方法、规范或领域约束参考。
- [`references/treatment_recommendations.md`](../references/treatment_recommendations.md)：方法、规范或领域约束参考。

### 执行脚本（5）

- [`scripts/biomarker_classifier.py`](../scripts/biomarker_classifier.py)：可复用执行或验证脚本。
- [`scripts/build_decision_tree.py`](../scripts/build_decision_tree.py)：可复用执行或验证脚本。
- [`scripts/create_cohort_tables.py`](../scripts/create_cohort_tables.py)：可复用执行或验证脚本。
- [`scripts/generate_survival_analysis.py`](../scripts/generate_survival_analysis.py)：可复用执行或验证脚本。
- [`scripts/validate_cds_document.py`](../scripts/validate_cds_document.py)：可复用执行或验证脚本。

### 模板与素材（7）

- [`assets/biomarker_report_template.tex`](../assets/biomarker_report_template.tex)：可复用模板、样式或示例素材。
- [`assets/clinical_pathway_template.tex`](../assets/clinical_pathway_template.tex)：可复用模板、样式或示例素材。
- [`assets/cohort_analysis_template.tex`](../assets/cohort_analysis_template.tex)：可复用模板、样式或示例素材。
- [`assets/color_schemes.tex`](../assets/color_schemes.tex)：可复用模板、样式或示例素材。
- [`assets/example_gbm_cohort.md`](../assets/example_gbm_cohort.md)：可复用模板、样式或示例素材。
- [`assets/recommendation_strength_guide.md`](../assets/recommendation_strength_guide.md)：可复用模板、样式或示例素材。
- [`assets/treatment_recommendation_template.tex`](../assets/treatment_recommendation_template.tex)：可复用模板、样式或示例素材。

仅在相关步骤需要时读取相应参考或脚本；运行脚本前应检查参数、输入路径、输出路径及是否会修改文件。

## 9. 边界

- 技能产出不构成诊断、处方或个体医疗建议。
- 真实患者数据必须满足知情同意、隐私、伦理和访问控制要求。
- 模型性能必须在目标人群和外部数据上验证，不能直接跨人群外推。
- 本技能的职责是“组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持”，不能替代与任务相关的伦理、临床、法律、安全或领域专家审查。
- 外部数据、接口和模型的内容可能变化；重要结论应保存来源、访问时间和稳定标识。

## 10. 相关技能

- [Treatment Plans](../../treatment-plans/locales/zh-CN.md)：以 LaTeX/PDF 格式为所有临床专业生成简洁（3-4 页）、重点突出的医疗计划。支持一般医疗、康复治疗、心理保健、慢性病管理、围手术期护理和疼痛管理。包括 SMART 目标框架、以最少文本引用的循证干预措施、法规遵从性 (HIPAA) 和专业格式。优先考虑简洁性和临床可操作性。
- [Clinical Reports](../../clinical-reports/locales/zh-CN.md)：撰写全面的临床报告，包括病例报告（CARE 指南）、诊断报告（放射学/病理学/实验室）、临床试验报告（ICH-E3、SAE、CSR）和患者文件（SOAP、H&P、出院小结）。全面支持模板、法规遵从性（HIPAA、FDA、ICH-GCP）和验证工具。
- [Cbioportal Database](../../cbioportal-database/locales/zh-CN.md)：查询 cBioPortal 的癌症基因组学数据，包括数百项癌症研究的体细胞突变、拷贝数改变、基因表达和生存数据。对于癌症靶标验证、癌基因/肿瘤抑制基因分析和患者水平基因组分析至关重要。

这些技能与本技能处于相近任务域。组合使用前先划分每个技能的输入、输出和责任边界，避免重复处理或相互覆盖。

## 11. 与其他技能的关系

- **上游准备：**[Clinicaltrials Database](../../clinicaltrials-database/locales/zh-CN.md)可用于准备或核对本技能所需的“临床问题、医学数据或证据资料”。
- **本技能职责：**Clinical Decision Support 聚焦于“组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持”，负责完成“整理临床与精准医学证据；处理受控医学数据；标注适用边界与风险”。
- **下游承接：**[Scientific Writing](../../../scientific-communication/scientific-writing/locales/zh-CN.md)可继续使用本技能产生的“证据摘要、分析结果或结构化记录”开展后续分析、表达或交付。
- **分工原则：**若任务重点已经从“组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持”转移到其他领域，应把本技能的可追溯产出作为交接材料，而不是让一个技能包办全部科研流程。
