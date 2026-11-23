---
sldb:
  by: agent
  at: '2026-11-23T04:38:07Z'
  authority: generated
  via: create_document
id: task-deskops-trae-un-roledoc-desk-identity-instalable-en-cualquier-desk-y-runtime-template-lo-materializa
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-234447-suggestion-roledoc-de-identidad-de-desk-desk-identity-y-su-traduccion-a-agente-scion.md
depends_on:
- task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale
pills: []
files:
- deskops/cli/commands/desk.py
- deskops/runtime/scion.py
- deskops/cli/commands/runtime.py
- tests/test_desk_sync.py
- tests/test_scion_runtime.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops trae un RoleDoc desk-identity instalable en cualquier desk y runtime template lo materializa como agente scion persistente (--mode identity)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-234447 (scion-coordination, workflow scion + deskops de JP): no hay RoleDoc para la identidad de un desk. deskops tiene deskops-executor, deskops-supervisor y deskops-tester en desk/roles; sldb no tiene desk/roles. El piloto wf-desks arma el prompt pegando reglas de /mnt/ssd/proyectos/wf-desks/bin/desk-prompt.sh delante de desk/roles/deskops-supervisor.md, fuera de deskops. Texto base vigente, autorizado por Governance: /srv/wt/labchile_chatbots/.encargo-triaje-inbox.txt. Relacionadas, no se duplican: task-el-runtime-profile-traduce-los-tools-del-roledoc-al-vocabulario-de-claude-y-el-alias-de-modelo-sale (tools del RoleDoc a claude, dependencia) y task-runtime-template-de-scion-image-resources-y-volumes-van-en-un-archivo-config-y-el-tipo-de-hijo-sale (image, resources y volumes en --config).

## Goal

_Describe the concrete result this task must produce._

(1) deskops empaqueta como dato (junto a las plantillas de deskops/data/templates) un RoleDoc desk-identity: name desk-identity, kind claude, tools read, grep, find, ls, bash, y un cuerpo con estas reglas: triar el inbox propio (ack con motivo, tarea + ack, o dejar abierto lo que pide decisión de JP y decirlo); reenviar lo ajeno por deskops message send --to <dueño>; registrar un acuerdo cerrado en un hilo como atom con la referencia del hilo, una sola vez; mandar lo sin dueño a su destino; no implementar código, no despachar, no tocar la cola, no hacer push; desk/ y .sldb/ solo con los CLI; todo comando con --root <raíz del desk>. (2) deskops desk update --apply (y el modo en seco lo lista) instala ese RoleDoc en desk/roles de un desk que no lo tiene, con deskops add role por debajo; no pisa uno existente. (3) deskops runtime template acepta --mode identity: escribe un agents.md de identidad persistente que nombra la raíz del desk y el proyecto scion, sin worktree por agente (workspace relativo en un proyecto de carpeta sin git, el único modo que admite reincarnate) y sin las instrucciones de ejecutor/tester/coordinador.

## Scope

_State what is in scope and what is out of scope._

Entra: el RoleDoc empaquetado, deskops/cli/commands/desk.py (instalación en update), deskops/runtime/scion.py y deskops/cli/commands/runtime.py (--mode identity), goldens de ayuda, tests/test_scion_runtime.py y tests/test_desk_sync.py. No entra: crear el agente en scion, el hook que lo despierta (tarea aparte), cambios en el repo scion, el mapa de propiedad.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test en tests/test_desk_sync.py: test_desk_update_installs_desk_identity_role (en seco lo lista; con --apply queda desk/roles con el RoleDoc desk-identity y deskops show role desk-identity lo lee; una segunda corrida no cambia nada; uno existente no se pisa). p2: test en tests/test_scion_runtime.py: test_runtime_template_identity_mode (el agents.md nombra la raíz del desk, no menciona worktree ni deskops dispatch, y --mode con un valor desconocido sigue fallando con el mensaje de hoy actualizado). p3: implementar. p4: goldens de ayuda. p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_desk_sync.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos pasan y deskops runtime template desk-identity --mode identity --root <desk temporal> escribe el template sin error.
