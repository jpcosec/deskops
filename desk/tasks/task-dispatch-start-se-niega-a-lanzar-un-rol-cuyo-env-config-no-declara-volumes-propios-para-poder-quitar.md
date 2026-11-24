---
sldb:
  by: agent
  at: '2026-11-24T02:17:54Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-start-se-niega-a-lanzar-un-rol-cuyo-env-config-no-declara-volumes-propios-para-poder-quitar
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234509-suggestion-seguridad-todo-agente-claude-del-broker-recibe-sldb-1-y-dev-shm-en-escritura-sea-del-proyecto-que-sea.md
depends_on:
- task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale
pills: []
files:
- deskops/dispatch.py
- docs/operator-manual.md
- tests/test_dispatch.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# dispatch start se niega a lanzar un rol cuyo env_config no declara volumes propios, para poder quitar el montaje global de SLDB_1 y /dev/shm de los agentes claude

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234509 (scion-coordination, medido el 2026-11-23): todo agente claude del broker recibe /mnt/ssd/proyectos/SLDB_1 y /dev/shm montados en escritura, 6 Gi y red del host, sea del proyecto que sea, aunque se pase otro --config: viene de profiles.local.harness_overrides.claude en el settings.yaml de scion del usuario (piloto IR). Un agente de mepu, ftcourier o un desk de heyantonia puede escribir en deskops y sldb; Governance lo marca como bloqueante para usar scion con sus desks. Quitar ese montaje global es decisión de JP y lo ejecuta scion-coordination en ventana, no esta tarea. ORDEN: esta tarea no corre antes de que cierre task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale, es decir, antes de que las plantillas deskops-executor y deskops-tester declaren sus propios volumes en su --config; si no, al quitar el montaje global los ejecutores y testers se quedan sin workspace.

## Goal

_Describe the concrete result this task must produce._

(1) deskops dispatch start lee el env_config del rol (DispatchRole.env_config) antes de lanzar; si el archivo no existe, no declara volumes, o ninguno de sus volumes contiene cfg.workspace, no lanza, imprime "env_config <ruta> no declara un volume que contenga <workspace>" y sale con un código distinto de 0 (no reintentable por la cola). (2) deskops doctor avisa lo mismo para cada rol de dispatch del desk. (3) docs/operator-manual.md, en la sección de despacho, dice que cada rol declara sus volumes y que el montaje global de scion se retira (por decisión de JP) una vez que todos los desks despachados lo hacen.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/dispatch.py, el chequeo de doctor, docs/operator-manual.md, tests/test_dispatch.py y el test de doctor que corresponda. No entra: editar el settings.yaml de scion ni reiniciar el server (scion-coordination, en ventana, con OK de JP), los env_config de .bootstrap (son de la máquina), el piloto wf-desks (declara sus propios volumes aparte).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_dispatch.py con scion falso: test_start_refuses_role_without_volumes, test_start_refuses_volumes_that_do_not_cover_workspace, test_start_launches_when_volumes_cover_workspace. p2: test de doctor con un env_config sin volumes. p3: implementar. p4: suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_doctor_alerts.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan; con el desk/config.json real de deskops y los env_config de .bootstrap ya con volumes (de la tarea runtime-template), deskops doctor --root . no da el aviso nuevo.
