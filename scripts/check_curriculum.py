#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Traceability gate: assessment criteria (CE) must line up everywhere.

This is the docs-project equivalent of "every requirement has a test":

  1. curriculum.yml is internally consistent (no invented CE, hours add up).
  2. Every CE in the curriculum is covered by a unit, or declared `uncovered`
     with an explicit decision. A forgotten CE fails the build.
  3. Every CE declared in feature_list.json matches what the curriculum
     assigns to that unit -- not one more, not one less.
  4. Every CE declared in a published page's front matter exists, and matches
     its feature.
  5. The dual and intermodular sections only cite real CE.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

CURRICULUM = Path("harness/curriculum.yml")
FEATURES = Path("feature_list.json")
DOCS = Path("docs")


def split_front_matter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    meta = yaml.safe_load(parts[1]) or {}
    return meta if isinstance(meta, dict) else {}


def flat(covers: dict) -> set[str]:
    return {f"{ra}.{ce}" for ra, ces in (covers or {}).items() for ce in ces}


def main() -> int:
    if not CURRICULUM.is_file():
        print(f"error: {CURRICULUM} not found; run from the repository root")
        return 2

    cur = yaml.safe_load(CURRICULUM.read_text(encoding="utf-8"))
    problems: list[str] = []

    all_ce = {
        f"{ra['id']}.{key}"
        for ra in cur["learning_outcomes"]
        for key in ra["criteria"]
    }

    # 1. hours
    total = sum(u["hours"] for u in cur["units"])
    declared = cur["module"]["hours_used"]
    if total != declared:
        problems.append(f"HOURS      units add up to {total} h, module declares {declared} h")

    # 2. coverage
    covered: set[str] = set()
    unit_ce: dict[str, set[str]] = {}
    for unit in cur["units"]:
        ces = flat(unit.get("covers"))
        ghost = ces - all_ce
        if ghost:
            problems.append(f"GHOST      {unit['id']} declares CE that do not exist: {sorted(ghost)}")
        unit_ce[unit["id"]] = ces
        covered |= ces

    declared_uncovered = {x["ce"] for x in (cur.get("uncovered") or [])}
    for ce in sorted(all_ce - covered - declared_uncovered):
        problems.append(f"ORPHAN     {ce} is covered by no unit and is not declared in `uncovered:`")
    for entry in cur.get("uncovered") or []:
        if entry.get("decision") == "pending":
            problems.append(f"UNDECIDED  {entry['ce']} is uncovered with `decision: pending`")
        if entry["ce"] in covered:
            problems.append(f"CONTRADICT {entry['ce']} is listed as uncovered but a unit covers it")

    # 3. dual / intermodular
    for section, items in (
        ("dual", [x["ce"] for x in (cur.get("dual", {}).get("consolidated_in_company") or [])]),
        ("intermodular", cur.get("intermodular", {}).get("contributes_ce") or []),
    ):
        for ce in items:
            if ce not in all_ce:
                problems.append(f"GHOST      {section} cites {ce}, which does not exist")
            elif ce not in covered:
                problems.append(
                    f"UNBACKED   {section} cites {ce}, but no unit covers it in the centre"
                )

    # 4. features
    checked_pages = 0
    if FEATURES.is_file():
        data = json.loads(FEATURES.read_text(encoding="utf-8"))
        for feat in data["features"]:
            fid = feat["id"]
            fce = flat(feat.get("curriculum"))
            unit = feat.get("unit")
            if unit and unit in unit_ce and fce != unit_ce[unit]:
                missing = sorted(unit_ce[unit] - fce)
                extra = sorted(fce - unit_ce[unit])
                problems.append(
                    f"MISMATCH   feature {fid} ({unit}): missing {missing or '-'}, extra {extra or '-'}"
                )

            # 5. published pages
            for locale in ("en", "es"):
                target = feat.get("target", {}).get(locale)
                if not target or not Path(target).is_file():
                    continue
                checked_pages += 1
                meta = split_front_matter(Path(target).read_text(encoding="utf-8"))
                page_ce = set(meta.get("ce") or [])
                ghost = page_ce - all_ce
                if ghost:
                    problems.append(f"GHOST      {target} declares nonexistent CE: {sorted(ghost)}")
                if page_ce and page_ce != fce:
                    problems.append(f"MISMATCH   {target} CE differ from feature {fid}")

    # 6. every page under docs/ that declares CE, whether or not a feature
    #    claims it. An orphan page with invented CE used to slip through here.
    known_targets = set()
    if FEATURES.is_file():
        for feat in json.loads(FEATURES.read_text(encoding="utf-8"))["features"]:
            known_targets |= {v for v in (feat.get("target") or {}).values() if v}

    for page in sorted(DOCS.rglob("*.md")):
        meta = split_front_matter(page.read_text(encoding="utf-8"))
        page_ce = set(meta.get("ce") or [])
        if not page_ce:
            continue
        if str(page) not in known_targets:
            problems.append(f"UNCLAIMED  {page} declares CE but no feature owns it")
            checked_pages += 1
        ghost = page_ce - all_ce
        if ghost:
            problems.append(f"GHOST      {page} declares nonexistent CE: {sorted(ghost)}")

    print(f"Curriculum: {len(all_ce)} CE, {len(cur['units'])} units, {total} h. Pages checked: {checked_pages}.")
    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in sorted(set(problems)):
            print(f"  {p}")
        return 1
    print("Traceability OK: every CE accounted for.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
