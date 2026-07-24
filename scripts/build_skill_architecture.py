#!/usr/bin/env python3
"""Generate a readable system overview and five linked skill architecture maps."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "brand" / "skill-architecture"
LEGACY_OVERVIEW = ROOT / "assets" / "brand" / "skill-architecture-map.svg"
EN_OVERVIEW = ROOT / "assets" / "brand" / "skill-architecture-map.en.svg"

WIDTH = 1800
DETAIL_COLUMNS = 3

STAGES = [
    {
        "id": "discovery",
        "color": "#2563EB",
        "soft": "#EAF2FF",
        "title": {"zh-CN": "研究发现与方案设计", "en": "Research Discovery & Study Design"},
        "goal": {
            "zh-CN": "把研究问题转化为可检索、可验证、可执行的研究方案",
            "en": "Turn a research question into a searchable, testable, executable study plan",
        },
        "input": {"zh-CN": "研究主题与初步问题", "en": "Topic and initial question"},
        "output": {"zh-CN": "证据地图与研究方案", "en": "Evidence map and study plan"},
        "next": {"zh-CN": "进入专业研究分支", "en": "Enter a domain research branch"},
        "categories": [
            "academic-core",
            "literature-management",
            "research-methods",
            "scientific-databases",
        ],
    },
    {
        "id": "life-health",
        "color": "#059669",
        "soft": "#E8F8F1",
        "title": {"zh-CN": "生命科学与健康研究", "en": "Life Science & Health Research"},
        "goal": {
            "zh-CN": "从组学、临床与结构层面形成可验证的生命科学证据",
            "en": "Build testable life-science evidence across omics, clinical, and structural levels",
        },
        "input": {"zh-CN": "样本、序列、影像与临床问题", "en": "Samples, sequences, images, and clinical questions"},
        "output": {"zh-CN": "生物学发现与医学证据", "en": "Biological findings and medical evidence"},
        "next": {"zh-CN": "汇入数据建模与验证", "en": "Feed data modeling and validation"},
        "categories": [
            "bioinformatics-genomics",
            "clinical-precision-medicine",
            "protein-structural-biology",
        ],
    },
    {
        "id": "domain-sciences",
        "color": "#D97706",
        "soft": "#FFF4DF",
        "title": {"zh-CN": "跨学科专业计算", "en": "Cross-domain Scientific Computing"},
        "goal": {
            "zh-CN": "连接分子、材料、金融与空间数据，完成领域级计算研究",
            "en": "Connect molecular, materials, finance, and spatial data for domain research",
        },
        "input": {"zh-CN": "结构、物性、市场与空间数据", "en": "Structural, physical, market, and spatial data"},
        "output": {"zh-CN": "预测、模拟与领域结论", "en": "Predictions, simulations, and domain findings"},
        "next": {"zh-CN": "汇入数据建模与验证", "en": "Feed data modeling and validation"},
        "categories": [
            "cheminformatics-drug-discovery",
            "materials-physics",
            "finance-economics",
            "geospatial-remote-sensing",
        ],
    },
    {
        "id": "data-compute",
        "color": "#7C3AED",
        "soft": "#F1EBFF",
        "title": {"zh-CN": "实验、数据与智能计算", "en": "Experiments, Data & Intelligent Computing"},
        "goal": {
            "zh-CN": "把实验与多源数据转化为可复现、可解释、可审计的模型和结果",
            "en": "Turn experiments and multi-source data into reproducible, explainable results",
        },
        "input": {"zh-CN": "实验记录与多源研究数据", "en": "Experimental records and multi-source data"},
        "output": {"zh-CN": "统计结果、模型与可复现产物", "en": "Statistics, models, and reproducible artifacts"},
        "next": {"zh-CN": "进入论文与成果生产", "en": "Enter scholarly production"},
        "categories": [
            "lab-automation",
            "data-analysis-statistics",
            "machine-learning-ai",
            "platform-infrastructure",
        ],
    },
    {
        "id": "communication",
        "color": "#DB2777",
        "soft": "#FDEAF3",
        "title": {"zh-CN": "论文创作与成果传播", "en": "Scholarly Writing & Research Impact"},
        "goal": {
            "zh-CN": "把证据、方法和结果组织为论文、图表、演示与可交付学术成果",
            "en": "Turn evidence, methods, and results into papers, figures, talks, and deliverables",
        },
        "input": {"zh-CN": "证据链、分析结果与素材", "en": "Evidence chain, results, and source material"},
        "output": {"zh-CN": "论文、图表、演示与审稿回复", "en": "Papers, figures, talks, and review responses"},
        "next": {"zh-CN": "审稿反馈回流研究发现", "en": "Review feedback returns to discovery"},
        "categories": [
            "document-data-tools",
            "scientific-communication",
            "presentation-visualization",
        ],
    },
]

CATEGORY_PURPOSES = {
    "academic-core": {
        "zh-CN": "检索、精读、写作、审稿与证据治理的主控工作流",
        "en": "Core workflows for search, reading, writing, review, and evidence governance",
    },
    "literature-management": {
        "zh-CN": "系统检索、筛选、引用管理与文献证据整合",
        "en": "Systematic search, screening, citation management, and evidence synthesis",
    },
    "scientific-communication": {
        "zh-CN": "论文、基金、审稿回复与规范化学术表达",
        "en": "Papers, grants, reviewer responses, and rigorous scholarly communication",
    },
    "presentation-visualization": {
        "zh-CN": "科研图表、海报、幻灯片与出版级视觉表达",
        "en": "Scientific figures, posters, slides, and publication-ready visual communication",
    },
    "research-methods": {
        "zh-CN": "研究问题、实验设计、批判思维与可复现性",
        "en": "Research questions, study design, critical reasoning, and reproducibility",
    },
    "bioinformatics-genomics": {
        "zh-CN": "序列、组学、单细胞与基因组分析",
        "en": "Sequence, omics, single-cell, and genomic analysis",
    },
    "cheminformatics-drug-discovery": {
        "zh-CN": "分子结构、性质预测、虚拟筛选与药物发现",
        "en": "Molecular structures, property prediction, virtual screening, and drug discovery",
    },
    "clinical-precision-medicine": {
        "zh-CN": "临床证据、医学影像与精准医疗分析",
        "en": "Clinical evidence, medical imaging, and precision medicine analysis",
    },
    "protein-structural-biology": {
        "zh-CN": "蛋白结构、功能注释、设计与工程",
        "en": "Protein structure, functional annotation, design, and engineering",
    },
    "machine-learning-ai": {
        "zh-CN": "机器学习建模、训练、推理、优化与解释",
        "en": "Machine-learning modeling, training, inference, optimization, and interpretation",
    },
    "materials-physics": {
        "zh-CN": "材料模拟、量子计算、物理建模与科学计算",
        "en": "Materials simulation, quantum computing, physical modeling, and computation",
    },
    "data-analysis-statistics": {
        "zh-CN": "数据清理、统计推断、建模与分析报告",
        "en": "Data cleaning, statistical inference, modeling, and analytical reporting",
    },
    "scientific-databases": {
        "zh-CN": "专业科学数据库检索、整合与规范化",
        "en": "Domain database search, integration, and normalization",
    },
    "lab-automation": {
        "zh-CN": "实验协议、仪器控制、液体处理与自动化",
        "en": "Protocols, instrument control, liquid handling, and laboratory automation",
    },
    "document-data-tools": {
        "zh-CN": "PDF、文档、表格、演示与结构化转换",
        "en": "PDFs, documents, spreadsheets, presentations, and structured conversion",
    },
    "finance-economics": {
        "zh-CN": "金融市场、企业数据与宏观经济研究",
        "en": "Financial markets, company data, and macroeconomic research",
    },
    "geospatial-remote-sensing": {
        "zh-CN": "GIS、遥感影像、空间计算与地球观测",
        "en": "GIS, remote sensing, spatial computation, and earth observation",
    },
    "platform-infrastructure": {
        "zh-CN": "计算环境、云资源、任务编排与科研基础设施",
        "en": "Compute environments, cloud resources, orchestration, and infrastructure",
    },
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def trim(value: str, limit: int) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def wrap_text(value: str, limit: int, max_lines: int = 2) -> list[str]:
    if len(value) <= limit:
        return [value]
    if " " not in value:
        lines = [value[index : index + limit] for index in range(0, len(value), limit)]
    else:
        lines = []
        current = ""
        for word in value.split():
            candidate = f"{current} {word}".strip()
            if current and len(candidate) > limit:
                lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = trim(lines[-1], max(2, limit - 1))
    return lines


def localized(value: dict, lang: str) -> str:
    return value[lang]


def category_name(category: dict, lang: str) -> str:
    return category["zh"] if lang == "zh-CN" else category["en"]


def skill_count(stage: dict, skills: list[dict]) -> int:
    category_ids = set(stage["categories"])
    return sum(skill["category"] in category_ids for skill in skills)


def svg_shell(width: int, height: int, title: str, description: str) -> list[str]:
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        ),
        f'<title id="title">{esc(title)}</title>',
        f'<desc id="desc">{esc(description)}</desc>',
        """
