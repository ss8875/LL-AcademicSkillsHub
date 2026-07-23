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
    checks = {
        "python": {"ok": sys.version_info >= (3, 10), "value": platform.python_version(), "required": ">=3.10"},
        "catalog": {"ok": (ROOT / "catalog" / "skills.json").is_file(), "value": "catalog/skills.json"},
        "site": {"ok": (ROOT / "site" / "index.html").is_file(), "value": "site/index.html"},
        "git": {"ok": shutil.which("git") is not None, "value": shutil.which("git") or "not found", "optional": True},
        "platformDownload": {
            "ok": bool(_env_value("LIANLIN_PLATFORM_DOWNLOAD_URL")),
            "value": "configured" if _env_value("LIANLIN_PLATFORM_DOWNLOAD_URL") else "not configured",
            "optional": True,
        },
    }
    required_ok = all(item["ok"] for item in checks.values() if not item.get("optional"))
    print(json.dumps({"ready": required_ok, "root": str(ROOT), "checks": checks}, ensure_ascii=False, indent=2))
    raise SystemExit(0 if required_ok else 1)


def _env_value(name: str) -> str:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return ""
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        if raw.strip().startswith(f"{name}="):
            return raw.split("=", 1)[1].strip()
    return ""


if __name__ == "__main__":
    main()
