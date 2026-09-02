# teacher/ — backend docente

**Esta carpeta está fuera del build de MkDocs a propósito, y su contenido es
visible en el repositorio a propósito.** No es un descuido ni algo pendiente de
arreglar: si alguien —persona o agente— propone moverla, cifrarla o borrarla
"por seguridad", la respuesta es no. La decisión está tomada y razonada en
`harness/principios.md`.

## Qué implica

Que el alumnado puede leer los solucionarios si se molesta en abrir el repo.
Por tanto **ninguna práctica puede apoyar su valor en el secreto**. La
evaluación se sostiene en:

- defensa oral del trabajo,
- variación de parámetros por alumno (direccionamiento, VLAN IDs, topología),
- resolución en vivo de una incidencia no vista,

no en que la solución sea inaccesible.

## Qué vive aquí

| Carpeta | Contenido |
| --- | --- |
| `labs/` | Solucionarios, emparejados 1:1 con las prácticas de `docs/labs/` |
| `sessions/` | Guiones de aula: temporalización real, errores típicos, sabotajes |
| `assessment/` | Rúbricas, instrumentos, banco de preguntas |

Todo en español. El gate bilingüe aplica sólo a `docs/`: esto es material tuyo,
no del alumno.

## Emparejamiento

Cada solucionario declara en su frontmatter a qué práctica corresponde:

```yaml
---
pairs_with: docs/labs/l2-security.en.md
source_sha: a1b2c3d4e5f6
---
```

`scripts/check_teacher.py` comprueba que el emparejamiento existe en ambos
sentidos y que el solucionario no se ha quedado desfasado respecto al
enunciado. Es el mismo invariante que aplica `check_translations.py` a la
traducción española, sobre otro eje.

## Lo único que sí es un fallo

Que una página de `docs/` enlace aquí. `mkdocs build --strict` no lo detecta
porque el destino está fuera del árbol publicado, así que lo comprueba
`check_teacher.py`.
