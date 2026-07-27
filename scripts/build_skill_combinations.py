#!/usr/bin/env python3
"""Build 50 deterministic, clickable skill-combination SVG maps."""

from __future__ import annotations

import html
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_FILE = ROOT / "catalog" / "skills.seed.json"
COMBINATIONS_FILE = ROOT / "catalog" / "skill-combinations.json"
OUTPUT_DIR = ROOT / "assets" / "brand" / "skill-combinations"
WIDTH = 1920
HEIGHT = 1080

PALETTES = {
    "研究发现与证据治理": ("#4F8CFF", "#75D7FF", "#0E2146"),
    "研究设计与项目治理": ("#8A7CFF", "#C3A8FF", "#221A50"),
    "学术表达与成果传播": ("#F06CB5", "#FFB5D9", "#471331"),
    "组学与生命科学": ("#14C9A8", "#76F2D2", "#0B3A35"),
    "药物发现与蛋白工程": ("#FF9D4D", "#FFD18A", "#4B2810"),
    "临床与精准医学": ("#FF647C", "#FFB0BE", "#4A1320"),
    "数据科学与人工智能": ("#9A7BFF", "#67D4FF", "#251B55"),
    "物理、材料与复杂系统": ("#F5C451", "#FFE59A", "#463510"),
    "自动化、经济与空间研究": ("#56B6FF", "#7FF0C5", "#113652"),
}

RADIAL_PATTERNS = {
    "radar",
    "triangulation",
    "fan-out",
    "visual-orchestra",
    "evidence-fusion",
    "network-fusion",
    "clinical-evidence-fusion",
    "macro-dashboard",
    "spatial-evidence",
}

LOOP_PATTERNS = {
    "closed-loop",
    "verification-loop",
    "review-loop",
    "traceability-chain",
    "atlas-loop",
    "analysis-loop",
    "design-build-test",
    "inference-loop",
    "simulation-loop",
    "systems-loop",
    "automation-loop",
}

PATTERN_NAMES = {
    "radar": "多源前沿雷达",
    "pipeline": "顺序交付链",
    "evidence-chain": "证据锚定链",
    "closed-loop": "闭环审计",
    "verification-loop": "交叉核验",
    "design-funnel": "研究设计漏斗",
    "proposal-stack": "申请论证栈",
    "triangulation": "三角互证",
    "decision-gate": "决策门",
    "review-loop": "审稿反馈环",
    "traceability-chain": "全链追溯",
    "fan-out": "多媒介分发",
    "visual-orchestra": "视觉协同",
    "data-foundation": "数据基础链",
    "atlas-loop": "图谱迭代环",
    "mechanism-chain": "机制推断链",
    "feature-pipeline": "特征工程链",
    "tree-building": "树模型构建",
    "evidence-fusion": "多证据融合",
    "platform-stack": "平台分层栈",
    "analysis-loop": "分析复核环",
    "curation-pipeline": "数据治理链",
    "model-stack": "模型分层栈",
    "screening-funnel": "筛选漏斗",
    "identification-ladder": "鉴定证据梯",
    "compute-stack": "计算验证栈",
    "network-fusion": "网络证据融合",
    "annotation-stack": "多层注释栈",
    "design-build-test": "设计—实验闭环",
    "translational-funnel": "转化证据漏斗",
    "clinical-evidence-fusion": "临床证据融合",
    "imaging-stack": "影像处理栈",
    "compliance-gates": "合规质量门",
    "signal-to-outcome": "信号—结局链",
    "human-in-the-loop": "专家在环",
    "baseline-pipeline": "基线工程链",
    "forecast-arena": "预测竞技场",
    "inference-loop": "推断校验环",
    "simulation-loop": "仿真学习环",
    "mlops-stack": "模型治理栈",
    "graph-stack": "图学习分层栈",
    "pareto-engine": "多目标引擎",
    "benchmark-arena": "跨框架基准",
    "observation-pipeline": "观测证据链",
    "verification-ladder": "数值验证梯",
    "discovery-funnel": "发现漏斗",
    "systems-loop": "系统反馈环",
    "automation-loop": "自动化闭环",
    "macro-dashboard": "宏观多源融合",
    "spatial-evidence": "空间证据网",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap_text(value: str, limit: int, max_lines: int) -> list[str]:
    """Wrap mixed Chinese/English text without external font metrics."""
    units: list[str] = []
    current = ""
    current_width = 0.0
    for char in value.strip():
        width = 1.0 if ord(char) > 255 else 0.58
        if current and current_width + width > limit:
            units.append(current.strip())
            current = char
            current_width = width
        else:
            current += char
            current_width += width
    if current.strip():
        units.append(current.strip())
    if len(units) > max_lines:
        units = units[:max_lines]
        units[-1] = units[-1][:-1] + "…" if units[-1] else "…"
    return units


def text_lines(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: int,
    fill: str,
    weight: int = 400,
    anchor: str = "start",
    line_height: float = 1.35,
    family: str = "'Microsoft YaHei','Noto Sans CJK SC','Segoe UI',sans-serif",
) -> str:
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else size * line_height
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy:.1f}">{esc(line)}</tspan>')
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" fill="{fill}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" font-family="{family}">'
        + "".join(tspans)
        + "</text>"
    )


