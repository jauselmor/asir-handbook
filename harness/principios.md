# Principios rectores — par-handbook

Estos principios guían el diseño de todo el material. No son contenido
publicable: son la brújula para decidir cómo se estructura cada unidad, qué se
prioriza y cómo se evalúa. Cuando una decisión de diseño no esté cubierta por
`conventions.md`, se resuelve mirando aquí.

## Misión

El éxito profesional exige más que un buen expediente: exige excelencia y
adaptabilidad. El objetivo es formar profesionales sólidos, con las puertas
abiertas a los entornos más exigentes del sector —capaces de incorporarse a
empresas de élite y competir a nivel internacional si así lo deciden—.

## Premisas

1. **Desarrollo de competencias clave.** El currículo está vivo y alineado con
   la realidad empresarial. Se priorizan las habilidades de mayor demanda:
   resolución de problemas complejos, pensamiento crítico, dominio tecnológico
   y agilidad de aprendizaje (learnability), la única competencia que no caduca.

2. **Simulación del mundo real.** Las dinámicas del aula replican los desafíos
   del mercado laboral: los estudiantes adquieren experiencia práctica y la
   mentalidad estratégica que buscan las empresas más innovadoras.

## Implicaciones de diseño

- **Techo abierto, suelo común.** Cada unidad garantiza los resultados de
  aprendizaje del título para todo el alumnado (suelo) y ofrece rutas de
  profundización opcionales para quien quiera llegar más lejos (techo). El
  techo se declara en `curriculum.yml` bajo `extension:`, para que quede
  justificado y no se confunda con relleno.
- **Inglés como fuente de verdad.** El contenido canónico se redacta en inglés;
  el español es requisito de cumplimiento normativo, no una traducción de
  segunda. El motivo es pedagógico antes que legal: el alumnado debe pasar por
  la incomodidad de leer, escribir y pensar en inglés, porque es la lengua de
  trabajo del sector.
- **Retos antes que ejercicios cerrados.** Siempre que sea posible, la práctica
  se plantea como incidencias/tickets del mundo real, no como ejercicios de
  respuesta única.
- **El solucionario no es secreto.** `teacher/` está fuera del build de MkDocs
  pero dentro del repositorio, y el repositorio puede ser público. Por tanto
  ninguna práctica puede apoyar su valor en que la solución sea inaccesible.
  La evaluación se sostiene en la defensa del trabajo, en la variación de
  parámetros por alumno y en la resolución en vivo, no en el ocultamiento.
- **La norma manda sobre la opinión.** Todo criterio de evaluación sale de
  `curriculum.yml`, que se cotejó contra el texto oficial. Cuando el contenido
  que quieres impartir y el CE no encajan, se documenta la discrepancia; no se
  reescribe el CE.
