---
sldb:
  by: agent
  at: '2026-11-16T00:45:05Z'
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

deskops/identity.py (ecosystem_registry_dir, load_ecosystem_registry, find_registered_desk, expanduser en resolve_registered_root), deskops/cli/commands/message.py (destino por find_registered_desk; identidad del remitente por raiz en el registro del ecosistema como ultimo recurso), deskops/cli/commands/repo.py (repo register resuelve la ruta con la misma resolve_registered_root de identity.py, con ~), tests/test_message_ecosystem_registry.py. Fuera: registrar repos en ~/setup (se hace despues con deskops repo register), cambiar el modelo RepositoryDoc. Precisiones (preflight-1): p1 DESKOPS_ECOSYSTEM_REGISTRY, si esta definida y no vacia, gana sobre el valor por defecto ~/setup/desk/registry; es el directorio registry (el que tiene repo-*.md), y las rutas relativas de sus entradas resuelven contra la raiz del repo que lo contiene (padre de desk/). p2 el ~ se expande solo en el campo path de RepositoryDoc, en todos los registros (local y del ecosistema); las rutas relativas siguen como hoy. p3 solo cuenta la entrada del repo pedido: si su raiz no existe en esta maquina, SLDBStoreError con 'does not exist on this machine' y rc 1; entradas ajenas no afectan. p4 no se escribe nada en ningun lado: ni inbox ni directorios del destino, ni la nota. p5 la raiz del remitente (find_context_root) se compara con resolve_registered_repo_by_root sobre las entradas del ecosistema; se toma el id de esa entrada; si no aparece, el error actual 'Unable to resolve sender identity'. Orden del remitente: registro propio, desk/config.json, ecosistema. p6 sin store en el remitente solo cambia la busqueda (no hay registro propio); la nota se escribe en el inbox del destino igual que hoy, con su store si lo tiene. p7 la entrega no cambia: un archivo nuevo desk/inbox/<fecha>-<kind>-<slug>.md en el destino, como hoy. p8 en repo.py solo cambia _resolve_registered_root de repo register.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_message_ecosystem_registry.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_message_ecosystem_registry.py en verde con el CLI real; deskops message send --to deskops desde un repo sin registro propio entrega en desk/inbox de deskops. Precisiones (bundle-1): b1 p4 rige solo en el caso de error (raiz del destino inexistente): ahi no se escribe nada; en el caso normal la nota se entrega como dice p6/p7. b2 para el remitente gana la primera fuente que responde en el orden registro propio, desk/config.json, ecosistema; no se comparan ni se combinan ids entre fuentes. b3 la comprobacion de raiz inexistente vale para la entrada que resolvio el destino, venga del registro propio o del ecosistema.
