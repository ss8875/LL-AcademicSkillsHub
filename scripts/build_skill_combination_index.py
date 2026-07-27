#!/usr/bin/env python3
"""Build the 50-map system overview SVG."""

from __future__ import annotations

import html
import json
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMBINATIONS = ROOT / "catalog" / "skill-combinations.json"
OUTPUT = ROOT / "assets" / "brand" / "skill-combinations" / "index.svg"
WIDTH = 1920
HEIGHT = 1080
COLORS = [
    "#4F8CFF",
    "#8A7CFF",
    "#F06CB5",
    "#14C9A8",
    "#FF9D4D",
    "#FF647C",
    "#9A7BFF",
    "#F5C451",
    "#56B6FF",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def wrap(value: str, limit: int, lines: int = 2) -> list[str]:
    result = [value[i : i + limit] for i in range(0, len(value), limit)]
    if len(result) > lines:
        result = result[:lines]
        result[-1] = result[-1][:-1] + "…"
    return result


def text(x: float, y: float, lines: list[str], size: int, fill: str, weight: int = 400, anchor: str = "start") -> str:
    body = "".join(
        f'<tspan x="{x}" dy="{0 if index == 0 else size * 1.35}">{esc(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" font-family="Microsoft YaHei,Noto Sans CJK SC,Segoe UI,sans-serif">{body}</text>'
    )


def main() -> None:
    combinations = json.loads(COMBINATIONS.read_text(encoding="utf-8"))
    chapters: OrderedDict[str, list[dict]] = OrderedDict()
    for item in combinations:
        chapters.setdefault(item["chapter"], []).append(item)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        "<title id=\"title\">187 项技能与 50 个协同工作流总览</title>",
        "<desc id=\"desc\">九大研究协同系统串联 50 张技能组合脑图，覆盖全部 187 项技能。</desc>",
        "<defs>",
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060D1A"/><stop offset="0.55" stop-color="#0A1730"/><stop offset="1" stop-color="#102347"/></linearGradient>',
        '<pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse"><path d="M50 0H0V50" fill="none" stroke="#8DA2C7" stroke-opacity=".06"/></pattern>',
        '<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="15" flood-color="#000814" flood-opacity=".45"/></filter>',
        '<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#77C9FF"/></marker>',
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/><rect width="{WIDTH}" height="{HEIGHT}" fill="url(#grid)"/>',
        '<circle cx="1600" cy="60" r="520" fill="#4F8CFF" fill-opacity=".08"/>',
        text(64, 72, ["LL-AcademicSkillsHub · 技能协同系统"], 15, "#78D8FF", 700),
        text(64, 137, ["187 项技能 · 50 个专业协作脑图"], 43, "#F8FAFF", 800),
        text(64, 179, ["每张图组合 3–6 项技能；全部技能至少出现一次；输入、交接、产出与质量门完整可审计。"], 18, "#AAB8D3", 400),
        '<rect x="1430" y="62" width="132" height="70" rx="18" fill="#4F8CFF" fill-opacity=".14" stroke="#4F8CFF"/>',
        '<rect x="1578" y="62" width="132" height="70" rx="18" fill="#14C9A8" fill-opacity=".14" stroke="#14C9A8"/>',
        '<rect x="1726" y="62" width="132" height="70" rx="18" fill="#F5C451" fill-opacity=".14" stroke="#F5C451"/>',
        text(1496, 91, ["187"], 25, "#FFFFFF", 800, "middle"),
        text(1496, 116, ["技能全覆盖"], 11, "#9FB1CF", 600, "middle"),
        text(1644, 91, ["245"], 25, "#FFFFFF", 800, "middle"),
        text(1644, 116, ["协作席位"], 11, "#9FB1CF", 600, "middle"),
        text(1792, 91, ["18"], 25, "#FFFFFF", 800, "middle"),
        text(1792, 116, ["专业类别"], 11, "#9FB1CF", 600, "middle"),
    ]

    card_w, card_h = 560, 220
    gap_x, gap_y = 48, 34
    start_x, start_y = 64, 232
    positions: list[tuple[float, float]] = []
    for index in range(9):
        row, col = divmod(index, 3)
        if row % 2 == 1:
            col = 2 - col
        positions.append((start_x + col * (card_w + gap_x), start_y + row * (card_h + gap_y)))

    for index in range(8):
        x1, y1 = positions[index]
        x2, y2 = positions[index + 1]
        if abs(y1 - y2) < 10:
            start = (x1 + card_w, y1 + card_h / 2) if x2 > x1 else (x1, y1 + card_h / 2)
            end = (x2, y2 + card_h / 2) if x2 > x1 else (x2 + card_w, y2 + card_h / 2)
            parts.append(
                f'<path d="M{start[0]} {start[1]} L{end[0]} {end[1]}" stroke="#77C9FF" '
                f'stroke-width="2" stroke-opacity=".45" marker-end="url(#arrow)"/>'
            )
        else:
            parts.append(
                f'<path d="M{x1 + card_w / 2} {y1 + card_h} C{x1 + card_w / 2} {y1 + card_h + 20}, '
                f'{x2 + card_w / 2} {y2 - 20}, {x2 + card_w / 2} {y2}" fill="none" stroke="#77C9FF" '
                f'stroke-width="2" stroke-opacity=".45" marker-end="url(#arrow)"/>'
            )

    for index, ((chapter, items), (x, y), color) in enumerate(zip(chapters.items(), positions, COLORS), 1):
        first = int(items[0]["id"][:2])
        last = int(items[-1]["id"][:2])
        parts.extend(
            [
                f'<a href="../../../docs/skill-combinations.zh-CN.md#chapter-{index:02d}">',
                f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="26" fill="#0D1931" stroke="{color}" stroke-width="1.5" filter="url(#shadow)"/>',
                f'<rect x="{x}" y="{y}" width="9" height="{card_h}" rx="4" fill="{color}"/>',
                f'<circle cx="{x + 48}" cy="{y + 44}" r="22" fill="{color}" fill-opacity=".16" stroke="{color}"/>',
                text(x + 48, y + 51, [f"{index:02d}"], 14, "#FFFFFF", 800, "middle"),
                text(x + 86, y + 42, [chapter], 22, "#F7FAFF", 750),
                text(x + 86, y + 70, [f"组合 {first:02d}–{last:02d} · {len(items)} 张图"], 12, color, 700),
                text(x + 28, y + 114, wrap(items[0]["title"], 25, 1), 15, "#C9D5EA", 600),
                text(x + 28, y + 145, wrap(items[-1]["title"], 25, 1), 15, "#A5B4D0", 500),
                f'<rect x="{x + 28}" y="{y + 174}" width="{card_w - 56}" height="26" rx="9" fill="{color}" fill-opacity=".10"/>',
                text(x + 42, y + 192, ["发现 → 获取 → 分析 → 验证 → 交付"], 12, color, 700),
                "</a>",
            ]
        )
    parts.extend(
        [
            text(64, 1044, ["研究发现 → 方案设计 → 领域研究 → 数据智能 → 学术交付 → 反馈回流"], 14, "#7D8EAD", 600),
            text(1856, 1044, ["点击任一系统进入完整 50 图图库"], 13, "#7D8EAD", 500, "end"),
            "</svg>",
        ]
    )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("".join(parts), encoding="utf-8")
    print(f"Built overview: {OUTPUT}")


if __name__ == "__main__":
    main()
