# Paper Slide Deck

[返回技能总览](../../../../README.md) · [English](en.md) · [查看原始 SKILL](../SKILL.md)

## 1. 技能简介

从学术论文和内容生成专业的幻灯片图像。使用样式说明创建全面的轮廓，自动检测 PDF 中的图形，然后生成单独的幻灯片图像。当用户要求“创建幻灯片”、“进行演示”、“生成幻灯片”或“幻灯片”时使用。

它属于“学术演示与可视化”类别，核心定位是：把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料。本说明把原始技能的技术内容整理为中文使用契约；涉及具体命令、参数或版本时，仍以[原始 `SKILL.md`](../SKILL.md)及随附文件为准。

## 2. 适合用它做什么

- 设计学术图表与版式
- 把数据转化为可读视觉
- 输出演示或出版素材
- 当你已有“数据、论点、目标媒介”，并希望得到“图表、海报、幻灯片或图形文件”时使用。
- 当任务需要围绕“把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料”形成可复核、可继续加工的中间产物时使用。

不建议仅因为技能名称相近就直接调用；先确认研究对象、输入格式和预期产出与本页描述一致。

## 3. 工作方式

本技能按“输入契约 → 执行 → 验证 → 交付”工作。原始指令的重点阅读路径为：`使用方式` → `脚本与接口` → `模式与参数` → `示例与预览` → `专题说明` → `工作流程` → `参考资料` → `边界与问题排查`。

1. **定义视觉材料要传达的核心结论、受众和使用媒介。** 本技能至少需要：数据、论点、目标媒介。
2. **核对数据结构、图形类型、版式尺寸与期刊或会务规范。** 保留关键选择、参数、筛选条件和中间结果，便于复核。
3. **生成图表、页面或视觉草稿，并保留可编辑源文件。** 执行重点包括：设计学术图表与版式；把数据转化为可读视觉；输出演示或出版素材。
4. **检查标注、配色、可访问性、分辨率和数据—图形一致性。** 最终交付：图表、海报、幻灯片或图形文件。
5. **交付前复核。** 检查结果是否回答原始问题，是否区分事实、推断和不确定性，是否留下足够的复现与交接信息。

## 4. 请求说明

你可以直接用自然语言提出任务。一个高质量请求最好同时写清目标、输入、约束、产出格式和验收标准。

### 推荐请求模板

> 请使用“Paper Slide Deck”处理【数据、论点、目标媒介】。目标是【写明研究目标】；请遵守【时间范围、对象范围、格式或方法约束】，输出【图表、海报、幻灯片或图形文件】，并列出关键步骤、证据来源、不确定性和需要人工确认的事项。

### 可直接改写的请求

- “请用 Paper Slide Deck 完成设计学术图表与版式。我的材料是【数据、论点、目标媒介】，结果请整理为【图表、海报、幻灯片或图形文件】。”
- “请先检查我提供的【数据、论点、目标媒介】是否足够，再用 Paper Slide Deck 执行输出演示或出版素材；不要补造缺失信息。”
- “请把 Paper Slide Deck 的处理过程做成可复核记录，交付【图表、海报、幻灯片或图形文件】，同时标出假设、限制和下一步建议。”

## 5. 示例预览

| 环节 | 示例内容 |
|---|---|
| 任务目标 | 使用 **Paper Slide Deck** 完成“设计学术图表与版式” |
| 输入材料 | 数据、论点、目标媒介 |
| 处理重点 | 设计学术图表与版式；把数据转化为可读视觉；输出演示或出版素材 |
| 预期产出 | 图表、海报、幻灯片或图形文件 |
| 验收重点 | 结果可追溯、关键假设明确、与“把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料”的目标一致 |

示例只展示交付形态，不替代真实任务中的数据、参数、伦理审批、领域判断或人工复核。

## 6. 你需要提供

- **必需输入：**数据、论点、目标媒介。
- **任务目标：**要回答的问题、使用场景和完成标准。
- **范围限制：**研究对象、时间范围、排除条件、语言、格式或目标期刊等。
- **已有材料：**原始数据、文献、代码、图表、协议或草稿；请说明版本及允许使用的范围。
- **交付偏好：**文件格式、字段结构、是否需要脚本、是否保留中间结果与审计记录。

如果上述信息不全，应先列出缺口并向用户确认；不能把猜测当作用户已提供的事实。

## 7. 产出

- 图表、海报、幻灯片或图形文件。
- 一份简明的方法与参数说明，记录关键选择、版本、过滤或排除规则。
- 一份质量检查与未决问题清单，标出不能自动确认、需要领域专家复核的部分。
- 如任务产生文件，优先保留可编辑源文件，并将派生产物与用户原始材料分开。

## 8. 内置参考

- [原始 `SKILL.md`](../SKILL.md)：权威执行指令与完整技术细节。
- 随技能打包 **31** 个文件，按用途完整列出如下。

### 参考资料（23）

