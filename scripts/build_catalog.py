#!/usr/bin/env python3
"""Build bilingual catalog artifacts from the canonical seed records."""

from __future__ import annotations

import json
import os
import re
import html
from collections import Counter
from datetime import date
from pathlib import Path

from build_skill_guides import build_all_skill_guides


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_URL = "https://github.com/ss8875/LL-AcademicSkillsHub"

CATEGORY_TASKS_ZH = {
    "literature-management": "论文检索、筛选、引用管理与证据综述",
    "scientific-communication": "论文写作、基金申请、同行评审与学术表达",
    "presentation-visualization": "科研图表、海报、幻灯片与出版级可视化",
    "research-methods": "研究问题、实验设计、批判思维与可复现性",
    "bioinformatics-genomics": "序列、组学、单细胞与基因组分析",
    "cheminformatics-drug-discovery": "分子结构、性质预测、虚拟筛选与药物发现",
    "clinical-precision-medicine": "临床证据、医学影像与精准医疗分析",
    "protein-structural-biology": "蛋白结构、功能注释、设计与工程",
    "machine-learning-ai": "机器学习建模、训练、推理、优化与解释",
    "materials-physics": "材料模拟、量子计算、物理建模与科学计算",
    "data-analysis-statistics": "数据清理、统计推断、建模与分析报告",
    "scientific-databases": "专业科学数据库检索、整合与规范化",
    "lab-automation": "实验协议、仪器控制、液体处理与自动化",
    "document-data-tools": "PDF、文档、表格、演示文件与结构化转换",
    "finance-economics": "金融市场、企业数据与宏观经济研究",
    "geospatial-remote-sensing": "GIS、遥感影像、空间计算与地球观测",
    "platform-infrastructure": "计算环境、云资源、任务编排与科研基础设施",
    "academic-core": "检索、精读、写作、审稿与证据治理工作流",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def env_value(name: str) -> str:
    value = os.environ.get(name, "").strip()
    env_file = ROOT / ".env"
    if value or not env_file.exists():
        return value
    for raw in env_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.strip().startswith(f"{name}="):
            return raw.split("=", 1)[1].strip()
    return ""


def catalog_payload(categories: list[dict], skills: list[dict]) -> dict:
    source_counts = Counter(item["source"]["kind"] for item in skills)
    quality_counts = Counter(item["quality"]["status"] for item in skills)
    return {
        "project": {
            "id": "LL-AcademicSkillsHub",
            "repository": REPOSITORY_URL,
            "name": {"zh-CN": "链邻学术技能仓库", "en": "LL-AcademicSkillsHub"},
            "releaseScope": {
                "zh-CN": "本地部署，或下载链邻科研 AI 平台",
                "en": "Local deployment, or download Lianlin Research AI Platform",
            },
            "languages": ["zh-CN", "en"],
        },
        "summary": {
            "skillCount": len(skills),
            "categoryCount": len(categories),
            "firstPartyCount": source_counts["lianlin-first-party"],
            "thirdPartyCount": source_counts["pinned-third-party"],
            "qualityCounts": dict(sorted(quality_counts.items())),
        },
        "categories": categories,
        "skills": skills,
    }


def skills_markdown(categories: list[dict], skills: list[dict], lang: str) -> str:
    zh = lang == "zh-CN"
    title = "# 全部技能与功能" if zh else "# All Skills and Functions"
    intro = (
        "本页由 `catalog/skills.seed.json` 自动生成。质量状态是证据等级，不是营销标签；"
        "`cataloged` 表示已收录并完成结构检查，不能理解为运行时已验证。"
        if zh else
        "This page is generated from `catalog/skills.seed.json`. Quality status is an evidence level, not a marketing label; "
        "`cataloged` means indexed and structurally checked, not runtime-verified."
    )
    lines = [title, "", intro, ""]
    for category in categories:
        entries = [item for item in skills if item["category"] == category["id"]]
        heading = category["zh" if zh else "en"]
        lines.extend([f"## {category['order']:02d}. {heading} ({len(entries)})", ""])
        lines.append("| 技能 | 功能 | 来源 | 状态 |" if zh else "| Skill | Function | Source | Status |")
        lines.append("|---|---|---|---|")
        for item in entries:
            display = item["title"][lang]
            summary = item["summary"][lang].replace("|", "\\|").replace("\n", " ")
            source = (
                "链邻原创" if zh and item["source"]["kind"] == "lianlin-first-party"
                else "固定第三方" if zh
                else "Lianlin first-party" if item["source"]["kind"] == "lianlin-first-party"
                else "Pinned third-party"
            )
            link = f"../{item['paths'][lang]}"
            lines.append(f"| [{display}]({link}) | {summary} | {source} | `{item['quality']['status']}` |")
        lines.append("")
    return "\n".join(lines)


def categories_markdown(categories: list[dict], skills: list[dict], lang: str) -> str:
    zh = lang == "zh-CN"
    lines = ["# 技能分类地图" if zh else "# Skill Category Map", ""]
    lines.append(
        "公开架构从链邻品牌与科研任务出发；来源与许可证属于每项技能的治理字段，不作为顶层分类。"
        if zh else
        "The public architecture starts from the Lianlin brand and research tasks. Source and license are per-skill governance fields, not top-level categories."
    )
    lines.extend(["", "| # | 分类 | 数量 | 典型任务 |" if zh else "| # | Category | Count | Typical work |", "|---:|---|---:|---|"])
    examples_zh = {
        "literature-management":"检索、筛选、引用与综述",
        "scientific-communication":"论文、基金、审稿与学术表达",
        "presentation-visualization":"图表、海报、幻灯片与出版图形",
        "research-methods":"问题、设计、偏倚与可复现性",
        "bioinformatics-genomics":"序列、组学与基因组分析",
        "cheminformatics-drug-discovery":"结构、性质、筛选与药物发现",
        "clinical-precision-medicine":"临床证据与精准医学分析",
        "protein-structural-biology":"蛋白结构、设计与功能分析",
        "machine-learning-ai":"建模、训练、推理与评估",
        "materials-physics":"材料模拟与物理计算",
        "data-analysis-statistics":"清理、统计、建模与报告",
        "scientific-databases":"领域数据库查询与数据规范化",
        "lab-automation":"协议、仪器与自动化实验",
        "document-data-tools":"文档、表格与结构化转换",
        "finance-economics":"金融、市场与宏观经济数据",
        "geospatial-remote-sensing":"GIS、遥感与空间分析",
        "platform-infrastructure":"计算资源、环境与基础设施",
        "academic-core":"检索、精读、写作、审稿与证据治理工作流",
    }
    examples_en = {
        "literature-management":"Search, screening, citation, and review",
        "scientific-communication":"Papers, grants, peer review, and expression",
        "presentation-visualization":"Figures, posters, slides, and publication graphics",
        "research-methods":"Questions, design, bias, and reproducibility",
        "bioinformatics-genomics":"Sequences, omics, and genome analysis",
        "cheminformatics-drug-discovery":"Structures, properties, screening, and discovery",
        "clinical-precision-medicine":"Clinical evidence and precision-medicine analysis",
        "protein-structural-biology":"Protein structure, design, and function",
        "machine-learning-ai":"Modeling, training, inference, and evaluation",
        "materials-physics":"Materials simulation and physics computation",
        "data-analysis-statistics":"Cleaning, statistics, modeling, and reporting",
        "scientific-databases":"Domain database query and normalization",
        "lab-automation":"Protocols, instruments, and automated experiments",
        "document-data-tools":"Documents, spreadsheets, and structured conversion",
        "finance-economics":"Finance, market, and macroeconomic data",
        "geospatial-remote-sensing":"GIS, remote sensing, and spatial analysis",
        "platform-infrastructure":"Compute resources, environments, and infrastructure",
        "academic-core":"Search, close reading, writing, peer review, and evidence governance",
    }
    for category in categories:
        count = sum(item["category"] == category["id"] for item in skills)
        name = category["zh" if zh else "en"]
        example = (examples_zh if zh else examples_en)[category["id"]]
        lines.append(f"| {category['order']} | {name} | {count} | {example} |")
    lines.append("")
    return "\n".join(lines)


def markdown_cell(value: str) -> str:
    return html.escape(value, quote=False).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def zh_skill_showcase(
    categories: list[dict],
    skills: list[dict],
    descriptions: dict[str, str],
) -> str:
    """Render the complete Chinese README capability panorama from catalog facts."""
    lines = [
        "### 18 大分类 · 187 项技能完整能力清单",
        "",
        "从选题、检索、精读、实验与数据分析，到论文写作、审稿、可视化和成果传播，"
        "下面按科研任务完整展示仓库当前收录的全部技能。每一项都提供功能说明、输入输出、"
        "使用入口及运行条件。",
        "",
        "<p align=\"center\"><strong>如果这份科研能力地图对你有帮助，欢迎点击右上角 ⭐ Star 收藏，方便随时回来检索，也让更多研究者发现它。</strong></p>",
        "",
        "| # | 分类 | 技能数 | 覆盖任务 |",
        "|---:|---|---:|---|",
    ]

    for category in categories:
        entries = [item for item in skills if item["category"] == category["id"]]
        task = CATEGORY_TASKS_ZH[category["id"]]
        lines.append(
            f"| {category['order']:02d} | [{category['zh']}](#category-{category['id']}) | "
            f"**{len(entries)}** | {task} |"
        )

    lines.append("")
    for category in categories:
        entries = [item for item in skills if item["category"] == category["id"]]
        task = CATEGORY_TASKS_ZH[category["id"]]
        lines.extend([
            f'<a id="category-{category["id"]}"></a>',
            "",
            f"#### {category['order']:02d}. {category['zh']} · {len(entries)} 项",
            "",
            f"> {task}",
            "",
            "| 技能 | 能做什么 | 怎么使用 |",
            "|---|---|---|",
        ])
        for item in entries:
            title = markdown_cell(item["title"]["zh-CN"])
            locale_link = f"./{item['paths']['zh-CN']}"
            capabilities = "；".join(markdown_cell(value) for value in item["capabilities"]["zh-CN"])
            summary_zh = markdown_cell(item["summary"]["zh-CN"])
            if item["source"]["kind"] == "lianlin-first-party":
                function_text = f"{summary_zh}<br>**核心能力：**{capabilities}"
                skill_label = f"**[{title}]({locale_link})**<br><sub>链邻原创</sub>"
            else:
                translated = descriptions.get(item["id"], "").strip()
                if not translated:
                    raise ValueError(f"Missing Chinese showcase description: {item['id']}")
                function_text = (
                    f"**核心能力：**{capabilities}<br>"
                    f"<strong>能力说明：</strong>{markdown_cell(translated)}"
                )
                skill_label = f"**[{title}]({locale_link})**"

            usage = f"[详细用法]({locale_link})"
            lines.append(f"| {skill_label} | {function_text} | {usage} |")
        lines.extend(["", "[↑ 返回分类总览](#18-大分类--187-项技能完整能力清单)", ""])

    return "\n".join(lines).rstrip()


def zh_quick_start() -> str:
    """Render a task-first onboarding guide that covers all 18 categories."""
    return """## 快速开始

你不需要先记住 187 个技能名称。最简单的上手方式是：**先说清研究目标和已有材料，再让本地 Agent 从目录中选择合适的技能或技能组合。** 如果你已经知道技能名称，也可以在请求中直接指定。

### 第 1 步：选择使用方式

#### 方式 A：本地使用

在项目根目录运行：

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

浏览器打开 `http://127.0.0.1:8765/`，即可搜索分类、技能和功能。Windows 也可运行 `scripts\\setup.bat` 与 `scripts\\start.bat`；其他系统及环境检查请看[本地部署说明](./docs/deployment.zh-CN.md)。

找到技能后，先打开对应的“详细用法”，确认适用场景、需要提供的材料、工作方式、产出、内置参考和边界，再把技能目录接入你所使用的本地 Agent Skill 环境。

#### 方式 B：使用链邻科研 AI 平台

如果不想逐项安装、配置依赖或调试环境，可以直接使用链邻科研 AI 平台的一体化能力。下载与微信客服入口见下方“[不想本地安装？直接使用链邻科研 AI 平台](#lianlin-platform)”。

### 第 2 步：用一个完整请求启动任务

一个好请求应包含五个要素：**研究目标、已有材料、任务范围、期望产出、质量要求**。可以直接复制下面的通用模板：

> 请从 LL-AcademicSkillsHub 中选择最合适的技能或技能组合。我的研究目标是【要解决的问题】；已有材料是【论文、数据、代码、图片、协议或草稿】；任务范围是【研究对象、时间、语言、方法、期刊或排除条件】；请输出【表格、报告、代码、图件、文稿或审计清单】；要求保留证据来源和关键参数，区分事实、推断与不确定性，不补造缺失信息，并列出需要我确认的事项。

材料不完整也可以开始。请明确告诉 Agent“先检查输入是否充分”，让它先返回缺失项、风险与建议步骤，再决定是否执行。

### 第 3 步：按科研全流程找到入口

| 科研阶段 | 先从这些分类开始 | 能完成什么 |
|---|---|---|
| 选题与立项 | [学术核心能力](#category-academic-core) · [研究方法与科学思维](#category-research-methods) | 分析趋势与缺口、形成研究问题、提出假设、评估创新性与可行性 |
| 检索与证据获取 | [论文检索与文献管理](#category-literature-management) · [科学数据库](#category-scientific-databases) | 构造检索式、跨库搜索、去重筛选、获取元数据与合法全文 |
| 精读与知识整理 | [学术核心能力](#category-academic-core) · [文档处理与数据工具](#category-document-data-tools) | 解析 PDF 和文档、双语精读、定位证据、建立论文阅读卡与证据矩阵 |
| 研究设计与实验执行 | [研究方法与科学思维](#category-research-methods) · [实验室自动化与集成](#category-lab-automation) · [平台与基础设施](#category-platform-infrastructure) | 设计方案、识别偏倚、编写协议、连接实验流程、配置计算资源 |
| 数据处理与建模 | [数据分析与统计建模](#category-data-analysis-statistics) · [机器学习与人工智能](#category-machine-learning-ai) | 清理数据、统计推断、训练模型、诊断误差、解释结果与保存复现记录 |
| 论文写作与投稿 | [科学写作与学术交流](#category-scientific-communication) · [文档处理与数据工具](#category-document-data-tools) | 起草论文、基金与报告，润色语言，套用模板，生成投稿文件 |
| 图表与成果展示 | [学术演示与可视化](#category-presentation-visualization) | 制作论文图、机制图、海报、幻灯片与可编辑视觉材料 |
| 审稿、修订与治理 | [学术核心能力](#category-academic-core) · [科学写作与学术交流](#category-scientific-communication) | 模拟审稿、逐条回复、审计引用、检查数据可用性与成果合规边界 |

### 第 4 步：按专业研究领域进入

| 研究方向 | 相关分类 | 常见任务 |
|---|---|---|
| 生命科学与医学 | [生物信息与基因组学](#category-bioinformatics-genomics) · [临床医学与精准医疗](#category-clinical-precision-medicine) · [蛋白质工程与结构生物学](#category-protein-structural-biology) | 序列与组学分析、单细胞、医学影像、临床证据、蛋白结构与功能 |
| 化学、药物与材料 | [化学信息与药物发现](#category-cheminformatics-drug-discovery) · [材料科学与物理计算](#category-materials-physics) | 分子处理、性质预测、虚拟筛选、结构设计、材料模拟与物理计算 |
| 金融、经济与空间研究 | [金融与经济数据](#category-finance-economics) · [地理空间与遥感](#category-geospatial-remote-sensing) | 市场和宏观数据、企业研究、GIS、遥感影像与空间分析 |
| 跨学科计算研究 | [科学数据库](#category-scientific-databases) · [数据分析与统计建模](#category-data-analysis-statistics) · [机器学习与人工智能](#category-machine-learning-ai) · [平台与基础设施](#category-platform-infrastructure) | 数据采集、规范化、统计与 AI 建模、云端计算和任务编排 |

### 第 5 步：复制一个真实任务开始

| 想做什么 | 可以直接这样说 |
|---|---|
| 分析研究选题 | “围绕【研究方向】检索近五年代表性研究，区分热点、已解决问题和真实证据缺口，提出 3 个可执行选题，并从创新性、数据、方法、伦理和资源方面评分。” |
| 做可复现文献检索 | “把【研究问题】拆成概念块与同义词，为【目标数据库】设计可复现检索式，记录日期、过滤条件和命中数，去重后按【纳排标准】输出筛选表。” |
| 精读中英文论文 | “逐篇精读这些 PDF，建立中英文术语表，按研究问题、方法、样本、结果、限制抽取证据；每项关键结论标注页码、图表或章节位置。” |
| 做系统综述或证据表 | “基于这批论文建立证据矩阵，比较研究设计、样本、变量、方法、主要结果和偏倚风险；不要把作者主张与论文实际证据混在一起。” |
| 设计研究方案 | “根据【研究问题和已有证据】提出研究设计，写清假设、分析单位、采样、对照、测量、排除、缺失处理、主要终点和可复现计划，并列出需要伦理审查的部分。” |
| 分析科研数据 | “先检查这份数据的变量、缺失、异常、分布和采集质量，再选择合适的统计方法；输出可运行代码、效应量、不确定性、模型诊断和敏感性分析。” |
| 做专业领域分析 | “这是【序列、临床、分子、材料、金融或空间】数据。请先确认数据版本、单位、参考体系和适用方法，再选择相应领域技能完成分析，并给出验证方案。” |
| 写论文段落或全文 | “根据这些证据、结果和图表起草【摘要、引言、方法、结果或讨论】；保持事实、数字和引用不变，区分结果与解释，并标出证据不足的位置。” |
| 制作论文图和汇报 | “根据这些数据和结论设计投稿级多面板图，同时生成可编辑源文件、图注和数据映射；再将核心证据整理成一份组会汇报。” |
| 模拟审稿 | “从研究问题、创新性、方法、统计、图表、报告完整性和可复现性审查这篇稿件，按主要问题、次要问题和可执行修改建议输出审稿报告。” |
| 审计引用与参考文献 | “核对正文引文与参考文献的一致性，检查 DOI、作者、期刊、年份和页码；把结果分为已核验、部分匹配、冲突和无法核验，不要补造字段。” |
| 回复审稿意见 | “把审稿意见逐条拆解，关联到原稿位置和修改证据，起草礼貌、明确、可核查的回复；无法接受的建议请给出有证据的解释，并列出仍需作者决定的问题。” |

### 第 6 步：需要时组合多个技能

复杂科研任务通常不是调用一个技能，而是让多个技能按产物交接：

- **从选题到论文：**选题分析 → 可复现检索 → 全文精读 → 研究设计 → 数据分析 → 科研图表 → 论文写作 → 引用审计。
- **系统综述：**检索策略 → 去重筛选 → 全文证据抽取 → 偏倚评价 → 统计综合 → PRISMA 流程与综述写作。
- **数据论文：**数据与变量审计 → 领域分析 → 统计或机器学习 → 可视化 → 方法与结果写作 → 数据可用性说明。
- **投稿与返修：**期刊模板 → 投稿前审计 → 模拟审稿 → 修改稿 → 逐条回复 → 引用、图表和附件复核。

可以直接说：“请先给出技能编排顺序、每一步的输入输出和人工确认点，等我提供材料后分阶段执行。” 分阶段检查比一次生成全部结果更容易发现证据缺口和方法错误。
"""


def en_quick_start() -> str:
    """Render the English counterpart of the task-first onboarding guide."""
    return """## Quick start

You do not need to memorize 187 skill names. The easiest way to begin is to **state your research goal and available materials, then let your local Agent select the right skill or skill sequence from the catalog.** If you already know a skill name, mention it directly.

### Step 1: Choose how to use the project

#### Option A: Run it locally

From the repository root:

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

Open `http://127.0.0.1:8765/` to search categories, skills, and functions. Windows users may also run `scripts\\setup.bat` and `scripts\\start.bat`; see the [local deployment guide](./docs/deployment.en.md) for other systems and environment checks.

After finding a skill, open its detailed guide and check its use cases, required materials, workflow, outputs, references, and boundaries before connecting the skill directory to your local Agent Skill environment.

#### Option B: Use Lianlin Research AI Platform

If you do not want to install skills, configure dependencies, or debug the environment one by one, use the integrated Lianlin Research AI Platform. The download and WeChat support entry is in “[Don't want to install locally? Use Lianlin Research AI Platform](#lianlin-platform)”.

### Step 2: Start with one complete request

A useful request has five parts: **research goal, available materials, task scope, expected output, and quality requirements**. Copy and adapt this template:

> Select the most suitable skill or skill sequence from LL-AcademicSkillsHub. My research goal is [the question to solve]. My available materials are [papers, data, code, images, protocols, or drafts]. The scope is [population, time range, language, method, target journal, or exclusions]. Produce [a table, report, code, figure, manuscript, or audit checklist]. Preserve evidence sources and key parameters, distinguish facts from inferences and uncertainty, do not invent missing information, and list the decisions that require my confirmation.

Incomplete materials are acceptable. Ask the Agent to check input sufficiency first and return missing items, risks, and a proposed plan before execution.

### Step 3: Enter through the research workflow

| Research stage | Start with these categories | Typical outcome |
|---|---|---|
| Topic selection and planning | Academic Core · Research Methods & Scientific Reasoning | Map trends and gaps, form research questions, propose hypotheses, and assess novelty and feasibility |
| Search and evidence acquisition | Literature Search & Management · Scientific Databases | Build queries, search across databases, deduplicate and screen records, and acquire metadata or lawful full text |
| Close reading and knowledge organization | Academic Core · Document Processing & Data Tools | Parse PDFs and documents, perform bilingual close reading, locate evidence, and create reading cards or evidence matrices |
| Study design and experiment execution | Research Methods & Scientific Reasoning · Laboratory Automation & Integration · Platform & Infrastructure | Design studies, identify bias, draft protocols, connect laboratory workflows, and configure compute resources |
| Data processing and modeling | Data Analysis & Statistical Modeling · Machine Learning & AI | Clean data, perform inference, train models, diagnose errors, interpret results, and preserve reproducibility records |
| Manuscript writing and submission | Scientific Writing & Communication · Document Processing & Data Tools | Draft papers, grants, and reports; improve language; apply templates; and prepare submission files |
| Figures and research communication | Academic Presentation & Visualization | Create paper figures, mechanism diagrams, posters, slide decks, and editable visual assets |
| Review, revision, and governance | Academic Core · Scientific Writing & Communication | Simulate peer review, prepare point-by-point responses, audit citations, and check data-availability or compliance boundaries |

### Step 4: Enter through your research domain

| Research domain | Relevant categories | Common work |
|---|---|---|
| Life science and medicine | Bioinformatics & Genomics · Clinical & Precision Medicine · Protein Engineering & Structural Biology | Sequence and omics analysis, single-cell workflows, medical imaging, clinical evidence, and protein structure or function |
| Chemistry, drug discovery, and materials | Cheminformatics & Drug Discovery · Materials Science & Computational Physics | Molecular processing, property prediction, virtual screening, structure design, materials simulation, and physics computation |
| Finance, economics, and spatial research | Finance & Economics Data · Geospatial & Remote Sensing | Market and macroeconomic data, company research, GIS, remote-sensing imagery, and spatial analysis |
| Cross-disciplinary computational research | Scientific Databases · Data Analysis & Statistical Modeling · Machine Learning & AI · Platform & Infrastructure | Data acquisition, normalization, statistical or AI modeling, cloud computing, and workflow orchestration |

### Step 5: Copy a real task to begin

| Goal | Example request |
|---|---|
| Analyze a research topic | “Search representative work from the past five years on [topic], separate active trends, solved problems, and evidence-backed gaps, then propose three feasible topics scored for novelty, data, methods, ethics, and resources.” |
| Run a reproducible literature search | “Split [research question] into concept blocks and synonyms, build reproducible queries for [databases], record dates, filters, and hit counts, deduplicate the results, and screen them with [criteria].” |
| Read Chinese and English papers closely | “Read these PDFs and build a bilingual terminology list. Extract the question, methods, sample, results, and limitations, and attach a page, figure, table, or section locator to every key claim.” |
| Build a systematic-review evidence table | “Create an evidence matrix for these papers, comparing design, sample, variables, methods, results, and risk of bias. Keep author claims separate from evidence demonstrated in the paper.” |
| Design a study | “Using [question and existing evidence], specify hypotheses, units of analysis, sampling, controls, measurements, exclusions, missing-data handling, primary outcomes, reproducibility plan, and any ethics-review requirements.” |
| Analyze research data | “Audit variables, missingness, outliers, distributions, and collection quality first. Then choose suitable statistical methods and return runnable code, effect sizes, uncertainty, diagnostics, and sensitivity analyses.” |
| Perform domain-specific analysis | “This is [sequence, clinical, molecular, materials, finance, or spatial] data. Confirm versions, units, reference systems, and method suitability before selecting the relevant domain skills and proposing validation.” |
| Draft a paper section or manuscript | “Draft the [abstract, introduction, methods, results, or discussion] from these sources, results, and figures. Preserve facts, numbers, and citations; separate results from interpretation; flag unsupported statements.” |
| Create figures and a presentation | “Design a submission-ready multi-panel figure from these data and conclusions, with editable source files, captions, and data mappings; then turn the central evidence into a lab-meeting deck.” |
| Simulate peer review | “Review this manuscript for the question, novelty, methods, statistics, figures, reporting completeness, and reproducibility. Return major issues, minor issues, and actionable revisions.” |
| Audit citations and references | “Check consistency between in-text citations and references, then verify DOI, authors, journal, year, and pages. Classify each item as verified, partial match, conflict, or unverifiable; do not invent fields.” |
| Respond to reviewers | “Decompose every reviewer comment, map it to manuscript locations and revision evidence, and draft a courteous, specific, verifiable response. Explain any declined request with evidence and list decisions still requiring the authors.” |

### Step 6: Combine skills when the task is complex

Complex research usually requires skills to hand off explicit artifacts:

- **Topic to paper:** topic analysis → reproducible search → full-text close reading → study design → data analysis → scientific figures → manuscript writing → citation audit.
- **Systematic review:** search strategy → deduplication and screening → evidence extraction → bias assessment → statistical synthesis → PRISMA flow and review writing.
- **Data paper:** data and variable audit → domain analysis → statistics or machine learning → visualization → methods and results writing → data-availability statement.
- **Submission and revision:** journal template → pre-submission audit → simulated peer review → revised manuscript → point-by-point response → citation, figure, and supplement checks.

You can say: “First propose the skill sequence, the input and output of each step, and the human checkpoints; execute it in stages after I provide the materials.” Staged review makes evidence gaps and methodological errors easier to detect than one-shot generation.
"""


def readme(lang: str, payload: dict, showcase_descriptions: dict[str, str] | None = None) -> str:
    zh = lang == "zh-CN"
    summary = payload["summary"]
    if zh:
        showcase = zh_skill_showcase(
            payload["categories"],
            payload["skills"],
            showcase_descriptions or {},
        )
        quick_start = zh_quick_start()
        return f"""<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub 链邻学术技能仓库" width="100%">
</p>

<p align="center">
  <strong>本地优先、中英双语、分级审计的学术 AI 技能仓库</strong><br>
  <a href="./README.en.md">English</a> ·
  <a href="./docs/skills.zh-CN.md">全部技能</a> ·
  <a href="./docs/deployment.zh-CN.md">本地部署</a> ·
  <a href="./docs/quality-model.zh-CN.md">质量模型</a> ·
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/actions">质量流水线</a>
</p>

# 链邻学术技能仓库

LL-AcademicSkillsHub 将科研技能按任务体系，分门别类全流程完成科研论文创作，共**{summary['skillCount']} 项技能**、**{summary['categoryCount']} 个类别**。

## 你可以做什么

- 从[全部技能与功能目录](./docs/skills.zh-CN.md)按科研任务找到合适能力；
- 查看每项技能的输入、输出、环境、网络、凭据、风险、来源与质量状态；
- 在 Windows、macOS 或 Linux 上使用 Python 标准库启动本地可搜索站点；
- 不想逐项配置技能时，选择链邻科研 AI 平台的一体化使用方式。

{quick_start}
<a id="lianlin-platform"></a>

## 不想本地安装？直接使用链邻科研 AI 平台

<p align="center">
  <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="下载链邻科研 AI 平台或添加微信客服" width="100%">
</p>

{showcase}

## 品牌与推广边界

链邻科研 AI 平台只在 README、文档站、下载页和发行说明等明确位置介绍，不作为“每次自动运行”的技能，不打断正常科研流程。官方下载地址尚未提供时，页面显示真实的“待配置”状态，不伪造链接或二维码。

## 质量与来源

`cataloged → beta → tested → verified → gold` 是逐级证据状态；收录不等于验证。第三方固定包保留上游指令，并单独标注来源与许可证复核状态。详见 [质量模型](./docs/quality-model.zh-CN.md)、[第三方声明](./THIRD_PARTY_NOTICES.md)与生成的[审计报告](./reports/audit.zh-CN.md)。

## 许可证

链邻原创代码与文档采用 Apache-2.0。第三方技能继续适用其上游条款，不能因进入本仓库而被自动视为 Apache-2.0。
"""
    quick_start = en_quick_start()
    return f"""<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub" width="100%">
</p>

<p align="center">
  <strong>Local-first, bilingual, and evidence-tiered academic AI skills</strong><br>
  <a href="./README.md">中文</a> ·
  <a href="./docs/skills.en.md">All skills</a> ·
  <a href="./docs/deployment.en.md">Local setup</a> ·
  <a href="./docs/quality-model.en.md">Quality model</a> ·
  <a href="https://github.com/ss8875/LL-AcademicSkillsHub/actions">Quality workflow</a>
</p>

# LL-AcademicSkillsHub

LL-AcademicSkillsHub organizes research skills into a searchable, installable, and auditable bilingual catalog. The first release contains **{summary['skillCount']} skills** across **{summary['categoryCount']} categories**: **{summary['firstPartyCount']} Lianlin first-party core skills** and **{summary['thirdPartyCount']} pinned third-party skills**.

## What you can do

- Find capabilities by research task in the [complete skill and function catalog](./docs/skills.en.md).
- Inspect inputs, outputs, runtime, network, credentials, risk, source, and quality status.
- Run the searchable local site on Windows, macOS, or Linux using only the Python standard library.
- Choose the integrated Lianlin Research AI Platform route if individual skill setup is inconvenient.

{quick_start}
<a id="lianlin-platform"></a>

## Don't want to install locally? Use Lianlin Research AI Platform

<p align="center">
  <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="Download Lianlin Research AI Platform or contact WeChat support" width="100%">
</p>

## Brand and promotion boundary

Lianlin Research AI Platform appears only on explicit surfaces such as the README, documentation site, download page, and release notes. It is not an always-running skill and never interrupts research workflows. Until an official URL is supplied, the site states that it is unconfigured instead of inventing a link or QR code.

## Quality and provenance

`cataloged → beta → tested → verified → gold` are evidence levels; inclusion is not verification. Pinned third-party instructions remain upstream work and carry separate provenance and license-review status. See the [quality model](./docs/quality-model.en.md), [third-party notices](./THIRD_PARTY_NOTICES.md), and generated [audit report](./reports/audit.en.md).

## License

Lianlin first-party code and original documentation are Apache-2.0. Third-party skills remain under their upstream terms and do not become Apache-2.0 merely by inclusion.
"""


def main() -> None:
    categories = load_json(ROOT / "catalog" / "categories.seed.json")
    skills = load_json(ROOT / "catalog" / "skills.seed.json")
    showcase_descriptions = load_json(
        ROOT / "catalog" / "showcase-descriptions.zh-CN.json"
    )["descriptions"]
    payload = catalog_payload(categories, skills)
    write_json(ROOT / "catalog" / "categories.json", categories)
    write_json(ROOT / "catalog" / "skills.json", skills)
    write_json(ROOT / "site" / "data" / "catalog.json", payload)
    platform_url = env_value("LIANLIN_PLATFORM_DOWNLOAD_URL")
    if platform_url and not re.fullmatch(r"https://[^\s]+", platform_url):
        raise SystemExit("LIANLIN_PLATFORM_DOWNLOAD_URL must be blank or an https:// URL")
    write_json(ROOT / "site" / "config.json", {"platformDownloadUrl": platform_url or None})
    guide_summary = build_all_skill_guides(categories, skills, showcase_descriptions)
    (ROOT / "docs" / "skills.zh-CN.md").write_text(skills_markdown(categories, skills, "zh-CN"), encoding="utf-8")
    (ROOT / "docs" / "skills.en.md").write_text(skills_markdown(categories, skills, "en"), encoding="utf-8")
    (ROOT / "docs" / "categories.zh-CN.md").write_text(categories_markdown(categories, skills, "zh-CN"), encoding="utf-8")
    (ROOT / "docs" / "categories.en.md").write_text(categories_markdown(categories, skills, "en"), encoding="utf-8")
    (ROOT / "README.md").write_text(
        readme("zh-CN", payload, showcase_descriptions),
        encoding="utf-8",
    )
    (ROOT / "README.en.md").write_text(readme("en", payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "builtOn": date.today().isoformat(),
                **payload["summary"],
                **guide_summary,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