def rounded_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str,
    stroke: str = "none",
    stroke_width: float = 1,
    radius: float = 24,
    opacity: float = 1,
    filter_id: str | None = None,
) -> str:
    filter_attr = f' filter="url(#{filter_id})"' if filter_id else ""
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{radius:.1f}" fill="{fill}" fill-opacity="{opacity}" '
        f'stroke="{stroke}" stroke-width="{stroke_width}"{filter_attr}/>'
    )


def connector(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    color: str,
    *,
    dashed: bool = False,
    marker: bool = True,
    opacity: float = 0.7,
) -> str:
    dx = (x2 - x1) * 0.45
    dash = ' stroke-dasharray="9 9"' if dashed else ""
    marker_attr = ' marker-end="url(#arrow)"' if marker else ""
    return (
        f'<path d="M {x1:.1f} {y1:.1f} C {x1 + dx:.1f} {y1:.1f}, '
        f'{x2 - dx:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}" fill="none" '
        f'stroke="{color}" stroke-width="2.4" stroke-opacity="{opacity}"'
        f'{dash}{marker_attr}/>'
    )


def skill_link(skill: dict) -> str:
    return "../../../" + skill["paths"]["zh-CN"].replace("\\", "/")


def node_card(
    x: float,
    y: float,
    w: float,
    h: float,
    node: dict,
    skill: dict,
    category_name: str,
    index: int,
    primary: str,
    accent: str,
) -> str:
    title = skill["title"]["zh-CN"]
    title_is_latin = not any("\u3400" <= char <= "\u9fff" for char in title)
    title_is_long = len(title) > (23 if title_is_latin else 12)
    title_size = 15 if title_is_latin else (15 if title_is_long else 18)
    title_limit = 14 if title_is_latin else 13
    title_lines = wrap_text(title, title_limit, 2 if title_is_long else 1)
    id_y = y + (64 if len(title_lines) > 1 else 51)
    role_y = y + (101 if len(title_lines) > 1 else 90)
    role_lines = wrap_text(node["role"], 18, 2)
    handoff_lines = wrap_text(node["handoff"], 19, 2)
    parts = [f'<a href="{esc(skill_link(skill))}" target="_top">']
    parts.append(f"<title>{esc(title)} · {esc(category_name)} · {esc(node['role'])}</title>")
    parts.append(
        rounded_rect(
            x,
            y,
            w,
            h,
            fill="#101C36",
            stroke=primary,
            stroke_width=1.4,
            radius=24,
            opacity=0.98,
            filter_id="shadow",
        )
    )
    parts.append(
        f'<circle cx="{x + 32:.1f}" cy="{y + 32:.1f}" r="18" '
        f'fill="{primary}" fill-opacity="0.2" stroke="{accent}" stroke-width="1.5"/>'
    )
    parts.append(text_lines(x + 32, y + 39, [f"{index:02d}"], size=14, fill="#FFFFFF", weight=700, anchor="middle"))
    parts.append(
        text_lines(
            x + 58,
            y + 27,
            title_lines,
            size=title_size,
            fill="#F7FAFF",
            weight=700,
            line_height=1.1,
        )
    )
    parts.append(
        text_lines(
            x + 58,
            id_y,
            wrap_text(skill["id"], 30, 1),
            size=12,
            fill="#8294B7",
            weight=500,
            family="'Cascadia Mono','Segoe UI Mono',monospace",
        )
    )
    parts.append(text_lines(x + 22, role_y, role_lines, size=16, fill="#C9D5EC", weight=500, line_height=1.25))
    parts.append(
        rounded_rect(
            x + 18,
            y + h - 46,
            w - 36,
            30,
            fill=primary,
            stroke="none",
            radius=11,
            opacity=0.13,
        )
    )
    parts.append(text_lines(x + 32, y + h - 26, ["交接"], size=11, fill=accent, weight=700))
    parts.append(
        text_lines(
            x + 78,
            y + h - 26,
            handoff_lines[:1],
            size=12,
            fill="#E7EEFC",
            weight=500,
        )
    )
    parts.append("</a>")
    return "".join(parts)


