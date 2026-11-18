FILE:desk/tasks/task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution.md
---
sldb:
  by: agent
  at: '2026-11-18T07:04:57Z'
  authority: generated
  via: save_document_payload
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
- deskops/lifecycle.py
- deskops/services/tasks.py
- deskops/runtime/scion.py
- deskops/cli/registry.py
- deskops/data/desk_declaration.yaml
- tests/test_lifecycle_graph.py
- tests/test_scion_runtime.py
- docs/operator-manual.md
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

Dos cambios.

(1) Transicion de vuelta. La siembra del lifecycle (los archivos de la carpeta `deskops/data/lifecycle` y su lista en `deskops/data/desk_declaration.yaml`) gana una transicion de `RitualDoc:ritual-testing` a `RitualDoc:ritual-execution` con `relation_type: task_returns_to_execution`, sin condicion, con `attributes.sets.status: active`, `attributes.terminal: false` y un atributo nuevo `attributes.manual: true`, mas su archivo de tipo, copiando la forma de `deskops/data/lifecycle/testing-task_hands_to_closeout.md` y `deskops/data/lifecycle/type-task_hands_to_closeout.md`. Una transicion con `manual: true` nunca la toma el avance normal: `deskops advance task <id>` sin opciones se comporta exactamente como hoy. `deskops advance task <id> --back --reason "<texto>"` toma solo transiciones manuales desde el nodo actual; agrega a `history` la cadena `task_returns_to_execution: <texto>` (hoy history guarda solo el relation_type; esta entrada lleva ademas el motivo); corre los post-hooks de esa transicion igual que cualquier avance. `--back` sin `--reason`, o con motivo vacio, sale con codigo 2 y un mensaje; `--reason` sin `--back` sale con codigo 2; `--back` en un nodo sin transicion manual sale bloqueado con el mensaje `no hay transicion de vuelta desde <nodo>`.

(2) Regla del ejecutor. El agents.md del modo executor (funcion `_render_agents_md` de `deskops/runtime/scion.py`) dice que, si el ejecutor termina bloqueado o sin cambios, NO corre `deskops advance task`: escribe el bloqueo en result-summary.md y termina con `sciontool status blocked "<motivo>"`.

El manual (`docs/operator-manual.md`, seccion `Inspect, edit, and advance a task`) documenta `--back --reason` y el atributo `manual`.

## Scope

_State what is in scope and what is out of scope._

Dentro: la carpeta `deskops/data/lifecycle` y `deskops/data/desk_declaration.yaml`, `deskops/lifecycle.py`, `deskops/services/tasks.py`, la opcion en `deskops/cli/registry.py` y el comando que la recibe, `deskops/runtime/scion.py`, `tests/test_lifecycle_graph.py`, `tests/test_scion_runtime.py`, `docs/operator-manual.md`, y los goldens de ayuda que cambien por la opcion nueva. Fuera: aplicar la transicion a desks reales (lo hace despues `deskops desk update --apply` en cada desk). Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_scion_runtime.py` pasa, con tests nuevos sobre un desk desechable de `tmp_path` que comprueban: (a) una tarea en ritual-testing vuelve a ritual-execution con `--back --reason`, queda con status active y su history termina en `task_returns_to_execution: <texto>`; (b) sin `--back`, desde ritual-testing el avance normal sigue yendo a ritual-closeout y nunca toma la transicion manual; (c) los tres casos de codigo 2 y el caso bloqueado; (d) un post-hook declarado en la transicion de vuelta corre; (e) el agents.md del ejecutor contiene `sciontool status blocked`.
- Los goldens de ayuda afectados se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` y se conservan solo los que cambian por la opcion nueva.
- `deskops doctor --root .` sobre un desk recien creado con `deskops init` no informa deriva por la transicion nueva.

## Done When

_Name the observable condition that makes the task complete._

En un desk desechable una tarea en ritual-testing vuelve a ritual-execution con `advance task --back --reason`, y sin `--back` el avance normal no cambia; el agents.md del ejecutor trae la regla del bloqueo.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

