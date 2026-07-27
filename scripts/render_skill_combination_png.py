#!/usr/bin/env python3
"""Render skill-combination SVG maps to exact 1920×1080 PNG files."""

from __future__ import annotations

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SVG_DIR = ROOT / "assets" / "brand" / "skill-combinations"
PNG_DIR = SVG_DIR / "png"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Render only the first N maps")
    args = parser.parse_args()
    paths = sorted(SVG_DIR.glob("[0-9][0-9]-*.svg"))
    if args.limit:
        paths = paths[: args.limit]
    elif (SVG_DIR / "index.svg").exists():
        paths = [SVG_DIR / "index.svg", *paths]
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
        for path in paths:
            page.goto(path.resolve().as_uri(), wait_until="load")
            page.screenshot(
                path=str(PNG_DIR / f"{path.stem}.png"),
                clip={"x": 0, "y": 0, "width": 1920, "height": 1080},
            )
        browser.close()
    print(f"Rendered {len(paths)} PNG maps in {PNG_DIR}")


if __name__ == "__main__":
    main()
