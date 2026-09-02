#!/usr/bin/env bash
# Verificación completa del repositorio. Si esto está en verde, el estado del
# repositorio es coherente. Lo ejecutan los hooks de .claude/settings.json y el
# CI, así que no se puede saltar.
set -uo pipefail

G='\033[0;32m'; R='\033[0;31m'; Y='\033[0;33m'; N='\033[0m'
ok()   { echo -e "${G}[OK]${N}    $1"; }
bad()  { echo -e "${R}[FALLO]${N} $1"; FAILED=$((FAILED+1)); }
warn() { echo -e "${Y}[AVISO]${N} $1"; }
sec()  { echo; echo "── $1 ──────────────────────────────────────"; }

FAILED=0
cd "$(dirname "$0")"

sec "1. Entorno"
if command -v uv >/dev/null 2>&1; then
  ok "uv $(uv --version | cut -d' ' -f2)"
  RUN="uv run"
else
  bad "uv no está instalado. Es innegociable: https://docs.astral.sh/uv/"
  RUN="python3"
fi

sec "2. Integridad del backlog"
$RUN - <<'PY'
import json, sys
from pathlib import Path
d = json.loads(Path("feature_list.json").read_text(encoding="utf-8"))
valid = set(d["rules"]["valid_status"]); types = d["types"]; ids = set()
bad = []
for f in d["features"]:
    if f["id"] in ids: bad.append(f"id duplicado: {f['id']}")
    ids.add(f["id"])
    if f["status"] not in valid: bad.append(f"{f['id']}: status inválido '{f['status']}'")
    if f["type"] not in types: bad.append(f"{f['id']}: type desconocido '{f['type']}'")
    if f["sdd_level"] == "full" and f["status"] not in ("pending",) and not Path(f["spec_dir"]).is_dir():
        bad.append(f"{f['id']}: sdd_level=full en estado '{f['status']}' sin {f['spec_dir']}")
    for dep in f.get("dependencies", []):
        if dep not in {x["id"] for x in d["features"]}: bad.append(f"{f['id']}: dependencia inexistente '{dep}'")
n = sum(1 for f in d["features"] if f["status"] == "in_progress")
if n > 1: bad.append(f"{n} features in_progress; sólo puede haber una")
for b in bad: print("  " + b)
print(f"{len(d['features'])} features, {n} in_progress")
sys.exit(1 if bad else 0)
PY
[ $? -eq 0 ] && ok "feature_list.json coherente" || bad "feature_list.json incoherente"

sec "3. Trazabilidad del currículo"
$RUN scripts/check_curriculum.py && ok "Todo CE trazado" || bad "Fallo de trazabilidad de CE"

sec "4. Estructura de las páginas"
$RUN scripts/check_structure.py && ok "Plantilla respetada" || bad "Páginas fuera de plantilla"

sec "5. Traducciones"
$RUN scripts/check_translations.py && ok "Traducciones al día" || bad "Traducciones pendientes o desfasadas"

sec "6. Backend docente"
$RUN scripts/check_teacher.py && ok "Emparejamientos correctos" || bad "Problemas en teacher/"

sec "7. Fuentes normativas"
$RUN scripts/check_sources.py ${CHECK_SOURCES_OFFLINE:+--offline} && ok "Normativa sin cambios" || bad "Revisa la normativa"

sec "8. Build del sitio"
if $RUN mkdocs build --strict --site-dir /tmp/par_site >/tmp/par_build.log 2>&1; then
  ok "mkdocs build --strict"
else
  bad "mkdocs build --strict falló"; tail -15 /tmp/par_build.log | sed 's/^/      /'
fi

sec "9. Resumen"
if [ "$FAILED" -eq 0 ]; then
  ok "Entorno listo. Puedes empezar a trabajar."
  exit 0
fi
echo -e "${R}[FALLO]${N} $FAILED comprobación(es) en rojo."
echo
echo "Si es la primera vez que clonas el repositorio, lo normal es que falle"
echo "el paso 5 con UNREVIEWED en docs/index.es.md. No es un bug: es la puerta"
echo "humana. Lee la traducción y pon 'reviewed: true' en su frontmatter."
exit 1