def base_svg(combo: dict, number: int, primary: str, accent: str, deep: str) -> list[str]:
    title_lines = wrap_text(combo["title"], 56, 2)
    goal_lines = wrap_text(combo["goal"], 72, 2)
    return [
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
            f'aria-labelledby="title desc">'
        ),
        f"<title id=\"title\">{esc(combo['title'])}</title>",
        f"<desc id=\"desc\">{esc(combo['goal'])}</desc>",
        "<defs>",
        (
            f'<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="#07101F"/><stop offset="0.55" stop-color="#0A1630"/>'
            f'<stop offset="1" stop-color="{deep}"/></linearGradient>'
        ),
        (
            f'<radialGradient id="glow" cx="50%" cy="40%" r="60%">'
            f'<stop offset="0" stop-color="{primary}" stop-opacity="0.22"/>'
            f'<stop offset="1" stop-color="{primary}" stop-opacity="0"/></radialGradient>'
        ),
        '<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M 48 0 L 0 0 0 48" fill="none" stroke="#8DA2C7" stroke-opacity="0.055" stroke-width="1"/></pattern>',
        '<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="18" flood-color="#000814" flood-opacity="0.45"/></filter>',
        f'<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="{accent}"/></marker>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>',
        f'<ellipse cx="1030" cy="430" rx="760" ry="510" fill="url(#glow)"/>',
        f'<rect x="0" y="0" width="12" height="{HEIGHT}" fill="{primary}"/>',
        rounded_rect(64, 52, 176, 40, fill=primary, radius=12, opacity=0.16),
        text_lines(152, 78, [f"组合 {number:02d} / 50"], size=15, fill=accent, weight=700, anchor="middle"),
        rounded_rect(252, 52, 250, 40, fill="#FFFFFF", radius=12, opacity=0.055),
        text_lines(377, 78, [combo["chapter"]], size=14, fill="#AAB9D4", weight=600, anchor="middle"),
        rounded_rect(1540, 52, 316, 40, fill="#FFFFFF", radius=12, opacity=0.055),
        text_lines(
            1698,
            78,
            [PATTERN_NAMES.get(combo["pattern"], combo["pattern"])],
            size=14,
            fill=accent,
            weight=600,
            anchor="middle",
        ),
        text_lines(64, 141, title_lines, size=42, fill="#F8FAFF", weight=800),
        text_lines(66, 210 if len(title_lines) == 1 else 248, goal_lines, size=18, fill="#9DAECC", weight=400),
    ]


