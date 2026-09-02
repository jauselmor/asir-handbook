# AGENTS.md — mapa del repositorio

No leas este repositorio entero. Lee esta tabla, y abre sólo el archivo que
necesites cuando lo necesites.

| Archivo | Qué contiene | Cuándo leerlo |
| --- | --- | --- |
| `CLAUDE.md` | Protocolo de arranque y rol | Siempre, lo primero |
| `feature_list.json` | Backlog: qué hay que hacer y en qué estado está | Al empezar cualquier sesión |
| `harness/principios.md` | La brújula pedagógica | Antes de decidir qué contenido entra o cómo se plantea |
| `harness/conventions.md` | Estilo, glosario EN→ES, estructura de página | Antes de escribir o editar cualquier `.md` de `docs/` |
| `harness/verification.md` | Las seis comprobaciones y qué garantiza cada una | Antes de cerrar una feature, o si `init.sh` falla |
| `harness/curriculum.yml` | RA, CE y fuentes normativas. **Fuente de verdad** | Al declarar CE en una página, o al tocar cobertura |
| `CHECKPOINTS.md` | Qué significa «terminado» para cada tipo de feature | Al revisar, y antes de marcar `done` |
| `specs/<id>/` | Especificación aprobada de una feature | Al implementar esa feature, nunca antes |
| `progress/current.md` | Estado de la sesión en curso | Al arrancar y al cerrar |
| `progress/history.md` | Bitácora append-only | Sólo para escribir al final; no lo leas entero |
| `teacher/` | Solucionarios, guiones de aula, evaluación | Al escribir un lab; nunca se enlaza desde `docs/` |

## Reglas que no dependen del rol

1. **Una feature `in_progress` a la vez.** El backlog lo verifica `init.sh`.
2. **El inglés es la fuente de verdad.** El `.es.md` se escribe después.
3. **`reviewed: true` lo pone una persona.** Nunca un agente, bajo ningún motivo.
4. **Los CE se copian literales de `curriculum.yml`.** Es texto normativo.
5. **Nunca escribas en `docs/` un enlace a `teacher/`.**
6. **No hagas commit a `main` ni push sin aprobación explícita.**

## El resultado va a disco, no al chat

Cada subagente escribe su salida en un archivo y devuelve **una sola línea**
con el veredicto y la ruta:

```
APPROVED -> progress/review_up06_switching_vlans.md
```

El contenido no circula por la conversación: no se degrada al pasar de un
agente a otro y queda versionado en git.

## Estados de una feature

```
pending ──[spec_author]──> spec_ready ──⏸ HUMANO──> in_progress ──[implementer → reviewer]──> done
```

Las features con `sdd_level: light` o `none` se saltan `spec_ready` y la parada
humana; van directas a `in_progress`. Qué nivel le toca a cada tipo está en
`feature_list.json`, bajo `types`.
