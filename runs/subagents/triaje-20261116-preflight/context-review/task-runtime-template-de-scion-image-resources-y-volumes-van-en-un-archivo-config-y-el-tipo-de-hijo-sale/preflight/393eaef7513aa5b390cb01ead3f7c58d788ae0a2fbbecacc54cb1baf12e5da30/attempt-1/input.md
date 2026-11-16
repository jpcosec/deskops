FILE:desk/tasks/task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale.md
---
sldb:
  by: agent
  at: '2026-11-16T04:02:36Z'
  authority: generated
  via: create_document
id: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-232023-suggestion-runtime-template-scion-ignora-resources-y-volumes-del-template-van-como-config-del-agente.md
depends_on: []
pills: []
files:
- deskops/runtime/scion.py
- deskops/cli/commands/runtime.py
- tests/test_scion_runtime.py
- tests/fixtures/golden (ayuda de runtime template)
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-scion-coordinator-progresses-authorized-work
---

# runtime template de scion: image, resources y volumes van en un archivo --config y el tipo de hijo sale de un flag

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del piloto scion en IR, fase 1 (2026-11-15). scion ignora en scion-agent.yaml las claves de entorno image, resources, volumes, kubernetes y telemetry; la prueba de humo dio memory.max=max, sin /dev/shm del host y sin /mnt/ssd/proyectos/SLDB_1. Con `scion start --config <archivo>` si se aplican (6Gi, 2 CPU, ambos montajes). Ademas, el agents.md del coordinador fija role-deskops-executor/role-deskops-tester y --type deskops-executor/deskops-tester, pero en el desk de IR el ejecutor es ir-executor.

## Goal

_Describe the concrete result this task must produce._

`deskops runtime template` escribe image, resources, volumes, kubernetes y telemetry en un archivo aparte (scion-env.yaml, junto al template) y ya no en scion-agent.yaml; scion_start_argv agrega `--config <ruta de scion-env.yaml>`; el agents.md del coordinador usa ese --config al lanzar hijos. Los ids de rol y el --type del ejecutor y del tester salen de dos flags nuevos de `runtime template` (--executor-role y --tester-role, por defecto los de deskops).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/runtime/scion.py (alrededor de las lineas 84-135, 266-300, 440-463 y 588-607), deskops/cli/commands/runtime.py, sus goldens de ayuda y tests/test_scion_runtime.py. No entra: cambios en el repo scion, lanzar scion de verdad, la imagen del contenedor, el engine de review dentro del contenedor (tarea aparte).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Separar en scion.py las claves de entorno del dict del template y escribirlas en scion-env.yaml. 2) scion_start_argv recibe la ruta y agrega --config. 3) La plantilla del agents.md del coordinador nombra --config y usa los roles recibidos. 4) Flags --executor-role/--tester-role en runtime.py con default role-deskops-executor/role-deskops-tester. 5) Tests: el template no contiene resources ni volumes; scion-env.yaml si; el argv incluye --config; con --executor-role ir-executor el agents.md generado nombra ir-executor y no deskops-executor.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_runtime_profiles.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; sin fallas nuevas respecto de main)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro casos de test del paso 5 pasan y los goldens de ayuda quedan actualizados con los flags nuevos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

