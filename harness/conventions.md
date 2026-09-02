# Convenciones de escritura

Cuándo leerlo: antes de escribir o editar cualquier página de `docs/`.

## Idioma

- El archivo `.en.md` es la fuente de verdad. Se escribe primero, siempre.
- El archivo `.es.md` es obligatorio y se escribe después, a partir del inglés.
- El frontmatter del español lleva `source_sha` (huella del cuerpo en inglés) y
  `reviewed`. **`reviewed: true` lo pone una persona, nunca un agente.** Si el
  inglés cambia, el `source_sha` deja de cuadrar y la traducción queda `STALE`.
- Inglés técnico llano. Nada de florituras ni de voz de folleto. El lector es
  alguien de primero de ciclo que puede no tener el inglés muy rodado: frases
  cortas, vocabulario concreto, y el término técnico siempre en inglés aunque
  se glose entre paréntesis la primera vez.

## Glosario EN → ES

Términos que deben traducirse siempre igual, para que el alumnado los reconozca
entre las dos versiones:

| Inglés | Español |
| --- | --- |
| switch | conmutador |
| router | router (no «enrutador») |
| trunk link | enlace troncal |
| default route | ruta por defecto |
| subnet mask | máscara de subred |
| broadcast domain | dominio de difusión |
| collision domain | dominio de colisión |
| port security | seguridad de puerto |
| root bridge | puente raíz |
| learning outcome | resultado de aprendizaje (RA) |
| assessment criterion | criterio de evaluación (CE) |

La electrónica de red conserva el nombre inglés cuando es el que se usa en la
CLI y en la documentación del fabricante. Se traduce el concepto, no el comando.

## Estructura obligatoria de una página de unidad

Toda página en `docs/units/` lleva este frontmatter:

```yaml
---
title: <título de la unidad>
unit: UP6
hours: 25
term: 2
ce: [RA3.a, RA3.b, RA5.b]      # deben existir en harness/curriculum.yml
---
```

Y estas secciones, en este orden y con estos títulos exactos (en inglés en el
`.en.md`, con la traducción fijada en el `.es.md`):

1. `## What you will learn` / `## Qué vas a aprender`
2. `## Assessment criteria` / `## Criterios de evaluación`
3. `## Contents` / `## Contenidos`
4. `## Going further` / `## Para ir más lejos`  *(el techo; opcional)*

`scripts/check_structure.py` verifica esto. Una sección extra no rompe nada;
una obligatoria que falte, sí.

## Criterios de evaluación en la página

Los CE van dentro de un bloque colapsable, para que estén disponibles sin
comerse la pantalla:

```markdown
??? info "Assessment criteria (RA3)"
    - **a)** ...
```

El texto del CE se copia literal de `curriculum.yml`. No se parafrasea: es
texto normativo.

## Markdown

- Nada de HTML crudo salvo que la maquetación lo exija de verdad.
- Enlaces relativos entre páginas con extensión `.md`, para que
  `mkdocs build --strict` detecte los rotos.
- **Ninguna página de `docs/` enlaza a `teacher/`.** Es un fallo de build.
- Diagramas con Mermaid, no con imágenes, salvo topologías que Mermaid no sepa
  representar.
