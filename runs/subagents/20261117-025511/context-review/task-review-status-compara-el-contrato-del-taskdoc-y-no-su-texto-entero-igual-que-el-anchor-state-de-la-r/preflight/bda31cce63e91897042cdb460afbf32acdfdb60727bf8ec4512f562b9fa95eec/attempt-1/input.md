FILE:desk/tasks/task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r.md
---
sldb:
  by: agent
  at: '2026-11-17T01:27:05Z'
  authority: generated
  via: save_document_payload
id: task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-020638-suggestion-review-status-marca-stale-un-recibo-cuando-solo-cambia-la-cabecera-sldb-at-o-los-tags-del-taskdoc.md
- desk/inbox/20261116-094650-suggestion-editar-tags-de-una-tarea-deja-stale-sus-recibos-preflight-y-bundle.md
- desk/inbox/20261116-094652-suggestion-cambiar-el-tag-host-de-una-tarea-deja-stale-sus-recibos-preflight-y-bundle.md
depends_on: []
pills: []
files:
- deskops/services/review.py
- deskops/models/review.py
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-review-status-preserves-current-dispositions
---

# review status compara el contrato del TaskDoc y no su texto entero, igual que el anchor_state de la regla de activacion

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de pron del 2026-11-16, confirmada en deskops el mismo dia: tras `deskops edit task <id> tags '[...]'` (tags no es campo del contrato) `deskops review status` marca stale el preflight y el bundle, porque el input_sha256 se calcula sobre el texto completo del TaskDoc (incluye la cabecera sldb.at, que cambia en cada save, y los tags). En cambio `sldb rules explain rule-activation-task-code <tarea>` sigue dando true con anchor_state intact. Los dos chequeos discrepan, y el supervisor rutea por tags host:*, lo que empuja a repetir revisiones por nada.

## Goal

_Describe the concrete result this task must produce._

`deskops review status` dice stale solo cuando cambio el contrato del TaskDoc (TaskDoc.__contract__: title, goal, scope, implementation_path, files, validation, done_when) o alguna otra fuente del input de la revision (para bundle: pills, atomos, rituales y archivos enlazados), y no cuando cambian la cabecera sldb, tags, status, current_node, history o references. Para un TaskDoc, su estado coincide con el anchor_state del recibo que evalua la regla de activacion.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/review.py (ReviewService._state_for_key alrededor de la linea 763 y el calculo de input_sha256 alrededor de 482, mas la funcion que arma input_data) y tests/test_review_command.py. Opcion elegida: el estado se calcula con un hash de la proyeccion del TaskDoc a sus campos de contrato (mas las demas fuentes sin cambios), no con el input_sha256 de la corrida, que sigue igual para la evidencia. No entra: cambiar input.md ni el input_sha256 registrado, ni cambiar las reglas de activacion. Precisiones del preflight 1: el digest es el contract_sha256 del TaskDoc que sldb calcula sobre __contract__ (el mismo que usa el contrato de despacho del rol deskops-supervisor; se ubica con grep -rn contract_sha256 deskops ../sldb/src). El ReviewDoc nuevo guarda ese valor en un campo contract_sha256 (string hex). Para bundle, las demas fuentes (pills, atomos, rituales y los archivos de files) siguen entrando al hash como hoy; solo la parte del TaskDoc se reemplaza por su contract_sha256. Recibos viejos sin el campo: se comparan como hoy (input_sha256 del input entero). review status sigue mostrando un estado por clave (preflight, bundle) con la misma agregacion que hoy en _state_for_key (prioridad accepted > rejected > pending > incomplete entre los recibos vigentes). El campo contract_sha256 se agrega al modelo ReviewDoc (deskops/models/review.py).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer review.py:440-520 y 740-800. 2) Funcion contract_digest(task) sobre __contract__ (el mismo digest que usa deskops para el contrato, si existe: buscar __contract__ en deskops/). 3) _state_for_key compara ese digest con el guardado en el ReviewDoc (si el ReviewDoc no lo guarda, se agrega el campo al escribir el recibo; recibos viejos sin el campo siguen con la comparacion actual). 4) Tests: editar tags y status despues de un recibo aceptado deja status accepted; editar goal lo deja stale.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_command.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas = cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahi; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los dos casos del paso 4 pasan; en el desk de deskops, una tarea con recibos aceptados y tags editados da accepted en review status.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-review-status-compara-el-contrato-del-taskdoc-y-no-su-texto-entero-igual-que-el-anchor-state-de-la-r: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

