---
sldb:
  by: agent
  at: '2026-11-25T03:15:02Z'
  authority: generated
  via: save_document_payload
id: task-el-reap-del-intento-n-de-un-ejecutor-encola-el-tester-aunque-la-tarea-ya-este-en-ritual-testing
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references:
- deskops/dispatch.py
- tests/test_dispatch.py
- 3b9d6f5ed73c6556c34c2801a3f4c8da01f955b5
depends_on: []
pills: []
files:
- deskops/dispatch.py
- tests/test_dispatch.py
task_type: task.debug
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-reap-encola-el-tester-tras-integrar-un-ejecutor
---

# El reap del intento N de un ejecutor encola el tester aunque la tarea ya este en ritual-testing

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-082659-unclear-reintento-de-ejecutor-no-encola-tester-tras-el-reap: tras un FALLA el intento 2 commitea, hace advance y el reap integra, pero no se encola dispatch-tester porque la tarea ya estaba en ritual-testing; el coordinador lo encola a mano.

## Goal

_Describe the concrete result this task must produce._

Despues de integrar el commit de un ejecutor, dispatch reap encola dispatch-tester de la tarea si no hay un tester vivo ni pendiente, sea el intento que sea.

## Scope

_State what is in scope and what is out of scope._

deskops/dispatch.py (reap) y sus tests; nada de la maquina de estados de rituales.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo: /mnt/ssd/proyectos/SLDB_1/deskops (raiz). Contexto: el tester se encola hoy solo por el hook 'encola-tester' de la transicion execution -> testing (desk/lifecycle/execution-task_activates.md: corre 'deskops queue add dispatch-tester'). En un intento 2 la tarea ya esta en ritual-testing, no hay transicion y nadie encola el tester. Cambio, solo en deskops/dispatch.py, funcion reap(root, task_id): 1) Dentro del bucle, cuando role == 'executor' y _integrate_branch(root, name, task_id) devuelve code == 0, marcar integrated = True. Si _integrate_branch falla o el ejecutor no se reapea, no se hace nada nuevo. 2) Al final de reap, antes de los return, si integrated y no hubo tester vivo de la tarea en el mismo bucle (agente con labels deskops.role == 'tester' que quedo como 'vivo') y no hay en deskops.queue un trabajo pendiente o corriendo de kind 'dispatch-tester' con ese task_id (leer los JSON de queue_dir(root)/'pending' y /'running' con su campo task_id; reutilizar queue._jobs y queue._read_job), llamar queue.enqueue(root, 'dispatch-tester', task_id, 'reap') e imprimir 'encolado: dispatch-tester'. La deduplicacion es por task_id y kind, sin importar el intento. 3) Tests en tests/test_dispatch.py siguiendo los fakes de scion que ya usa ese archivo: (a) ejecutor reapeado e integrado sin tester pendiente -> queda un JSON dispatch-tester en runs/queue/pending con ese task_id; (b) con uno ya pendiente -> sigue habiendo uno solo; (c) si _integrate_branch falla -> no se encola. Correr solo tests/test_dispatch.py.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_dispatch.py tiene los casos (a) encola tras integrar, (b) no duplica con uno pendiente y (c) no encola si la integracion falla; el archivo completo pasa.
