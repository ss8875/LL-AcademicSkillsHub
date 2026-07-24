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
from build_skill_architecture import build_skill_architecture


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
        "本页由 `catalog/skills.seed.json` 自动生成，按科研任务分类展示全部技能及其功能。"
        "点击技能名称可查看对应的中文详细用法。"
        if zh else
        "This page is generated from `catalog/skills.seed.json`. Quality status is an evidence level, not a marketing label; "
        "`cataloged` means indexed and structurally checked, not runtime-verified."
    )
    lines = [title, "", intro, ""]
    for category in categories:
        entries = [item for item in skills if item["category"] == category["id"]]
        heading = category["zh" if zh else "en"]
        lines.extend([f"## {category['order']:02d}. {heading} ({len(entries)})", ""])
        lines.append("| 技能 | 功能 |" if zh else "| Skill | Function | Source | Status |")
        lines.append("|---|---|" if zh else "|---|---|---|---|")
        for item in entries:
            display = item["title"][lang]
            summary = item["summary"][lang].replace("|", "\\|").replace("\n", " ")
            link = f"../{item['paths'][lang]}"
            if zh:
                lines.append(f"| [{display}]({link}) | {summary} |")
                continue
            source = (
                "Lianlin first-party" if item["source"]["kind"] == "lianlin-first-party"
                else "Pinned third-party"
            )
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


