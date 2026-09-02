# CHECKPOINTS.md — qué significa «terminado»

El `reviewer` comprueba estos puntos. Si alguno falla, la feature no se cierra.
Los checkpoints dependen del `type` de la feature.

## C0 — Comunes a todo tipo

- [ ] `./init.sh` termina en verde.
- [ ] La feature está en `feature_list.json` y su `status` refleja la realidad.
- [ ] Hay exactamente una feature `in_progress` (o ninguna, si se acaba de cerrar).
- [ ] No hay cambios sin commitear que no formen parte de esta feature.
- [ ] `progress/history.md` tiene una entrada nueva con el resultado.

## C1 — `content_theory` (páginas de unidad)

- [ ] Existen `target.en` y `target.es`, y el español no está vacío ni es un `TODO`.
- [ ] El frontmatter lleva `title`, `unit`, `hours`, `term` y `ce`.
- [ ] `hours` y `term` coinciden con los de `harness/curriculum.yml` para esa UP.
- [ ] Todos los CE de `ce:` existen en el currículo y coinciden con los que
      `curriculum.yml` asigna a esa unidad. Ni uno de más, ni uno de menos.
- [ ] El texto de cada CE está copiado literal, dentro de un bloque `??? info`.
- [ ] Están las cuatro secciones obligatorias de `harness/conventions.md`.
- [ ] Los términos del glosario se han traducido según la tabla, sin inventar.
- [ ] Si hay sección «Going further», su contenido figura en `extension:` del
      currículo o no pretende cubrir ningún CE.
- [ ] El español queda con `reviewed: false`. **El revisor no lo cambia.**

## C2 — `content_lab` (prácticas)

Todo lo de C1, y además:

- [ ] Existe el archivo emparejado en `teacher/labs/` con `pairs_with` apuntando
      a la versión inglesa de la práctica.
- [ ] El solucionario no está vacío: contiene los comandos reales de resolución.
- [ ] La práctica **no depende del secreto**: se puede seguir defendiendo aunque
      el alumno lea el solucionario (ver `harness/principios.md`).
- [ ] Los comandos de consola son reales y ejecutables en el entorno declarado
      en `context.environment`. Nada de comandos plausibles pero inventados.
- [ ] Hay un criterio de verificación por parte del alumno: cómo sabe él, sin
      preguntar, si lo ha hecho bien.
- [ ] Ninguna página de `docs/` enlaza al solucionario.

## C3 — `content_lab_update` (ampliación de una práctica)

- [ ] El cambio es **aditivo**: `git diff` no muestra líneas eliminadas del
      contenido previo, sólo añadidas.
- [ ] La sección nueva se integra donde toca, no pegada al final sin criterio.
- [ ] Si la ampliación cubre CE nuevos, se han añadido al frontmatter y el
      solucionario se ha ampliado en paralelo.
- [ ] El `source_sha` del español se ha invalidado (la traducción vuelve a
      quedar `STALE`, y eso es correcto: hay que retraducir).

## C4 — `layout_config` (mkdocs.yml, estilos)

- [ ] `mkdocs build --strict` pasa.
- [ ] El cambio no afecta a `docs_dir` de forma que `teacher/` entre en el build.
- [ ] Si se toca `pymdownx.snippets`, el `base_path` sigue acotado y no incluye
      la raíz del repositorio.
- [ ] No se ha añadido ningún plugin sin fijar su versión en `pyproject.toml`.

## C5 — `pedagogy_eval` (rúbricas, instrumentos)

- [ ] Todo CE citado existe en el currículo.
- [ ] La rúbrica tiene descriptores por nivel, no sólo porcentajes.
- [ ] Los pesos suman 100 % dentro de cada RA.
- [ ] Vive en `teacher/assessment/`, fuera del build.
