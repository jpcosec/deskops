---
sldb:
  by: agent
  at: '2026-11-24T02:19:33Z'
  authority: generated
  via: save_document_payload
id: task-las-rutas-y-credenciales-de-maquina-de-dispatch-e-integrate-salen-de-desk-config-json-versionado-a-d
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-182810-unclear-orden-pedido-por-el-concilio-clones-primero-y-rutas-de-m-quina-en-desk-config-json.md
- desk/inbox/20261123-034522-suggestion-dispatch-no-se-puede-partir-entre-config-json-y-config-local-json-el-proyecto-y-los-roles-no-quedan-versionados.md
- desk/inbox/20261123-101520-suggestion-no-hay-comando-para-declarar-un-queue-job-nuevo-ni-el-bloque-integrate-en-desk-config-json.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las rutas y credenciales de máquina de dispatch e integrate salen del config.json versionado del desk a su config.local.json (no versionado) en deskops y sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261122-182810-unclear-orden-pedido-por-el-concilio-clones-primero-y-rutas-de-m-quina-en-desk-config-json (2026-11-22, concilio): desk/config.json de deskops y sldb guarda en dispatch e integrate rutas de una máquina (/mnt/ssd/..., /home/robocop/.scion/...) y un credential.helper con la cuenta de una persona. Para llevar dispatch a otros desks hay que separar lo de cada máquina sin versionarlo. El mecanismo ya existe: DeskConfig.load (deskops/config.py:104) mezcla el config.local.json del desk (no versionado) sobre config.json, con deep merge, y el config.local.json del desk (no versionado) está en .gitignore. Queue, dispatch e integrate leen por DeskConfig.load, así que cubre dispatch e integrate. Falta usarlo y poder escribirlo sin editar a mano.

## Goal

_Describe the concrete result this task must produce._

1) Un comando de deskops escribe una clave en el config.local.json del desk (no versionado) (por ejemplo deskops config set --local <ruta.de.clave> <valor> --root ., o el que encaje con el comando queue job set de la tarea hermana de la cola), validando el resultado con DeskConfig. 2) En deskops y sldb, las claves de máquina de dispatch e integrate (suite con rutas absolutas, tools_checkout, tests_lock, push_env con credential.helper, rutas de scion) pasan a config.local.json con ese comando, y config.json queda solo con lo versionable (branch, mode, remote_url sin credenciales, timeouts, retry_exit_codes). 3) deskops doctor avisa si config.json versionado contiene rutas absolutas o un credential.helper.

## Scope

_State what is in scope and what is out of scope._

Dentro: el comando nuevo, el aviso de doctor, tests y docs; aplicarlo en deskops (este desk). sldb lo aplica su coordinador con el comando nuevo. Fuera: el modo pr de integrate (tarea hermana).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test del comando: escribe una clave anidada en config.local.json de un desk temporal y DeskConfig.load la toma por encima de config.json. p2: test del aviso de doctor. p3: implementar. p4: aplicar en deskops y comprobar que la cola sigue andando (deskops queue list). p5: suite con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_config.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan y el desk/config.json de deskops no contiene rutas absolutas ni credential.helper.
