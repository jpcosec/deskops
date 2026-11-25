---
sldb:
  by: agent
  at: '2026-11-25T02:51:34Z'
  authority: generated
  via: save_document_payload
id: task-un-dispatch-start-que-falla-antes-de-que-arranque-el-agente-no-gasta-intento
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files:
- deskops/dispatch.py
- tests/test_dispatch.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-un-dispatch-start-que-falla-antes-de-que-el-agente-arranque-no-gasta-intento
---

# Un dispatch start que falla antes de que arranque el agente no gasta intento

## Rationale

_Explain why this task exists or the business driver behind it._

Piloto UI-122 de MEPU (nota PARA DESKOPS 20261124-220541 punto 4): dos fallas de infraestructura de scion dejaron la tarea sin intentos sin haber trabajado; quedaron el run_dir, el worktree, la rama y el commit del RunDoc.

## Goal

_Describe the concrete result this task must produce._

Si scion templates sync o scion start fallan, o el agente queda en fase error, dispatch start borra el run_dir, destrackea el RunDoc, deshace su commit (o commitea el borrado), quita worktree y rama, y avisa fallo tecnico reintentable; el siguiente start usa el mismo intento.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py (start), tests/test_dispatch.py y el parrafo de start fallido en docs/operator-manual.md (Integrate modes). Fuera: reap, el modo pr y el contador de intentos (sigue siendo la existencia del run_dir).

## Implementation Path

_Outline the expected implementation route or affected surface._

1. En start, antes de record_scion_run, anota los archivos del store (_STORE_RUN_PATHS) sin cambios locales; tras _commit_run_store guarda el sha del commit del RunDoc si HEAD avanzo. 2. Envuelve scion templates sync, el prompt, git worktree add y scion start en una ruta de fallo tecnico: si sync o start salen con codigo distinto de 0, o si scion list muestra al agente con phase error o failed (FAILED_PHASES), llama _undo_start y devuelve el codigo de scion (6, EXIT_SCION_ERROR, para la fase error; 8 si falla worktree add). 3. _undo_start(root, name, run_dir, run_commit, clean_store), en este orden y tolerando pasos ya hechos (idempotente): quita worktree y rama deskops/<name> si existen; destrackea el RunDoc run-<slug>; borra el run_dir (su existencia es lo unico que cuenta como intento); si HEAD sigue siendo el commit del RunDoc hace git reset --soft HEAD^, saca del indice esas rutas y devuelve los archivos de clean_store a HEAD; si HEAD ya avanzo (otro commit encima) commitea con pathspec el borrado como 'run: <name> deshecho (fallo tecnico de scion)' con [skip ci], sin tocar trabajo ajeno. 4. Si el agente existe en scion (fase error), scion delete <name> --yes para poder reusar el nombre. 5. Salida en stdout: 'fallo tecnico: <detalle>' y 'no se gasto el intento N de <task> <rol>: reintentable'. 6. Tests: start con scion start o sync fallando tres veces seguidas no deja run_dir, commit ni cambios en .sldb/runs y el cuarto start (sin falla) usa el intento 1; agente en phase error se borra y devuelve 6; con un commit ajeno encima se commitea el borrado.

## Validation

_List the checks required before this task can close._

- pytest tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

pytest tests/test_dispatch.py pasa con los tests nuevos de start fallido, y dos fallas seguidas de scion start ya no dejan la tarea 'sin intentos'.
