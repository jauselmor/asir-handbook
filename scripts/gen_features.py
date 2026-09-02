#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = ["pyyaml"]
# ///
"""Regenerate feature_list.json from harness/curriculum.yml.

The curriculum is the source of truth for units, hours, terms and assessment
criteria. Editing feature_list.json by hand lets the two drift apart, and
check_curriculum.py will start reporting MISMATCH. Run this instead.

Work already done is preserved: status, spec_dir, teacher, dependencies and
anything under `context` survive a regeneration. Only the curriculum-derived
fields are rewritten.

Usage:
    uv run scripts/gen_features.py            # show what would change
    uv run scripts/gen_features.py --write
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

CURRICULUM = Path("harness/curriculum.yml")
FEATURES = Path("feature_list.json")

# Slug and English title per unit. Adding a unit to curriculum.yml means adding
# it here too -- deliberately manual, so a new unit is a conscious decision.
SLUGS = {
    "UP1":  ("up01-network-basics",   "Introducción a las Redes de Datos"),
    "UP2":  ("up02-architecture",     "Arquitectura de Red y Modelos de Referencia"),
    "UP3":  ("up03-physical-media",   "Medios Físicos e Infraestructura de Red - PRL"),
    "UP4":  ("up04-wireless",         "Tecnologías de Redes Inalámbricas WLAN"),
    "UP5":  ("up05-ip-addressing",    "Direccionamiento Lógico IP (IPv4 e IPv6)"),
    "UP6":  ("up06-switching-vlans",  "Configuración y Administración de Switches y VLANs"),
    "UP7":  ("up07-network-services", "Servicios de Soporte de Red (DHCP, SNMP, DNS)"),
    "UP8":  ("up08-routing",          "Enrutamiento Estático y Dinámico (RIPv2, OSPF)"),
    "UP9":  ("up09-wan-nat",          "Acceso a Internet desde la LAN y Tecnologías WAN"),
    "UP10": ("up10-acls",             "Filtrado de Tráfico mediante ACLs"),
}

PRESERVED = ("status", "teacher", "dependencies", "spec_dir", "context")

TYPES = {
    "layout_config":      {"sdd_level": "none",  "human_gate": False,
                           "writes": ["mkdocs.yml", "docs/stylesheets/"], "bilingual": False},
    "content_theory":     {"sdd_level": "full",  "human_gate": True,
                           "writes": ["docs/units/"], "bilingual": True, "teacher_file": False},
    "content_lab":        {"sdd_level": "full",  "human_gate": True,
                           "writes": ["docs/labs/"], "bilingual": True, "teacher_file": True},
    "content_lab_update": {"sdd_level": "light", "human_gate": False,
                           "writes": ["docs/labs/"], "bilingual": True, "teacher_file": True,
                           "additive_only": True},
    "pedagogy_eval":      {"sdd_level": "full",  "human_gate": True,
                           "writes": ["teacher/assessment/"], "bilingual": False},
}

RULES = {
    "one_in_progress_at_a_time": True,
    "human_gate_before_implementation": "sólo para sdd_level=full",
    "valid_status": ["pending", "spec_ready", "in_progress", "done", "blocked"],
    "english_is_source_of_truth": True,
    "spanish_is_mandatory": True,
    "every_declared_ce_must_exist_in_curriculum": True,
    "curriculum_source": "harness/curriculum.yml",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="apply changes")
    args = parser.parse_args()

    if not CURRICULUM.is_file():
        print(f"error: {CURRICULUM} not found; run from the repository root")
        return 2

    cur = yaml.safe_load(CURRICULUM.read_text(encoding="utf-8"))

    existing: dict[str, dict] = {}
    extra: list[dict] = []
    if FEATURES.is_file():
        old = json.loads(FEATURES.read_text(encoding="utf-8"))
        unit_ids = {f"{SLUGS[u['id']][0].replace('-', '_')}" for u in cur["units"] if u["id"] in SLUGS}
        for feat in old["features"]:
            if feat["id"] in unit_ids:
                existing[feat["id"]] = feat
            else:
                extra.append(feat)  # labs, layout tasks... not derived from units

    features: list[dict] = []
    previous: str | None = None
    changes: list[str] = []

    for unit in cur["units"]:
        uid = unit["id"]
        if uid not in SLUGS:
            print(f"error: {uid} is in curriculum.yml but not in SLUGS; add it to this script")
            return 2
        slug, title = SLUGS[uid]
        fid = slug.replace("-", "_")
        prev = existing.get(fid, {})

        feature = {
            "id": fid,
            "type": "content_theory",
            "unit": uid,
            "title": title,
            "status": prev.get("status", "pending"),
            "sdd_level": "full",
            "target": {"en": f"docs/units/{slug}.en.md", "es": f"docs/units/{slug}.es.md"},
            "teacher": prev.get("teacher"),
            "dependencies": prev.get("dependencies", [previous] if previous else []),
            "spec_dir": prev.get("spec_dir", f"specs/{fid}/"),
            "curriculum": unit.get("covers") or {},
            "context": {**prev.get("context", {}), "hours": unit["hours"], "term": unit["term"]},
        }

        if not prev:
            changes.append(f"NEW      {fid}")
        else:
            if prev.get("curriculum") != feature["curriculum"]:
                changes.append(f"CE       {fid}: {prev.get('curriculum')} -> {feature['curriculum']}")
            if prev.get("context", {}).get("hours") != unit["hours"]:
                changes.append(f"HOURS    {fid}: {prev.get('context', {}).get('hours')} -> {unit['hours']}")

        features.append(feature)
        previous = fid

    for feat in extra:
        changes.append(f"KEPT     {feat['id']} (not unit-derived)")

    doc = {
        "project": "par-handbook",
        "module": cur["module"]["code"],
        "description": "Material del módulo 0370 (PAR) del CFGS ASIR. Sitio MkDocs bilingüe con backend docente.",
        "rules": RULES,
        "types": TYPES,
        "features": features + extra,
    }

    if not changes:
        print("feature_list.json is already in sync with the curriculum.")
        return 0

    print(f"{len(changes)} change(s):\n")
    for c in changes:
        print(f"  {c}")

    if not args.write:
        print("\nDry run. Re-run with --write to apply.")
        return 0

    FEATURES.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nWrote {FEATURES} ({len(doc['features'])} features).")
    print("Now run ./init.sh.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