def zh_installation() -> str:
    """Render the complete Chinese local deployment and skill installation guide."""
    return """## 安装说明

LL-AcademicSkillsHub 的本地使用分为两个层次，请先确认自己需要哪一种：

| 你的目的 | 应执行的步骤 | 完成后得到什么 |
|---|---|---|
| 浏览、搜索和阅读全部技能 | 完成“部署本地技能目录” | 一个只在本机运行的技能检索网站，可查看 18 个分类、187 项技能及详细用法 |
| 让本地 Agent 实际调用技能 | 先部署目录，再完成“安装技能到本地 Agent” | 技能目录被复制到 Agent 的技能路径，重启 Agent 后即可按技能名称或自然语言调用 |
| 不想配置本地环境 | 使用上方链邻科研 AI 平台入口 | 通过一体化平台使用科研能力 |

### 1. 准备环境

| 项目 | 最低要求 | 用途 |
|---|---|---|
| 操作系统 | Windows 10/11、macOS 12+ 或常见 Linux 发行版 | 运行本地目录和脚本 |
| Python | 3.10 或更高版本 | 构建、检查并启动本地技能目录 |
| Git | 可选 | 克隆仓库和获取后续更新；没有 Git 也可以下载 ZIP |
| 磁盘空间 | 至少 100 MB | 保存仓库、目录数据和说明文档 |
| Node.js | 18 或更高版本，仅安装 Agent 技能时需要 | 通过 `npx skills` 选择和复制技能 |

先在终端检查已经安装的版本：

```text
python --version
git --version
node --version
npm --version
```

只部署本地技能目录时，**不需要 Node.js、Docker、数据库或额外 Python 包**。如果只缺少 Git，可以在 GitHub 项目页点击 `Code → Download ZIP`，解压后继续下面的步骤。

### 2. 方式一：部署本地技能目录

#### 2.1 下载项目

推荐使用 Git，这样后续可以直接更新：

```powershell
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
```

如果下载的是 ZIP，请完整解压，然后在终端进入解压后的 `LL-AcademicSkillsHub` 目录。后续命令必须在项目根目录执行，不要停留在 `C:\\Windows\\System32` 等系统目录。

#### 2.2 Windows 自动部署

在项目根目录打开 PowerShell：

```powershell
.\\scripts\setup.ps1
.\\scripts\start.ps1
```

`setup.ps1` 会依次完成四件事：

1. 检查 Python 是否达到 3.10；
2. 首次运行时把 `.env.example` 复制为本机 `.env`；
3. 重新生成中英文目录和 187 项技能说明；
4. 执行仓库审计和本地环境诊断。

出现 `Setup complete` 后再执行 `start.ps1`。如果 PowerShell 提示禁止执行脚本，不需要修改系统策略，直接使用仓库提供的批处理入口：

```bat
scripts\setup.bat
scripts\start.bat
```

#### 2.3 macOS 或 Linux 部署

```bash
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
cp .env.example .env
python3 scripts/build_catalog.py
python3 scripts/validate_repo.py
python3 scripts/doctor.py
python3 scripts/serve.py
```

前三个 Python 命令分别负责生成目录、审计仓库和检查环境；最后一个命令启动本地网站。

#### 2.4 打开、停止和重新启动

看到下面的提示说明服务已经启动：

```text
LL-AcademicSkillsHub: http://127.0.0.1:8765/site/
Press Ctrl+C to stop.
```

在浏览器打开：

```text
http://127.0.0.1:8765/
```

根地址会自动跳转到 `/site/`。启动服务的终端窗口需要保持打开；按 `Ctrl+C` 可安全停止，之后再次运行 `scripts\\start.ps1` 或 `python3 scripts/serve.py` 即可重新启动。

#### 2.5 修改端口和访问范围

默认配置保存在项目根目录的 `.env`：

```dotenv
LL_HOST=127.0.0.1
LL_PORT=8765
```

端口被占用时，可以把 `LL_PORT` 改为 `9000`，或临时指定：

```powershell
.\\scripts\start.ps1 --port 9000
```

`127.0.0.1` 表示只有本机可以访问。除非已经配置防火墙、访问控制、反向代理和 TLS，否则不要把 `LL_HOST` 改成 `0.0.0.0`。

#### 2.6 验证部署是否成功

Windows：

```powershell
python scripts\doctor.py
python -m unittest discover -s tests -v
```

macOS / Linux：

```bash
python3 scripts/doctor.py
python3 -m unittest discover -s tests -v
```

`doctor.py` 输出中的 `"ready": true` 表示目录和站点文件齐全；测试应以 `OK` 结束。浏览器中还应能够搜索技能、切换 18 个分类并打开“详细用法”。

#### 2.7 获取项目更新

使用 Git 安装时：

```powershell
git pull
.\\scripts\setup.ps1
```

macOS / Linux 把第二条替换为前面的三个生成与检查命令。使用 ZIP 时，需要重新下载新版并解压；如果修改过 `.env`，更新前请先备份该文件。

### 3. 方式二：安装技能到本地 Agent

仓库中的实际技能位于 `skills/<分类>/<技能名>/`，每个技能以完整的 `SKILL.md` 目录为安装单元。已经实测 `npx skills` 可以从本仓库识别全部 **187 项技能**。

#### 3.1 查看可安装技能

先安装 Node.js 18 或更高版本，然后运行：

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --list
```

正常结果会显示 `Found 187 skills`，并列出 `ll-paper-search`、`ll-paper-analysis`、`scanpy`、`scientific-writing` 等技能名称。

#### 3.2 把全部技能安装到 Codex

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex --skill '*' --yes --copy
```

`--global` 表示所有本地项目都可使用；`--agent codex` 指定目标 Agent；`--skill '*'` 选择全部技能；`--copy` 保留完整技能目录，而不是只复制单个 `SKILL.md`。

#### 3.3 只给当前项目安装一个技能

省略 `--global` 即安装到当前项目。下面示例只安装链邻论文检索技能：

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --agent codex --skill ll-paper-search --yes --copy
```

将 `ll-paper-search` 替换为 `--list` 返回的任意技能名即可。

#### 3.4 一次安装一组科研工作流

例如同时安装论文检索、精读和引用审计：

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex `
  --skill ll-paper-search `
  --skill ll-paper-analysis `
  --skill ll-citation-audit `
  --yes --copy
```

在 macOS / Linux 中把 PowerShell 换行符 `` ` `` 改为反斜杠 `\\`，也可以把命令写在同一行。

#### 3.5 检查、更新并让技能生效

```powershell
npx skills list --global --agent codex --json
npx skills update --global --yes
```

安装或更新后需要**完全关闭并重新打开 Agent 会话**，让它重新扫描技能目录。安装工具负责复制技能文件；某些专业技能所需的 Python/R 包、外部程序、模型或 API 凭据，应在真正使用该技能时按“详细用法”配置。

### 4. 常见问题

| 现象 | 原因 | 处理方法 |
|---|---|---|
| `python` 无法识别 | Python 未安装或未加入 PATH | 安装 Python 3.10+，Windows 安装时勾选 `Add Python to PATH`，重开终端 |
| `git` 无法识别 | Git 未安装 | 安装 Git，或直接使用 GitHub 的 `Download ZIP` |
| `winget` 无法识别 | 当前 Windows 没有 Windows 包管理器 | 本项目不依赖 `winget`；从 Python、Git 或 Node.js 官网下载安装即可 |
| PowerShell 禁止运行脚本 | 系统执行策略限制 | 使用 `scripts\\setup.bat` 和 `scripts\\start.bat` |
| `npx` 无法识别 | Node.js/npm 未安装或终端尚未刷新 | 安装 Node.js 18+，关闭并重新打开终端 |
| 端口 8765 被占用 | 其他程序正在使用该端口 | 运行 `scripts\\start.ps1 --port 9000`，或修改 `.env` |
| 浏览器打不开页面 | 服务未启动、终端已关闭或地址错误 | 重新启动服务并打开 `http://127.0.0.1:8765/` |
| Agent 看不到新技能 | Agent 在安装前已经启动 | 完全退出 Agent，重新打开后再检查技能列表 |
| 技能已安装但执行失败 | 缺少该技能的专业运行依赖 | 打开对应“详细用法”，按需安装依赖并配置凭据 |

更完整的系统说明也可查看[本地部署文档](./docs/deployment.zh-CN.md)。
"""