def bottom_panels(combo: dict, primary: str, accent: str) -> str:
    y = 864
    h = 152
    gap = 18
    widths = [420, 520, 420, 420]
    xs = [64]
    for width in widths[:-1]:
        xs.append(xs[-1] + width + gap)
    labels = ["研究输入", "协同增益", "最终产出", "质量门"]
    values = [combo["input"], combo["gain"], combo["output"], combo["quality"]]
    parts: list[str] = []
    for index, (x, width, label, value) in enumerate(zip(xs, widths, labels, values)):
        parts.append(
            rounded_rect(
                x,
                y,
                width,
                h,
                fill="#0C1830",
                stroke=primary if index in {1, 2} else "#314260",
                stroke_width=1.2,
                radius=22,
                opacity=0.96,
            )
        )
        parts.append(text_lines(x + 24, y + 31, [label], size=13, fill=accent if index in {1, 2} else "#8FA2C4", weight=700))
        parts.append(
            text_lines(
                x + 24,
                y + 64,
                wrap_text(value, 23 if width < 500 else 31, 3),
                size=15,
                fill="#D5DEEF",
                weight=500,
            )
        )
    parts.append(text_lines(64, 1054, ["LL-AcademicSkillsHub · 链邻学术技能仓库"], size=12, fill="#61718E", weight=600))
    parts.append(text_lines(1856, 1054, ["每个节点可点击查看详细用法"], size=12, fill="#61718E", weight=500, anchor="end"))
    return "".join(parts)


def pipeline_layout(
    combo: dict,
    skill_index: dict[str, dict],
    category_index: dict[str, str],
    primary: str,
    accent: str,
) -> str:
    nodes = combo["skills"]
    count = len(nodes)
    parts: list[str] = []
    positions: list[tuple[float, float]] = []
    card_w, card_h = (310, 178)
    if count <= 4:
        total = count * card_w + (count - 1) * 44
        start_x = (WIDTH - total) / 2
        positions = [(start_x + i * (card_w + 44), 430) for i in range(count)]
    else:
        first_count = math.ceil(count / 2)
        second_count = count - first_count
        first_total = first_count * card_w + (first_count - 1) * 62
        second_total = second_count * card_w + max(0, second_count - 1) * 62
        first_start = (WIDTH - first_total) / 2
        second_start = (WIDTH - second_total) / 2
        positions.extend((first_start + i * (card_w + 62), 316) for i in range(first_count))
        positions.extend(
            (second_start + (second_count - 1 - i) * (card_w + 62), 612)
            for i in range(second_count)
        )
    for index in range(count - 1):
        x1, y1 = positions[index]
        x2, y2 = positions[index + 1]
        if abs(y2 - y1) < 10:
            if x2 > x1:
                parts.append(connector(x1 + card_w, y1 + card_h / 2, x2, y2 + card_h / 2, accent))
            else:
                parts.append(connector(x1, y1 + card_h / 2, x2 + card_w, y2 + card_h / 2, accent))
        else:
            parts.append(connector(x1 + card_w / 2, y1 + card_h, x2 + card_w / 2, y2, accent))
    if combo["pattern"] in LOOP_PATTERNS and count >= 3:
        x_last, y_last = positions[-1]
        x_first, y_first = positions[0]
        parts.append(
            f'<path d="M {x_last + card_w / 2:.1f} {y_last + card_h:.1f} '
            f'C {x_last + card_w / 2:.1f} 835, {x_first + card_w / 2:.1f} 835, '
            f'{x_first + card_w / 2:.1f} {y_first + card_h:.1f}" fill="none" '
            f'stroke="{primary}" stroke-width="2" stroke-dasharray="10 10" '
            f'stroke-opacity="0.65" marker-end="url(#arrow)"/>'
        )
        parts.append(text_lines(960, 828, ["反馈、复核与迭代"], size=13, fill=accent, weight=700, anchor="middle"))
    for index, (node, (x, y)) in enumerate(zip(nodes, positions), 1):
        skill = skill_index[node["id"]]
        parts.append(
            node_card(
                x,
                y,
                card_w,
                card_h,
                node,
                skill,
                category_index[skill["category"]],
                index,
                primary,
                accent,
            )
        )
    return "".join(parts)