<defs>
  <linearGradient id="page" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#F8FAFF"/>
    <stop offset="1" stop-color="#F4F7FB"/>
  </linearGradient>
  <pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse">
    <path d="M48 0H0V48" fill="none" stroke="#0F172A" stroke-opacity=".035"/>
  </pattern>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0F172A" flood-opacity=".10"/>
  </filter>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
    <path d="M0 0L12 6L0 12Z" fill="#64748B"/>
  </marker>
  <marker id="feedback" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
    <path d="M0 0L12 6L0 12Z" fill="#0F9F8F"/>
  </marker>
  <style>
    text { font-family: Inter, "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif; }
    .eyebrow { font-size: 17px; font-weight: 800; letter-spacing: 3px; fill: #64748B; }
    .page-title { font-size: 44px; font-weight: 900; fill: #0F172A; }
    .page-subtitle { font-size: 20px; fill: #475569; }
    .stage-title { font-size: 24px; font-weight: 900; fill: #0F172A; }
    .stage-goal { font-size: 16px; fill: #475569; }
    .count { font-size: 15px; font-weight: 800; }
    .category-title { font-size: 23px; font-weight: 900; fill: #0F172A; }
    .category-purpose { font-size: 16px; fill: #64748B; }
    .skill-title { font-size: 17px; font-weight: 700; fill: #172033; }
    .skill-id { font-size: 11px; font-weight: 600; fill: #64748B; letter-spacing: .25px; }
    .label { font-size: 13px; font-weight: 900; letter-spacing: 1px; fill: #64748B; }
    .flow-value { font-size: 18px; font-weight: 800; fill: #172033; }
    .footer { font-size: 15px; fill: #64748B; }
  </style>
</defs>
""",
        f'<rect width="{width}" height="{height}" fill="url(#page)"/>',
        f'<rect width="{width}" height="{height}" fill="url(#grid)"/>',
        '<circle cx="1650" cy="70" r="290" fill="#2563EB" opacity=".035"/>',
        '<circle cx="80" cy="900" r="240" fill="#0F9F8F" opacity=".035"/>',
    ]


def overview_card(
    parts: list[str],
    stage: dict,
    number: int,
    x: int,
    y: int,
    width: int,
    height: int,
    categories_by_id: dict[str, dict],
    skills: list[dict],
    lang: str,
) -> None:
    color = stage["color"]
    count = skill_count(stage, skills)
    title = localized(stage["title"], lang)
    goal = localized(stage["goal"], lang)
    goal_lines = wrap_text(goal, 20 if lang == "zh-CN" else 40)
    category_names = [
        category_name(categories_by_id[item], lang) for item in stage["categories"]
    ]
    category_lines = [
        " · ".join(category_names[index : index + 2])
        for index in range(0, len(category_names), 2)
    ]
    parts.extend(
        [
            f'<g filter="url(#shadow)">',
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="26" fill="#FFFFFF" stroke="#D9E2EE"/>',
            f'<rect x="{x}" y="{y}" width="12" height="{height}" rx="6" fill="{color}"/>',
            f'<rect x="{x + 28}" y="{y + 24}" width="94" height="34" rx="17" fill="{stage["soft"]}"/>',
            f'<text x="{x + 75}" y="{y + 47}" text-anchor="middle" class="count" fill="{color}">0{number}</text>',
            f'<text x="{x + 142}" y="{y + 49}" font-size="22" font-weight="900" fill="#0F172A">{esc(title)}</text>',
            f'<text x="{x + 30}" y="{y + 91}" class="label">{"目标" if lang == "zh-CN" else "GOAL"}</text>',
        ]
    )
    for line_index, line in enumerate(goal_lines):
        parts.append(
            f'<text x="{x + 30}" y="{y + 117 + line_index * 22}" class="stage-goal">{esc(line)}</text>'
        )
    parts.extend(
        [
            f'<line x1="{x + 30}" y1="{y + 154}" x2="{x + width - 30}" y2="{y + 154}" stroke="#E2E8F0"/>',
            f'<text x="{x + 30}" y="{y + 181}" class="label">{"能力分类" if lang == "zh-CN" else "CAPABILITY GROUPS"}</text>',
            f'<text x="{x + width - 30}" y="{y + 181}" text-anchor="end" class="count" fill="{color}">{count} SKILLS</text>',
        ]
    )
    for line_index, line in enumerate(category_lines):
        parts.append(
            f'<text x="{x + 30}" y="{y + 207 + line_index * 25}" '
            f'font-size="14" font-weight="700" fill="#334155">{esc(line)}</text>'
        )
    parts.append('</g>')


def overview_svg(categories: list[dict], skills: list[dict], lang: str) -> str:
    zh = lang == "zh-CN"
    categories_by_id = {category["id"]: category for category in categories}
    title = "科研全流程技能系统" if zh else "End-to-End Academic Skills System"
    subtitle = (
        "1 张总览串联 5 个阶段；专业研究双分支并行，证据反馈形成闭环"
        if zh
        else "One overview links five stages; parallel domain branches converge into an evidence feedback loop"
    )
    foundation = (
        "证据链治理  ·  可复现计算  ·  数据与权限管理  ·  人工复核  ·  全流程审计"
        if zh
        else "Evidence governance  ·  Reproducible compute  ·  Data and access control  ·  Human review  ·  Auditability"
    )
    parts = svg_shell(
        WIDTH,
        1040,
        f"LL-AcademicSkillsHub {title}",
        f"{len(skills)} skills across {len(categories)} categories in five linked research stages.",
    )
    parts.extend(
        [
            '<text x="70" y="68" class="eyebrow">LL-ACADEMICSKILLSHUB · RESEARCH OPERATING SYSTEM</text>',
            f'<text x="70" y="126" class="page-title">{esc(title)}</text>',
            f'<text x="70" y="164" class="page-subtitle">{esc(subtitle)}</text>',
            f'<rect x="1450" y="72" width="280" height="74" rx="22" fill="#0F172A"/>',
            f'<text x="1590" y="106" text-anchor="middle" font-size="30" font-weight="900" fill="#FFFFFF">{len(skills)}</text>',
            f'<text x="1590" y="132" text-anchor="middle" font-size="13" font-weight="800" fill="#CBD5E1">SKILLS · {len(categories)} CATEGORIES</text>',
        ]
    )

    # Stage 1 splits into two professional research branches and reconverges at stage 4.
    overview_card(parts, STAGES[0], 1, 60, 320, 350, 260, categories_by_id, skills, lang)
    overview_card(parts, STAGES[1], 2, 490, 210, 390, 250, categories_by_id, skills, lang)
    overview_card(parts, STAGES[2], 3, 490, 535, 390, 250, categories_by_id, skills, lang)
    overview_card(parts, STAGES[3], 4, 970, 320, 350, 260, categories_by_id, skills, lang)
    overview_card(parts, STAGES[4], 5, 1400, 320, 340, 260, categories_by_id, skills, lang)

    arrow_style = 'fill="none" stroke="#64748B" stroke-width="3" marker-end="url(#arrow)"'
    parts.extend(
        [
            f'<path d="M410 390 C450 390 448 335 490 335" {arrow_style}/>',
            f'<path d="M410 510 C450 510 448 660 490 660" {arrow_style}/>',
            f'<path d="M880 335 C930 335 925 390 970 390" {arrow_style}/>',
            f'<path d="M880 660 C930 660 925 510 970 510" {arrow_style}/>',
            f'<path d="M1320 450 H1400" {arrow_style}/>',
            (
                '<path d="M1570 580 C1570 875 230 875 230 580" fill="none" stroke="#0F9F8F" '
                'stroke-width="3" stroke-dasharray="10 9" marker-end="url(#feedback)"/>'
            ),
            f'<text x="900" y="848" text-anchor="middle" font-size="17" font-weight="800" fill="#0F9F8F">'
            f'{"审稿、复核与新证据持续回流" if zh else "Review, validation, and new evidence continuously feed back"}</text>',
            '<rect x="120" y="910" width="1560" height="72" rx="24" fill="#FFFFFF" stroke="#D9E2EE"/>',
            '<text x="180" y="940" class="label">RESEARCH FOUNDATION</text>',
            (
                f'<text x="180" y="965" font-size="18" font-weight="800" fill="#172033">'
                f'{esc(foundation)}</text>'
            ),
            '<text x="1725" y="1018" text-anchor="end" class="footer">LL-AcademicSkillsHub · 2026</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts) + "\n"


def flow_box(
    parts: list[str],
    x: int,
    y: int,
    width: int,
    label: str,
    value: str,
    color: str,
    soft: str,
    lang: str,
) -> None:
    lines = wrap_text(value, 17 if lang == "zh-CN" else 30)
    parts.extend(
        [
            f'<rect x="{x}" y="{y}" width="{width}" height="108" rx="22" fill="#FFFFFF" stroke="#D9E2EE" filter="url(#shadow)"/>',
            f'<rect x="{x}" y="{y}" width="8" height="108" rx="4" fill="{color}"/>',
            f'<text x="{x + 28}" y="{y + 34}" class="label">{esc(label)}</text>',
            f'<rect x="{x + 26}" y="{y + 49}" width="{width - 50}" height="42" rx="13" fill="{soft}"/>',
        ]
    )
    if len(lines) == 1:
        parts.append(
            f'<text x="{x + 43}" y="{y + 77}" class="flow-value">{esc(lines[0])}</text>'
        )
    else:
        for line_index, line in enumerate(lines):
            parts.append(
                f'<text x="{x + 43}" y="{y + 67 + line_index * 18}" '
                f'font-size="15" font-weight="800" fill="#172033">{esc(line)}</text>'
            )


def detail_svg(
    stage: dict,
    stage_index: int,
    categories: list[dict],
    skills: list[dict],
    lang: str,
) -> str:
    zh = lang == "zh-CN"
    categories_by_id = {category["id"]: category for category in categories}
    skills_by_category = {
        category_id: [skill for skill in skills if skill["category"] == category_id]
        for category_id in stage["categories"]
    }
    category_heights = {}
    for category_id, entries in skills_by_category.items():
        rows = math.ceil(len(entries) / DETAIL_COLUMNS)
        category_heights[category_id] = 112 + rows * 62
    height = 495 + sum(category_heights.values()) + 26 * (len(stage["categories"]) - 1) + 100

    title = localized(stage["title"], lang)
    goal = localized(stage["goal"], lang)
    count = skill_count(stage, skills)
    parts = svg_shell(
        WIDTH,
        height,
        f"{stage_index:02d} {title}",
        f"{count} skills in stage {stage_index} of the LL-AcademicSkillsHub research workflow.",
    )
    color = stage["color"]
    soft = stage["soft"]
    parts.extend(
        [
            f'<rect x="0" y="0" width="18" height="{height}" fill="{color}"/>',
            '<text x="70" y="66" class="eyebrow">LL-ACADEMICSKILLSHUB · SKILL ARCHITECTURE</text>',
            f'<rect x="70" y="94" width="94" height="54" rx="19" fill="{soft}"/>',
            f'<text x="117" y="130" text-anchor="middle" font-size="24" font-weight="900" fill="{color}">0{stage_index}</text>',
            f'<text x="188" y="134" class="page-title">{esc(title)}</text>',
            f'<text x="70" y="184" class="page-subtitle">{esc(goal)}</text>',
            f'<rect x="1460" y="82" width="270" height="82" rx="24" fill="{color}"/>',
            f'<text x="1595" y="119" text-anchor="middle" font-size="32" font-weight="900" fill="#FFFFFF">{count}</text>',
            f'<text x="1595" y="146" text-anchor="middle" font-size="13" font-weight="900" fill="#FFFFFF" opacity=".9">'
            f'{"项技能" if zh else "STAGE SKILLS"}</text>',
        ]
    )

    flow_y = 230
    box_width = 376
    box_gap = 54
    flow_values = [
        ("输入" if zh else "INPUT", localized(stage["input"], lang)),
        ("阶段任务" if zh else "STAGE GOAL", goal),
        ("输出" if zh else "OUTPUT", localized(stage["output"], lang)),
        ("流向" if zh else "NEXT", localized(stage["next"], lang)),
    ]
    for index, (label, value) in enumerate(flow_values):
        x = 70 + index * (box_width + box_gap)
        flow_box(parts, x, flow_y, box_width, label, value, color, soft, lang)
        if index < 3:
            parts.append(
                f'<path d="M{x + box_width + 10} {flow_y + 54} H{x + box_width + box_gap - 12}" '
                'fill="none" stroke="#64748B" stroke-width="3" marker-end="url(#arrow)"/>'
            )

    parts.extend(
        [
            f'<text x="70" y="405" class="label">{"阶段能力清单" if zh else "STAGE CAPABILITY MAP"}</text>',
            f'<text x="70" y="444" font-size="28" font-weight="900" fill="#0F172A">'
            f'{"每项技能都落在明确任务节点中" if zh else "Every skill belongs to an explicit research task"}</text>',
        ]
    )

    cursor_y = 480
    for category_id in stage["categories"]:
        category = categories_by_id[category_id]
        entries = skills_by_category[category_id]
        card_height = category_heights[category_id]
        category_label = category_name(category, lang)
        purpose = CATEGORY_PURPOSES[category_id][lang]
        parts.extend(
            [
                f'<rect x="70" y="{cursor_y}" width="1660" height="{card_height}" rx="26" fill="#FFFFFF" stroke="#D9E2EE" filter="url(#shadow)"/>',
                f'<rect x="70" y="{cursor_y}" width="12" height="{card_height}" rx="6" fill="{color}"/>',
                f'<rect x="104" y="{cursor_y + 25}" width="62" height="38" rx="15" fill="{soft}"/>',
                f'<text x="135" y="{cursor_y + 51}" text-anchor="middle" class="count" fill="{color}">{category["order"]:02d}</text>',
                f'<text x="188" y="{cursor_y + 53}" class="category-title">{esc(category_label)}</text>',
                f'<text x="1692" y="{cursor_y + 52}" text-anchor="end" class="count" fill="{color}">{len(entries)} SKILLS</text>',
                f'<text x="105" y="{cursor_y + 86}" class="category-purpose">{esc(purpose)}</text>',
            ]
        )

        pill_x0 = 105
        pill_y0 = cursor_y + 104
        pill_width = 515
        pill_gap = 24
        rows = math.ceil(len(entries) / DETAIL_COLUMNS)
        for item_index, skill in enumerate(entries):
            column = item_index // rows
            row = item_index % rows
            x = pill_x0 + column * (pill_width + pill_gap)
            y = pill_y0 + row * 62
            title_value = skill["title"][lang]
            title_limit = 27 if zh else 48
            parts.extend(
                [
                    f'<rect x="{x}" y="{y}" width="{pill_width}" height="48" rx="14" fill="{soft}" stroke="{color}" stroke-opacity=".16"/>',
                    f'<circle cx="{x + 20}" cy="{y + 18}" r="5" fill="{color}"/>',
                    f'<text x="{x + 34}" y="{y + 22}" class="skill-title"><title>{esc(title_value)}</title>{esc(trim(title_value, title_limit))}</text>',
                    f'<text x="{x + 34}" y="{y + 40}" class="skill-id">{esc(skill["id"])}</text>',
                ]
            )
        cursor_y += card_height + 26

    previous_title = localized(STAGES[stage_index - 2]["title"], lang) if stage_index > 1 else (
        "研究问题" if zh else "Research question"
    )
    next_title = localized(STAGES[stage_index]["title"], lang) if stage_index < len(STAGES) else (
        "审稿反馈与新证据" if zh else "Review feedback and new evidence"
    )
    parts.extend(
        [
            f'<line x1="70" y1="{height - 70}" x2="1730" y2="{height - 70}" stroke="#CBD5E1"/>',
            f'<text x="70" y="{height - 35}" class="footer">← {esc(previous_title)}</text>',
            f'<text x="900" y="{height - 35}" text-anchor="middle" class="footer">'
            f'{"阶段 02 与 03 为并行专业研究分支" if zh else "Stages 02 and 03 are parallel domain-research branches"}</text>',
            f'<text x="1730" y="{height - 35}" text-anchor="end" class="footer">{esc(next_title)} →</text>',
            '</svg>',
        ]
    )
    return "\n".join(parts) + "\n"


def validate_mapping(categories: list[dict], skills: list[dict]) -> None:
    mapped = [category_id for stage in STAGES for category_id in stage["categories"]]
    expected = [category["id"] for category in categories]
    if len(mapped) != len(set(mapped)) or set(mapped) != set(expected):
        raise ValueError("The five-stage map must cover every category exactly once")
    if sum(skill_count(stage, skills) for stage in STAGES) != len(skills):
        raise ValueError("The five-stage map must cover every skill exactly once")


def detail_path(stage_index: int, stage: dict, lang: str) -> Path:
    suffix = "zh-CN" if lang == "zh-CN" else "en"
    return OUTPUT_DIR / f"{stage_index:02d}-{stage['id']}.{suffix}.svg"


def build_skill_architecture(
    categories: list[dict] | None = None,
    skills: list[dict] | None = None,
) -> list[Path]:
    categories = categories or load_json(ROOT / "catalog" / "categories.seed.json")
    skills = skills or load_json(ROOT / "catalog" / "skills.seed.json")
    validate_mapping(categories, skills)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = []
    for lang, overview_path in (("zh-CN", LEGACY_OVERVIEW), ("en", EN_OVERVIEW)):
        overview_path.write_text(overview_svg(categories, skills, lang), encoding="utf-8")
        outputs.append(overview_path)
        for stage_index, stage in enumerate(STAGES, start=1):
            path = detail_path(stage_index, stage, lang)
            path.write_text(
                detail_svg(stage, stage_index, categories, skills, lang),
                encoding="utf-8",
            )
            outputs.append(path)
    return outputs


def main() -> None:
    for path in build_skill_architecture():
        print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
