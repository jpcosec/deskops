---
sldb:
  by: agent
  at: '2026-11-24T18:27:27Z'
  authority: generated
  via: save_document_payload
id: task-desk-update-en-seco-lista-los-tags-de-tareas-con-namespace-sin-declarar-y-apply-no-mete-taskdoc-en-t
status: deferred
summary: ''
tags: []
current_node: ''
history: []
references:
- desk/inbox/20261122-231220-suggestion-desk-update-apply-activa-la-validaci-n-de-tags-de-taskdoc-y-deja-tareas-sin-poder-editarse-namespaces-del-roadmap-sin-declarar.md
depends_on: []
pills: []
files:
- deskops/atom_tags.py
- deskops/cli/commands/desk.py
- tests/test_desk_sync.py
- tests/test_atom_tags.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# desk update en seco lista los tags de tareas con namespace sin declarar y --apply no mete TaskDoc en tag_models mientras queden

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-231220 (repo-governance, visto el 22-11 en ftcourier, mepu, labchile_chatbots, shared_llm-gateway y Chatbot_Infra): deskops desk update --apply declara los namespaces en .sldb/store.yaml y mete TaskDoc en tag_models (deskops/atom_tags.py, TAG_MODELS y sync_tag_declaration, desde 5d10b2eb); desde ahí el store valida los tags de las tareas, y las tareas del roadmap de noviembre traen namespaces que ningún desk declaró (certeza, roadmap, pr, capa, categoria, nodo, responsable, semana). En ftcourier deskops edit task empezó a fallar con SLDBRuleViolationError tag_namespace y doctor sumó 55 errores; en mepu falló en las 12 tareas MEPU-N. Esta tarea cubre el punto (1) de la nota; el punto (2), heredar namespaces del desk coordinador, espera decisión de JP y la nota queda abierta por eso.

## Goal

_Describe the concrete result this task must produce._

(1) deskops desk update (en seco) lista, por namespace no declarado (ni en desk/atoms/tag-namespaces.yaml ni en FLAT_NAMESPACES), cuántas tareas lo usan y hasta 5 ids: "- Tags de tareas sin namespace declarado: capa (12: task-a, ...)". (2) Con --apply, si hay alguno, declara los namespaces para AtomDoc y ProtoAtomDoc pero NO agrega TaskDoc a tag_models, imprime la misma lista y "TaskDoc queda sin validar: declara los namespaces con deskops atoms add-namespace y vuelve a correr desk update --apply". Sin tags sin declarar, el comportamiento es el de hoy (TaskDoc entra). (3) Si el store ya tiene TaskDoc en tag_models y hay tags sin declarar, --apply lo saca, para que deskops edit task vuelva a funcionar.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/atom_tags.py (wanted_tag_declaration / sync_tag_declaration), deskops/cli/commands/desk.py (alrededor de las líneas 383-485), tests/test_atom_tags.py y tests/test_desk_sync.py. No entra: declarar namespaces en otros desks, el punto (2) de la nota (namespaces heredados del desk coordinador por store enlazado).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_desk_sync.py sobre un desk temporal con una tarea con tag capa:x: test_update_dry_run_lists_undeclared_task_tags, test_update_apply_keeps_taskdoc_out_of_tag_models_with_undeclared_tags (después, deskops edit task sobre esa tarea funciona), test_update_apply_removes_taskdoc_when_tasks_have_undeclared_tags, test_update_apply_adds_taskdoc_when_all_declared. p2: implementar. p3: suite con -n 4. p4: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_desk_sync.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_atom_tags.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan y deskops desk update --root . en este desk (sin tags sin declarar) no cambia nada.