def en_installation() -> str:
    """Render the complete English local deployment and skill installation guide."""
    return """## Installation

Local use has two separate layers. Choose the one that matches your goal:

| Goal | What to complete | Result |
|---|---|---|
| Browse, search, and read every skill | Deploy the local skill catalog | A private local website covering 18 categories, 187 skills, and their detailed guides |
| Let a local Agent invoke skills | Deploy the catalog, then install skills into the Agent | Complete skill directories in the Agent's skill path, available after the Agent restarts |
| Avoid local configuration | Use the Lianlin Research AI Platform entry above | Integrated access to the research capabilities |

### 1. Prerequisites

| Component | Minimum | Purpose |
|---|---|---|
| Operating system | Windows 10/11, macOS 12+, or a mainstream Linux distribution | Run the local catalog and scripts |
| Python | 3.10 or newer | Build, validate, and serve the catalog |
| Git | Optional | Clone and update the repository; a ZIP download also works |
| Disk | At least 100 MB | Store the repository, catalog data, and guides |
| Node.js | 18 or newer, only for Agent skill installation | Select and copy skills with `npx skills` |

Check installed versions:

```text
python --version
git --version
node --version
npm --version
```

The local catalog itself needs **no Node.js, Docker, database, or third-party Python package**. If Git is unavailable, select `Code → Download ZIP` on GitHub, extract the archive, and continue below.

### 2. Method one: Deploy the local skill catalog

#### 2.1 Download the repository

Git is recommended because it makes later updates simple:

```powershell
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
```

For a ZIP download, extract the complete archive and open a terminal in the extracted `LL-AcademicSkillsHub` directory. Run every following command from the repository root, not from a system directory such as `C:\\Windows\\System32`.

#### 2.2 Automated Windows setup

Open PowerShell in the repository root:

```powershell
.\\scripts\setup.ps1
.\\scripts\start.ps1
```

`setup.ps1` checks Python 3.10+, creates the local `.env` file on first run, regenerates the bilingual catalog and all 187 guides, then runs the repository audit and environment doctor.

After `Setup complete` appears, run `start.ps1`. If PowerShell blocks script execution, use the supplied batch entry points without changing the system execution policy:

```bat
scripts\setup.bat
scripts\start.bat
```

#### 2.3 macOS or Linux setup

```bash
git clone https://github.com/ss8875/LL-AcademicSkillsHub.git
cd LL-AcademicSkillsHub
cp .env.example .env
python3 scripts/build_catalog.py
python3 scripts/validate_repo.py
python3 scripts/doctor.py
python3 scripts/serve.py
```

The first three Python commands generate the catalog, audit the repository, and check the environment. The last command starts the local website.

#### 2.4 Open, stop, and restart

A successful start prints:

```text
LL-AcademicSkillsHub: http://127.0.0.1:8765/site/
Press Ctrl+C to stop.
```

Open `http://127.0.0.1:8765/`; the root URL redirects to `/site/`. Keep the terminal open while using the site. Press `Ctrl+C` to stop it safely, then run `scripts\\start.ps1` or `python3 scripts/serve.py` to restart.

#### 2.5 Change the port or bind address

Local settings live in `.env`:

```dotenv
LL_HOST=127.0.0.1
LL_PORT=8765
```

If the port is busy, change `LL_PORT` to `9000` or run:

```powershell
.\\scripts\start.ps1 --port 9000
```

`127.0.0.1` allows access only from the same computer. Do not change it to `0.0.0.0` unless firewall rules, access control, a reverse proxy, and TLS are already configured.

#### 2.6 Verify the deployment

Windows:

```powershell
python scripts\doctor.py
python -m unittest discover -s tests -v
```

macOS / Linux:

```bash
python3 scripts/doctor.py
python3 -m unittest discover -s tests -v
```

`"ready": true` in the doctor output confirms that the catalog and site exist; the tests should finish with `OK`. The browser should let you search skills, switch among 18 categories, and open detailed guides.

#### 2.7 Update the repository

For a Git installation:

```powershell
git pull
.\\scripts\setup.ps1
```

On macOS or Linux, rerun the generation and validation commands above after `git pull`. ZIP users should download and extract the new version; back up a customized `.env` first.

### 3. Method two: Install skills into a local Agent

Installable units live under `skills/<category>/<skill-name>/` and retain their complete `SKILL.md` directories. The repository has been tested with `npx skills`, which discovers all **187 skills**.

#### 3.1 List available skills

Install Node.js 18 or newer, then run:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --list
```

A successful scan prints `Found 187 skills` and names such as `ll-paper-search`, `ll-paper-analysis`, `scanpy`, and `scientific-writing`.

#### 3.2 Install every skill globally for Codex

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex --skill '*' --yes --copy
```

`--global` makes the skills available to all local projects; `--agent codex` selects the target Agent; `--skill '*'` selects every skill; and `--copy` preserves each complete skill directory.

#### 3.3 Install one skill for the current project

Omit `--global` for a project-scoped installation:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --agent codex --skill ll-paper-search --yes --copy
```

Replace `ll-paper-search` with any exact name returned by `--list`.

#### 3.4 Install a research workflow

For example, install paper search, close reading, and citation audit together:

```powershell
npx skills add ss8875/LL-AcademicSkillsHub --global --agent codex `
  --skill ll-paper-search `
  --skill ll-paper-analysis `
  --skill ll-citation-audit `
  --yes --copy
```

On macOS or Linux, replace the PowerShell continuation character `` ` `` with `\\`, or place the command on one line.

#### 3.5 Check, update, and activate

```powershell
npx skills list --global --agent codex --json
npx skills update --global --yes
```

After installation or update, **fully close and reopen the Agent session** so it rescans its skill directories. The installer copies skill files; configure any specialized Python/R packages, external programs, models, or API credentials only when the selected detailed guide requires them.

### 4. Troubleshooting

| Symptom | Cause | Resolution |
|---|---|---|
| `python` is not recognized | Python is missing or not on PATH | Install Python 3.10+; select `Add Python to PATH` on Windows, then reopen the terminal |
| `git` is not recognized | Git is missing | Install Git or use GitHub's `Download ZIP` |
| `winget` is not recognized | Windows Package Manager is unavailable | This project does not require `winget`; use the official Python, Git, or Node.js installers |
| PowerShell blocks scripts | Execution policy restriction | Use `scripts\\setup.bat` and `scripts\\start.bat` |
| `npx` is not recognized | Node.js/npm is missing or the terminal is stale | Install Node.js 18+, then reopen the terminal |
| Port 8765 is busy | Another process uses the port | Run `scripts\\start.ps1 --port 9000` or edit `.env` |
| The browser cannot connect | The service is stopped or the URL is wrong | Restart the service and open `http://127.0.0.1:8765/` |
| The Agent cannot see a new skill | The Agent started before installation | Exit the Agent completely, reopen it, and check the skill list |
| An installed skill fails at runtime | A specialized dependency is missing | Open that skill's detailed guide and configure the required dependency or credential |

See the [local deployment document](./docs/deployment.en.md) for the compact system reference.
"""


