# Bitácora

Append-only. Una entrada por feature cerrada o por decisión estructural.

---

## 2026-09-02 — Inicialización del repositorio

Arnés adaptado desde `betta-tech/harness-sdd` a un proyecto doc-as-code.
Cambios estructurales respecto al modelo original:

- `docs/` pasa a ser el contenido publicable de MkDocs; las reglas del arnés se
  mueven a `harness/` para no colisionar.
- Los tests unitarios se sustituyen por seis comprobaciones ejecutables
  (`harness/verification.md`).
- La trazabilidad `R<n> ↔ test` pasa a ser `CE ↔ página`.
- Las features se tipan (`content_theory`, `content_lab`, …) y cada tipo lleva
  su `sdd_level`, de modo que la puerta humana sólo dispara donde hace falta.
- `curriculum.yml` extraído del RD 1629/2009 y cotejado contra el BOE: 58 CE.
- `feature_list.json` se genera a partir de `curriculum.yml`, no a mano.
