#!/usr/bin/env python3
"""Create a deterministic local-release archive and checksum manifest."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ARCHIVE = DIST / "LL-AcademicSkillsHub-local.zip"
MANIFEST = DIST / "manifest.json"
INCLUDE_DIRS = (".github", "assets", "catalog", "docs", "reports", "site", "skills", "scripts", "tests")
INCLUDE_FILES = (
    ".env.example", "BRAND.md", "CHANGELOG.md", "COMMERCIAL_LICENSE.md", "CONTRIBUTING.md",
    "LICENSE", "PROJECT_SCOPE.md", "README.md", "README.en.md", "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
)
EXCLUDE_NAMES = {"__pycache__", ".DS_Store", "Thumbs.db"}


def release_files() -> list[Path]:
    files: list[Path] = []
    for directory in INCLUDE_DIRS:
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and not any(part in EXCLUDE_NAMES for part in path.parts):
                files.append(path)
    files.extend(ROOT / name for name in INCLUDE_FILES if (ROOT / name).is_file())
    return sorted(set(files), key=lambda path: path.relative_to(ROOT).as_posix())


def main() -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    files = release_files()
    entries = []
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(ROOT).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(f"LL-AcademicSkillsHub/{relative}", date_time=(2026, 7, 23, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, data)
            entries.append({"path": relative, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    payload = {
        "archive": ARCHIVE.name,
        "archiveSize": ARCHIVE.stat().st_size,
        "archiveSha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        "fileCount": len(entries),
        "files": entries,
    }
    MANIFEST.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("archive","archiveSize","archiveSha256","fileCount")}, indent=2))


if __name__ == "__main__":
    main()
