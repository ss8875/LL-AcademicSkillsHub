#!/usr/bin/env python3
"""Check whether the local documentation runtime is ready."""

from __future__ import annotations

import json
import platform
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    site_config = _json_file(ROOT / "site" / "config.json")
    platform_url = site_config.get("platformDownloadUrl", "")
    checks = {
        "python": {"ok": sys.version_info >= (3, 10), "value": platform.python_version(), "required": ">=3.10"},
        "catalog": {"ok": (ROOT / "catalog" / "skills.json").is_file(), "value": "catalog/skills.json"},
        "site": {"ok": (ROOT / "site" / "index.html").is_file(), "value": "site/index.html"},
        "git": {"ok": shutil.which("git") is not None, "value": shutil.which("git") or "not found", "optional": True},
        "platformDownload": {
            "ok": platform_url.startswith("https://"),
            "value": platform_url or "not configured",
        },
    }
    required_ok = all(item["ok"] for item in checks.values() if not item.get("optional"))
    print(json.dumps({"ready": required_ok, "root": str(ROOT), "checks": checks}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if required_ok else 1)


def _json_file(path: Path) -> dict:
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


if __name__ == "__main__":
    main()
