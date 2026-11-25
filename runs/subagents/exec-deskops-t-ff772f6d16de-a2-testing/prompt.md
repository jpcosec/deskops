Task: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
Title: runtime template de scion: image, resources y volumes van en un archivo --config y el tipo de hijo sale de un flag
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
- atom-scion-coordinator-progresses-authorized-work
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-23T11:45:18Z'
  authority: generated
  via: save_document_payload
id: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
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

deskops runtime template escribe image, resources, volumes, kubernetes y telemetry en scion-env.yaml (mismo directorio de salida que scion-agent.yaml, sobrescrito en cada corrida) y ya no en scion-agent.yaml; scion_start_argv agrega --config <ruta de scion-env.yaml>; el agents.md del coordinador usa ese --config al lanzar hijos. Dos flags nuevos de runtime template, --executor-role y --tester-role, reciben un id de RoleDoc completo (con prefijo role-; defaults role-deskops-executor y role-deskops-tester); el --type de cada hijo es ese id sin 'role-'. Ejemplo: --executor-role role-ir-executor -> rol role-ir-executor y --type ir-executor.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/runtime/scion.py (alrededor de las lineas 84-135, 266-300, 440-463 y 588-607), deskops/cli/commands/runtime.py, sus goldens de ayuda y tests/test_scion_runtime.py. No entra: cambios en el repo scion, lanzar scion de verdad, la imagen del contenedor, el engine de review dentro del contenedor (tarea aparte). Precisiones del preflight 1: scion-env.yaml se escribe en el mismo directorio de salida que scion-agent.yaml y se sobrescribe en cada corrida; contiene, como claves de primer nivel y con los mismos valores que hoy van al template, solo image, resources, volumes, kubernetes y telemetry (las que esten presentes). El agents.md del coordinador lo genera hoy runtime template en scion.py (alrededor de 588-607). El --type de cada hijo es el id de rol sin el prefijo 'role-' (role-ir-executor -> ir-executor); los defaults son role-deskops-executor y role-deskops-tester.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Separar en scion.py las claves de entorno del dict del template y escribirlas en scion-env.yaml. 2) scion_start_argv recibe la ruta y agrega --config. 3) La plantilla del agents.md del coordinador nombra --config y usa los roles recibidos. 4) Flags --executor-role/--tester-role en runtime.py con default role-deskops-executor/role-deskops-tester. 5) Tests: el template no contiene resources ni volumes; scion-env.yaml si; el argv incluye --config; con --executor-role ir-executor el agents.md generado nombra ir-executor y no deskops-executor.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_runtime_profiles.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los cuatro casos de test del paso 5 pasan y los goldens de ayuda quedan actualizados con los flags nuevos.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
