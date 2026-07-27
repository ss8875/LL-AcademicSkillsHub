#!/usr/bin/env python3
"""Build the Chinese gallery for all 50 skill-combination maps."""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMBINATIONS = ROOT / "catalog" / "skill-combinations.json"
SKILLS = ROOT / "catalog" / "skills.seed.json"
OUTPUT = ROOT / "docs" / "skill-combinations.zh-CN.md"


def main() -> None:
    combinations = json.loads(COMBINATIONS.read_text(encoding="utf-8"))
    skills = json.loads(SKILLS.read_text(encoding="utf-8"))
    skill_index = {item["id"]: item for item in skills}
    chapters: OrderedDict[str, list[dict]] = OrderedDict()
    for item in combinations:
        chapters.setdefault(item["chapter"], []).append(item)

    lines = [
        "# 187 项技能 · 50 个专业协作脑图",
        "",
        "这不是把技能名称排列在一起的海报。每张图都描述一个可执行科研任务：明确输入，分配 3–6 项技能的独立职责，标出技能之间交接的中间产物，并以最终产出和质量门收束。",
        "",
        "- **50** 个科研组合场景",
        "- **187 / 187** 项技能全覆盖",
        "- **245** 个技能协作席位",
        "- **45** 项枢纽技能跨流程复用",
        "- 每张图同时提供可编辑 SVG 与 1920×1080 PNG",
        "",
        "## 系统总览",
        "",
        '<p align="center">',
        '  <a href="../assets/brand/skill-combinations/index.svg">',
        '    <img src="../assets/brand/skill-combinations/index.svg" alt="187 项技能与 50 个协同工作流总览" width="100%">',
        "  </a>",
        "</p>",
        "",
        "## 怎样读一张图",
        "",
        "1. 先看顶部的研究目标与协作模式；",
        "2. 按编号和箭头读取技能职责；",
        "3. 查看每个节点底部的“交接”产物；",
        "4. 用底部的研究输入、协同增益、最终产出和质量门判断是否适合你的任务；",
        "5. 点击 SVG 中的技能节点，可以直接进入该技能的中文详细用法。",
        "",
        "## 九大协同系统",
        "",
    ]
    for index, (chapter, items) in enumerate(chapters.items(), 1):
        lines.append(f"- [{index:02d} · {chapter}](#chapter-{index:02d})：组合 {items[0]['id'][:2]}–{items[-1]['id'][:2]}")
    lines.append("")

    for chapter_index, (chapter, items) in enumerate(chapters.items(), 1):
        lines.extend(
            [
                f'<a id="chapter-{chapter_index:02d}"></a>',
                "",
                f"## {chapter_index:02d} · {chapter}",
                "",
            ]
        )
        for combo in items:
            number = combo["id"][:2]
            svg = f"../assets/brand/skill-combinations/{combo['id']}.svg"
            png = f"../assets/brand/skill-combinations/png/{combo['id']}.png"
            usage_parts = []
            for node_index, node in enumerate(combo["skills"]):
                skill = skill_index[node["id"]]
                if node_index == 0:
                    lead = "先由"
                elif node_index == len(combo["skills"]) - 1:
                    lead = "最后由"
                else:
                    lead = "再由"
                usage_parts.append(
                    f"{lead} **{skill['title']['zh-CN']}** {node['role']}，"
                    f"交付“{node['handoff']}”"
                )
            usage_sentence = "；".join(usage_parts) + "。"
            lines.extend(
                [
                    f'<details id="{combo["id"]}" open>',
                    f"<summary><strong>{number} · {combo['title']}</strong></summary>",
                    "",
                    f"> {combo['goal']}",
                    "",
                    '<p align="center">',
                    f'  <a href="{svg}">',
                    f'    <img src="{svg}" alt="{combo["title"]}" width="100%">',
                    "  </a>",
                    "</p>",
                    "",
                    f"**组合使用方式：**{usage_sentence}",
                    "",
                    f"**输入：**{combo['input']}<br>",
                    f"**产出：**{combo['output']}<br>",
                    f"**协同增益：**{combo['gain']}<br>",
                    f"**质量门：**{combo['quality']}",
                    "",
                    "**组合技能：**",
                    "",
                ]
            )
            for node in combo["skills"]:
                skill = skill_index[node["id"]]
                link = "../" + skill["paths"]["zh-CN"].replace("\\", "/")
                lines.append(
                    f"- [{skill['title']['zh-CN']}]({link})：{node['role']} → `{node['handoff']}`"
                )
            lines.extend(
                [
                    "",
                    f"[打开可编辑 SVG]({svg}) · [下载高清 PNG]({png})",
                    "",
                    "</details>",
                    "",
                ]
            )

    lines.extend(
        [
            "## 数据与质量审计",
            "",
            "- 权威组合数据：[`catalog/skill-combinations.json`](../catalog/skill-combinations.json)",
            "- 自动审计报告：[`reports/skill-combination-audit.zh-CN.md`](../reports/skill-combination-audit.zh-CN.md)",
            "- 视觉总检板：[`reports/skill-combination-contact-sheet.png`](../reports/skill-combination-contact-sheet.png)",
            "- 生成脚本：[`scripts/build_skill_combinations.py`](../scripts/build_skill_combinations.py)",
            "- 验证脚本：[`scripts/validate_skill_combinations.py`](../scripts/validate_skill_combinations.py)",
            "",
        ]
    )
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Built gallery: {OUTPUT}")


if __name__ == "__main__":
    main()