- [`references/analysis-framework.md`](../references/analysis-framework.md)：方法、规范或领域约束参考。
- [`references/base-prompt.md`](../references/base-prompt.md)：方法、规范或领域约束参考。
- [`references/content-rules.md`](../references/content-rules.md)：方法、规范或领域约束参考。
- [`references/figure-container-template.md`](../references/figure-container-template.md)：方法、规范或领域约束参考。
- [`references/modification-guide.md`](../references/modification-guide.md)：方法、规范或领域约束参考。
- [`references/outline-template.md`](../references/outline-template.md)：方法、规范或领域约束参考。
- [`references/styles/academic-paper.md`](../references/styles/academic-paper.md)：方法、规范或领域约束参考。
- [`references/styles/blueprint.md`](../references/styles/blueprint.md)：方法、规范或领域约束参考。
- [`references/styles/bold-editorial.md`](../references/styles/bold-editorial.md)：方法、规范或领域约束参考。
- [`references/styles/chalkboard.md`](../references/styles/chalkboard.md)：方法、规范或领域约束参考。
- [`references/styles/corporate.md`](../references/styles/corporate.md)：方法、规范或领域约束参考。
- [`references/styles/dark-atmospheric.md`](../references/styles/dark-atmospheric.md)：方法、规范或领域约束参考。
- [`references/styles/editorial-infographic.md`](../references/styles/editorial-infographic.md)：方法、规范或领域约束参考。
- [`references/styles/fantasy-animation.md`](../references/styles/fantasy-animation.md)：方法、规范或领域约束参考。
- [`references/styles/intuition-machine.md`](../references/styles/intuition-machine.md)：方法、规范或领域约束参考。
- [`references/styles/minimal.md`](../references/styles/minimal.md)：方法、规范或领域约束参考。
- [`references/styles/notion.md`](../references/styles/notion.md)：方法、规范或领域约束参考。
- [`references/styles/pixel-art.md`](../references/styles/pixel-art.md)：方法、规范或领域约束参考。
- [`references/styles/scientific.md`](../references/styles/scientific.md)：方法、规范或领域约束参考。
- [`references/styles/sketch-notes.md`](../references/styles/sketch-notes.md)：方法、规范或领域约束参考。
- [`references/styles/vector-illustration.md`](../references/styles/vector-illustration.md)：方法、规范或领域约束参考。
- [`references/styles/vintage.md`](../references/styles/vintage.md)：方法、规范或领域约束参考。
- [`references/styles/watercolor.md`](../references/styles/watercolor.md)：方法、规范或领域约束参考。

### 执行脚本（8）

- [`scripts/apply-template.ts`](../scripts/apply-template.ts)：可复用执行或验证脚本。
- [`scripts/detect-figures.ts`](../scripts/detect-figures.ts)：可复用执行或验证脚本。
- [`scripts/extract-figure.ts`](../scripts/extract-figure.ts)：可复用执行或验证脚本。
- [`scripts/generate-slides.py`](../scripts/generate-slides.py)：可复用执行或验证脚本。
- [`scripts/merge-to-pdf.ts`](../scripts/merge-to-pdf.ts)：可复用执行或验证脚本。
- [`scripts/merge-to-pptx.ts`](../scripts/merge-to-pptx.ts)：可复用执行或验证脚本。
- [`scripts/package-lock.json`](../scripts/package-lock.json)：可复用执行或验证脚本。
- [`scripts/package.json`](../scripts/package.json)：可复用执行或验证脚本。

仅在相关步骤需要时读取相应参考或脚本；运行脚本前应检查参数、输入路径、输出路径及是否会修改文件。

## 9. 边界

- 不把示意图或 AI 生成图当作真实实验图像和定量结果。
- 不通过截断坐标轴、隐藏样本或不当配色制造误导性视觉结论。
- 图中统计标注、样本量和误差定义必须来自已核验数据。
- 本技能的职责是“把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料”，不能替代与任务相关的伦理、临床、法律、安全或领域专家审查。
- 外部数据、接口和模型的内容可能变化；重要结论应保存来源、访问时间和稳定标识。

## 10. 相关技能

- [Latex Posters](../../latex-posters/locales/zh-CN.md)：使用 beamerposter、tikzposter 或 baposter 在 LaTeX 中创建专业研究海报。支持会议演示、学术海报和科学传播。包括布局设计、配色方案、多栏格式、图形集成以及针对视觉传达的海报特定最佳实践。
- [Markdown Mermaid Writing](../../markdown-mermaid-writing/locales/zh-CN.md)：全面的 Markdown 与 Mermaid 图表写作技能，适用于科学文档、研究报告、分析材料和可视化内容。以文本化图表作为可维护的文档标准，提供 Markdown/Mermaid 样式指南、24 类图表参考和 9 套文档模板。
- [Scientific Slides](../../scientific-slides/locales/zh-CN.md)：为研究演讲构建幻灯片和演示文稿。使用它来制作 PowerPoint 幻灯片、会议演示、研讨会演讲、研究演示、论文答辩幻灯片或任何科学演讲。提供幻灯片结构、设计模板、计时指导和视觉验证。适用于 PowerPoint 和 LaTeX Beamer。

这些技能与本技能处于相近任务域。组合使用前先划分每个技能的输入、输出和责任边界，避免重复处理或相互覆盖。

## 11. 与其他技能的关系

- **上游准备：**[Statistical Analysis](../../../data-analysis-statistics/statistical-analysis/locales/zh-CN.md)可用于准备或核对本技能所需的“数据、论点、目标媒介”。
- **本技能职责：**Paper Slide Deck 聚焦于“把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料”，负责完成“设计学术图表与版式；把数据转化为可读视觉；输出演示或出版素材”。
- **下游承接：**[Venue Templates](../../../scientific-communication/venue-templates/locales/zh-CN.md)可继续使用本技能产生的“图表、海报、幻灯片或图形文件”开展后续分析、表达或交付。
- **分工原则：**若任务重点已经从“把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料”转移到其他领域，应把本技能的可追溯产出作为交接材料，而不是让一个技能包办全部科研流程。
