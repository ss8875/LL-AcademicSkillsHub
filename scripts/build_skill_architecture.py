#!/usr/bin/env python3
"""Generate the deterministic bilingual SVG skill architecture map."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "brand" / "skill-architecture-map.svg"

WIDTH = 3200
HEIGHT = 2070
CARD_Y = 1050
CARD_W = 420
CARD_H = 900
CARD_GAP = 25
CARD_X0 = 55

CLUSTERS = [
    {
        "id": "discovery",
        "zh": "研究发现与证据",
        "en": "DISCOVERY & EVIDENCE",
        "color": "#49d8ff",
        "categories": [
            "academic-core",
            "literature-management",
            "research-methods",
            "scientific-databases",
        ],
        "hub": (350, 650),
    },
    {
        "id": "life",
        "zh": "生命科学与健康",
        "en": "LIFE & HEALTH",
        "color": "#5ce6a5",
        "categories": [
            "bioinformatics-genomics",
            "clinical-precision-medicine",
            "protein-structural-biology",
        ],
        "hub": (900, 570),
    },
    {
        "id": "matter",
        "zh": "分子、材料与物理",
        "en": "MOLECULES & PHYSICS",
        "color": "#ffb65e",
        "categories": [
            "cheminformatics-drug-discovery",
            "materials-physics",
        ],
        "hub": (1250, 735),
    },
    {
        "id": "society",
        "zh": "社会、金融与地球",
        "en": "SOCIETY & EARTH",
        "color": "#bd8cff",
        "categories": [
            "finance-economics",
            "geospatial-remote-sensing",
        ],
        "hub": (1600, 570),
    },
    {
        "id": "data",
        "zh": "数据、统计与智能",
        "en": "DATA & AI",
        "color": "#7795ff",
        "categories": [
            "data-analysis-statistics",
            "machine-learning-ai",
        ],
        "hub": (2070, 650),
    },
    {
        "id": "communication",
        "zh": "写作、视觉与传播",
        "en": "COMMUNICATION & IMPACT",
        "color": "#ff76b7",
        "categories": [
            "scientific-communication",
            "presentation-visualization",
        ],
        "hub": (2670, 650),
    },
    {
        "id": "operations",
        "zh": "实验、文档与平台",
        "en": "RESEARCH OPERATIONS",
        "color": "#38d8c5",
        "categories": [
            "lab-automation",
            "document-data-tools",
            "platform-infrastructure",
        ],
        "hub": (1600, 900),
    },
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def short(value: str, limit: int = 27) -> str:
    return value if len(value) <= limit else value[: limit - 1] + "…"


def line_path(start: tuple[int, int], end: tuple[int, int], bend: int = 0) -> str:
    x1, y1 = start
    x2, y2 = end
    mx = (x1 + x2) / 2
    return f"M{x1},{y1} C{mx},{y1 + bend} {mx},{y2 - bend} {x2},{y2}"


def cluster_count(cluster: dict, skills: list[dict]) -> int:
    category_ids = set(cluster["categories"])
    return sum(skill["category"] in category_ids for skill in skills)


def architecture_svg(categories: list[dict], skills: list[dict]) -> str:
    categories_by_id = {category["id"]: category for category in categories}
    skills_by_category = {
        category["id"]: [skill for skill in skills if skill["category"] == category["id"]]
        for category in categories
    }

    mapped = [category_id for cluster in CLUSTERS for category_id in cluster["categories"]]
    expected = [category["id"] for category in categories]
    if len(mapped) != len(set(mapped)) or set(mapped) != set(expected):
        raise ValueError("Architecture cluster mapping must cover every category exactly once")
    if sum(cluster_count(cluster, skills) for cluster in CLUSTERS) != len(skills):
        raise ValueError("Architecture cluster counts must cover every skill exactly once")

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">LL-AcademicSkillsHub 技能架构图</title>',
        (
            f'<desc id="desc">A connected architecture map of {len(skills)} academic skills '
            f'across {len(categories)} categories and seven composable research capability domains.</desc>'
        ),
        """
