FILE:desk/tasks/task-deskops-dispatch-toma-los-roles-del-desk-de-deskops-para-tareas-de-otros-desks-sldb-ir-y-deskops-int.md
---
sldb:
  by: agent
  at: '2026-11-18T13:45:12Z'
  authority: generated
  via: save_document_payload
id: task-deskops-dispatch-toma-los-roles-del-desk-de-deskops-para-tareas-de-otros-desks-sldb-ir-y-deskops-int
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

# deskops dispatch toma los roles del desk de deskops para tareas de otros desks (sldb, IR), y deskops integrate trata un tip ya pusheado como éxito

## Rationale

_Explain why this task exists or the business driver behind it._

JP decidió el 2026-11-18 encender el despacho automático en deskops, sldb e IR. deskops dispatch start busca el RoleDoc en el desk de la tarea (find_role_doc(root, role), deskops/dispatch.py:92); sldb e IR no tienen deskops-executor ni deskops-tester en desk/roles y fallan con 'no RoleDoc with id or name'. El despacho manual que funciona usa runtime template --root <deskops> --task-root <desk de la tarea> --task-repo <repo>. Además, deskops integrate falla en fast-forward cuando el tip ya está en origin/main (31460a48, 2026-11-18), así que repetir un integrate ya hecho deja un fallo en vez de un no-op.

## Goal

_Describe the concrete result this task must produce._

deskops dispatch start y reap funcionan con --root sldb o IR tomando los roles (y el template) del desk de deskops, y deskops integrate devuelve 0 sin pushear cuando el tip ya es ancestro de origin/<branch>.

## Scope

_State what is in scope and what is out of scope._

En alcance: (a) un campo opcional roles_root en el bloque dispatch del desk/config.json del desk de la TAREA, el que se pasa con --root (p. ej. sldb/desk/config.json): ruta del repo cuyo desk/roles tiene los RoleDoc. Se aplica expanduser(); si es relativa se resuelve contra la raíz de la tarea; se guarda absoluta. Por defecto es la raíz de la tarea, y así deskops se comporta como hoy. (b) dispatch.start usa roles_root para find_role_doc y como root de la misma llamada a runtime template que hace hoy (deskops/dispatch.py, el bloque que escribe el template en templates_dir/<nombre del rol>); task_root es la raíz de la tarea y task_repo es el campo project_identity del desk/config.json de la tarea, o el nombre del directorio de la raíz si falta. El run_dir y el RunDoc quedan bajo la raíz de la tarea, como hoy. (c) dispatch.reap no cambia: no usa roles y sigue listando con _list_agents (scion list --project <project> --format json, deskops/dispatch.py:45) y filtrando por la etiqueta deskops.task_id. Solo se agrega un test que muestra que funciona con --root de un desk sin roles. (d) integrate: la rama es el campo branch del bloque integrate del desk/config.json de --root. Después del fetch que integrate ya hace en el paso copia (deskops/integrate.py:261), si el tip ya es ancestro de origin/<branch>: rc 0, imprime 'ya integrado: <tip corto>', no pushea ni corre la suite y agrega la línea a <raíz>/runs/hooks/events.log con la misma función que escribe hoy las líneas ok/fallo (deskops/integrate.py:213), con resultado 'ya-integrado'. Fuera de alcance: copiar RoleDocs a otros desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: dispatch start con un desk de tarea sin roles y roles_root apuntando a un desk con roles arma el template y el argv de scion (con scion simulado, como los tests actuales de dispatch). p2: implementar roles_root en DispatchConfig y en dispatch.start (reap no cambia; solo su test con --root de otro desk). p3: test e implementación del caso 'ya integrado' en integrate. p4: docs/operator-manual.md (secciones de dispatch e integrate) y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py tests/test_integrate.py
- suite completa de deskops (la corre el integrador)

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos pasan, la suite completa de deskops pasa y con roles_root=/mnt/ssd/proyectos/SLDB_1/deskops en el config de sldb, 'deskops dispatch start executor --task <una tarea de sldb> --root sldb' llega al scion start (verificable con scion simulado).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-dispatch-toma-los-roles-del-desk-de-deskops-para-tareas-de-otros-desks-sldb-ir-y-deskops-int: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