def readme(
    lang: str,
    payload: dict,
    showcase_descriptions: dict[str, str] | None = None,
    platform_release: dict | None = None,
) -> str:
    zh = lang == "zh-CN"
    summary = payload["summary"]
    platform_release = platform_release or {}
    platform_url = platform_release.get("downloadUrl", "")
    platform_version = platform_release.get("version", "")
    platform_size = platform_release.get("sizeMiB", "")
    platform_sha256 = platform_release.get("sha256", "")
    if zh:
        showcase = zh_skill_showcase(
            payload["categories"],
            payload["skills"],
            showcase_descriptions or {},
        )
        installation = zh_installation()
        return f"""<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub 链邻学术技能仓库" width="100%">
</p>

<p align="center">
  <strong>本地优先、中英双语、分级审计的学术 AI 技能仓库</strong><br>
  <a href="./README.en.md">English</a> ·
  <a href="./docs/skills.zh-CN.md">全部技能</a> ·
  <a href="./docs/deployment.zh-CN.md">本地部署</a> ·
  <a href="{platform_url}">下载科研 AI 平台</a> ·
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

## 技能架构图

<p align="center">
  <a href="./assets/brand/skill-architecture-map.svg">
    <img src="./assets/brand/skill-architecture-map.svg" alt="链邻学术技能仓库 187 项技能架构图" width="100%">
  </a>
</p>

<p align="center"><sub>从研究发现、专业计算、数据智能到成果传播，7 大能力域通过证据反馈与科研基础设施有机连接。点击图片查看可缩放全尺寸图。</sub></p>

<a id="lianlin-platform"></a>

## 不想本地安装？直接使用链邻科研 AI 平台

<p align="center">
  <a href="{platform_url}">
    <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="下载链邻科研 AI 平台或添加微信客服" width="100%">
  </a>
</p>

<p align="center">
  <a href="{platform_url}"><strong>⬇ 下载链邻科研 AI 平台 {platform_version}（Windows 安装版）</strong></a><br>
  <sub>约 {platform_size} MB · SHA-256：<code>{platform_sha256}</code></sub>
</p>

{showcase}

{installation}

## 质量与来源

`cataloged → beta → tested → verified → gold` 是逐级证据状态；收录不等于验证。第三方固定包保留上游指令，并单独标注来源与许可证复核状态。详见 [质量模型](./docs/quality-model.zh-CN.md)、[第三方声明](./THIRD_PARTY_NOTICES.md)与生成的[审计报告](./reports/audit.zh-CN.md)。

## 许可证

链邻原创代码与文档采用 Apache-2.0。第三方技能继续适用其上游条款，不能因进入本仓库而被自动视为 Apache-2.0。
"""
    installation = en_installation()
    return f"""<p align="center">
  <img src="./assets/brand/hero-bilingual.svg" alt="LL-AcademicSkillsHub" width="100%">
</p>

<p align="center">
  <strong>Local-first, bilingual, and evidence-tiered academic AI skills</strong><br>
  <a href="./README.md">中文</a> ·
  <a href="./docs/skills.en.md">All skills</a> ·
  <a href="./docs/deployment.en.md">Local setup</a> ·
  <a href="{platform_url}">Download Research AI Platform</a> ·
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

## Skill Architecture Map

<p align="center">
  <a href="./assets/brand/skill-architecture-map.svg">
    <img src="./assets/brand/skill-architecture-map.svg" alt="Architecture map connecting all 187 LL-AcademicSkillsHub skills" width="100%">
  </a>
</p>

<p align="center"><sub>Seven capability domains connect research discovery, domain computation, data intelligence, research operations, and scholarly communication. Click the image for the scalable full-size map.</sub></p>

<a id="lianlin-platform"></a>

## Don't want to install locally? Use Lianlin Research AI Platform

<p align="center">
  <a href="{platform_url}">
    <img src="./assets/brand/platform-promo/platform-wechat-banner.png" alt="Download Lianlin Research AI Platform or contact WeChat support" width="100%">
  </a>
</p>

<p align="center">
  <a href="{platform_url}"><strong>⬇ Download Lianlin Research AI Platform {platform_version} for Windows</strong></a><br>
  <sub>Approx. {platform_size} MB · SHA-256: <code>{platform_sha256}</code></sub>
</p>

{installation}

## Quality and provenance

`cataloged → beta → tested → verified → gold` are evidence levels; inclusion is not verification. Pinned third-party instructions remain upstream work and carry separate provenance and license-review status. See the [quality model](./docs/quality-model.en.md), [third-party notices](./THIRD_PARTY_NOTICES.md), and generated [audit report](./reports/audit.en.md).

## License

Lianlin first-party code and original documentation are Apache-2.0. Third-party skills remain under their upstream terms and do not become Apache-2.0 merely by inclusion.
"""


