FILE:desk/tasks/task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act.md
---
sldb:
  by: agent
  at: '2026-11-16T06:01:09Z'
  authority: generated
  via: save_document_payload
id: task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-002453-suggestion-piloto-scion-fase-1-brechas-del-coordinador-y-del-ejecutor-claude-en-contenedor.md
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
- deskops/models/run.py
- deskops/services/closure.py
- tests/test_scion_runtime.py
- tests/test_closeout.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-scion-coordinator-progresses-authorized-work
from_drawer: desk/drawer/tasks/task-correlacionar-intentos-scion-con-rundoc-y-closeout.md
---

# RunDoc por intento: identidad propia, intencion y confirmacion de dispatch separadas y el closeout actualiza el intento

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (auditoria del 2026-10-30) y requisito D6 de Governance. deskops/runtime/scion.py:842 usa run_id = run-<agent_slug>, sin distinguir reintentos; deskops/services/closure.py no toca RunDoc; la docstring de deskops/models/run.py:9-15 dice que nada lo escribe, pero record_scion_run (scion.py:823) si lo hace. La nota del piloto scion fase 1 confirma que el coordinador despacho sin escribir el RunDoc de intencion.

## Goal

_Describe the concrete result this task must produce._

Cada intento tiene un RunDoc propio: id run-<agent_slug> en el intento 1 y run-<agent_slug>-a2 en el 2 (como el nombre del hijo en el contrato de despacho de desk/roles/deskops-supervisor.md, seccion Dispatch contract); el intento sale de la etiqueta deskops.attempt del despacho, sin contador nuevo. RunDoc gana dos campos: intent_at (cuando runtime template registra la intencion, outcome in_progress) y dispatch_confirmed_at (cuando se observa el agente en scion), mas external_ref scion://agent/<slug>. Un reintento nunca sobrescribe el anterior. closeout commit con --run-dir actualiza el RunDoc cuyo campo run_dir coincide (outcome, commit, finished_at); resolved-by no tiene run-dir y no toca RunDoc. La docstring de deskops/models/run.py describe quien escribe RunDoc, estos campos y el formato del id.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/runtime/scion.py, deskops/models/run.py, deskops/services/closure.py, tests/test_scion_runtime.py y tests/test_closeout.py. Primero se verifica en el repo scion hermano (/mnt/ssd/proyectos/SLDB_1/scion) que identidad de ejecucion expone la API (Agent.RunID/PreviousRunIDs en pkg/store/models.go); si no esta expuesta, se usa solo la identidad interna. No entra: importar conversaciones o mensajes de scion, otro broker, replicacion, UI. Precisiones del preflight 1: el id es run-<agent_slug> en el intento 1 y run-<agent_slug>-a2 en el 2, igual que el nombre del hijo en el contrato de despacho del rol deskops-supervisor (no hay intento 3). El intento sale de la etiqueta deskops.attempt del despacho, no de un contador nuevo. Si la API de scion no expone el run id, se usa solo la identidad interna y la docstring de run.py lo dice. El cierre localiza el RunDoc por su campo run_dir igual al --run-dir de closeout commit; resolved-by, que no tiene run-dir, no toca RunDoc. La docstring de run.py describe: quien escribe RunDoc (runtime template y closeout), los campos de intencion y confirmacion y el formato del id. tests/test_model_contract_snapshot.py y tests/fixtures/model_contract_hashes.json se actualizan con pytest --update-golden si el test lo admite, o editando el hash como indica el mensaje del test.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer scion.py:800-860, models/run.py y close_from_run en closure.py. 2) id por intento desde deskops.attempt. 3) Campos intent_at, dispatch_confirmed_at y external_ref. 4) closure actualiza el RunDoc del run_dir. 5) Tests: dos intentos -> dos RunDoc; el cierre del segundo actualiza solo el segundo; RunDocs viejos sin los campos nuevos siguen leyendose.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 5 pasan y el cambio de contrato de RunDoc queda registrado en el snapshot de modelos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

