#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Every unit page follows the template in harness/conventions.md.

A page that looks fine but drops "Assessment criteria" is a compliance hole,
so the template is enforced rather than suggested.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

UNITS = Path("docs/units")
REQUIRED_META = ("title", "unit", "hours", "term", "ce")
REQUIRED_SECTIONS = {
    "en": ["## What you will learn", "## Assessment criteria", "## Contents"],
    "es": ["## Qué vas a aprender", "## Criterios de evaluación", "## Contenidos"],
}


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return (meta if isinstance(meta, dict) else {}), parts[2]


def main() -> int:
    problems: list[str] = []
    checked = 0

    # A published page must never contain a placeholder, wherever it lives.
    # This runs over all of docs/, not just docs/units/: a TODO stub in any
    # published page is a lie the translation gate would otherwise accept.
    for page in sorted(Path("docs").rglob("*.md")):
        if "TODO" in page.read_text(encoding="utf-8"):
            problems.append(f"TODO       {page} contains a TODO placeholder")

    if UNITS.is_dir():
        for page in sorted(UNITS.glob("*.md")):
            m = re.search(r"\.(en|es)\.md$", page.name)
            if not m:
                problems.append(f"LOCALE     {page} has no .en.md / .es.md suffix")
                continue
            locale = m.group(1)
            checked += 1

            meta, body = split_front_matter(page.read_text(encoding="utf-8"))
            for key in REQUIRED_META:
                if key not in meta:
                    problems.append(f"META       {page} is missing front-matter key '{key}'")

            for section in REQUIRED_SECTIONS[locale]:
                if section not in body:
                    problems.append(f"SECTION    {page} is missing '{section}'")

            if len(body.strip()) < 200:
                problems.append(f"EMPTY      {page} is suspiciously short ({len(body.strip())} chars)")

    print(f"Checked {checked} unit pages, {len(list(Path('docs').rglob('*.md')))} published pages.")
    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print("All published pages clean; unit pages follow the template.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
