---
sldb:
  by: agent
  at: '2026-11-21T04:33:52Z'
  authority: generated
  via: save_document_payload
id: task-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota-cuando-lo-demas-despues-del-closeout-es-s
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/integrate.py
- tests/test_integrate.py
- e727297a14d8ec20ccbb931aa9e976ea57330d87
depends_on: []
pills: []
files:
- CHANGELOG.md
- deskops/integrate.py
- tests/test_integrate.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-integrate-extiende-el-tip-sobre-un-merge-de-la-rama-remota
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
