#!/usr/bin/env python3
"""Build a visual QA contact sheet for all 50 rendered maps."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PNG_DIR = ROOT / "assets" / "brand" / "skill-combinations" / "png"
OUTPUT = ROOT / "reports" / "skill-combination-contact-sheet.png"
COLS = 5
THUMB_W = 360
THUMB_H = 203
GAP = 14
MARGIN = 24
HEADER = 70


def main() -> None:
    paths = sorted(PNG_DIR.glob("[0-9][0-9]-*.png"))
    rows = (len(paths) + COLS - 1) // COLS
    width = MARGIN * 2 + COLS * THUMB_W + (COLS - 1) * GAP
    height = HEADER + MARGIN + rows * THUMB_H + (rows - 1) * GAP + MARGIN
    sheet = Image.new("RGB", (width, height), "#07101F")
    draw = ImageDraw.Draw(sheet)
    draw.text((MARGIN, 20), "LL-AcademicSkillsHub · 50 Skill Combination Maps · Visual QA", fill="#EAF2FF")
    for index, path in enumerate(paths):
        row, col = divmod(index, COLS)
        x = MARGIN + col * (THUMB_W + GAP)
        y = HEADER + row * (THUMB_H + GAP)
        with Image.open(path) as source:
            thumb = source.convert("RGB").resize((THUMB_W, THUMB_H), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y))
        draw.rectangle((x, y, x + THUMB_W - 1, y + THUMB_H - 1), outline="#27466F", width=1)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUTPUT, quality=95)
    print(f"Built contact sheet: {OUTPUT}")


if __name__ == "__main__":
    main()
