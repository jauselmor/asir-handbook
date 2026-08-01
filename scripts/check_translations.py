#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Verify that every English page has a current, reviewed Spanish translation.

English is the source of truth. Spanish is required for regulatory compliance,
so a missing or stale translation must fail the build rather than silently
falling back to English.

Usage:
    uv run scripts/check_translations.py
    uv run scripts/check_translations.py --update-hashes
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

import yaml

DOCS = Path("docs")
SOURCE_LOCALE = "en"
TARGET_LOCALE = "es"
FRONT_MATTER = "---"


def body_sha(path: Path) -> str:
    """Short digest of a file's content, ignoring its front matter."""
    text = path.read_text(encoding="utf-8")
    _, body = split_front_matter(text)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith(FRONT_MATTER):
        return {}, text
    parts = text.split(FRONT_MATTER, 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    if not isinstance(meta, dict):
        meta = {}
    return meta, parts[2]


def target_for(source: Path) -> Path:
    """docs/redes/vlan.en.md -> docs/redes/vlan.es.md"""
    stem = source.name.removesuffix(f".{SOURCE_LOCALE}.md")
    return source.with_name(f"{stem}.{TARGET_LOCALE}.md")


def write_hash(target: Path, meta: dict, digest: str) -> None:
    text = target.read_text(encoding="utf-8")
    _, body = split_front_matter(text)
    meta["source_sha"] = digest
    header = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).strip()
    target.write_text(f"---\n{header}\n---{body}", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update-hashes",
        action="store_true",
        help="rewrite source_sha in translations (use after reviewing them)",
    )
    args = parser.parse_args()

    if not DOCS.is_dir():
        print(f"error: {DOCS}/ not found; run from the repository root")
        return 2

    problems: list[str] = []
    checked = 0

    for source in sorted(DOCS.rglob(f"*.{SOURCE_LOCALE}.md")):
        checked += 1
        target = target_for(source)
        rel = target.relative_to(DOCS)

        if not target.exists():
            problems.append(f"MISSING    {rel} (no Spanish translation)")
            continue

        meta, _ = split_front_matter(target.read_text(encoding="utf-8"))
        digest = body_sha(source)

        if args.update_hashes:
            write_hash(target, meta, digest)
            continue

        if meta.get("source_sha") != digest:
            problems.append(f"STALE      {rel} (English source changed since translation)")
        if meta.get("reviewed") is not True:
            problems.append(f"UNREVIEWED {rel} (set 'reviewed: true' after human review)")

    if args.update_hashes:
        print(f"Updated source_sha in translations for {checked} English pages.")
        return 0

    print(f"Checked {checked} English pages.")
    if problems:
        print(f"\n{len(problems)} problem(s) found:\n")
        for p in problems:
            print(f"  {p}")
        print("\nSpanish is required for compliance. Fix these before publishing.")
        return 1

    print("All translations present, current, and reviewed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
