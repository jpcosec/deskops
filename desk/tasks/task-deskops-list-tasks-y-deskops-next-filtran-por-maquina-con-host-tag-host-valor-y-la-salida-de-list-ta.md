---
sldb:
  by: agent
  at: '2026-11-24T18:27:30Z'
  authority: generated
  via: save_document_payload
id: task-deskops-list-tasks-y-deskops-next-filtran-por-maquina-con-host-tag-host-valor-y-la-salida-de-list-ta
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261122-214748-unclear-de-ftcourier-a-la-tarea-le-falta-un-campo-para-decir-en-qu-m-quina-y-con-qu-ejecutor-corre.md
depends_on: []
pills: []
files:
- deskops/services/tasks.py
- tests/test_cli.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops list tasks y deskops next filtran por máquina con --host (tag host:<valor>) y la salida de list tasks muestra el host

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261122-214748 (reenviada desde ftcourier, nota 20261119-233140): la tarea no tiene dónde decir en qué máquina corre; en ftcourier se marca con tags host:robocop2 / host:local y en el título, pero deskops next, el Board y deskops list tasks no lo usan ni lo filtran. La parte de declarar la máquina ya está resuelta: el namespace de tags host se declaró en 5d10b2eb (closeout 9a308322, task-deskops-declara-el-namespace-de-tags-host-para-marcar-en-que-maquina-corre-cada-tarea; FLAT_NAMESPACES en deskops/atom_tags.py). Falta usarlo. El ejecutor por desk ya lo fija dispatch.roles en desk/config.json; un ejecutor por tarea no entra aquí.

## Goal

_Describe the concrete result this task must produce._

(1) deskops list tasks --host <valor> lista solo las tareas con el tag host:<valor>; --host none lista las que no tienen tag host. La salida de texto agrega el host de cada tarea (o "-") y la json un campo host. (2) deskops next sin task_id acepta --host <valor> y elige solo entre tareas de ese host. Sin --host, ambas salidas listan lo mismo que hoy (solo se agrega la columna/campo host).

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/tasks.py (list_tasks), los comandos list y next de deskops/cli, goldens de ayuda y de salida, y tests/test_cli.py. No entra: el Board, un campo nuevo en TaskDoc, un ejecutor por tarea, deskops runtime workers.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests en tests/test_cli.py sobre un desk temporal con tres tareas (host:robocop2, host:local, sin host): test_list_tasks_filters_by_host, test_list_tasks_host_none, test_list_tasks_json_has_host, test_next_filters_by_host. p2: implementar. p3: goldens. p4: suite con -n 4. p5: commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q -p no:cacheprovider tests (suite completa una vez antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Los cuatro tests nuevos pasan y los goldens de salida quedan actualizados solo con la columna host.
