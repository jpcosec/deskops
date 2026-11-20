Task: task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise
Title: dispatch start lanza cada ejecutor en su propio git worktree, para que agentes en paralelo no se pisen el árbol de trabajo
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
  at: '2026-11-20T18:03:58Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise
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

# dispatch start lanza cada ejecutor en su propio git worktree, para que agentes en paralelo no se pisen el árbol de trabajo

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20, sldb: con dispatch en paralelo (bdf06f81), cuatro ejecutores de tareas distintas trabajaron a la vez en el mismo checkout /mnt/ssd/proyectos/SLDB_1/sldb. El primero en commitear (0f91540d, tarea on_write) se llevó el código de las otras tres (atoms_by_view, notations from-graph, store_check). El commit de raw_atoms_by_view (eb42a49e) quedó vacío y el tester no pudo atribuir el cambio. Lo mismo puede pasar con dos ejecutores en deskops, y con los commits de desk del coordinador. El coordinador retiene los ejecutores de un repo mientras otro trabaja en él.

## Goal

_Describe the concrete result this task must produce._

dispatch start crea para cada ejecutor un git worktree propio: una rama 'deskops/<agente>' desde la punta local del repo, en un directorio de trabajo bajo el workspace montado (p. ej. <repo>/.worktrees/<agente>, ignorado por git). El agente trabaja y commitea ahí. El tester prueba ese worktree. Al cierre, integrate (o closeout) trae el commit de la rama a la rama principal con cherry-pick o rebase y fast-forward, y borra el worktree y la rama. Los agentes de distintas tareas no comparten árbol de trabajo ni índice.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start y reap), el template de scion o el prompt para que el agente trabaje en su worktree, deskops/integrate.py o closeout para traer la rama, tests, docs/operator-manual.md y CHANGELOG. Fuera: scion.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: diseño en el informe, con cómo ve el contenedor el worktree (montado bajo el workspace) y cómo llega el commit a main (cherry-pick sobre main local, que es lo que hoy usa integrate). p2: tests: dos dispatch start de tareas distintas en un repo temporal crean worktrees y ramas separadas; los cambios de una no aparecen en la otra; reap borra el worktree; integrate trae solo el commit de su tarea. p3: implementar. p4: docs y CHANGELOG; commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

Tests nuevos y tests/test_dispatch.py y tests/test_integrate.py pasan; la suite completa la corre integrate.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-dispatch-start-lanza-cada-ejecutor-en-su-propio-git-worktree-para-que-agentes-en-paralelo-no-se-pise"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
