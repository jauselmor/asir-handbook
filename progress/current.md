# Sesión actual

**Estado:** repositorio recién inicializado. Ninguna feature en curso.

## Siguiente paso

1. Revisar `docs/index.es.md` y poner `reviewed: true` si la traducción vale.
   Es la primera puerta humana y `init.sh` la señala en el paso 5.
2. Resolver las decisiones pendientes de `harness/curriculum.yml`:
   - los tres CE en `uncovered:` con `decision: pending` (RA3.g, RA7.e, RA7.f),
   - `dual.hours_in_company` y `dual.coordination`,
   - dar por buenos o corregir los bloques `status: draft` de dual e intermodular,
   - confirmar las dos UP marcadas `disputed: true` (UP7 y UP10).
3. Arrancar la primera feature: `up01_network_basics`.

Hasta que el punto 2 esté cerrado, `check_curriculum.py` seguirá en rojo. Es lo
correcto: son decisiones tuyas, no del arnés.
