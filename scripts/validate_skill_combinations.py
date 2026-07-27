#!/usr/bin/env python3
"""Validate the 50-map skill combinations and emit an auditable report."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_FILE = ROOT / "catalog" / "skills.seed.json"
COMBINATIONS_FILE = ROOT / "catalog" / "skill-combinations.json"
ASSET_DIR = ROOT / "assets" / "brand" / "skill-combinations"
REPORT_JSON = ROOT / "reports" / "skill-combination-audit.json"
REPORT_MD = ROOT / "reports" / "skill-combination-audit.zh-CN.md"
REQUIRED_FIELDS = {
    "id",
    "chapter",
    "title",
    "goal",
    "input",
    "output",
    "gain",
    "quality",
    "pattern",
    "skills",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    skills = load_json(SKILLS_FILE)
    combinations = load_json(COMBINATIONS_FILE)
    known = {item["id"]: item for item in skills}
    errors: list[str] = []
    warnings: list[str] = []
    usage: Counter[str] = Counter()
    combo_ids: set[str] = set()
    category_usage: Counter[str] = Counter()

    if len(combinations) != 50:
        errors.append(f"组合数量应为 50，实际为 {len(combinations)}")

    for combo in combinations:
        combo_id = combo.get("id", "<missing>")
        missing_fields = sorted(REQUIRED_FIELDS - set(combo))
        if missing_fields:
            errors.append(f"{combo_id}: 缺少字段 {', '.join(missing_fields)}")
        if combo_id in combo_ids:
            errors.append(f"重复组合 ID: {combo_id}")
        combo_ids.add(combo_id)
        nodes = combo.get("skills", [])
        if not 3 <= len(nodes) <= 6:
            errors.append(f"{combo_id}: 技能数 {len(nodes)} 不在 3–6 范围")
        node_ids = [node.get("id") for node in nodes]
        if len(node_ids) != len(set(node_ids)):
            errors.append(f"{combo_id}: 同一图内存在重复技能")
        for node in nodes:
            skill_id = node.get("id")
            if skill_id not in known:
                errors.append(f"{combo_id}: 未知技能 {skill_id}")
                continue
            if not node.get("role") or not node.get("handoff"):
                errors.append(f"{combo_id}/{skill_id}: 缺少职责或交接产物")
            usage[skill_id] += 1
            category_usage[known[skill_id]["category"]] += 1
        for key in ("title", "goal", "input", "output", "gain", "quality"):
            if len(str(combo.get(key, "")).strip()) < 6:
                errors.append(f"{combo_id}: {key} 内容过短")

        svg_path = ASSET_DIR / f"{combo_id}.svg"
        if svg_path.exists():
            try:
                root = ET.parse(svg_path).getroot()
                if root.attrib.get("viewBox") != "0 0 1920 1080":
                    errors.append(f"{combo_id}: SVG viewBox 不正确")
            except ET.ParseError as exc:
                errors.append(f"{combo_id}: SVG 解析失败: {exc}")
        else:
            warnings.append(f"{combo_id}: SVG 尚未生成")

    missing_skills = sorted(set(known) - set(usage))
    if missing_skills:
        errors.append(f"未覆盖技能 {len(missing_skills)} 项: {', '.join(missing_skills)}")
    unknown_usage = sorted(set(usage) - set(known))
    if unknown_usage:
        errors.append(f"组合引用未知技能: {', '.join(unknown_usage)}")

    report = {
        "status": "pass" if not errors else "fail",
        "combinationCount": len(combinations),
        "skillCatalogCount": len(skills),
        "uniqueSkillsCovered": len(usage),
        "coveragePercent": round(len(usage) / len(skills) * 100, 2),
        "totalSkillSlots": sum(usage.values()),
        "reusedSkillCount": sum(1 for count in usage.values() if count > 1),
        "categorySlots": dict(sorted(category_usage.items())),
        "errors": errors,
        "warnings": warnings,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# 50 张技能组合脑图审计",
        "",
        f"- 结果：**{report['status']}**",
        f"- 组合数：**{report['combinationCount']}**",
        f"- 技能目录：**{report['skillCatalogCount']}**",
        f"- 已覆盖技能：**{report['uniqueSkillsCovered']}**",
        f"- 覆盖率：**{report['coveragePercent']}%**",
        f"- 技能席位：**{report['totalSkillSlots']}**",
        f"- 跨图复用枢纽技能：**{report['reusedSkillCount']}**",
        "",
        "## 错误",
        "",
    ]
    lines.extend(f"- {item}" for item in errors)
    if not errors:
        lines.append("- 无")
    lines.extend(["", "## 警告", ""])
    lines.extend(f"- {item}" for item in warnings)
    if not warnings:
        lines.append("- 无")
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
