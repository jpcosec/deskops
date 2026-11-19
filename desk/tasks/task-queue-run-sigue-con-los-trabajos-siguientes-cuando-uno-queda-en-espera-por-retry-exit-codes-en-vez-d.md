---
sldb:
  by: agent
  at: '2026-11-19T18:13:14Z'
  authority: generated
  via: create_document
id: task-queue-run-sigue-con-los-trabajos-siguientes-cuando-uno-queda-en-espera-por-retry-exit-codes-en-vez-d
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

# queue run sigue con los trabajos siguientes cuando uno queda en espera por retry_exit_codes, en vez de detener la cola

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-19: con tres dispatch-executor encolados juntos en el desk de deskops, la cola se trabó. El primer ejecutor terminó, pero su contenedor sigue ocupando el cupo de scion hasta el dispatch-reap, que el hook encola al final. El segundo dispatch-executor salía con 3 (ocupado), volvía a pending y queue run retornaba sin correr nada más (decisión de la tarea a7f4d4fd). El reap, detrás, nunca corría: 5 reintentos en 17 minutos y la cola parada. El coordinador sacó a mano los ejecutores en espera.

## Goal

_Describe the concrete result this task must produce._

Cuando un trabajo vuelve a pending por retry_exit_codes, queue run lo saltea en esa corrida y sigue con los siguientes pendientes en orden (con --all), así un dispatch-reap o un integrate que está detrás corre aunque haya un ejecutor esperando cupo. Un trabajo que ya quedó en espera en esa corrida no se reintenta hasta la próxima, sin bucle. Sin --all se corre un solo trabajo como hoy. Un fallo sigue deteniendo la cola.

## Scope

_State what is in scope and what is out of scope._

Dentro: run_queue en deskops/queue.py y tests/test_queue.py; docs/operator-manual.md (Host queue) y CHANGELOG. Fuera: el formato del JSON y retry_exit_codes, que no cambian.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: test que falla antes: tres trabajos pendientes, A sale con 3 y tiene retry_exit_codes [3], B y C salen con 0; queue run --all deja A en pending con attempts 1, B y C en done, retorna 0 e imprime 'en espera: <A> ocupado (exit 3)'. Segundo test: si todos los pendientes quedan en espera, la corrida termina sin bucle. p2: implementar en run_queue con un conjunto de ids salteados en la corrida. p3: docs y CHANGELOG. p4: commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos y tests/test_queue.py pasan; la suite completa la corre integrate.
