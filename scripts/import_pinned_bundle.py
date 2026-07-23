#!/usr/bin/env python3
"""Import the pinned academic-skill snapshot and create Lianlin first-party skills.

The importer is deterministic and intentionally does not depend on the malformed
legacy display catalog. Source SKILL.md files are preserved byte-for-byte.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CATEGORIES_FILE = PROJECT_ROOT / "catalog" / "categories.seed.json"
CORE_SOURCE_DIR_NAMES = {"沁言学术skills", "qinyan-academic-skills"}
CORE_RENAMES = {
    "qinyan-topic-analysis": "ll-topic-analysis",
    "qinyan-paper-search": "ll-paper-search",
    "qinyan-paper-analysis": "ll-paper-analysis",
    "qinyan-paper-polish": "ll-paper-polish",
    "qinyan-citation": "ll-citation-audit",
}
DISALLOWED_IDS = {"offer-k-dense-web"}

CATEGORY_PROFILE = {
    "literature-management": {
        "cap_zh": ["检索与筛选学术文献", "整理元数据与引用信息", "保存可复核的检索证据"],
        "cap_en": ["Search and screen scholarly literature", "Organize metadata and citations", "Preserve auditable search evidence"],
        "inputs_zh": ["研究问题、关键词、检索限制"], "inputs_en": ["Research question, keywords, and search limits"],
        "outputs_zh": ["文献记录、筛选结果或引用数据"], "outputs_en": ["Literature records, screening results, or citation data"],
    },
    "scientific-communication": {
        "cap_zh": ["组织学术论证", "改善科学表达", "按受众和体裁调整内容"],
        "cap_en": ["Structure academic arguments", "Improve scientific expression", "Adapt content to audience and genre"],
        "inputs_zh": ["研究材料、目标体裁、读者要求"], "inputs_en": ["Research material, target genre, and audience requirements"],
        "outputs_zh": ["学术文本或交流材料"], "outputs_en": ["Academic text or communication material"],
    },
    "presentation-visualization": {
        "cap_zh": ["设计学术图表与版式", "把数据转化为可读视觉", "输出演示或出版素材"],
        "cap_en": ["Design scholarly figures and layouts", "Turn data into readable visuals", "Produce presentation or publication assets"],
        "inputs_zh": ["数据、论点、目标媒介"], "inputs_en": ["Data, message, and target medium"],
        "outputs_zh": ["图表、海报、幻灯片或图形文件"], "outputs_en": ["Charts, posters, slides, or graphic files"],
    },
    "research-methods": {
        "cap_zh": ["明确研究问题与假设", "设计可复现研究流程", "识别偏倚、限制与核验点"],
        "cap_en": ["Clarify questions and hypotheses", "Design reproducible research workflows", "Identify bias, limitations, and validation points"],
        "inputs_zh": ["研究问题、数据条件、方法约束"], "inputs_en": ["Research question, data conditions, and methodological constraints"],
        "outputs_zh": ["研究设计、分析计划或方法评估"], "outputs_en": ["Study design, analysis plan, or methodological assessment"],
    },
    "bioinformatics-genomics": {
        "cap_zh": ["处理生物序列与组学数据", "调用领域数据库和分析工具", "形成可复现生信结果"],
        "cap_en": ["Process sequences and omics data", "Use domain databases and analysis tools", "Produce reproducible bioinformatics results"],
        "inputs_zh": ["序列、组学数据或样本元数据"], "inputs_en": ["Sequences, omics data, or sample metadata"],
        "outputs_zh": ["分析表、图形、注释或模型结果"], "outputs_en": ["Analysis tables, figures, annotations, or model results"],
    },
    "cheminformatics-drug-discovery": {
        "cap_zh": ["分析化学结构与性质", "查询化学和药物数据库", "支持候选物筛选与评估"],
        "cap_en": ["Analyze chemical structures and properties", "Query chemistry and drug databases", "Support candidate screening and assessment"],
        "inputs_zh": ["分子结构、化合物标识或筛选条件"], "inputs_en": ["Molecular structures, compound identifiers, or screening criteria"],
        "outputs_zh": ["结构数据、性质预测或候选清单"], "outputs_en": ["Structure data, property predictions, or candidate lists"],
    },
    "clinical-precision-medicine": {
        "cap_zh": ["整理临床与精准医学证据", "处理受控医学数据", "标注适用边界与风险"],
        "cap_en": ["Organize clinical and precision-medicine evidence", "Handle controlled medical data", "State applicability limits and risks"],
        "inputs_zh": ["临床问题、医学数据或证据资料"], "inputs_en": ["Clinical question, medical data, or evidence material"],
        "outputs_zh": ["证据摘要、分析结果或结构化记录"], "outputs_en": ["Evidence summaries, analysis results, or structured records"],
    },
    "protein-structural-biology": {
        "cap_zh": ["分析蛋白序列与结构", "运行结构生物学工作流", "评估设计结果与不确定性"],
        "cap_en": ["Analyze protein sequences and structures", "Run structural-biology workflows", "Assess design results and uncertainty"],
        "inputs_zh": ["蛋白序列、结构或设计目标"], "inputs_en": ["Protein sequences, structures, or design goals"],
        "outputs_zh": ["结构、评分、注释或设计候选"], "outputs_en": ["Structures, scores, annotations, or design candidates"],
    },
    "machine-learning-ai": {
        "cap_zh": ["准备数据与建模流程", "训练或调用机器学习模型", "评估性能、偏差与复现条件"],
        "cap_en": ["Prepare data and modeling workflows", "Train or invoke machine-learning models", "Evaluate performance, bias, and reproducibility"],
        "inputs_zh": ["数据、任务定义与计算约束"], "inputs_en": ["Data, task definition, and compute constraints"],
        "outputs_zh": ["模型、预测、指标或实验记录"], "outputs_en": ["Models, predictions, metrics, or experiment records"],
    },
    "materials-physics": {
        "cap_zh": ["执行材料与物理计算", "组织模拟输入和参数", "解析结果并记录计算条件"],
        "cap_en": ["Run materials and physics computations", "Organize simulation inputs and parameters", "Interpret results and record compute conditions"],
        "inputs_zh": ["结构、参数或物理模型"], "inputs_en": ["Structures, parameters, or physical models"],
        "outputs_zh": ["模拟结果、性质数据或分析报告"], "outputs_en": ["Simulation results, property data, or analysis reports"],
    },
    "data-analysis-statistics": {
        "cap_zh": ["清理与验证研究数据", "实施统计分析和建模", "报告效应、不确定性与限制"],
        "cap_en": ["Clean and validate research data", "Perform statistical analysis and modeling", "Report effects, uncertainty, and limitations"],
        "inputs_zh": ["结构化数据、分析问题与统计假设"], "inputs_en": ["Structured data, analytical question, and statistical assumptions"],
        "outputs_zh": ["分析表、模型、图形或可复现报告"], "outputs_en": ["Analysis tables, models, figures, or reproducible reports"],
    },
    "scientific-databases": {
        "cap_zh": ["查询领域科学数据库", "解析并规范化返回记录", "保留来源、版本与查询条件"],
        "cap_en": ["Query domain scientific databases", "Parse and normalize returned records", "Retain source, version, and query conditions"],
        "inputs_zh": ["标识符、关键词或数据库查询"], "inputs_en": ["Identifiers, keywords, or database queries"],
        "outputs_zh": ["结构化数据库记录与来源信息"], "outputs_en": ["Structured database records and provenance"],
    },
    "lab-automation": {
        "cap_zh": ["规划实验自动化步骤", "连接仪器、协议或实验数据", "记录执行状态与故障边界"],
        "cap_en": ["Plan laboratory automation steps", "Connect instruments, protocols, or experiment data", "Record execution state and failure boundaries"],
        "inputs_zh": ["实验协议、仪器参数或样本计划"], "inputs_en": ["Protocols, instrument parameters, or sample plans"],
        "outputs_zh": ["自动化流程、运行记录或实验产物"], "outputs_en": ["Automation workflows, run logs, or experiment artifacts"],
    },
    "document-data-tools": {
        "cap_zh": ["读取与转换科研文档", "提取结构化内容", "保持版式、字段与来源可追溯"],
        "cap_en": ["Read and transform research documents", "Extract structured content", "Preserve layout, fields, and provenance"],
        "inputs_zh": ["文档、表格或数据文件"], "inputs_en": ["Documents, spreadsheets, or data files"],
        "outputs_zh": ["转换文件、结构化数据或校验报告"], "outputs_en": ["Converted files, structured data, or validation reports"],
    },
    "finance-economics": {
        "cap_zh": ["查询金融与宏观经济数据", "规范时间序列和指标定义", "完成可复核分析"],
        "cap_en": ["Query financial and macroeconomic data", "Normalize time series and metric definitions", "Perform auditable analysis"],
        "inputs_zh": ["指标、市场、时间范围或数据集"], "inputs_en": ["Metrics, markets, time ranges, or datasets"],
        "outputs_zh": ["时间序列、指标表或分析结果"], "outputs_en": ["Time series, metric tables, or analysis results"],
    },
    "geospatial-remote-sensing": {
        "cap_zh": ["处理空间与遥感数据", "执行坐标、栅格和矢量分析", "输出地图与空间统计结果"],
        "cap_en": ["Process geospatial and remote-sensing data", "Perform coordinate, raster, and vector analysis", "Produce maps and spatial statistics"],
        "inputs_zh": ["空间数据、影像、坐标系与分析范围"], "inputs_en": ["Spatial data, imagery, coordinate system, and area of interest"],
        "outputs_zh": ["地图、空间数据集或统计结果"], "outputs_en": ["Maps, spatial datasets, or statistical results"],
    },
    "platform-infrastructure": {
        "cap_zh": ["检查运行资源与依赖", "组织计算和平台配置", "记录环境限制与可复现条件"],
        "cap_en": ["Inspect runtime resources and dependencies", "Organize compute and platform configuration", "Record environment limits and reproducibility conditions"],
        "inputs_zh": ["运行目标、资源需求与环境信息"], "inputs_en": ["Execution goal, resource needs, and environment information"],
        "outputs_zh": ["环境报告、部署配置或运行结果"], "outputs_en": ["Environment reports, deployment configuration, or run results"],
    },
}

FIRST_PARTY = [
    {
        "id": "ll-topic-analysis", "title_zh": "链邻学术选题分析", "title_en": "Lianlin Research Topic Analysis",
        "summary_zh": "以可追溯文献证据评估研究趋势、缺口、创新性、理论价值、实践价值与可行性。",
        "summary_en": "Evaluate trends, gaps, novelty, theoretical value, practical value, and feasibility with traceable literature evidence.",
        "workflow_zh": ["明确研究对象、范围、时间窗与判定标准", "构造多组同义词和排除词并记录检索式", "建立代表性文献与近年文献证据表", "区分“尚未发现”与“证据证明不存在”", "按新颖性、价值、数据、方法、伦理和资源评分", "输出候选题目、证据、不确定性与下一步验证"],
        "workflow_en": ["Define the object, scope, time window, and decision criteria", "Build synonym and exclusion sets and record queries", "Create an evidence table of foundational and recent work", "Distinguish not found from proven absent", "Score novelty, value, data, methods, ethics, and resources", "Report candidate topics, evidence, uncertainty, and next validation"],
        "inputs_zh": ["研究方向、学科边界、资源与时间约束"], "inputs_en": ["Research direction, disciplinary boundary, resources, and time constraints"],
        "outputs_zh": ["选题评分矩阵、证据表、风险与验证计划"], "outputs_en": ["Topic scorecard, evidence table, risks, and validation plan"],
    },
    {
        "id": "ll-paper-search", "title_zh": "链邻可复现论文检索", "title_en": "Lianlin Reproducible Paper Search",
        "summary_zh": "设计并执行可复现的多来源论文检索、去重、筛选与证据留存流程。",
        "summary_en": "Design and execute reproducible multi-source paper search, deduplication, screening, and evidence capture.",
        "workflow_zh": ["把研究问题拆为概念块与同义词", "选择适配学科的数据库并注明覆盖差异", "保存完整检索式、日期、过滤条件与命中数", "按 DOI、标题、作者和年份分层去重", "以预先定义的纳排标准筛选", "输出 PRISMA 风格流转统计与可复现查询记录"],
        "workflow_en": ["Decompose the question into concept blocks and synonyms", "Choose discipline-appropriate databases and state coverage differences", "Save exact queries, dates, filters, and hit counts", "Deduplicate by DOI, title, author, and year", "Screen with predefined criteria", "Export PRISMA-style flow counts and reproducible query records"],
        "inputs_zh": ["研究问题、数据库范围、纳排标准、日期范围"], "inputs_en": ["Research question, database scope, eligibility criteria, and date range"],
        "outputs_zh": ["检索日志、去重文献集、筛选表与流程统计"], "outputs_en": ["Search log, deduplicated corpus, screening table, and flow counts"],
    },
    {
        "id": "ll-paper-analysis", "title_zh": "链邻论文证据分析", "title_en": "Lianlin Paper Evidence Analysis",
        "summary_zh": "从研究问题、理论、方法、数据、结果、创新与限制形成可追溯的论文阅读卡。",
        "summary_en": "Build a traceable paper evidence card spanning question, theory, methods, data, results, novelty, and limitations.",
        "workflow_zh": ["记录论文身份、版本与获取方式", "分离作者陈述、论文证据与分析者推断", "抽取研究设计、样本、变量、方法和主要结果", "将每项关键结论定位到页码、图表或章节", "评估内部效度、外部效度、统计与报告风险", "生成一页阅读卡和跨论文可比较字段"],
        "workflow_en": ["Record paper identity, version, and acquisition route", "Separate author claims, paper evidence, and analyst inference", "Extract design, sample, variables, methods, and main results", "Anchor each key claim to a page, figure, table, or section", "Assess internal, external, statistical, and reporting validity", "Produce a one-page evidence card with cross-paper fields"],
        "inputs_zh": ["论文全文或合法可用文本、分析问题"], "inputs_en": ["Full paper or lawfully available text and analysis question"],
        "outputs_zh": ["带定位证据的论文阅读卡与质量评估"], "outputs_en": ["Paper evidence card with anchors and quality appraisal"],
    },
    {
        "id": "ll-paper-polish", "title_zh": "链邻学术论文润色", "title_en": "Lianlin Academic Manuscript Polish",
        "summary_zh": "在不改变事实、数据和学术含义的前提下优化逻辑、术语、语气、衔接与语言表达。",
        "summary_en": "Improve logic, terminology, tone, cohesion, and language without changing facts, data, or scholarly meaning.",
        "workflow_zh": ["确认期刊、读者、语言变体与允许改动范围", "锁定数字、单位、引文、专名和关键结论", "先处理论证结构与段落功能，再处理句子", "标注可能改变含义或需要作者确认的修改", "核对术语一致性、时态、语态与缩写", "输出修订稿、修改说明和待确认问题"],
        "workflow_en": ["Confirm journal, audience, language variant, and allowed edit scope", "Lock numbers, units, citations, proper nouns, and key conclusions", "Edit argument and paragraph function before sentences", "Flag edits that may alter meaning or need author confirmation", "Check terminology, tense, voice, and abbreviations", "Return revised text, change notes, and author queries"],
        "inputs_zh": ["原稿、目标期刊要求、术语表与禁止改动项"], "inputs_en": ["Draft, target journal requirements, terminology list, and locked content"],
        "outputs_zh": ["修订稿、差异说明与作者问题清单"], "outputs_en": ["Revised draft, change rationale, and author query list"],
    },
    {
        "id": "ll-citation-audit", "title_zh": "链邻学术引用审计", "title_en": "Lianlin Scholarly Citation Audit",
        "summary_zh": "核验 DOI、作者、期刊、年份、卷期页码及正文引文与参考文献的一致性。",
        "summary_en": "Verify DOI, authors, venue, year, volume, issue, pages, and consistency between in-text citations and references.",
        "workflow_zh": ["解析正文引文与参考文献列表", "按 DOI、题名和作者匹配权威元数据", "区分已核验、部分匹配、冲突和无法核验", "检查漏引、多引、重复、顺序及格式规则", "不为无法确认的条目补造字段", "输出逐条审计表、修复建议和未决项"],
        "workflow_en": ["Parse in-text citations and the reference list", "Match authoritative metadata by DOI, title, and author", "Classify verified, partial, conflicting, and unresolved records", "Check missing, orphaned, duplicate, ordering, and style issues", "Never fabricate fields for unresolved records", "Return a per-item audit table, fixes, and open questions"],
        "inputs_zh": ["正文、参考文献、目标引用格式"], "inputs_en": ["Manuscript, reference list, and target citation style"],
        "outputs_zh": ["引用审计表、修复后的参考文献与未核验清单"], "outputs_en": ["Citation audit table, corrected references, and unresolved list"],
    },
    {
        "id": "ll-bilingual-evidence-reader", "title_zh": "链邻双语全文证据精读", "title_en": "Lianlin Bilingual Full-Text Evidence Reader",
        "summary_zh": "跨中英文全文进行术语对齐、逐项证据定位、方法比较与不确定性标注。",
        "summary_en": "Align terminology across Chinese and English full texts, anchor evidence, compare methods, and label uncertainty.",
        "workflow_zh": ["确认文本版本、语言和可用范围", "建立中英文术语对照表并保留原词", "按问题、方法、数据、结果和限制抽取证据", "为事实与引文记录页码或结构定位", "区分直译、意译、领域约定与不可等价术语", "输出双语证据矩阵和差异说明"],
        "workflow_en": ["Confirm text versions, languages, and available scope", "Build a bilingual terminology map retaining source terms", "Extract evidence for questions, methods, data, results, and limits", "Record page or structural anchors for facts and quotations", "Separate literal, contextual, conventional, and non-equivalent terms", "Produce a bilingual evidence matrix and discrepancy notes"],
        "inputs_zh": ["中英文论文全文或合法节选、研究问题"], "inputs_en": ["Chinese and English full texts or lawful excerpts and a research question"],
        "outputs_zh": ["双语术语表、证据矩阵与差异报告"], "outputs_en": ["Bilingual glossary, evidence matrix, and discrepancy report"],
    },
    {
        "id": "ll-lawful-fulltext-acquisition", "title_zh": "链邻合法全文获取", "title_en": "Lianlin Lawful Full-Text Acquisition",
        "summary_zh": "通过开放获取、机构权限、作者存档与馆际服务等合规路径定位论文全文。",
        "summary_en": "Locate paper full text through compliant routes such as open access, institutional access, author deposits, and library services.",
        "workflow_zh": ["规范 DOI、题名、作者和版本信息", "优先检索出版社开放版本和可信开放仓储", "区分已发表版、作者接收稿、预印本和补充材料", "记录许可证、访问日期、版本和稳定链接", "遇到付费墙时转向机构图书馆、馆际互借或联系作者", "不绕过访问控制、不抓取盗版源、不传播受限全文"],
        "workflow_en": ["Normalize DOI, title, authors, and version metadata", "Search publisher-open copies and trusted repositories first", "Distinguish version of record, accepted manuscript, preprint, and supplements", "Record license, access date, version, and stable URL", "Use institutional libraries, interlibrary loan, or author contact for paywalls", "Do not bypass controls, scrape pirate sources, or redistribute restricted full text"],
        "inputs_zh": ["DOI、题名、作者或文献清单"], "inputs_en": ["DOI, title, author, or literature list"],
        "outputs_zh": ["合法获取路径、版本与许可证记录、未获取清单"], "outputs_en": ["Lawful access routes, version and license records, and unresolved list"],
    },
    {
        "id": "ll-research-data-availability", "title_zh": "链邻研究数据可用性与 FAIR", "title_en": "Lianlin Research Data Availability & FAIR",
        "summary_zh": "审查研究数据的可发现、可访问、可互操作、可复用状态并起草数据可用性声明。",
        "summary_en": "Review research data for findability, accessibility, interoperability, and reuse, then draft a data-availability statement.",
        "workflow_zh": ["盘点数据集、代码、材料和派生结果", "确认隐私、伦理、合同、知识产权和禁运限制", "选择领域仓储并规划持久标识符和版本", "检查元数据、格式、字典、许可证与复现说明", "按 FAIR 原则给出差距和优先修复项", "起草与实际访问条件一致的数据可用性声明"],
        "workflow_en": ["Inventory datasets, code, materials, and derived results", "Confirm privacy, ethics, contract, IP, and embargo constraints", "Choose a domain repository and plan persistent identifiers and versions", "Check metadata, formats, dictionaries, licenses, and reproduction notes", "Assess FAIR gaps and prioritized remediations", "Draft a statement consistent with actual access conditions"],
        "inputs_zh": ["数据资产清单、政策要求、访问限制"], "inputs_en": ["Data asset inventory, policy requirements, and access constraints"],
        "outputs_zh": ["FAIR 检查表、存储计划与数据可用性声明"], "outputs_en": ["FAIR checklist, deposit plan, and data-availability statement"],
    },
    {
        "id": "ll-experiment-notebook", "title_zh": "链邻实验笔记与材料追溯", "title_en": "Lianlin Experiment Notebook & Material Traceability",
        "summary_zh": "把实验目的、材料批次、协议偏差、原始数据、环境与结果连接成不可含混的追溯记录。",
        "summary_en": "Connect aims, material lots, protocol deviations, raw data, environment, and results into an unambiguous traceability record.",
        "workflow_zh": ["分配实验、样本、材料和文件的稳定标识", "实验前冻结目的、假设、协议与判定标准", "记录批次、仪器、校准、环境、操作者和时间", "把偏差、失败和异常与原始数据一起保留", "以校验和或版本号连接原始、处理与分析产物", "生成可复现实验包和交接摘要"],
        "workflow_en": ["Assign stable identifiers to experiments, samples, materials, and files", "Freeze aims, hypotheses, protocols, and decision criteria before the run", "Record lots, instruments, calibration, environment, operator, and time", "Retain deviations, failures, and anomalies with raw data", "Link raw, processed, and analytical artifacts by checksum or version", "Generate a reproducibility package and handoff summary"],
        "inputs_zh": ["实验方案、材料清单、仪器记录与数据路径"], "inputs_en": ["Protocol, material list, instrument records, and data paths"],
        "outputs_zh": ["结构化实验笔记、追溯矩阵与复现实验包清单"], "outputs_en": ["Structured notebook, traceability matrix, and reproduction package manifest"],
    },
    {
        "id": "ll-research-to-patent", "title_zh": "链邻科研成果到专利分析", "title_en": "Lianlin Research-to-Patent Analysis",
        "summary_zh": "将科研成果拆分为技术特征，开展先前技术检索并形成发明披露与风险清单。",
        "summary_en": "Decompose research outputs into technical features, search prior art, and produce an invention disclosure and risk register.",
        "workflow_zh": ["在公开前确认保密状态、作者贡献与时间线", "把技术方案拆成必要特征、可选特征和效果", "构造关键词、分类号、申请人和引证检索策略", "将文献逐项映射到技术特征并标注公开日期", "区分新颖性线索、创造性线索、实施支持和权属问题", "输出发明披露草案并建议由专利专业人士复核"],
        "workflow_en": ["Confirm confidentiality, contributor roles, and timeline before disclosure", "Decompose the solution into essential features, optional features, and effects", "Build keyword, classification, assignee, and citation search strategies", "Map each reference to technical features and publication dates", "Separate novelty, inventive-step, enablement, and ownership signals", "Draft an invention disclosure and recommend professional patent review"],
        "inputs_zh": ["技术说明、实验结果、公开记录与目标法域"], "inputs_en": ["Technical description, experimental results, disclosure history, and target jurisdiction"],
        "outputs_zh": ["技术特征表、先前技术矩阵、披露草案与风险清单"], "outputs_en": ["Feature chart, prior-art matrix, disclosure draft, and risk register"],
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source-dir", type=Path, help="Directory containing category folders")
    group.add_argument("--archive", type=Path, help="Pinned ZIP archive")
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--replace", action="store_true", help="Replace generated skills and seed catalog")
    return parser.parse_args()


def read_frontmatter(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return path.parent.name, ""
    parts = text.split("---", 2)
    if len(parts) < 3:
        return path.parent.name, ""
    lines = parts[1].splitlines()
    values: dict[str, str] = {}
    current = ""
    for raw in lines:
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", raw)
        if match:
            current = match.group(1)
            value = match.group(2).strip().strip("\"'")
            values[current] = "" if value in {">", "|", ">-", "|-"} else value
        elif current and raw.startswith((" ", "\t")):
            values[current] = (values[current] + " " + raw.strip()).strip()
    return values.get("name", path.parent.name), values.get("description", "")


def clean_text(value: str, fallback: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    if not value or value == ">":
        return fallback
    return value[:900]


def detect_environment(skill_dir: Path, skill_text: str) -> dict:
    suffixes = {p.suffix.lower() for p in skill_dir.rglob("*") if p.is_file()}
    runtime = ["agent skill instructions"]
    if ".py" in suffixes:
        runtime.append("Python")
    if suffixes & {".js", ".mjs", ".cjs", ".ts"}:
        runtime.append("Node.js")
    if suffixes & {".r", ".rmd"}:
        runtime.append("R")
    if suffixes & {".sh"}:
        runtime.append("POSIX shell")
    if suffixes & {".ps1"}:
        runtime.append("PowerShell")
    credentials = sorted(set(re.findall(r"\b[A-Z][A-Z0-9_]*(?:API_KEY|TOKEN|SECRET|ACCESS_KEY)\b", skill_text)))
    lowered = skill_text.lower()
    network = "required" if any(token in lowered for token in (" api", "http://", "https://", "database", "server")) else "unknown"
    return {"runtime": runtime, "network": network, "credentials": credentials}


def locate_source_root(source: Path) -> Path:
    candidates = [source, source / "skills", source / "academic-skills-pinned" / "skills"]
    for candidate in candidates:
        if candidate.is_dir() and any(candidate.rglob("SKILL.md")):
            return candidate
    raise SystemExit(f"No SKILL.md files found below {source}")


def category_for_source(folder_name: str, categories: list[dict]) -> str:
    match = re.match(r"^(\d{2})-", folder_name)
    if match:
        index = int(match.group(1))
        if 1 <= index <= 17:
            return categories[index - 1]["id"]
    if folder_name in CORE_SOURCE_DIR_NAMES or "学术" in folder_name:
        return "academic-core"
    raise ValueError(f"Unmapped source category: {folder_name}")


def write_locale(path: Path, lang: str, record: dict) -> None:
    zh = lang == "zh-CN"
    title = record["title"][lang]
    summary = record["summary"][lang]
    caps = record["capabilities"][lang]
    inputs = record["inputs"][lang]
    outputs = record["outputs"][lang]
    if zh:
        body = [
            f"# {title}", "", summary, "", "## 主要功能", "",
            *[f"- {item}" for item in caps], "", "## 输入", "",
            *[f"- {item}" for item in inputs], "", "## 输出", "",
            *[f"- {item}" for item in outputs], "", "## 本地使用说明", "",
            "先阅读根目录 `SKILL.md` 及其引用文件，再检查目录记录中的运行环境、凭据、网络、风险与许可证状态。第三方技能的本页说明不替代上游指令。", "",
            f"质量状态：`{record['quality']['status']}`；来源类型：`{record['source']['kind']}`。", "",
        ]
    else:
        body = [
            f"# {title}", "", summary, "", "## Main capabilities", "",
            *[f"- {item}" for item in caps], "", "## Inputs", "",
            *[f"- {item}" for item in inputs], "", "## Outputs", "",
            *[f"- {item}" for item in outputs], "", "## Local-use note", "",
            "Read the root `SKILL.md` and its referenced files first, then check the catalog record for runtime, credential, network, risk, and license status. This profile does not replace upstream instructions for third-party skills.", "",
            f"Quality status: `{record['quality']['status']}`; source kind: `{record['source']['kind']}`.", "",
        ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")


def make_record(
    *,
    skill_id: str,
    category: str,
    title_zh: str,
    title_en: str,
    summary_zh: str,
    summary_en: str,
    capabilities_zh: list[str],
    capabilities_en: list[str],
    inputs_zh: list[str],
    inputs_en: list[str],
    outputs_zh: list[str],
    outputs_en: list[str],
    environment: dict,
    source_kind: str,
    upstream: str,
    license_status: str,
    quality: str,
    risk: str,
) -> dict:
    base = f"skills/{category}/{skill_id}"
    return {
        "id": skill_id,
        "category": category,
        "title": {"zh-CN": title_zh, "en": title_en},
        "summary": {"zh-CN": summary_zh, "en": summary_en},
        "capabilities": {"zh-CN": capabilities_zh, "en": capabilities_en},
        "inputs": {"zh-CN": inputs_zh, "en": inputs_en},
        "outputs": {"zh-CN": outputs_zh, "en": outputs_en},
        "environment": environment,
        "quality": {"status": quality, "testedOn": []},
        "risk": {
            "level": risk,
            "notes": {
                "zh-CN": "使用前检查外部服务、数据权限、成本、隐私和领域有效性。",
                "en": "Check external services, data permissions, cost, privacy, and domain validity before use.",
            },
        },
        "source": {"kind": source_kind, "upstream": upstream, "licenseStatus": license_status},
        "paths": {"skill": f"{base}/SKILL.md", "zh-CN": f"{base}/locales/zh-CN.md", "en": f"{base}/locales/en.md"},
        "availability": {"local": True, "platform": True},
    }


def create_first_party_skill(root: Path, spec: dict) -> dict:
    category = "academic-core"
    skill_dir = root / "skills" / category / spec["id"]
    skill_dir.mkdir(parents=True, exist_ok=True)
    description = f"{spec['summary_en']} Use when a user needs {spec['title_en'].lower()}."
    skill_md = [
        "---", f"name: {spec['id']}", f"description: {description}", "---", "",
        f"# {spec['title_en']}", "", "Follow an evidence-first workflow. Never fabricate sources, metadata, measurements, or legal status.", "",
        "## Workflow", "", *[f"{i}. {step}" for i, step in enumerate(spec["workflow_en"], 1)], "",
        "## Output contract", "", "- Separate sourced facts, analyst inference, uncertainty, and recommended actions.",
        "- Attach stable identifiers or location anchors to consequential evidence.",
        "- State missing inputs and coverage limits explicitly.",
        "- Preserve the user's original materials; write derived artifacts separately.",
        "- Require professional or institutional review for clinical, ethical, legal, patent, or high-stakes decisions.", "",
        "## Bilingual guidance", "", "Read `locales/zh-CN.md` for the complete Chinese workflow or `locales/en.md` for the English workflow.", "",
    ]
    (skill_dir / "SKILL.md").write_text("\n".join(skill_md), encoding="utf-8")
    record = make_record(
        skill_id=spec["id"], category=category,
        title_zh=spec["title_zh"], title_en=spec["title_en"],
        summary_zh=spec["summary_zh"], summary_en=spec["summary_en"],
        capabilities_zh=spec["workflow_zh"], capabilities_en=spec["workflow_en"],
        inputs_zh=spec["inputs_zh"], inputs_en=spec["inputs_en"],
        outputs_zh=spec["outputs_zh"], outputs_en=spec["outputs_en"],
        environment={"runtime": ["agent skill instructions"], "network": "optional", "credentials": []},
        source_kind="lianlin-first-party", upstream="LL-AcademicSkillsHub",
        license_status="first-party", quality="beta", risk="medium",
    )
    write_locale(skill_dir / "locales" / "zh-CN.md", "zh-CN", record)
    write_locale(skill_dir / "locales" / "en.md", "en", record)
    return record


def main() -> None:
    args = parse_args()
    root = args.project_root.resolve()
    categories = json.loads((root / "catalog" / "categories.seed.json").read_text(encoding="utf-8"))
    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    if args.archive:
        temp_dir = tempfile.TemporaryDirectory(prefix="ll-academic-import-")
        with zipfile.ZipFile(args.archive) as archive:
            archive.extractall(temp_dir.name)
        source_root = locate_source_root(Path(temp_dir.name))
    else:
        source_root = locate_source_root(args.source_dir.resolve())

    skills_root = root / "skills"
    seed_file = root / "catalog" / "skills.seed.json"
    if (skills_root.exists() or seed_file.exists()) and not args.replace:
        raise SystemExit("Generated output already exists. Re-run with --replace to regenerate.")
    if skills_root.exists():
        shutil.rmtree(skills_root)
    skills_root.mkdir(parents=True)

    records: list[dict] = []
    skipped: list[str] = []
    for source_skill in sorted(source_root.rglob("SKILL.md"), key=lambda p: str(p).lower()):
        source_dir = source_skill.parent
        skill_id = source_dir.name
        if skill_id in DISALLOWED_IDS:
            skipped.append(skill_id)
            continue
        if skill_id in CORE_RENAMES:
            skipped.append(f"{skill_id}->{CORE_RENAMES[skill_id]}")
            continue
        category = category_for_source(source_dir.parent.name, categories)
        destination = skills_root / category / skill_id
        shutil.copytree(source_dir, destination)
        name, description = read_frontmatter(destination / "SKILL.md")
        title_en = name.replace("-", " ").title() if name == skill_id else name
        fallback = f"Upstream academic skill for {title_en}."
        summary_en = clean_text(description, fallback)
        category_item = next(item for item in categories if item["id"] == category)
        profile = CATEGORY_PROFILE[category]
        summary_zh = f"用于“{category_item['zh']}”场景的 {title_en} 技能。具体能力以原始 SKILL.md 为准；使用前应核对运行环境、外部服务与许可证状态。"
        raw_text = (destination / "SKILL.md").read_text(encoding="utf-8", errors="replace")
        environment = detect_environment(destination, raw_text)
        high_risk = category in {"clinical-precision-medicine", "lab-automation"} or any(
            term in raw_text.lower() for term in ("delete", "clinical", "patient", "medical device", "execute trade")
        )
        record = make_record(
            skill_id=skill_id, category=category,
            title_zh=title_en, title_en=title_en,
            summary_zh=summary_zh, summary_en=summary_en,
            capabilities_zh=profile["cap_zh"], capabilities_en=profile["cap_en"],
            inputs_zh=profile["inputs_zh"], inputs_en=profile["inputs_en"],
            outputs_zh=profile["outputs_zh"], outputs_en=profile["outputs_en"],
            environment=environment, source_kind="pinned-third-party",
            upstream=f"pinned-bundle:{source_dir.parent.name}/{skill_id}",
            license_status="metadata-declared", quality="cataloged",
            risk="high" if high_risk else "unknown",
        )
        write_locale(destination / "locales" / "zh-CN.md", "zh-CN", record)
        write_locale(destination / "locales" / "en.md", "en", record)
        records.append(record)

    for spec in FIRST_PARTY:
        records.append(create_first_party_skill(root, spec))

    records.sort(key=lambda item: (next(c["order"] for c in categories if c["id"] == item["category"]), item["id"]))
    seed_file.parent.mkdir(parents=True, exist_ok=True)
    seed_file.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    result = {
        "externalImported": sum(r["source"]["kind"] == "pinned-third-party" for r in records),
        "firstPartyCreated": sum(r["source"]["kind"] == "lianlin-first-party" for r in records),
        "total": len(records),
        "skipped": skipped,
        "source": str(source_root),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if temp_dir is not None:
        temp_dir.cleanup()


if __name__ == "__main__":
    main()
