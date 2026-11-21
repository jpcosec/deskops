Task: task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u
Title: dispatch commitea también el run.md del run dir junto con su RunDoc (integrate fallaba en store con un agente vivo)
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T19:01:25Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# dispatch commitea también el run.md del run dir junto con su RunDoc (integrate fallaba en store con un agente vivo)

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: el integrate de la tarea de init y .gitignore falló con 'fallo: store: ruta ausente en el commit: runs/subagents/exec-deskops-e-e70b6cd9c7de/run.md'. Desde el arreglo de RunDoc (d42ee663, integrado en b9674d25), dispatch start commitea con pathspec los archivos de store del RunDoc (_commit_run_store y _run_store_paths, deskops/dispatch.py:186), pero no el run.md del run dir, que es el archivo trackeado del RunDoc. El run dir recién se commitea en el closeout. Mientras haya un agente vivo, el tip lleva un RunDoc cuyo archivo no está en el commit, y el gate de store de integrate lo rechaza: ningún integrate de deskops pasa con un agente corriendo.

## Goal

_Describe the concrete result this task must produce._

_run_store_paths incluye el run.md del run dir del agente (runs/subagents/exec-<nombre>/run.md, y -testing para testers, el mismo de _run_dir_for), si existe. _commit_run_store lo commitea junto con el store, con pathspec. Así el RunDoc commiteado siempre tiene su archivo en el mismo commit, e integrate pasa el gate de store con agentes vivos. El closeout que después commitea el run dir completo no se rompe (run.md ya trackeado).

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (_run_store_paths y _commit_run_store), tests/test_dispatch.py y CHANGELOG. Fuera: el gate de store de integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: después de dispatch start (simulado), el commit 'run: <agente>' contiene el run.md del run dir además del shard del RunDoc. p2: test de que el gate de store (el mismo chequeo que corre integrate) pasa sobre ese commit. p3: implementar. p4: tests/test_dispatch.py e tests/test_integrate.py en verde, también con LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es. p5: CHANGELOG; commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo. No hace falta la suite completa: la corre integrate.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos, tests/test_dispatch.py y tests/test_integrate.py pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-dispatch-commitea-tambien-el-run-md-del-run-dir-junto-con-su-rundoc-integrate-fallaba-en-store-con-u"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
