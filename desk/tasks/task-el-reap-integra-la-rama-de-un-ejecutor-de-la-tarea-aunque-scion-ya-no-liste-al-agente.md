---
sldb:
  by: agent
  at: '2026-11-25T05:34:47Z'
  authority: generated
  via: create_document
id: task-el-reap-integra-la-rama-de-un-ejecutor-de-la-tarea-aunque-scion-ya-no-liste-al-agente
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El reap integra la rama de un ejecutor de la tarea aunque scion ya no liste al agente

## Rationale

_Explain why this task exists or the business driver behind it._

En IR, el reap de task-sin-marcador-parity borro el agente deskops-e-6735ed85d05b y fallo con exit 8 por un index.lock antes de integrar; el reap reencolado salio con 0 sin integrar 94eb610 porque reap() solo llama _integrate_branch para agentes que _list_agents devuelve, y el tester quedo esperando. Se integro a mano llamando _integrate_branch (IR 3de8d97).

## Goal

_Describe the concrete result this task must produce._

Que reap integre toda rama deskops/<ejecutor> de la tarea con commits fuera de la base aunque el agente ya no exista, y encole el tester como hoy.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py (reap) y un test. Fuera: el resto de dispatch.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/deskops. En reap(), despues del bucle de agentes, para los intentos 1 y 2 de executor de la tarea (scion_child_identity(task_path,'executor',attempt) como en la funcion de la linea ~379 que busca la rama de un ejecutor; si el TaskDoc ya no existe, derivar el nombre como lo haga esa funcion o saltar), si la rama deskops/<name> existe y su nombre no esta en reaped ni vivo, llamar _integrate_branch(root, name, task_id) con el mismo manejo de codigos (EXIT_BUSY -> busy, otro -> conflict, 0 con mensaje 'integrado' -> integrated). Test nuevo tests/test_reap_orphan_branch.py con _list_agents monkeypatcheado a [] y un repo git temporal con una rama deskops/<name> con un commit: reap la integra en la base, borra la rama y encola dispatch-tester.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 PYTHONPATH=. pytest -q tests/test_reap_orphan_branch.py

## Done When

_Name the observable condition that makes the task complete._

reap integra una rama de ejecutor huerfana y encola el tester; tests/test_reap_orphan_branch.py pasa con los tests de reap existentes.