def main() -> None:
    categories = load_json(ROOT / "catalog" / "categories.seed.json")
    skills = load_json(ROOT / "catalog" / "skills.seed.json")
    build_skill_architecture(categories, skills)
    showcase_descriptions = load_json(
        ROOT / "catalog" / "showcase-descriptions.zh-CN.json"
    )["descriptions"]
    platform_release = load_json(ROOT / "catalog" / "platform-release.json")
    payload = catalog_payload(categories, skills)
    write_json(ROOT / "catalog" / "categories.json", categories)
    write_json(ROOT / "catalog" / "skills.json", skills)
    write_json(ROOT / "site" / "data" / "catalog.json", payload)
    platform_url = env_value("LIANLIN_PLATFORM_DOWNLOAD_URL") or platform_release["downloadUrl"]
    if not re.fullmatch(r"https://[^\s]+", platform_url):
        raise SystemExit("LIANLIN_PLATFORM_DOWNLOAD_URL must be blank or an https:// URL")
    write_json(
        ROOT / "site" / "config.json",
        {
            "platformDownloadUrl": platform_url,
            "platformVersion": platform_release["version"],
            "platformSizeMiB": platform_release["sizeMiB"],
            "platformSha256": platform_release["sha256"],
        },
    )
    guide_summary = build_all_skill_guides(categories, skills, showcase_descriptions)
    (ROOT / "docs" / "skills.zh-CN.md").write_text(skills_markdown(categories, skills, "zh-CN"), encoding="utf-8")
    (ROOT / "docs" / "skills.en.md").write_text(skills_markdown(categories, skills, "en"), encoding="utf-8")
    (ROOT / "docs" / "categories.zh-CN.md").write_text(categories_markdown(categories, skills, "zh-CN"), encoding="utf-8")
    (ROOT / "docs" / "categories.en.md").write_text(categories_markdown(categories, skills, "en"), encoding="utf-8")
    (ROOT / "README.md").write_text(
        readme("zh-CN", payload, showcase_descriptions, platform_release),
        encoding="utf-8",
    )
    (ROOT / "README.en.md").write_text(
        readme("en", payload, platform_release=platform_release),
        encoding="utf-8",
    )
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
