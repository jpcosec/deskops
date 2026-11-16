---
sldb:
  by: agent
  at: '2026-11-16T06:05:38Z'
  authority: generated
  via: save_document_payload
id: task-cc53-docs-configuration-md-explica-que-es-configuracion-y-como-se-declara-un-tipo-de-tarea-nuevo-con
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Entra: docs/configuration.md, docs/operator-manual.md, docs/workflow-policy-reference.md, docs/faq.md, deskops/data/faq.md, desk/rituals (solo via deskops edit ritual), tests/test_docs_recipes.py, CHANGELOG.md. Las dos pruebas de ayuda existentes siguen pasando: tests/test_output_goldens.py (goldens de ayuda) y tests/test_cli_help_examples.py (ejemplos). No entra: cambiar codigo de deskops. Precisiones del preflight 1: un ritual se corrige si, para alguna coincidencia del grep, el archivo o comando nombrado no existe hoy (ls o deskops --help lo confirman); la frase se reemplaza por el comando o archivo vigente que hace lo mismo y, si no hay, se borra. Receta de vista nueva: declarar un ViewDoc en el desk (formato de los ViewDoc de deskops/data), deskops desk update --apply, y verla con deskops view <nombre> --root .; test_docs_recipes.py la ejecuta tambien y comprueba que la vista responde.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/models, deskops/data/rules y la doc de sldb rules. 2) Escribir el doc. 3) Test de receta. 4) Enlaces, FAQ, rituales, CHANGELOG.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_docs_recipes.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

configuration.md existe con ambas recetas; test_docs_recipes pasa (tarea bloqueada y luego activada); enlaces y FAQ presentes.