<defs>
  <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#050b17"/>
    <stop offset=".48" stop-color="#0a1830"/>
    <stop offset="1" stop-color="#07111f"/>
  </linearGradient>
  <linearGradient id="core" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#47e5c2"/>
    <stop offset=".48" stop-color="#4cb8ff"/>
    <stop offset="1" stop-color="#9a7cff"/>
  </linearGradient>
  <radialGradient id="coreFill">
    <stop offset="0" stop-color="#173f62"/>
    <stop offset=".72" stop-color="#0b203a"/>
    <stop offset="1" stop-color="#07111f"/>
  </radialGradient>
  <pattern id="grid" width="64" height="64" patternUnits="userSpaceOnUse">
    <path d="M64 0H0V64" fill="none" stroke="#a9d6ff" stroke-opacity=".055" stroke-width="1"/>
    <circle cx="0" cy="0" r="1.6" fill="#8ecfff" fill-opacity=".12"/>
  </pattern>
  <filter id="softGlow" x="-80%" y="-80%" width="260%" height="260%">
    <feGaussianBlur stdDeviation="18" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <filter id="nodeGlow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="7" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">
    <path d="M0 0L12 6L0 12Z" fill="#7dd9ff"/>
  </marker>
  <style>
    text { font-family: Inter, "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", Arial, sans-serif; }
    .eyebrow { font-size: 20px; font-weight: 700; letter-spacing: 5px; fill: #68efd0; }
    .title { font-size: 56px; font-weight: 800; fill: #f7fbff; }
    .subtitle { font-size: 23px; fill: #a9c5df; }
    .hub-zh { font-size: 21px; font-weight: 800; fill: #f7fbff; }
    .hub-en { font-size: 12px; font-weight: 700; letter-spacing: 1.5px; fill: #a9c5df; }
    .hub-count { font-size: 16px; font-weight: 800; }
    .card-zh { font-size: 20px; font-weight: 800; fill: #f7fbff; }
    .card-en { font-size: 11px; font-weight: 700; letter-spacing: 1.2px; fill: #91abc3; }
    .category { font-size: 15px; font-weight: 800; fill: #eaf6ff; }
    .skill { font-size: 12.4px; font-weight: 500; fill: #b9cce0; }
    .legend { font-size: 15px; fill: #9db6ce; }
  </style>
</defs>
""",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#background)"/>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>',
        '<ellipse cx="1600" cy="430" rx="1180" ry="410" fill="#2c91ff" opacity=".035"/>',
        '<ellipse cx="1600" cy="460" rx="820" ry="300" fill="#4ce8c0" opacity=".025"/>',
        '<text x="90" y="82" class="eyebrow">LL-ACADEMICSKILLSHUB · RESEARCH OPERATING SYSTEM</text>',
        '<text x="90" y="150" class="title">技能架构图</text>',
        (
            f'<text x="90" y="197" class="subtitle">{len(skills)} 项技能 · '
            f'{len(categories)} 个分类 · 7 大可组合能力域 · 从研究问题到论文交付</text>'
        ),
        '<text x="3110" y="80" text-anchor="end" class="subtitle">链邻学术技能仓库</text>',
        '<text x="3110" y="116" text-anchor="end" class="legend">EVIDENCE · COMPUTE · CREATE · AUDIT</text>',
    ]

    center = (1600, 370)
    hub_positions = {cluster["id"]: cluster["hub"] for cluster in CLUSTERS}

    # Central-to-domain neural links.
    for cluster in CLUSTERS:
        hub = cluster["hub"]
        parts.append(
            f'<path d="{line_path(center, hub, 45)}" fill="none" stroke="{cluster["color"]}" '
            'stroke-width="3" stroke-opacity=".38" stroke-dasharray="7 10"/>'
        )

    # Primary research flow and evidence feedback.
    discovery = hub_positions["discovery"]
    data = hub_positions["data"]
    communication = hub_positions["communication"]
    for domain_id in ("life", "matter", "society"):
        domain = hub_positions[domain_id]
        parts.append(
            f'<path d="{line_path((discovery[0] + 105, discovery[1]), (domain[0] - 105, domain[1]), -18)}" '
            'fill="none" stroke="#7dd9ff" stroke-width="4" stroke-opacity=".55" marker-end="url(#arrow)"/>'
        )
        parts.append(
            f'<path d="{line_path((domain[0] + 105, domain[1]), (data[0] - 105, data[1]), 24)}" '
            'fill="none" stroke="#7dd9ff" stroke-width="4" stroke-opacity=".55" marker-end="url(#arrow)"/>'
        )
    parts.extend(
        [
            (
                f'<path d="{line_path((data[0] + 110, data[1]), (communication[0] - 115, communication[1]), 0)}" '
                'fill="none" stroke="#7dd9ff" stroke-width="5" stroke-opacity=".68" marker-end="url(#arrow)"/>'
            ),
            (
                f'<path d="M{communication[0]},{communication[1] - 76} '
                f'C{communication[0] - 110},245 {discovery[0] + 110},245 {discovery[0]},{discovery[1] - 76}" '
                'fill="none" stroke="#ff76b7" stroke-width="3.5" stroke-opacity=".5" '
                'stroke-dasharray="10 12" marker-end="url(#arrow)"/>'
            ),
        ]
    )

    # Cross-cutting operations platform.
    operations = hub_positions["operations"]
    for cluster_id in ("discovery", "life", "matter", "society", "data", "communication"):
        target = hub_positions[cluster_id]
        parts.append(
            f'<path d="{line_path((operations[0], operations[1] - 50), (target[0], target[1] + 57), 20)}" '
            'fill="none" stroke="#38d8c5" stroke-width="2.2" stroke-opacity=".26" stroke-dasharray="4 10"/>'
        )

    # Central core.
    parts.extend(
        [
            '<circle cx="1600" cy="370" r="150" fill="#40c7ff" opacity=".08" filter="url(#softGlow)"/>',
            '<circle cx="1600" cy="370" r="132" fill="url(#coreFill)" stroke="url(#core)" stroke-width="5"/>',
            '<circle cx="1600" cy="370" r="111" fill="none" stroke="#9ee8ff" stroke-opacity=".18" stroke-width="1.5"/>',
            '<text x="1600" y="330" text-anchor="middle" font-size="20" font-weight="800" fill="#68efd0">LL-ACADEMIC</text>',
            '<text x="1600" y="365" text-anchor="middle" font-size="23" font-weight="800" fill="#ffffff">科研能力中枢</text>',
            f'<text x="1600" y="407" text-anchor="middle" font-size="28" font-weight="900" fill="#ffffff">{len(skills)}</text>',
            f'<text x="1600" y="435" text-anchor="middle" font-size="14" font-weight="700" fill="#a9c5df">SKILLS · {len(categories)} CATEGORIES</text>',
            '<text x="1600" y="470" text-anchor="middle" font-size="13" fill="#83e9d1">可搜索 · 可安装 · 可组合</text>',
        ]
    )

    # Domain hubs.
    for cluster in CLUSTERS:
        x, y = cluster["hub"]
        count = cluster_count(cluster, skills)
        color = cluster["color"]
        parts.extend(
            [
                f'<circle cx="{x}" cy="{y}" r="96" fill="{color}" opacity=".08" filter="url(#nodeGlow)"/>',
                f'<rect x="{x - 132}" y="{y - 62}" width="264" height="124" rx="28" '
                f'fill="#0a192d" stroke="{color}" stroke-width="2.5"/>',
                f'<circle cx="{x - 102}" cy="{y - 30}" r="8" fill="{color}" filter="url(#nodeGlow)"/>',
                f'<text x="{x}" y="{y - 18}" text-anchor="middle" class="hub-zh">{esc(cluster["zh"])}</text>',
                f'<text x="{x}" y="{y + 9}" text-anchor="middle" class="hub-en">{esc(cluster["en"])}</text>',
                f'<rect x="{x - 42}" y="{y + 24}" width="84" height="27" rx="13.5" fill="{color}" opacity=".15"/>',
                f'<text x="{x}" y="{y + 44}" text-anchor="middle" class="hub-count" fill="{color}">{count} SKILLS</text>',
            ]
        )

    # Capability cards and complete skill leaf lists.
    for index, cluster in enumerate(CLUSTERS):
        x = CARD_X0 + index * (CARD_W + CARD_GAP)
        card_center = x + CARD_W / 2
        color = cluster["color"]
        count = cluster_count(cluster, skills)
        hub_x, hub_y = cluster["hub"]
        parts.extend(
            [
                f'<path d="{line_path((hub_x, hub_y + 66), (int(card_center), CARD_Y), 40)}" '
                f'fill="none" stroke="{color}" stroke-width="2.2" stroke-opacity=".34"/>',
                f'<rect x="{x}" y="{CARD_Y}" width="{CARD_W}" height="{CARD_H}" rx="28" '
                'fill="#081426" fill-opacity=".92" stroke="#31506f" stroke-width="1.4"/>',
                f'<rect x="{x}" y="{CARD_Y}" width="{CARD_W}" height="9" rx="4.5" fill="{color}"/>',
                f'<circle cx="{x + 30}" cy="{CARD_Y + 50}" r="7" fill="{color}" filter="url(#nodeGlow)"/>',
                f'<text x="{x + 48}" y="{CARD_Y + 57}" class="card-zh">{esc(cluster["zh"])}</text>',
                f'<text x="{x + 24}" y="{CARD_Y + 87}" class="card-en">{esc(cluster["en"])}</text>',
                f'<text x="{x + CARD_W - 24}" y="{CARD_Y + 67}" text-anchor="end" '
                f'font-size="32" font-weight="900" fill="{color}">{count}</text>',
                f'<line x1="{x + 24}" y1="{CARD_Y + 105}" x2="{x + CARD_W - 24}" y2="{CARD_Y + 105}" '
                'stroke="#35506c" stroke-width="1"/>',
            ]
        )

        cursor_y = CARD_Y + 136
        for category_id in cluster["categories"]:
            category = categories_by_id[category_id]
            entries = skills_by_category[category_id]
            parts.extend(
                [
                    f'<rect x="{x + 20}" y="{cursor_y - 18}" width="{CARD_W - 40}" height="28" rx="9" '
                    f'fill="{color}" opacity=".09"/>',
                    f'<text x="{x + 31}" y="{cursor_y + 2}" class="category">'
                    f'{category["order"]:02d} · {esc(category["zh"])}</text>',
                    f'<text x="{x + CARD_W - 31}" y="{cursor_y + 2}" text-anchor="end" '
                    f'font-size="13" font-weight="800" fill="{color}">{len(entries)}</text>',
                ]
            )
            cursor_y += 29
            rows = math.ceil(len(entries) / 2)
            for item_index, skill in enumerate(entries):
                column = item_index // rows
                row = item_index % rows
                skill_x = x + 29 + column * 194
                skill_y = cursor_y + row * 21
                label = short(skill["id"])
                full_title = f'{skill["title"]["zh-CN"]} · {skill["id"]}'
                parts.extend(
                    [
                        f'<circle cx="{skill_x}" cy="{skill_y - 4}" r="3.2" fill="{color}" opacity=".85"/>',
                        f'<text x="{skill_x + 10}" y="{skill_y}" class="skill"><title>{esc(full_title)}</title>'
                        f'{esc(label)}</text>',
                    ]
                )
            cursor_y += rows * 21 + 21

    parts.extend(
        [
            '<line x1="90" y1="1980" x2="3110" y2="1980" stroke="#29445f"/>',
            '<circle cx="105" cy="2025" r="5" fill="#49d8ff"/>',
            '<text x="124" y="2031" class="legend">主流程：发现证据 → 专业计算 → 数据智能 → 成果传播 → 审稿反馈</text>',
            '<circle cx="1320" cy="2025" r="5" fill="#38d8c5"/>',
            '<text x="1339" y="2031" class="legend">横向底座：实验自动化 · 文档处理 · 计算平台</text>',
            '<text x="3100" y="2031" text-anchor="end" class="legend">每个节点可安装 · 每条链路可组合 · 每项产出可审计</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


def build_skill_architecture(
    categories: list[dict] | None = None,
    skills: list[dict] | None = None,
) -> Path:
    categories = categories or load_json(ROOT / "catalog" / "categories.seed.json")
    skills = skills or load_json(ROOT / "catalog" / "skills.seed.json")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(architecture_svg(categories, skills), encoding="utf-8")
    return OUTPUT


def main() -> None:
    path = build_skill_architecture()
    print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
