FILE:desk/tasks/task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li.md
---
sldb:
  by: agent
  at: '2026-11-16T00:43:51Z'
  authority: generated
  via: save_document_payload
id: task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li
status: draft
summary: message send --to cae al registro del ecosistema (~/setup/desk/registry)
  cuando el registro del remitente no lista el destino
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/identity.py
- deskops/cli/commands/message.py
- deskops/cli/commands/repo.py
- tests/test_message_ecosystem_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# message send --to resuelve el destino en el registro del ecosistema cuando el registro propio no lo lista

## Rationale

_Explain why this task exists or the business driver behind it._

MEPU (15-11, prioridad alta): deskops message send --to deskops no resuelve desde otro repo porque solo se lee el desk/registry del remitente y el de MEPU no lista a nadie; bloquea a los agentes que avisan entre repos.

## Goal

_Describe the concrete result this task must produce._

--to <repo> busca primero en el registro del remitente y despues en el registro del ecosistema (~/setup/desk/registry, o la variable DESKOPS_ECOSYSTEM_REGISTRY), tambien desde un repo sin store; las rutas del registro aceptan ~ para valer en todas las maquinas; una raiz registrada que no existe en esta maquina es un error y no se escribe nada.

## Scope

_State what is in scope and what is out of scope._

deskops/identity.py (ecosystem_registry_dir, load_ecosystem_registry, find_registered_desk, expanduser en resolve_registered_root), deskops/cli/commands/message.py (destino por find_registered_desk; identidad del remitente por raiz en el registro del ecosistema como ultimo recurso), deskops/cli/commands/repo.py (misma resolucion de rutas), tests/test_message_ecosystem_registry.py. Fuera: registrar repos en ~/setup (se hace con deskops repo register), cambiar el modelo RepositoryDoc.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_message_ecosystem_registry.py en verde con el CLI real; deskops message send --to deskops desde un repo sin registro propio entrega en desk/inbox de deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-message-send-to-resuelve-el-destino-en-el-registro-del-ecosistema-cuando-el-registro-propio-no-lo-li: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

