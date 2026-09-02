#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml", "httpx"]
# ///
"""Watch the legal sources the curriculum is built on.

curriculum.yml is only trustworthy while the norms behind it stay put. Sources
marked `fetch: auto` are downloaded and hashed; if the hash moves, the build
fails and somebody has to look at what changed.

dogv.gva.es blocks automated access via robots.txt, so the regional sources are
marked `fetch: manual`: for those the script can only nag when `checked_on`
gets older than `review_every_days`. That is a real limitation, recorded in the
YAML rather than papered over.

Usage:
    uv run scripts/check_sources.py
    uv run scripts/check_sources.py --update-fingerprints
    uv run scripts/check_sources.py --offline      # skip network, check dates only
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import sys
from pathlib import Path

import yaml

CURRICULUM = Path("harness/curriculum.yml")
DEFAULT_REVIEW_DAYS = 365


def fetch(url: str) -> bytes | None:
    try:
        import httpx

        r = httpx.get(url, timeout=30, follow_redirects=True)
        r.raise_for_status()
        return r.content
    except Exception as exc:  # network unavailable, blocked, 404...
        print(f"  ! could not fetch {url}: {type(exc).__name__}")
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update-fingerprints", action="store_true")
    parser.add_argument("--offline", action="store_true", help="skip network access")
    args = parser.parse_args()

    if not CURRICULUM.is_file():
        print(f"error: {CURRICULUM} not found; run from the repository root")
        return 2

    raw = CURRICULUM.read_text(encoding="utf-8")
    cur = yaml.safe_load(raw)
    today = dt.date.today()

    problems: list[str] = []
    warnings: list[str] = []
    updates: dict[str, str] = {}

    for src in cur.get("sources", []):
        sid, url, mode = src["id"], src.get("url"), src.get("fetch", "manual")

        if not url:
            problems.append(f"NO_URL     {sid} has no URL; it cannot be tracked")
            continue

        if mode == "auto" and not args.offline:
            content = fetch(url)
            if content is None:
                warnings.append(f"UNREACHABLE {sid} could not be checked this run")
                continue
            digest = hashlib.sha256(content).hexdigest()[:16]
            stored = src.get("fingerprint")
            if stored is None or args.update_fingerprints:
                updates[sid] = digest
                warnings.append(f"RECORDED   {sid} fingerprint {digest}")
            elif stored != digest:
                problems.append(
                    f"CHANGED    {sid} has changed ({stored} -> {digest}). "
                    f"Review {url} before trusting curriculum.yml."
                )
        else:
            checked = src.get("checked_on")
            if not checked:
                warnings.append(f"NEVER      {sid} has never been reviewed manually")
                continue
            age = (today - checked).days if isinstance(checked, dt.date) else None
            limit = src.get("review_every_days", DEFAULT_REVIEW_DAYS)
            if age is not None and age > limit:
                problems.append(f"OVERDUE    {sid} last reviewed {age} days ago (limit {limit})")

    if updates:
        for sid, digest in updates.items():
            raw = raw.replace(
                f"    id: {sid}\n", f"    id: {sid}\n", 1
            )  # anchor kept simple; rewrite below
        # rewrite fingerprints in place, line-oriented to preserve comments
        lines = raw.splitlines(keepends=True)
        current: str | None = None
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("- id:"):
                current = stripped.split("- id:", 1)[1].strip()
            elif stripped.startswith("fingerprint:") and current in updates:
                indent = line[: len(line) - len(line.lstrip())]
                lines[i] = f"{indent}fingerprint: {updates[current]}\n"
        CURRICULUM.write_text("".join(lines), encoding="utf-8")
        print(f"Recorded {len(updates)} fingerprint(s) in {CURRICULUM}.")

    print(f"Sources: {len(cur.get('sources', []))} tracked.")
    for w in warnings:
        print(f"  {w}")
    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print("Legal sources OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