def radial_layout(
    combo: dict,
    skill_index: dict[str, dict],
    category_index: dict[str, str],
    primary: str,
    accent: str,
    loop: bool,
) -> str:
    nodes = combo["skills"]
    count = len(nodes)
    cx, cy = 960, 518
    radius_x, radius_y = 560, 245
    card_w, card_h = 320, 178
    start_angle = -math.pi / 2
    positions: list[tuple[float, float]] = []
    for index in range(count):
        angle = start_angle + 2 * math.pi * index / count
        px = cx + radius_x * math.cos(angle) - card_w / 2
        py = cy + radius_y * math.sin(angle) - card_h / 2
        positions.append((px, py))
    parts: list[str] = []
    for x, y in positions:
        parts.append(connector(x + card_w / 2, y + card_h / 2, cx, cy, primary, dashed=not loop, marker=False, opacity=0.35))
    if loop:
        for index in range(count):
            x1, y1 = positions[index]
            x2, y2 = positions[(index + 1) % count]
            parts.append(
                connector(
                    x1 + card_w / 2,
                    y1 + card_h / 2,
                    x2 + card_w / 2,
                    y2 + card_h / 2,
                    accent,
                    opacity=0.45,
                )
            )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="132" fill="{primary}" fill-opacity="0.12" stroke="{primary}" stroke-width="1.8"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="112" fill="#0D1A33" stroke="{accent}" stroke-opacity="0.45" stroke-width="1.2"/>')
    parts.append(text_lines(cx, cy - 34, ["协同核心"], size=14, fill=accent, weight=700, anchor="middle"))
    parts.append(text_lines(cx, cy + 4, wrap_text(combo["gain"], 18, 4), size=15, fill="#E4EBF8", weight=600, anchor="middle"))
    for index, (node, (x, y)) in enumerate(zip(nodes, positions), 1):
        skill = skill_index[node["id"]]
        parts.append(
            node_card(
                x,
                y,
                card_w,
                card_h,
                node,
                skill,
                category_index[skill["category"]],
                index,
                primary,
                accent,
            )
        )
    return "".join(parts)


def build_map(
    combo: dict,
    number: int,
    skill_index: dict[str, dict],
    category_index: dict[str, str],
) -> str:
    primary, accent, deep = PALETTES[combo["chapter"]]
    parts = base_svg(combo, number, primary, accent, deep)
    if combo["pattern"] in RADIAL_PATTERNS:
        parts.append(radial_layout(combo, skill_index, category_index, primary, accent, loop=False))
    elif combo["pattern"] in LOOP_PATTERNS:
        parts.append(radial_layout(combo, skill_index, category_index, primary, accent, loop=True))
    else:
        parts.append(pipeline_layout(combo, skill_index, category_index, primary, accent))
    parts.append(bottom_panels(combo, primary, accent))
    parts.append("</svg>")
    return "".join(parts)


def main() -> None:
    skills = load_json(SKILLS_FILE)
    combinations = load_json(COMBINATIONS_FILE)
    categories = load_json(ROOT / "catalog" / "categories.seed.json")
    skill_index = {item["id"]: item for item in skills}
    category_index = {item["id"]: item["zh"] for item in categories}
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for number, combo in enumerate(combinations, 1):
        path = OUTPUT_DIR / f"{combo['id']}.svg"
        path.write_text(
            build_map(combo, number, skill_index, category_index),
            encoding="utf-8",
        )
    print(f"Generated {len(combinations)} SVG maps in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
