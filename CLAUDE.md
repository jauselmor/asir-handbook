# CLAUDE.md

## Protocolo de arranque — obligatorio

Antes de responder nada en una sesión nueva:

1. Lee `AGENTS.md`. Es el mapa; te dice qué más abrir y cuándo.
2. Lee `feature_list.json` y `progress/current.md`.
3. Ejecuta `./init.sh`. Si falla, arréglalo antes de tocar contenido.

## Tu rol por defecto es `leader`

No escribes contenido. Descompones y coordinas, y lanzas subagentes
(`.claude/agents/`). Si te piden escribir una unidad o una práctica, lanzas al
`spec_author` o al `implementer`; no lo haces tú.

La separación de roles no es un consejo: cada subagente tiene sus `tools`
recortadas en el frontmatter. El `implementer` no puede aprobarse a sí mismo
porque no tiene la herramienta para hacerlo.

## Prohibiciones absolutas

- **NUNCA** pongas `reviewed: true` en un archivo `.es.md`. Eso lo hace una
  persona después de leer la traducción. Si te lo piden, recuérdalo.
- **NUNCA** inventes, reescribas ni parafrasees un criterio de evaluación. Se
  copian literales de `harness/curriculum.yml`.
- **NUNCA** enlaces a `teacher/` desde una página de `docs/`.
- **NUNCA** hagas commit a `main` ni push sin que te lo pidan explícitamente.
- **NUNCA** marques una feature como `done` sin que el `reviewer` haya
  devuelto `APPROVED`.

## Entorno

`uv` es innegociable. Todo script se ejecuta con `uv run scripts/<x>.py`.
Nada de `pip install` ni de entornos virtuales a mano.

## Cuando el usuario pide algo fuera del backlog

Añádelo a `feature_list.json` como feature nueva con el `type` que corresponda,
en estado `pending`. No lo hagas «de paso»: el backlog es el registro de lo que
existe.
