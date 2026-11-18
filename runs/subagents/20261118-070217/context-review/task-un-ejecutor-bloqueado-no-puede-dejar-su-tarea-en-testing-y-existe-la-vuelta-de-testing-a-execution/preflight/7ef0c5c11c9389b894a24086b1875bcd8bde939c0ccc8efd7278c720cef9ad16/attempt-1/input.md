FILE:desk/tasks/task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution.md
---
sldb:
  by: agent
  at: '2026-11-18T05:54:20Z'
  authority: generated
  via: create_document
id: task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/services/tasks.py
- deskops/runtime/scion.py
- deskops/cli/registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Un ejecutor bloqueado no puede dejar su tarea en testing y existe la vuelta de testing a execution

## Rationale

_Explain why this task exists or the business driver behind it._

El 2026-11-18 un ejecutor scion del desk de sldb entrego BLOQUEADO (necesitaba una decision de diseno), sin codigo, y aun asi corrio `deskops advance task`: la tarea paso a ritual-testing con status active. La transicion task_activates solo mira los recibos preflight y bundle, y no hay ninguna transicion que devuelva una tarea de ritual-testing a ritual-execution. El coordinador tuvo que relanzar con la tarea en un nodo que no corresponde.

## Goal

_Describe the concrete result this task must produce._

Dos cambios. (1) El lifecycle sembrado por deskops gana una transicion de ritual-testing a ritual-execution, de tipo `task_returns_to_execution`, que deja status active y que `deskops advance task` solo toma cuando se le pide con una opcion nueva `--back` acompanada de `--reason <texto>`; el motivo queda en el history de la tarea. (2) El agents.md del modo executor de `deskops runtime template` dice que, si el ejecutor termina bloqueado o sin cambios, NO corre `deskops advance task`: escribe el bloqueo en result-summary.md y termina con `sciontool status blocked "<motivo>"`.

## Scope

_State what is in scope and what is out of scope._

Dentro: la siembra del lifecycle (el modulo que escribe las RelationDoc de `desk/lifecycle`), `advance_task` en `deskops/services/tasks.py`, la opcion en `deskops/cli/registry.py`, `_render_agents_md` en `deskops/runtime/scion.py`, tests y manual. Fuera: aplicar la transicion nueva a desks reales (lo hace `deskops desk update --apply` en cada desk, despues). Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_scion_runtime.py

## Done When

_Name the observable condition that makes the task complete._

En un desk desechable una tarea en ritual-testing vuelve a ritual-execution con `advance task --back --reason`, y sin `--back` el avance normal no cambia; el agents.md del ejecutor trae la regla del bloqueo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

