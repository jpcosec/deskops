FILE:desk/tasks/task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act.md
---
sldb:
  by: agent
  at: '2026-11-16T04:01:48Z'
  authority: generated
  via: create_document
id: task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

Cada intento tiene un RunDoc propio con id run-<agent_slug>-<n> (o equivalente estable), que separa la identidad interna del intento, la identidad del agente y la referencia externa scion://agent/<slug>; registra la intencion (outcome in_progress) y la confirmacion de dispatch como hechos distintos; un reintento nunca sobrescribe el anterior; closeout commit y resolved-by actualizan exactamente el RunDoc del intento cerrado (outcome, commit, timestamps). La docstring de run.py queda al dia.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/runtime/scion.py, deskops/models/run.py, deskops/services/closure.py, tests/test_scion_runtime.py y tests/test_closeout.py. Primero se verifica en el repo scion hermano (/mnt/ssd/proyectos/SLDB_1/scion) que identidad de ejecucion expone la API (Agent.RunID/PreviousRunIDs en pkg/store/models.go); si no esta expuesta, se usa solo la identidad interna. No entra: importar conversaciones o mensajes de scion, otro broker, replicacion, UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer scion.py:800-860, models/run.py y close_from_run en closure.py. 2) Contador de intento por tarea+contrato. 3) Campos de intencion y confirmacion. 4) closure actualiza el RunDoc del run_dir. 5) Tests: dos intentos -> dos RunDoc; cierre actualiza solo el segundo; RunDocs viejos siguen leyendose.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_model_contract_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Los tres casos del paso 5 pasan y el cambio de contrato de RunDoc queda registrado en el snapshot de modelos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-rundoc-por-intento-identidad-propia-intencion-y-confirmacion-de-dispatch-separadas-y-el-closeout-act: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

