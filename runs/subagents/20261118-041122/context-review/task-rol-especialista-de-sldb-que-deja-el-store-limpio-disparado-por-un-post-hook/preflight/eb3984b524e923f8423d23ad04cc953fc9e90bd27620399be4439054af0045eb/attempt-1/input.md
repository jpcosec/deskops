FILE:desk/tasks/task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook.md
---
sldb:
  by: agent
  at: '2026-11-17T23:06:43Z'
  authority: generated
  via: create_document
id: task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook
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
files:
- deskops/runtime/scion.py
- tests/test_scion_runtime.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-automatic-routines-vs-llm-tasks
---

# Rol especialista de sldb que deja el store limpio, disparado por un post-hook

## Rationale

_Explain why this task exists or the business driver behind it._

JP pidio un agente especialista de sldb que deje siempre limpio el store del desk despues de cada tarea (documentos sin registrar, anclas perdidas, mutaciones fuera del CLI). Hoy eso lo revisa a mano el coordinador o el integrador, y el ejecutor de la tarea de post-hooks edito un atom a mano sin que nada lo frenara.

## Goal

_Describe the concrete result this task must produce._

El desk de deskops trae un RoleDoc de especialista de sldb (creado con `deskops add role`) cuyo encargo es: correr `sldb stores check` y `deskops doctor` sobre el desk, corregir con el CLI lo que sea mecanico (registrar o actualizar documentos editados fuera del CLI, quitar del indice documentos que ya no existen) y dejar por escrito en una nota del inbox lo que requiere una decision. `deskops runtime template` lo materializa como template scion en un modo propio, con su agents.md. El manual del operador muestra el post-hook que lo despacha en la transicion a closeout.

## Scope

_State what is in scope and what is out of scope._

Dentro: el RoleDoc, el modo nuevo de `runtime template` y su agents.md, una prueba que materializa el template, el manual. Fuera: cambios en sldb; que el especialista toque codigo o cierre tareas; declarar el hook en desks reales.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py
- deskops graph missing --root .

## Done When

_Name the observable condition that makes the task complete._

`deskops runtime template` del rol especialista produce scion-agent.yaml, system-prompt.md y agents.md con el encargo descrito; el test del template pasa; el manual documenta el hook.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

