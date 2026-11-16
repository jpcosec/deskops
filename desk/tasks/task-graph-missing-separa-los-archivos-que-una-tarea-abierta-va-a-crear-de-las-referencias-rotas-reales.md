---
sldb:
  by: agent
  at: '2026-11-16T06:21:59Z'
  authority: generated
  via: save_document_payload
id: task-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas-reales
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-010912-unclear-graph-missing-no-distingue-archivos-que-la-tarea-va-a-crear-ya-borrados-o-de-otro-repo.md
depends_on: []
pills: []
files:
- deskops/graph/checks.py
- deskops/cli/commands/graph.py
- tests/test_graph_checks.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-knowledge-graph-connects-desk-and-source-files
---

# graph missing separa los archivos que una tarea abierta va a crear de las referencias rotas reales

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de deskops del 2026-11-16 (triaje). SOURCE_PATH (deskops/graph/desk_graph.py:122-125) convierte en arista toda mencion deskops|desk|tests|spec|docs/<ruta>.<ext> del texto de un TaskDoc, y graph missing la reporta como missing_declared_target si el archivo no existe. Hoy hay unos 30 faltantes asi en desk/tasks: archivos que la tarea va a crear (tests/test_ascii_ids.py, docs/configuration.md, deskops/graph/paths.py...), archivos citados como ya borrados (deskops/specs/loader.py) y rutas de otro repo (docs/spec/spec-procesos-modelables.md de Governance). graph missing da rc 0 igual. Reescribir las rutas para esquivar el detector falsea la evidencia, asi que quedan tal cual.

## Goal

_Describe the concrete result this task must produce._

Cuando el origen de un missing_declared_target es un TaskDoc abierto (status distinto de closed, superseded, cancelled o retired) y el destino es un source_file, test_file o doc inexistente, graph missing lo reporta como informational con el codigo planned_target, separado de la lista de faltantes; los mismos destinos desde documentos que no son tareas abiertas siguen como missing. La salida dice cuantos son de cada tipo.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/checks.py (donde se arma la lista de missing y de informational; buscar MISSING_TARGET_KINDS y 'informational'), la salida de deskops graph missing en deskops/cli/commands/graph.py y tests/test_graph_checks.py. No entra: cambiar SOURCE_PATH ni el extractor, ni ocultar los planned_target (se siguen listando). Precisiones del preflight 1: el estado se lee del campo status del frontmatter del TaskDoc de origen; un status ausente o desconocido cuenta como abierto. El tipo de destino lo da el kind del nodo que ya asigna el extractor (source_file, test_file, doc). planned_target va en el campo kind del hallazgo, con el mismo reason. La linea de resumen pasa a 'N missing, M informational (P planned_target)'. Se distingue planned de mal escrito solo por el estado del origen: una ruta mal escrita en una tarea abierta tambien sale como planned_target, y eso es aceptado.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer checks.py y graph.py (comando missing). 2) Clasificar por estado del TaskDoc de origen. 3) Tests: tarea en draft (del sandbox del test) que cita un archivo de test inexistente da planned_target informational; un atomo del sandbox que cita ese mismo archivo da missing; una tarea cerrada (en history) no aplica porque ya no esta en desk/tasks.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_checks.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops graph missing --root . (los faltantes de tareas abiertas salen como planned_target informational)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 3 pasan y graph missing en el desk de deskops separa planned_target de missing.
