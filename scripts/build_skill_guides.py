#!/usr/bin/env python3
"""Build detailed Chinese usage guides for every catalog skill.

The guide structure is intentionally stable so README links, documentation,
and repository tests can treat it as a public documentation contract. Content
is grounded in the canonical catalog record, the original SKILL.md outline,
and the files actually bundled with each skill.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

STOP_WORDS = {
    "a", "an", "and", "as", "at", "be", "by", "for", "from", "in", "into",
    "is", "it", "of", "on", "or", "that", "the", "this", "to", "use", "using",
    "when", "with", "skill", "skills", "scientific", "research",
}

HEADING_ZH = {
    "overview": "能力概览",
    "when to use this skill": "适用场景",
    "when to use": "适用场景",
    "quick start": "快速开始",
    "quick start guide": "快速开始",
    "workflow": "工作流程",
    "core workflow": "核心流程",
    "workflow summary": "流程摘要",
    "usage": "使用方式",
    "setup": "准备与配置",
    "configuration": "配置",
    "common tasks": "常见任务",
    "examples": "示例",
    "example workflows": "示例流程",
    "best practices": "最佳实践",
    "core principles and best practices": "核心原则与最佳实践",
    "common pitfalls": "常见问题",
    "common pitfalls to avoid": "应避免的问题",
    "limitations": "限制",
    "security": "安全",
    "validation": "验证",
    "final checklist": "最终检查清单",
    "output contract": "产出契约",
    "resources": "资源",
    "tools and scripts": "工具与脚本",
    "dependencies": "依赖",
    "integration with other skills": "与其他技能集成",
    "bilingual guidance": "双语说明",
    "pricing": "费用与配额",
    "complementary skills": "互补技能",
    "summary": "总结",
}


CATEGORY_GUIDES = {
    "literature-management": {
        "focus": "把研究问题转化为可复核的检索、筛选、引用与证据记录",
        "workflow": [
            "界定研究问题、学科范围、时间窗与纳排口径",
            "构造检索或采集策略，并保留数据库、查询式和日期",
            "清洗、去重、筛选并核对题录或全文证据",
            "把结果整理成可追溯的文献记录、引用数据或证据表",
        ],
        "boundary": [
            "数据库未检出不等于证据不存在，必须说明覆盖范围和检索日期",
            "题录、摘要和全文证据的可信层级不同，不应混为同一证据强度",
            "引用信息必须核对稳定标识符，不凭记忆补造 DOI、作者或页码",
        ],
    },
    "scientific-communication": {
        "focus": "把证据、方法和结论组织为清楚、准确、适配目标读者的学术表达",
        "workflow": [
            "明确文稿类型、目标读者、期刊或资助机构要求",
            "锁定事实、数据、术语、引用和不可改动的学术含义",
            "先搭建论证结构，再逐段完成写作、审阅或语言优化",
            "核对主张与证据、格式规范、术语一致性和修改痕迹",
        ],
        "boundary": [
            "不为增强说服力而虚构结果、引用、审稿意见或研究贡献",
            "语言润色不能替代方法学、统计学和领域专家审查",
            "涉及署名、利益冲突、伦理和投稿承诺时，以真实记录为准",
        ],
    },
    "presentation-visualization": {
        "focus": "把数据和论点转化为准确、易读、可编辑并适合传播的科研视觉材料",
        "workflow": [
            "定义视觉材料要传达的核心结论、受众和使用媒介",
            "核对数据结构、图形类型、版式尺寸与期刊或会务规范",
            "生成图表、页面或视觉草稿，并保留可编辑源文件",
            "检查标注、配色、可访问性、分辨率和数据—图形一致性",
        ],
        "boundary": [
            "不把示意图或 AI 生成图当作真实实验图像和定量结果",
            "不通过截断坐标轴、隐藏样本或不当配色制造误导性视觉结论",
            "图中统计标注、样本量和误差定义必须来自已核验数据",
        ],
    },
    "research-methods": {
        "focus": "把研究问题落实为可检验、可执行、可复现并能识别偏倚的方法方案",
        "workflow": [
            "明确研究问题、假设、分析单位与目标效应",
            "设计采样、对照、测量、随机化或质性研究程序",
            "预先定义排除、缺失、偏倚控制和判定规则",
            "形成协议、分析计划、风险清单与复现记录",
        ],
        "boundary": [
            "方法建议不能替代伦理审批、临床判断和法定合规程序",
            "不能在看到结果后静默改写假设、终点或排除规则",
            "样本量与效应判断需要领域参数，缺失时必须明确不确定性",
        ],
    },
    "bioinformatics-genomics": {
        "focus": "对序列、组学和基因组数据执行可追溯的处理、统计与生物学解释",
        "workflow": [
            "确认物种、参考版本、实验平台、样本设计和数据格式",
            "执行质量控制、标准化、比对、定量或特征构建",
            "完成统计比较、功能注释或多组学整合",
            "输出参数、软件版本、中间结果与可复现分析记录",
        ],
        "boundary": [
            "参考基因组、注释版本和数据库日期会影响结果，必须记录",
            "技术批次、样本混淆和低质量数据不能靠下游统计自动消除",
            "生物信息学关联不自动构成因果或临床有效性证据",
        ],
    },
    "cheminformatics-drug-discovery": {
        "focus": "围绕分子结构、性质、相互作用和候选优先级开展计算药物发现",
        "workflow": [
            "规范化分子、靶点、测定条件和结构表示",
            "选择描述符、预测、对接、筛选或生成方法",
            "运行计算并记录模型、参数、随机种子和适用域",
            "按活性、选择性、可合成性与风险形成候选排序",
        ],
        "boundary": [
            "计算评分和生成分子不是实验活性、安全性或成药性的证明",
            "结构标准化、质子化状态和测定条件差异会显著影响比较",
            "候选结论必须经实验验证，并遵守化学品、药物和知识产权规范",
        ],
    },
    "clinical-precision-medicine": {
        "focus": "组织临床、影像和分子证据，为研究分析与精确医学决策提供结构化支持",
        "workflow": [
            "确认研究或病例范围、数据来源、终点与人群定义",
            "完成脱敏、质量控制、特征提取和证据分级",
            "执行统计、影像或精准医学分析并标注不确定性",
            "输出供临床或研究团队复核的结构化报告",
        ],
        "boundary": [
            "技能产出不构成诊断、处方或个体医疗建议",
            "真实患者数据必须满足知情同意、隐私、伦理和访问控制要求",
            "模型性能必须在目标人群和外部数据上验证，不能直接跨人群外推",
        ],
    },
    "protein-structural-biology": {
        "focus": "围绕蛋白序列、结构、功能、相互作用与工程设计形成可验证分析",
        "workflow": [
            "确认序列、构建体、物种、结构来源和目标功能",
            "执行结构检索、预测、比较、注释或设计",
            "评估置信度、构象、界面、保守性和实验可行性",
            "输出结构文件、位点建议、证据和验证实验清单",
        ],
        "boundary": [
            "预测结构和计算设计不等同于真实构象、结合或功能",
            "编号体系、亚型、翻译后修饰和实验条件必须明确",
            "关键位点与设计候选需要生化、细胞或结构实验验证",
        ],
    },
    "machine-learning-ai": {
        "focus": "构建、训练、评估和解释适用于科研数据的机器学习与人工智能模型",
        "workflow": [
            "定义任务、预测目标、数据粒度、评价指标与基线",
            "划分数据并建立防止泄漏的预处理和验证流程",
            "训练或调用模型，记录参数、版本、种子和计算环境",
            "评估泛化、校准、误差、偏倚和可解释性后交付模型产物",
        ],
        "boundary": [
            "测试集、未来信息或同源样本泄漏会使性能失真",
            "单一指标不能代表模型的稳健性、公平性和实际效用",
            "生成或预测结果必须标注模型来源、置信度和人工复核要求",
        ],
    },
    "materials-physics": {
        "focus": "通过物理建模、材料模拟和科学计算研究结构—性质关系",
        "workflow": [
            "定义物理体系、边界条件、近似、单位和目标观测量",
            "准备结构、势函数、基组、网格或数值求解设置",
            "运行模拟并检查收敛性、守恒量和数值稳定性",
            "比较基准、实验或理论结果并保存可复现输入输出",
        ],
        "boundary": [
            "模拟结果只在模型假设、参数和收敛范围内成立",
            "单位、坐标、周期边界和数值精度错误会导致系统性偏差",
            "高成本计算应先做小规模验证，不直接把未收敛结果用于结论",
        ],
    },
    "data-analysis-statistics": {
        "focus": "把原始数据转化为透明、可复现且统计含义清楚的分析结果",
        "workflow": [
            "定义分析单位、变量字典、终点、缺失和排除规则",
            "检查数据质量、分布、异常值和采集过程",
            "选择与设计相匹配的统计模型并进行诊断",
            "报告效应量、不确定性、敏感性分析和可复现代码",
        ],
        "boundary": [
            "统计显著不等于实际重要、临床重要或因果关系",
            "不能静默删除异常值、改变分析单位或只报告有利结果",
            "模型假设、缺失机制、多重比较和样本依赖必须检查",
        ],
    },
    "scientific-databases": {
        "focus": "从专业科学数据库检索、整合和规范化可信记录",
        "workflow": [
            "明确实体类型、标识符、数据库范围和版本日期",
            "构造查询并记录字段、过滤器、分页和命中数",
            "解析、规范化、去重并处理跨库标识符映射",
            "输出带来源、版本和查询记录的结构化数据集",
        ],
        "boundary": [
            "数据库记录可能滞后、缺失或彼此冲突，必须保留来源与版本",
            "跨数据库标识符不应仅靠名称模糊匹配",
            "接口配额、许可、隐私和再分发限制必须遵守",
        ],
    },
    "lab-automation": {
        "focus": "把实验协议转化为可执行、可追踪并具备安全约束的自动化流程",
        "workflow": [
            "确认实验目的、材料、耗材、仪器型号和安全限制",
            "把协议拆为有状态步骤、体积、速度、温度和等待条件",
            "先模拟或小规模验证，再连接仪器执行",
            "保存运行日志、偏差、错误、样本位置和恢复步骤",
        ],
        "boundary": [
            "未经验证的代码不得直接控制真实仪器或处理危险材料",
            "体积、单位、板位、死体积和碰撞风险必须独立复核",
            "自动化不能替代实验室安全培训、设备手册和人工监护",
        ],
    },
    "document-data-tools": {
        "focus": "读取、生成、转换和检查科研文档、表格、演示与结构化文件",
        "workflow": [
            "确认源文件、目标格式、版式要求和需保留的结构元素",
            "解析内容与样式，选择无损编辑或受控转换路径",
            "生成新文件并保留原件、版本和中间产物",
            "渲染或重新读取结果，检查内容、公式、链接和版式",
        ],
        "boundary": [
            "格式转换可能丢失批注、公式、字体或布局，必须进行回读验证",
            "不覆盖用户原始文件，除非任务明确要求并已留存可恢复副本",
            "受密码、权限或数字签名保护的文档不得绕过访问控制",
        ],
    },
    "finance-economics": {
        "focus": "组织金融、企业与宏观经济数据，开展可追溯的研究分析",
        "workflow": [
            "定义市场、标的、指标、频率、币种和研究时间窗",
            "采集并对齐数据来源、交易日、复权、单位和发布日期",
            "执行描述、计量、估值或情景分析并检查稳健性",
            "报告假设、数据时点、不确定性和可复现计算",
        ],
        "boundary": [
            "历史数据和模型结果不保证未来表现，也不构成投资建议",
            "前视偏差、幸存者偏差、修订数据和时区错位必须处理",
            "付费数据、个人金融数据和交易接口受许可与合规限制",
        ],
    },
    "geospatial-remote-sensing": {
        "focus": "对地理、遥感和地球观测数据进行可靠的空间处理与分析",
        "workflow": [
            "确认研究区域、坐标参考系、空间分辨率和时间范围",
            "完成影像或矢量数据的质量控制、投影和预处理",
            "执行空间统计、分类、变化检测或地理计算",
            "输出地图、栅格、矢量、精度评估和处理记录",
        ],
        "boundary": [
            "坐标系、分辨率、重采样和空间配准错误会改变结论",
            "地图精度和遥感分类必须用独立参考数据验证",
            "敏感地理位置、个人轨迹和受限影像必须按权限处理",
        ],
    },
    "platform-infrastructure": {
        "focus": "配置稳定、可复现并可审计的科研计算环境和任务基础设施",
        "workflow": [
            "盘点操作系统、硬件、依赖、存储、网络和安全需求",
            "固定环境、软件与数据版本并配置最小权限",
            "先以小任务验证，再执行编排、并行或云端工作负载",
            "保存日志、资源用量、失败恢复和可复现环境说明",
        ],
        "boundary": [
            "基础设施操作可能产生费用、数据暴露或资源破坏风险",
            "密钥不得写入仓库、日志、截图或面向用户的产物",
            "扩容与并行前必须验证任务正确性、配额和停止条件",
        ],
    },
    "academic-core": {
        "focus": "用链邻原创证据工作流贯通选题、检索、精读、写作、审计与成果治理",
        "workflow": [
            "明确研究目标、证据标准、责任边界和最终交付物",
            "收集并定位来源，分开事实、推断、不确定性与建议",
            "按技能契约完成分析、写作、审计或治理任务",
            "输出证据锚点、未决问题、质量检查和可交接产物",
        ],
        "boundary": [
            "不虚构来源、元数据、研究结果、法律状态或专业结论",
            "高风险临床、伦理、法律、专利与知识产权事项必须专业复核",
            "明确缺失信息和覆盖限制，不把未核验推断写成已证实事实",
        ],
    },
}


FLOW_SKILLS = {
    "literature-management": ("ll-topic-analysis", "scientific-writing"),
    "scientific-communication": ("literature-review", "scientific-slides"),
    "presentation-visualization": ("statistical-analysis", "venue-templates"),
    "research-methods": ("ll-topic-analysis", "statistical-analysis"),
    "bioinformatics-genomics": ("ena-database", "statistical-analysis"),
    "cheminformatics-drug-discovery": ("chembl-database", "pdb-database"),
    "clinical-precision-medicine": ("clinicaltrials-database", "scientific-writing"),
    "protein-structural-biology": ("pdb-database", "diffdock"),
    "machine-learning-ai": ("exploratory-data-analysis", "scientific-visualization"),
    "materials-physics": ("modal", "statistical-analysis"),
    "data-analysis-statistics": ("scientific-critical-thinking", "scientific-visualization"),
    "scientific-databases": ("literature-review", "exploratory-data-analysis"),
    "lab-automation": ("scientific-critical-thinking", "exploratory-data-analysis"),
    "document-data-tools": ("get-available-resources", "scientific-writing"),
    "finance-economics": ("datacommons-client", "statistical-analysis"),
    "geospatial-remote-sensing": ("geo-database", "scientific-visualization"),
    "platform-infrastructure": ("scientific-critical-thinking", "exploratory-data-analysis"),
    "academic-core": ("literature-review", "scientific-writing"),
}


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()


def relative_link(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, start=from_file.parent).replace("\\", "/")


def tokens(item: dict) -> set[str]:
    text = " ".join(
        [
            item["id"].replace("-", " "),
            item["title"]["en"],
            item["summary"]["en"],
            " ".join(item["capabilities"]["en"]),
        ]
    ).lower()
    return {
        token
        for token in re.findall(r"[a-z0-9][a-z0-9.+#-]*", text)
        if len(token) > 2 and token not in STOP_WORDS
    }


def ranked_candidates(item: dict, candidates: list[dict]) -> list[dict]:
    source_tokens = tokens(item)

    def score(candidate: dict) -> tuple[float, str]:
        candidate_tokens = tokens(candidate)
        overlap = len(source_tokens & candidate_tokens)
        union = len(source_tokens | candidate_tokens) or 1
        return (overlap / union + overlap * 0.01, candidate["id"])

    return sorted(candidates, key=score, reverse=True)


def related_skills(item: dict, skills: list[dict], count: int = 3) -> list[dict]:
    candidates = [
        candidate
        for candidate in skills
        if candidate["id"] != item["id"] and candidate["category"] == item["category"]
    ]
    return ranked_candidates(item, candidates)[:count]


def skill_by_id(skills: list[dict], skill_id: str) -> dict:
    for item in skills:
        if item["id"] == skill_id:
            return item
    raise ValueError(f"Unknown relationship skill: {skill_id}")


def source_headings(skill_file: Path) -> list[str]:
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    headings = re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
    result: list[str] = []
    for heading in headings:
        clean = re.sub(r"[`*_]", "", heading).strip()
        key = clean.lower()
        translated = HEADING_ZH.get(key)
        clean = re.sub(r"\bSkill\b", "技能", clean, flags=re.IGNORECASE)
        clean = re.sub(r"\bPhase\b", "阶段", clean, flags=re.IGNORECASE)
        if (
            not translated
            and re.search(r"[\u3400-\u9fff]", clean)
            and not re.search(r"[A-Za-z]{4,}", clean)
        ):
            translated = clean
        if not translated:
            rules = [
                (("workflow", "how it works", "how to", "phase", "pipeline"), "工作流程"),
                (("example", "gallery", "demo", "preview"), "示例与预览"),
                (("resource", "reference", "attribution", "built by"), "参考资料"),
                (("practice", "guideline", "standard", "rule"), "实践规范"),
                (("pitfall", "troubleshoot", "error", "limitation", "consideration", "not"), "边界与问题排查"),
                (("output", "result", "deliverable"), "产出要求"),
                (("input", "requirement"), "输入要求"),
                (("method", "strategy", "approach"), "方法与策略"),
                (("install", "setup", "authentication", "environment", "dependency"), "安装与配置"),
                (("script", "command", "api", "technical"), "脚本与接口"),
                (("quality", "validation", "checklist", "rigor", "tone"), "质量检查"),
                (("model", "mode", "option", "parameter", "configuration", "selection"), "模式与参数"),
                (("integration", "complementary", "ecosystem"), "协同与集成"),
                (("capabilit", "principle", "concept", "feature"), "核心能力与原则"),
                (("use", "task", "pattern", "application"), "常见用法"),
                (("structure", "section", "criteria", "category", "type"), "任务结构"),
                (("overview", "introduction", "summary"), "能力概览"),
            ]
            translated = next(
                (label for keywords, label in rules if any(word in key for word in keywords)),
                "专题说明",
            )
        if translated not in result:
            result.append(translated)
    return result[:8]


def bundled_files(skill_root: Path) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {
        "参考资料": [],
        "执行脚本": [],
        "模板与素材": [],
        "其他随附文件": [],
    }
    for path in sorted(skill_root.rglob("*")):
        if not path.is_file() or path.name == "SKILL.md" or "locales" in path.parts:
            continue
        rel = path.relative_to(skill_root)
        if rel.parts[0] == "references":
            groups["参考资料"].append(path)
        elif rel.parts[0] == "scripts":
            groups["执行脚本"].append(path)
        elif rel.parts[0] == "assets":
            groups["模板与素材"].append(path)
        else:
            groups["其他随附文件"].append(path)
    return groups


def resource_section(locale_file: Path, skill_file: Path) -> list[str]:
    skill_root = skill_file.parent
    groups = bundled_files(skill_root)
    lines = [
        f"- [原始 `SKILL.md`]({relative_link(locale_file, skill_file)})：权威执行指令与完整技术细节。",
    ]
    total = sum(len(paths) for paths in groups.values())
    if total == 0:
        lines.append("- 本技能没有额外打包的参考、脚本或素材；执行时以原始 `SKILL.md` 为准。")
        return lines

    lines.append(f"- 随技能打包 **{total}** 个文件，按用途完整列出如下。")
    for label, paths in groups.items():
        if not paths:
            continue
        lines.extend(["", f"### {label}（{len(paths)}）", ""])
        for path in paths:
            display = path.relative_to(skill_root).as_posix()
            annotation = {
                "参考资料": "方法、规范或领域约束参考",
                "执行脚本": "可复用执行或验证脚本",
                "模板与素材": "可复用模板、样式或示例素材",
                "其他随附文件": "技能运行或说明所需的随附文件",
            }[label]
            lines.append(
                f"- [`{display}`]({relative_link(locale_file, path)})：{annotation}。"
            )
    return lines


def render_guide(
    item: dict,
    skills: list[dict],
    category_names: dict[str, str],
    descriptions: dict[str, str],
) -> str:
    locale_file = ROOT / item["paths"]["zh-CN"]
    skill_file = ROOT / item["paths"]["skill"]
    title = item["title"]["zh-CN"]
    category_name = category_names[item["category"]]
    profile = CATEGORY_GUIDES[item["category"]]
    description = (
        item["summary"]["zh-CN"]
        if item["source"]["kind"] == "lianlin-first-party"
        else descriptions[item["id"]].strip()
    )
    capabilities = item["capabilities"]["zh-CN"]
    inputs = item["inputs"]["zh-CN"]
    outputs = item["outputs"]["zh-CN"]
    headings = source_headings(skill_file)
    same_category = related_skills(item, skills)
    upstream_id, downstream_id = FLOW_SKILLS[item["category"]]
    upstream = skill_by_id(skills, upstream_id)
    downstream = skill_by_id(skills, downstream_id)

    overview_link = relative_link(locale_file, ROOT / "README.md")
    english_link = relative_link(locale_file, ROOT / item["paths"]["en"])
    source_link = relative_link(locale_file, skill_file)
    input_text = "；".join(inputs)
    output_text = "；".join(outputs)
    capability_text = "；".join(capabilities)
    outline = " → ".join(f"`{heading}`" for heading in headings) if headings else "原始执行指令"

    lines = [
        f"# {title}",
        "",
        f"[返回技能总览]({overview_link}) · [English]({english_link}) · [查看原始 SKILL]({source_link})",
        "",
        "## 1. 技能简介",
        "",
        description,
        "",
        f"它属于“{category_name}”类别，核心定位是：{profile['focus']}。"
        f"本说明把原始技能的技术内容整理为中文使用契约；涉及具体命令、参数或版本时，"
        f"仍以[原始 `SKILL.md`]({source_link})及随附文件为准。",
        "",
        "## 2. 适合用它做什么",
        "",
    ]
    lines.extend(f"- {capability}" for capability in capabilities)
    lines.extend(
        [
            f"- 当你已有“{input_text}”，并希望得到“{output_text}”时使用。",
            f"- 当任务需要围绕“{profile['focus']}”形成可复核、可继续加工的中间产物时使用。",
            "",
            "不建议仅因为技能名称相近就直接调用；先确认研究对象、输入格式和预期产出与本页描述一致。",
            "",
            "## 3. 工作方式",
            "",
            f"本技能按“输入契约 → 执行 → 验证 → 交付”工作。原始指令的重点阅读路径为：{outline}。",
            "",
        ]
    )
    for index, step in enumerate(profile["workflow"], start=1):
        if index == 1:
            detail = f"本技能至少需要：{input_text}。"
        elif index == 3:
            detail = f"执行重点包括：{capability_text}。"
        elif index == 4:
            detail = f"最终交付：{output_text}。"
        else:
            detail = "保留关键选择、参数、筛选条件和中间结果，便于复核。"
        lines.append(f"{index}. **{step}。** {detail}")
    lines.extend(
        [
            "5. **交付前复核。** 检查结果是否回答原始问题，是否区分事实、推断和不确定性，是否留下足够的复现与交接信息。",
            "",
            "## 4. 请求说明",
            "",
            "你可以直接用自然语言提出任务。一个高质量请求最好同时写清目标、输入、约束、产出格式和验收标准。",
            "",
            "### 推荐请求模板",
            "",
            f"> 请使用“{title}”处理【{input_text}】。目标是【写明研究目标】；"
            f"请遵守【时间范围、对象范围、格式或方法约束】，输出【{output_text}】，"
            "并列出关键步骤、证据来源、不确定性和需要人工确认的事项。",
            "",
            "### 可直接改写的请求",
            "",
            f"- “请用 {title} 完成{capabilities[0]}。我的材料是【{inputs[0]}】，结果请整理为【{outputs[0]}】。”",
            f"- “请先检查我提供的【{inputs[0]}】是否足够，再用 {title} 执行{capabilities[-1]}；不要补造缺失信息。”",
            f"- “请把 {title} 的处理过程做成可复核记录，交付【{output_text}】，同时标出假设、限制和下一步建议。”",
            "",
            "## 5. 示例预览",
            "",
            "| 环节 | 示例内容 |",
            "|---|---|",
            f"| 任务目标 | 使用 **{title}** 完成“{capabilities[0]}” |",
            f"| 输入材料 | {markdown_escape(input_text)} |",
            f"| 处理重点 | {markdown_escape(capability_text)} |",
            f"| 预期产出 | {markdown_escape(output_text)} |",
            f"| 验收重点 | 结果可追溯、关键假设明确、与“{profile['focus']}”的目标一致 |",
            "",
            "示例只展示交付形态，不替代真实任务中的数据、参数、伦理审批、领域判断或人工复核。",
            "",
            "## 6. 你需要提供",
            "",
        ]
    )
    lines.extend(f"- **必需输入：**{value}。" for value in inputs)
    lines.extend(
        [
            "- **任务目标：**要回答的问题、使用场景和完成标准。",
            "- **范围限制：**研究对象、时间范围、排除条件、语言、格式或目标期刊等。",
            "- **已有材料：**原始数据、文献、代码、图表、协议或草稿；请说明版本及允许使用的范围。",
            "- **交付偏好：**文件格式、字段结构、是否需要脚本、是否保留中间结果与审计记录。",
            "",
            "如果上述信息不全，应先列出缺口并向用户确认；不能把猜测当作用户已提供的事实。",
            "",
            "## 7. 产出",
            "",
        ]
    )
    lines.extend(f"- {value}。" for value in outputs)
    lines.extend(
        [
            "- 一份简明的方法与参数说明，记录关键选择、版本、过滤或排除规则。",
            "- 一份质量检查与未决问题清单，标出不能自动确认、需要领域专家复核的部分。",
            "- 如任务产生文件，优先保留可编辑源文件，并将派生产物与用户原始材料分开。",
            "",
            "## 8. 内置参考",
            "",
        ]
    )
    lines.extend(resource_section(locale_file, skill_file))
    lines.extend(
        [
            "",
            "仅在相关步骤需要时读取相应参考或脚本；运行脚本前应检查参数、输入路径、输出路径及是否会修改文件。",
            "",
            "## 9. 边界",
            "",
        ]
    )
    lines.extend(f"- {boundary}。" for boundary in profile["boundary"])
    lines.extend(
        [
            f"- 本技能的职责是“{profile['focus']}”，不能替代与任务相关的伦理、临床、法律、安全或领域专家审查。",
            "- 外部数据、接口和模型的内容可能变化；重要结论应保存来源、访问时间和稳定标识。",
            "",
            "## 10. 相关技能",
            "",
        ]
    )
    for related in same_category:
        related_file = ROOT / related["paths"]["zh-CN"]
        related_description = (
            related["summary"]["zh-CN"]
            if related["source"]["kind"] == "lianlin-first-party"
            else descriptions[related["id"]].strip()
        )
        lines.append(
            f"- [{related['title']['zh-CN']}]({relative_link(locale_file, related_file)})："
            f"{related_description}"
        )
    lines.extend(
        [
            "",
            "这些技能与本技能处于相近任务域。组合使用前先划分每个技能的输入、输出和责任边界，避免重复处理或相互覆盖。",
            "",
            "## 11. 与其他技能的关系",
            "",
        ]
    )
    upstream_file = ROOT / upstream["paths"]["zh-CN"]
    downstream_file = ROOT / downstream["paths"]["zh-CN"]
    lines.extend(
        [
            f"- **上游准备：**[{upstream['title']['zh-CN']}]({relative_link(locale_file, upstream_file)})"
            f"可用于准备或核对本技能所需的“{input_text}”。",
            f"- **本技能职责：**{title} 聚焦于“{profile['focus']}”，负责完成“{capability_text}”。",
            f"- **下游承接：**[{downstream['title']['zh-CN']}]({relative_link(locale_file, downstream_file)})"
            f"可继续使用本技能产生的“{output_text}”开展后续分析、表达或交付。",
            f"- **分工原则：**若任务重点已经从“{profile['focus']}”转移到其他领域，"
            "应把本技能的可追溯产出作为交接材料，而不是让一个技能包办全部科研流程。",
            "",
        ]
    )
    return "\n".join(lines)


def build_all_skill_guides(
    categories: list[dict],
    skills: list[dict],
    descriptions: dict[str, str],
) -> dict[str, int]:
    category_names = {category["id"]: category["zh"] for category in categories}
    missing_profiles = set(category_names) - set(CATEGORY_GUIDES)
    if missing_profiles:
        raise ValueError(f"Missing Chinese guide profiles: {sorted(missing_profiles)}")

    third_party = {
        item["id"] for item in skills if item["source"]["kind"] != "lianlin-first-party"
    }
    missing_descriptions = third_party - set(descriptions)
    if missing_descriptions:
        raise ValueError(
            f"Missing Chinese guide descriptions: {sorted(missing_descriptions)}"
        )

    resource_files = 0
    for item in skills:
        locale_file = ROOT / item["paths"]["zh-CN"]
        skill_file = ROOT / item["paths"]["skill"]
        locale_file.parent.mkdir(parents=True, exist_ok=True)
        locale_file.write_text(
            render_guide(item, skills, category_names, descriptions),
            encoding="utf-8",
        )
        resource_files += sum(
            len(paths) for paths in bundled_files(skill_file.parent).values()
        )
    return {"guides": len(skills), "bundledFilesDocumented": resource_files}


def main() -> None:
    categories = json.loads(
        (ROOT / "catalog" / "categories.seed.json").read_text(encoding="utf-8")
    )
    skills = json.loads(
        (ROOT / "catalog" / "skills.seed.json").read_text(encoding="utf-8")
    )
    descriptions = json.loads(
        (ROOT / "catalog" / "showcase-descriptions.zh-CN.json").read_text(
            encoding="utf-8"
        )
    )["descriptions"]
    print(
        json.dumps(
            build_all_skill_guides(categories, skills, descriptions),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
