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


def readme(lang: str, payload: dict, showcase_descriptions: dict[str, str] | None = None) -> str:
    zh = lang == "zh-CN"
    summary = payload["summary"]
    if zh:
        showcase = zh_skill_showcase(
            payload["categories"],
            payload["skills"],
            showcase_descriptions or {},
        )
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

## 立即开始

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

浏览器打开 `http://127.0.0.1:8765/`。也可运行 `scripts\\setup.bat` 和 `scripts\\start.bat`。

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

## Quick start

```powershell
./scripts/setup.ps1
./scripts/start.ps1
```

Open `http://127.0.0.1:8765/`. Windows users may also run `scripts\\setup.bat` and `scripts\\start.bat`.

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
