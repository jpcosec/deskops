---
sldb:
  by: agent
  at: '2026-11-23T01:55:57Z'
  authority: generated
  via: save_document_payload
id: task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-testing
history:
- task_activates
references:
- deskops/config.py
- deskops/dispatch.py
- deskops/integrate.py
- docs/operator-manual.md
- tests/test_dispatch.py
- tests/test_integrate.py
- ca7ecfc518fa8955e2d51e99caa72449fe5b5e1c
depends_on: []
pills: []
files:
- CHANGELOG.md
- deskops/config.py
- deskops/dispatch.py
- deskops/integrate.py
- docs/operator-manual.md
- tests/test_dispatch.py
- tests/test_integrate.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-integrate-en-modo-pr-termina-en-un-pr-hacia-la-rama-base-declarada
---

# integrate puede terminar en un PR a la rama base declarada (modo pr) en vez de un push directo, con el cierre dentro del PR

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de Governance 20261122-182718-suggestion-dispatch-reap-e-integrate-empujan-directo-no-sirven-en-repos-con-dev-protegida-ni-cumplen-la-regla-de-pr (2026-11-22, encargo coordinado con la sesión de Governance de JP). Regla de JP del 19-11: todo cambio entra por worktree, PR a dev, QA y main; y del 20-11: el cierre va dentro del PR. Hoy dispatch reap trae los commits del ejecutor a la rama base local (merge --ff-only o cherry-pick, deskops/dispatch.py) e integrate empuja directo al remoto (deskops/integrate.py:353-359, 'git push origin <tip>:<branch>'). Sirve para deskops y sldb, cuya main no está protegida, pero en los repos de heyantonia con dev protegida (Chatbot_Infra, ftcourier, labchile_chatbots) falla o se salta la regla. Governance no configura dispatch en esos desks hasta que esto exista. La rama base ya sale de la configuración (_base_branch, dispatch.py:93, usa integrate.branch), pero no hay modo PR.

## Goal

_Describe the concrete result this task must produce._

IntegrateConfig (deskops/config.py) gana un campo mode con dos valores: 'push' (el de hoy, por defecto, para deskops y sldb) y 'pr'. En modo pr, el ciclo dispatch start, reap e integrate termina en un PR abierto hacia integrate.branch (la rama base declarada, por ejemplo dev). No hay push directo ni merge local a la rama base. 1) reap en modo pr lleva los commits del ejecutor a una rama local de la tarea, task/<task-id>, creada desde la base, y no a la base. 2) El closeout de la tarea se commitea en esa misma rama, así el cierre va dentro del PR. 3) integrate en modo pr corre las mismas compuertas sobre la punta de task/<task-id>, la empuja al remoto como rama task/<task-id> y abre o actualiza el PR hacia integrate.branch con gh pr create (base = integrate.branch, título = el de la tarea, cuerpo con el id de la tarea y el resumen del closeout). Si el PR ya existe, solo empuja. Imprime la URL del PR. 4) El modo push queda igual. 5) La configuración por máquina (remote_url con credenciales, push_env, tools_checkout, rutas de suite) puede ir en el config.local.json del desk (no versionado), que DeskConfig.load ya mezcla sobre config.json (deskops/config.py:104) y que está en .gitignore. La tarea documenta esa división en docs/ y no versiona rutas de máquina nuevas.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/config.py (IntegrateConfig.mode), deskops/dispatch.py (reap en modo pr), el closeout si hace falta para commitear en la rama de la tarea, deskops/integrate.py (rama, push de la rama y PR), tests/test_integrate.py, tests/test_dispatch.py, docs de configuración y CHANGELOG. Fuera: mover las rutas de máquina de los config.json de deskops y sldb a config.local.json (lo hace el coordinador después) y la configuración de los desks de heyantonia (la hace Governance).

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test de integración con un remoto bare cuyo hook pre-receive rechaza todo push a refs/heads/dev (rama protegida simulada) y un gh falso en PATH, un script que registra sus argumentos y devuelve una URL. En modo pr, start (simulado), reap, closeout e integrate terminan con la rama task/<id> en el remoto, gh pr create llamado con --base dev, y dev sin tocar en el remoto ni en la base local. p2: test de que en modo push el comportamiento no cambia (los tests existentes de test_integrate.py siguen pasando). p3: implementar reap e integrate en modo pr, y el closeout en la rama de la tarea. p4: docs: qué va en config.json (versionado) y qué en config.local.json (por máquina). p5: suite completa con -n 4. p6: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_integrate.py tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

El test de remoto con dev protegida y gh falso pasa en modo pr, los tests de modo push siguen pasando y la suite completa está verde.
