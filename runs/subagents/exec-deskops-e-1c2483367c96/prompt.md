Task: task-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota-cuando-lo-demas-despues-del-closeout-es-s
Title: integrate extiende el tip sobre un merge de la rama remota cuando lo demás después del closeout es solo desk
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T04:15:45Z'
  authority: generated
  via: create_document
id: task-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota-cuando-lo-demas-despues-del-closeout-es-s
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
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

# integrate extiende el tip sobre un merge de la rama remota cuando lo demás después del closeout es solo desk

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21, sldb: origin/main recibió commits de otros (inbox de Governance, PR #3 de enlaces) después del closeout de notations validate (651a42a0). El coordinador mergeó origin/main en main local (e7e348f1) y re-encoló integrate, que falló dos veces con 'fast-forward: origin/main no es ancestro de 651a42a0'. extend_tip (deskops/integrate.py:226) hace git diff tip..HEAD, que incluye el código que trajo el merge desde el remoto, así que no extiende y se queda con el closeout, que no desciende del remoto. Rebasear en vez de mergear reescribiría los sha que citan los recibos.

## Goal

_Describe the concrete result this task must produce._

extend_tip devuelve HEAD cuando (a) la rama remota configurada (cfg.remote/cfg.branch, la misma que usa el paso fast-forward) es ancestro de HEAD y (b) los archivos que cambian los commits de tip..HEAD que no están en la rama remota, sin contar merges, son solo de desk/, .sldb/ o runs/ (git log --no-merges --name-only --format= HEAD ^tip ^<remoto>). Además, si el merge resolvió algún conflicto en archivos de código (el árbol del merge difiere de lo que daría la unión), no hace falta detectarlo: los gates corren igual sobre la copia limpia del tip extendido. Sin cambio para el caso actual de commits de desk sin merge.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/integrate.py (extend_tip y, si hace falta, cómo recibe la ref remota), tests/test_integrate.py y CHANGELOG. Fuera: el resto de los pasos de integrate.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes, en tests/test_integrate.py junto a test_tip_extends_over_later_desk_only_commits: el remoto recibe un commit de código de otro, el desk local lo mergea después del closeout y agrega un commit de desk; integrate --dry-run extiende el tip al merge y no falla en fast-forward. p2: test de que un commit de código local (no del remoto) después del closeout sigue sin extender. p3: implementar en extend_tip. p4: CHANGELOG; commit desde tu worktree con 'git commit -- <rutas>' y trailer Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py

## Done When

_Name the observable condition that makes the task complete._

Los dos tests nuevos y tests/test_integrate.py pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota-cuando-lo-demas-despues-del-closeout-es-s"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-1c2483367c96`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-1c2483367c96

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
