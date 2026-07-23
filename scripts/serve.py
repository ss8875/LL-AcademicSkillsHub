#!/usr/bin/env python3
"""Serve the repository root for the local catalog with no third-party dependencies."""

from __future__ import annotations

import argparse
import http.server
import os
from functools import partial
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_TOP_LEVEL = {"site", "skills", "docs", "assets"}
ALLOWED_ROOT_FILES = {"README.md", "README.en.md", "LICENSE", "THIRD_PARTY_NOTICES.md"}


class SafeRepositoryHandler(http.server.SimpleHTTPRequestHandler):
    """Expose published documentation while blocking configuration and internals."""

    def _allowed(self) -> bool:
        path = unquote(urlsplit(self.path).path)
        if path == "/":
            return True
        parts = [part for part in path.split("/") if part]
        if not parts or any(part.startswith(".") for part in parts):
            return False
        return parts[0] in ALLOWED_TOP_LEVEL or (len(parts) == 1 and parts[0] in ALLOWED_ROOT_FILES)

    def _guard(self) -> bool:
        if not self._allowed():
            self.send_error(404, "Not found")
            return False
        if urlsplit(self.path).path == "/":
            self.send_response(302)
            self.send_header("Location", "/site/")
            self.end_headers()
            return False
        return True

    def do_GET(self) -> None:
        if self._guard():
            super().do_GET()

    def do_HEAD(self) -> None:
        if self._guard():
            super().do_HEAD()


def load_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.environ.get("LL_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("LL_PORT", "8765")))
    args = parser.parse_args()
    handler = partial(SafeRepositoryHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer((args.host, args.port), handler)
    print(f"LL-AcademicSkillsHub: http://{args.host}:{args.port}/site/")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
