---
sldb:
  by: agent
  at: '2026-11-17T23:06:29Z'
  authority: generated
  via: create_document
id: task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
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
- deskops/lifecycle_hooks.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-automatic-routines-vs-llm-tasks
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Un runner del host toma de una cola los trabajos pesados que encolan los post-hooks

## Rationale

_Explain why this task exists or the business driver behind it._

Los post-hooks de una transicion corren donde corre `deskops advance task`. Cuando lo corre un ejecutor dentro de un contenedor scion, ahi no estan el cerrojo de tests de la maquina, el control de memoria ni las credenciales de push. La suite completa, la integracion y el push tienen que correr en el host, de a uno.

## Goal

_Describe the concrete result this task must produce._

Existe `deskops queue add` (lo llama un post-hook; escribe un trabajo como archivo en una cola del desk con el id de la tarea, la transicion y el tipo de trabajo) y `deskops queue run` (lo corre el host; toma el trabajo mas antiguo, verifica memoria disponible y que no haya otro trabajo corriendo, ejecuta el comando declarado para ese tipo de trabajo en la configuracion del desk, guarda el log y el resultado, y deja el trabajo como hecho o fallido). `deskops queue list` muestra pendientes, en curso y terminados. Un trabajo fallido deja una nota en el inbox del desk con la ruta del log.

## Scope

_State what is in scope and what is out of scope._

Dentro: la cola como archivos bajo runs del desk, los tres subcomandos, la configuracion de tipos de trabajo del desk, pruebas con comandos reales en un desk desechable, manual del operador. Fuera: un servicio permanente (el host llama `queue run` con un timer o a mano); cambios en scion; declarar hooks en desks reales.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q
- deskops graph missing --root .

## Done When

_Name the observable condition that makes the task complete._

En un desk desechable, un post-hook encola un trabajo, `queue run` lo ejecuta y deja log y resultado; dos `queue run` simultaneos no corren dos trabajos a la vez; un trabajo que falla deja la nota en el inbox.
