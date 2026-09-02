# Verificación

Cuándo leerlo: antes de dar por cerrada cualquier feature, y cuando `init.sh`
falle y no sepas por qué.

En un proyecto de software la verificación son los tests. Aquí no hay tests
unitarios, pero hay seis comprobaciones ejecutables. Todas las corre `init.sh`
y todas las corre el CI. Ninguna es opcional.

| Comprobación | Script | Qué garantiza |
| --- | --- | --- |
| Integridad del backlog | `init.sh` | JSON válido, un solo `in_progress`, spec presente si `sdd_level: full` y estado ≠ `pending` |
| Currículo | `check_curriculum.py` | Todo CE declarado existe; la cobertura está completa o justificada; dual e intermodular sólo citan CE reales |
| Estructura | `check_structure.py` | Frontmatter y secciones obligatorias en cada página de unidad |
| Traducción | `check_translations.py` | Todo `.en.md` tiene `.es.md` presente, al día y revisado por una persona |
| Backend docente | `check_teacher.py` | Emparejamiento lab ↔ solucionario, y que ninguna página publicada enlace a `teacher/` |
| Fuentes normativas | `check_sources.py` | Las normas no han cambiado bajo nuestros pies |
| Build | `mkdocs build --strict` | Ningún enlace roto, ninguna referencia inexistente |

## Trazabilidad: CE ↔ página

Es el invariante central. Sustituye al «cada requirement tiene un test» del
arnés de software:

- Todo CE que una página declara en su frontmatter **debe existir** en
  `harness/curriculum.yml`. Un CE inventado rompe el build.
- Todo CE del currículo **debe estar cubierto** por alguna unidad, o figurar en
  `uncovered:` con una decisión explícita. Un CE olvidado rompe el build.

La segunda mitad es la que evita descubrir en junio que nadie ha impartido
RA3.g. La primera evita que una página se adorne con criterios que no le tocan.

## Fuentes normativas

`check_sources.py` calcula el sha256 de cada fuente con `fetch: auto` y lo
compara con el `fingerprint` guardado. Si el BOE republica el texto, el CI
falla y te obliga a mirar qué cambió.

Las fuentes autonómicas están marcadas `fetch: manual`: `dogv.gva.es` bloquea
el acceso automatizado por `robots.txt`. Para esas, el script sólo avisa cuando
`checked_on` supera `review_every_days`. Es una limitación real, no un descuido:
está documentada en el propio YAML.

## El primer arranque falla, y es correcto

Al clonar el repositorio, `check_translations.py` marca `docs/index.es.md` como
`UNREVIEWED`. No es un bug: es la puerta humana disparando por primera vez.
Léete la traducción, y si te vale, pon `reviewed: true` en su frontmatter.
Ningún agente puede hacerlo por ti.
