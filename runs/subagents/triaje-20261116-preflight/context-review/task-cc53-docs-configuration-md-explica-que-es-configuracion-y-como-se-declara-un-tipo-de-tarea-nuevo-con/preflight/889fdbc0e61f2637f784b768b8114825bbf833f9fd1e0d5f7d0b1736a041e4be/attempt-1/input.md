FILE:desk/tasks/task-cc53-docs-configuration-md-explica-que-es-configuracion-y-como-se-declara-un-tipo-de-tarea-nuevo-con.md
---
sldb:
  by: agent
  at: '2026-11-16T04:08:58Z'
  authority: generated
  via: save_document_payload
id: task-cc53-docs-configuration-md-explica-que-es-configuracion-y-como-se-declara-un-tipo-de-tarea-nuevo-con
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-como-config/dag.yaml
depends_on: []
pills: []
files:
- docs/configuration.md
- docs/operator-manual.md
- docs/workflow-policy-reference.md
- docs/faq.md
- deskops/data/faq.md
- tests/test_docs_recipes.py
- CHANGELOG.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# CC53: docs/configuration.md explica que es configuracion y como se declara un tipo de tarea nuevo, con receta probada

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo CC53 (T5.3) del plan deskops-como-config, autorizado; dependencias CC31-CC34 y CC36 cerradas.

## Goal

_Describe the concrete result this task must produce._

docs/configuration.md mapea la configuracion de deskops (modelos y tipos de tarea, ReviewDoc y recibos, RelationDoc con attributes, RuleDoc de activacion, cierre y consistencia, ViewDoc, configuracion de grafo, semillas y plantillas) con su ubicacion en el paquete y en el desk y que ejecuta sldb en cada caso; trae una receta para declarar un tipo de tarea nuevo (subclase en desk/models/*.py, desk update --apply, RuleDoc propia, verlo con sldb rules explain y deskops advance) y otra para una vista nueva. tests/test_docs_recipes.py ejecuta la receta del tipo nuevo en un desk temporal: la tarea queda bloqueada y luego activada segun su regla. operator-manual.md y workflow-policy-reference.md enlazan a configuration.md; docs/faq.md y deskops/data/faq.md ganan 'donde esta la regla de X' y 'como agrego un tipo'. Rituales: se corrige con deskops solo el ritual cuyo texto nombre algo que ya no existe (`grep -rln 'spec/artifacts\|desk_graph.py\|doc_io\|advance task .* --to' desk/rituals`); si el grep esta vacio no se toca ninguno. CHANGELOG.

## Scope

_State what is in scope and what is out of scope._

Entra: docs/configuration.md, docs/operator-manual.md, docs/workflow-policy-reference.md, docs/faq.md, deskops/data/faq.md, desk/rituals (solo via deskops edit ritual), tests/test_docs_recipes.py, CHANGELOG.md. Las dos pruebas de ayuda existentes siguen pasando: tests/test_output_goldens.py (goldens de ayuda) y tests/test_cli_help_examples.py (ejemplos). No entra: cambiar codigo de deskops.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/models, deskops/data/rules y la doc de sldb rules. 2) Escribir el doc. 3) Test de receta. 4) Enlaces, FAQ, rituales, CHANGELOG.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_docs_recipes.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

configuration.md existe con ambas recetas; test_docs_recipes pasa (tarea bloqueada y luego activada); enlaces y FAQ presentes.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-cc53-docs-configuration-md-explica-que-es-configuracion-y-como-se-declara-un-tipo-de-tarea-nuevo-con: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

