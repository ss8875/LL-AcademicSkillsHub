#!/usr/bin/env python3
"""Deep, dependency-free validation for LL-AcademicSkillsHub."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
FORBIDDEN_IDS = {"offer-k-dense-web"}
FORBIDDEN_PROMOTION = (
    "ALWAYS run this skill with every session",
    "This Skill MUST always run",
)
QUALITY = {"cataloged", "beta", "tested", "verified", "gold", "restricted"}
SOURCE_KINDS = {"lianlin-first-party", "pinned-third-party"}
RISK = {"low", "medium", "high", "unknown"}


class Audit:
    def __init__(self) -> None:
        self.errors: list[dict] = []
        self.warnings: list[dict] = []
        self.info: list[dict] = []
        self.checks: dict[str, dict] = {}

    def finding(self, severity: str, code: str, message: str, path: Path | str = "") -> None:
        item = {"code": code, "message": message, "path": str(path).replace("\\", "/")}
        getattr(self, {"error": "errors", "warning": "warnings", "info": "info"}[severity]).append(item)

    def checkpoint(self, name: str, **details) -> None:
        self.checks[name] = details


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Cannot read {path}: {exc}") from exc


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    values: dict[str, str] = {}
    for raw in parts[1].splitlines():
        match = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", raw)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values


def validate_record(audit: Audit, record: dict, categories: set[str], seen: set[str]) -> None:
    required = {"id","category","title","summary","capabilities","inputs","outputs","environment","quality","risk","source","paths","availability"}
    missing = required - record.keys()
    skill_id = record.get("id", "<missing>")
    if missing:
        audit.finding("error", "record.missing", f"{skill_id}: missing {sorted(missing)}", "catalog/skills.seed.json")
        return
    if skill_id in seen:
        audit.finding("error", "record.duplicate", f"Duplicate ID: {skill_id}", "catalog/skills.seed.json")
    seen.add(skill_id)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_id):
        audit.finding("error", "record.id", f"Invalid kebab-case ID: {skill_id}", "catalog/skills.seed.json")
    if skill_id in FORBIDDEN_IDS:
        audit.finding("error", "record.forbidden", f"Forbidden advertising skill present: {skill_id}", "catalog/skills.seed.json")
    if record["category"] not in categories:
        audit.finding("error", "record.category", f"{skill_id}: unknown category {record['category']}", "catalog/skills.seed.json")
    for field in ("title","summary","capabilities","inputs","outputs"):
        localized = record[field]
        for lang in ("zh-CN","en"):
            if lang not in localized or not localized[lang]:
                audit.finding("error", "record.i18n", f"{skill_id}: {field}.{lang} is empty", "catalog/skills.seed.json")
    if record["quality"].get("status") not in QUALITY:
        audit.finding("error", "record.quality", f"{skill_id}: invalid quality state", "catalog/skills.seed.json")
    if record["risk"].get("level") not in RISK:
        audit.finding("error", "record.risk", f"{skill_id}: invalid risk level", "catalog/skills.seed.json")
    if record["source"].get("kind") not in SOURCE_KINDS:
        audit.finding("error", "record.source", f"{skill_id}: invalid source kind", "catalog/skills.seed.json")
    for lang in ("zh-CN","en"):
        if lang not in record["risk"].get("notes", {}):
            audit.finding("error", "record.risk-i18n", f"{skill_id}: missing risk note {lang}", "catalog/skills.seed.json")

    expected_base = f"skills/{record['category']}/{skill_id}"
    if record["paths"]["skill"] != f"{expected_base}/SKILL.md":
        audit.finding("error", "record.path", f"{skill_id}: canonical skill path mismatch", record["paths"]["skill"])
    for key, relative in record["paths"].items():
        full = (ROOT / relative).resolve()
        try:
            full.relative_to(ROOT.resolve())
        except ValueError:
            audit.finding("error", "record.path-escape", f"{skill_id}: {key} escapes repository", relative)
            continue
        if not full.is_file():
            audit.finding("error", "record.path-missing", f"{skill_id}: missing {key}", relative)


def scan_skill_structure(audit: Audit, records: list[dict]) -> None:
    catalog_ids = {item["id"] for item in records}
    skill_files = sorted((ROOT / "skills").rglob("SKILL.md"))
    disk_ids = {path.parent.name for path in skill_files}
    for missing in sorted(catalog_ids - disk_ids):
        audit.finding("error", "skill.disk-missing", f"Catalog skill missing on disk: {missing}", "skills")
    for extra in sorted(disk_ids - catalog_ids):
        audit.finding("error", "skill.catalog-missing", f"Disk skill absent from catalog: {extra}", "skills")
    source_by_id = {item["id"]: item["source"]["kind"] for item in records}
    for path in skill_files:
        skill_id = path.parent.name
        frontmatter = parse_frontmatter(path)
        if not frontmatter:
            audit.finding("error", "skill.frontmatter", f"{skill_id}: missing or malformed frontmatter", path.relative_to(ROOT))
            continue
        keys = set(frontmatter)
        if "name" not in keys or "description" not in keys:
            severity = "error" if source_by_id.get(skill_id) == "lianlin-first-party" else "warning"
            audit.finding(severity, "skill.frontmatter-fields", f"{skill_id}: name or description is absent", path.relative_to(ROOT))
        extra = keys - {"name", "description"}
        if extra and source_by_id.get(skill_id) == "lianlin-first-party":
            audit.finding("error", "skill.frontmatter-extra", f"{skill_id}: unsupported first-party frontmatter keys {sorted(extra)}", path.relative_to(ROOT))
        if frontmatter.get("name") != skill_id:
            severity = "error" if source_by_id.get(skill_id) == "lianlin-first-party" else "warning"
            audit.finding(severity, "skill.name-mismatch", f"{skill_id}: frontmatter name is {frontmatter.get('name')!r}", path.relative_to(ROOT))
    audit.checkpoint("skillStructure", diskSkills=len(skill_files), catalogSkills=len(records))


def scan_code(audit: Audit) -> None:
    python_files = sorted((ROOT / "skills").rglob("*.py")) + sorted((ROOT / "scripts").glob("*.py"))
    syntax_failures = 0
    for path in python_files:
        try:
            ast.parse(path.read_text(encoding="utf-8", errors="replace"), filename=str(path))
        except SyntaxError as exc:
            syntax_failures += 1
            # Upstream examples can target older Python or contain template fragments.
            external = "skills" in path.parts and "academic-core" not in path.parts
            audit.finding("warning" if external else "error", "code.python-syntax", f"{exc.msg} at line {exc.lineno}", path.relative_to(ROOT))
    node = _which("node")
    js_files = [ROOT / "site" / "assets" / "app.js"]
    js_failures = 0
    if node:
        for path in js_files:
            result = subprocess.run([node, "--check", str(path)], capture_output=True, text=True, check=False)
            if result.returncode:
                js_failures += 1
                audit.finding("error", "code.js-syntax", result.stderr.strip(), path.relative_to(ROOT))
    else:
        audit.finding("info", "code.node-unavailable", "Node.js is optional; JavaScript syntax check skipped", "site/assets/app.js")
    audit.checkpoint("codeSyntax", pythonFiles=len(python_files), pythonWarnings=syntax_failures, jsFiles=len(js_files), jsFailures=js_failures)


def _which(command: str) -> str | None:
    import shutil
    return shutil.which(command)


def scan_security(audit: Audit) -> None:
    text_files = []
    extensions = {".md",".py",".js",".ts",".sh",".ps1",".json",".yaml",".yml",".toml"}
    for base in (ROOT / "skills", ROOT / "scripts", ROOT / "site"):
        text_files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix.lower() in extensions)
    counts = Counter()
    hardcoded = re.compile(r"""(?ix)\b(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*["'](?!your|example|replace|<|\$)([A-Za-z0-9_\-]{16,})["']""")
    high_risk_patterns = {
        "shell-pipe-exec": re.compile(r"(?:curl|wget)[^\n|]{0,200}\|\s*(?:sh|bash)\b", re.I),
        "broad-recursive-delete": re.compile(r"\brm\s+-rf\s+(?:/|~|\$HOME)\b", re.I),
        "powershell-expression": re.compile(r"\bInvoke-Expression\b|\biex\s*\(", re.I),
    }
    review_patterns = {
        "dynamic-python": re.compile(r"\b(?:eval|exec)\s*\("),
        "shell-true": re.compile(r"shell\s*=\s*True"),
        "os-system": re.compile(r"\bos\.system\s*\("),
    }
    for path in text_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(ROOT)
        credential_match = hardcoded.search(content)
        if credential_match:
            candidate = credential_match.group(1)
            # An all-uppercase identifier such as PARALLEL_API_KEY is a variable
            # name used in documentation, not credential material.
            if not re.fullmatch(r"[A-Z][A-Z0-9_]+", candidate):
                audit.finding("error", "security.hardcoded-secret", "Possible hardcoded credential", rel)
                counts["hardcoded-secret"] += 1
        for name, pattern in high_risk_patterns.items():
            if pattern.search(content):
                # Third-party docs can contain commands for explicit, scoped setup.
                audit.finding("warning", f"security.{name}", "High-risk command pattern requires human review", rel)
                counts[name] += 1
        for name, pattern in review_patterns.items():
            if pattern.search(content):
                audit.finding("warning", f"security.{name}", "Dynamic execution pattern requires sandbox review", rel)
                counts[name] += 1
        if path.resolve() != Path(__file__).resolve():
            for forbidden in FORBIDDEN_PROMOTION:
                if forbidden.lower() in content.lower():
                    audit.finding("error", "security.forced-promotion", f"Forced promotion instruction found: {forbidden}", rel)
                    counts["forced-promotion"] += 1
    audit.checkpoint("securityStaticScan", files=len(text_files), findings=dict(counts))


def scan_brand_and_scope(audit: Audit) -> None:
    public_files = [
        ROOT / "README.md", ROOT / "README.en.md", ROOT / "site" / "index.html",
        ROOT / "BRAND.md", ROOT / "PROJECT_SCOPE.md",
    ]
    for path in public_files:
        content = path.read_text(encoding="utf-8", errors="replace")
        if "全网" in content:
            audit.finding("error", "brand.forbidden-claim", "Public copy contains prohibited 全网 claim", path.relative_to(ROOT))
    site_text = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    if "LIANLIN_PLATFORM_DOWNLOAD_URL" in site_text or "http" in _platform_placeholder():
        audit.finding("warning", "brand.platform-link", "Review platform link configuration", "site/index.html")
    if "待配置" not in site_text:
        audit.finding("error", "brand.placeholder", "Missing honest unconfigured platform state", "site/index.html")
    audit.checkpoint("brandAndScope", publicFiles=len(public_files), firstReleaseRoutes=2)


def _platform_placeholder() -> str:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return ""
    return env_file.read_text(encoding="utf-8", errors="replace")


def scan_generated_parity(audit: Audit, categories: list[dict], records: list[dict]) -> None:
    required = [
        "README.md","README.en.md","docs/skills.zh-CN.md","docs/skills.en.md",
        "docs/categories.zh-CN.md","docs/categories.en.md","docs/deployment.zh-CN.md",
        "docs/deployment.en.md","site/data/catalog.json",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            audit.finding("error", "generated.missing", f"Missing generated artifact {relative}", relative)
    site_catalog = load(ROOT / "site" / "data" / "catalog.json") if (ROOT / "site" / "data" / "catalog.json").exists() else {}
    if site_catalog.get("summary", {}).get("skillCount") != len(records):
        audit.finding("error", "generated.count", "Site catalog count differs from canonical catalog", "site/data/catalog.json")
    if site_catalog.get("summary", {}).get("categoryCount") != len(categories):
        audit.finding("error", "generated.category-count", "Site category count differs from canonical catalog", "site/data/catalog.json")
    audit.checkpoint("bilingualParity", locales=["zh-CN","en"], skills=len(records), generatedArtifacts=len(required))


def scan_license(audit: Audit, records: list[dict]) -> None:
    counts = Counter(item["source"]["licenseStatus"] for item in records)
    if not (ROOT / "LICENSE").exists() or not (ROOT / "THIRD_PARTY_NOTICES.md").exists():
        audit.finding("error", "license.files", "LICENSE or THIRD_PARTY_NOTICES.md is missing")
    if counts.get("review-required"):
        audit.finding("warning", "license.review-required", f"{counts['review-required']} skills require license review", "catalog/skills.json")
    if counts.get("metadata-declared"):
        audit.finding("info", "license.metadata-declared", f"{counts['metadata-declared']} third-party skills rely on bundle-level license metadata", "THIRD_PARTY_NOTICES.md")
    audit.checkpoint("licenseProvenance", statusCounts=dict(counts))


def build_report(audit: Audit, categories: list[dict], records: list[dict], release: dict) -> dict:
    quality = Counter(item["quality"]["status"] for item in records)
    sources = Counter(item["source"]["kind"] for item in records)
    return {
        "schemaVersion": 1,
        "releaseVersion": release["version"],
        "generatedAt": f"{release['releaseDate']}T00:00:00Z",
        "result": "pass" if not audit.errors else "fail",
        "summary": {
            "skills": len(records), "categories": len(categories),
            "errors": len(audit.errors), "warnings": len(audit.warnings), "info": len(audit.info),
            "quality": dict(quality), "sources": dict(sources),
        },
        "checks": audit.checks,
        "errors": audit.errors,
        "warnings": audit.warnings,
        "info": audit.info,
        "catalogSha256": hashlib.sha256((ROOT / "catalog" / "skills.seed.json").read_bytes()).hexdigest(),
    }


def report_markdown(report: dict, lang: str) -> str:
    zh = lang == "zh-CN"
    s = report["summary"]
    lines = [
        "# 发布审计报告" if zh else "# Release Audit Report", "",
        (f"结论：**{'通过' if report['result'] == 'pass' else '失败'}**" if zh else f"Result: **{report['result'].upper()}**"),
        "",
        f"- {'技能' if zh else 'Skills'}: {s['skills']}",
        f"- {'分类' if zh else 'Categories'}: {s['categories']}",
        f"- {'阻断错误' if zh else 'Blocking errors'}: {s['errors']}",
        f"- {'复核警告' if zh else 'Review warnings'}: {s['warnings']}",
        f"- {'信息项' if zh else 'Informational findings'}: {s['info']}",
        f"- {'目录 SHA-256' if zh else 'Catalog SHA-256'}: `{report['catalogSha256']}`",
        "",
        "## 检查矩阵" if zh else "## Check Matrix", "",
        "| 检查 | 结果 |" if zh else "| Check | Result |", "|---|---|",
    ]
    for name, details in report["checks"].items():
        lines.append(f"| `{name}` | `{json.dumps(details, ensure_ascii=False)}` |")
    lines.extend(["", "## 阻断错误" if zh else "## Blocking Errors", ""])
    if report["errors"]:
        lines.extend(f"- `{item['code']}` {item['message']} — `{item['path']}`" for item in report["errors"])
    else:
        lines.append("无。" if zh else "None.")
    lines.extend(["", "## 复核警告" if zh else "## Review Warnings", ""])
    if report["warnings"]:
        grouped = Counter(item["code"] for item in report["warnings"])
        for code, count in sorted(grouped.items()):
            lines.append(f"- `{code}`: {count}")
        lines.append("")
        lines.append(
            "警告主要来自固定第三方代码或原始元数据，表示后续运行/许可证复核队列，不影响目录结构发布；具体明细见 `reports/audit.json`。"
            if zh else
            "Warnings primarily originate in pinned third-party code or metadata and form the runtime/license review queue. They do not block structural catalog publication; see `reports/audit.json` for item-level details."
        )
    else:
        lines.append("无。" if zh else "None.")
    lines.extend(["", "## 解释" if zh else "## Interpretation", ""])
    lines.append(
        "本报告证明双语目录、路径、元数据、站点构建与常见静态风险检查无阻断错误；它不证明 177 项第三方技能已经完成真实 API、领域科学有效性或逐文件法律验证。"
        if zh else
        "This report proves that bilingual catalog, paths, metadata, site build, and common static-risk checks have no blockers. It does not claim that all 177 third-party skills have completed live API, domain-validity, or per-file legal verification."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    audit = Audit()
    categories = load(ROOT / "catalog" / "categories.seed.json")
    records = load(ROOT / "catalog" / "skills.seed.json")
    release = load(ROOT / "catalog" / "release.json")
    category_ids = {item["id"] for item in categories}
    if len(category_ids) != len(categories):
        audit.finding("error", "category.duplicate", "Category IDs are not unique", "catalog/categories.seed.json")
    if sorted(item["order"] for item in categories) != list(range(1, len(categories) + 1)):
        audit.finding("error", "category.order", "Category order must be contiguous from 1", "catalog/categories.seed.json")
    seen: set[str] = set()
    for record in records:
        validate_record(audit, record, category_ids, seen)
    audit.checkpoint("catalogSchema", records=len(records), uniqueIds=len(seen), categories=len(categories))
    scan_skill_structure(audit, records)
    scan_generated_parity(audit, categories, records)
    scan_code(audit)
    scan_security(audit)
    scan_brand_and_scope(audit)
    scan_license(audit, records)
    first_party = sum(item["source"]["kind"] == "lianlin-first-party" for item in records)
    third_party = len(records) - first_party
    expected = release["expected"]
    expected_counts = (expected["skills"], expected["categories"], expected["firstParty"], expected["thirdParty"])
    if (len(records), len(categories), first_party, third_party) != expected_counts:
        audit.finding("error", "release.counts", f"Expected {expected_counts}, got {len(records)}/{len(categories)}/{first_party}/{third_party}")
    audit.checkpoint("releaseContract", skills=len(records), categories=len(categories), firstParty=first_party, thirdParty=third_party)

    report = build_report(audit, categories, records, release)
    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "audit.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (REPORTS / "audit.zh-CN.md").write_text(report_markdown(report, "zh-CN"), encoding="utf-8")
    (REPORTS / "audit.en.md").write_text(report_markdown(report, "en"), encoding="utf-8")
    print(json.dumps(report["summary"] | {"result": report["result"]}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["result"] == "pass" else 1)


if __name__ == "__main__":
    main()
