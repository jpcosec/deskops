---
sldb:
  by: agent
  at: '2026-11-17T02:54:58Z'
  authority: generated
  via: create_document
id: task-se-retiran-del-drawer-los-planes-workspace-documental-gates-por-tipo-deskops-ui-y-deskops-como-confi
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/tasks/task-jp-decide-si-el-plan-workspace-documental-se-retira-con-sus-67-fichas-o-se-rescatan-nodos.md
depends_on:
- task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo
pills: []
files:
- tests/test_review_command.py
- tests/test_review_doc.py
- deskops/cli/registry.py
- docs/operator-manual.md
- docs/deskops-ui.md
- desk/drawer/plans/gates-por-tipo/dag.yaml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# se retiran del drawer los planes workspace-documental, gates-por-tipo, deskops-ui y deskops-como-config y el test de review node usa un plan fixture propio

## Rationale

_Explain why this task exists or the business driver behind it._

Triaje del drawer del 2026-11-16 pedido por el supervisor: cada nodo de los cuatro planes de desk/drawer/plans/ paso por deskops review node y se decidio botarlo o pasarlo a tarea. De 105 nodos solo dos siguen vigentes y ya tienen destino (GC08 es la tarea task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la; WS47 se pidio a sldb). El resto esta resuelto, duplicado por tareas activas u obsoleto, con su motivo en el recibo de review node de cada nodo (desk/reviews/deskops-<plan>-<nodo>/). Los planes no se pueden borrar sin mas: tests/test_review_command.py copia el plan real gates-por-tipo como fixture (PLAN_SRC) y tests/test_review_doc.py, deskops/cli/registry.py (ejemplos de ayuda), docs/operator-manual.md y docs/deskops-ui.md lo citan.

## Goal

_Describe the concrete result this task must produce._

desk/drawer/plans/ queda sin esos cuatro planes y desk/drawer/tasks/ sin la carpeta workspace-documental (git rm); los tests de review node usan un plan de prueba propio bajo tests/fixtures/plans/ (copia minima de gates-por-tipo con los nodos que los tests necesitan); los ejemplos de ayuda y las docs dejan de citar los planes borrados; los tests pasan.

## Scope

_State what is in scope and what is out of scope._

Entra: git rm de desk/drawer/plans/workspace-documental, desk/drawer/plans/gates-por-tipo, desk/drawer/plans/deskops-ui, desk/drawer/plans/deskops-como-config y desk/drawer/tasks/workspace-documental; el fixture nuevo en tests/fixtures/plans/; PLAN_SRC y las rutas de tests/test_review_command.py y tests/test_review_doc.py; los ejemplos de deskops/cli/registry.py que nombran gates-por-tipo (pasan a una ruta de ejemplo generica de plan) y sus goldens de ayuda; la linea de docs/operator-manual.md y la cita de docs/deskops-ui.md (queda como texto historico sin ruta viva). Sale: los recibos de review node ya escritos en desk/reviews/ (quedan como registro), la tarea de GC08 y tests/test_graph_missing_existing_files.py (usa rutas inventadas de un plan p, no los planes reales).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Copiar a tests/fixtures/plans/gates-por-tipo/ solo lo que los tests de review node leen (dag.yaml recortado a los nodos que usan, por ejemplo ROOT, GC01, GC02 y GC03) y apuntar PLAN_SRC ahi. 2) Correr los tests de review con el plan real todavia presente para comprobar el fixture. 3) git rm de los cuatro planes y de la carpeta de fichas. 4) Ajustar ejemplos de registry.py, regenerar solo sus goldens de ayuda, y las dos docs. 5) deskops graph missing --root . no debe sumar entradas nuevas por los planes borrados.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (sin entradas nuevas por los planes borrados)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro planes y la carpeta de fichas ya no estan en el arbol, los tests de review usan el fixture, ninguna ruta viva del repo cita los planes borrados, los cuatro archivos de test de la Validation pasan y graph missing no crece.
