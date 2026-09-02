#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Teacher backend invariants.

teacher/ sits outside the MkDocs build but inside the repository, and the
repository may be public. That is a deliberate choice (see
harness/principios.md), so this script does not try to keep it secret. It
enforces two things instead:

  1. Pairing. Every lab has a solution file and every solution file points at
     a lab that exists. If the lab changes after the solution was written, the
     solution goes STALE -- same invariant as the Spanish translations, applied
     to a different axis.
  2. No leaks into the published site. A page under docs/ must never link to
     teacher/. mkdocs build --strict cannot catch this because the target lives
     outside the docs tree.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

DOCS = Path("docs")
TEACHER = Path("teacher")
FEATURES = Path("feature_list.json")
LINK = re.compile(r"]\(\s*(?:\.\./)*teacher/|]\(\s*/teacher/")


def split_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return (meta if isinstance(meta, dict) else {}), parts[2]


def body_sha(path: Path) -> str:
    _, body = split_front_matter(path.read_text(encoding="utf-8"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def main() -> int:
    problems: list[str] = []

    # 1. no links from the published site into teacher/
    leaks = 0
    for page in sorted(DOCS.rglob("*.md")):
        for n, line in enumerate(page.read_text(encoding="utf-8").splitlines(), 1):
            if LINK.search(line):
                problems.append(f"LEAK       {page}:{n} links to teacher/ from a published page")
                leaks += 1

    # 2. pairing, driven by feature_list.json
    pairs = 0
    expected: set[Path] = set()
    if FEATURES.is_file():
        data = json.loads(FEATURES.read_text(encoding="utf-8"))
        types = data.get("types", {})
        for feat in data["features"]:
            needs = types.get(feat["type"], {}).get("teacher_file", False)
            solution = feat.get("teacher")
            source = feat.get("target", {}).get("en")

            if needs and not solution:
                problems.append(f"UNPAIRED   feature {feat['id']} is a {feat['type']} with no `teacher` file declared")
                continue
            if not solution:
                continue

            expected.add(Path(solution))
            if feat["status"] == "done" and not Path(solution).is_file():
                problems.append(f"MISSING    {solution} (declared by feature {feat['id']}, which is done)")
                continue
            if not Path(solution).is_file():
                continue

            pairs += 1
            meta, _ = split_front_matter(Path(solution).read_text(encoding="utf-8"))
            if meta.get("pairs_with") != source:
                problems.append(f"PAIRS_WITH {solution} should declare `pairs_with: {source}`")
            if source and Path(source).is_file():
                if meta.get("source_sha") != body_sha(Path(source)):
                    problems.append(f"STALE      {solution} (the lab changed after the solution was written)")

    # 3. orphan solutions
    if TEACHER.is_dir():
        for sol in sorted((TEACHER / "labs").glob("*.md")) if (TEACHER / "labs").is_dir() else []:
            if sol not in expected:
                problems.append(f"ORPHAN     {sol} is not declared by any feature")

    print(f"Teacher backend: {pairs} pairing(s) checked, {leaks} leak(s) found.")
    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        for p in problems:
            print(f"  {p}")
        return 1
    print("Teacher backend OK: pairings consistent, no leaks into docs/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
