FILE:desk/tasks/task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de.md
---
sldb:
  by: agent
  at: '2026-11-19T18:43:39Z'
  authority: generated
  via: save_document_payload
id: task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de
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

# dispatch start lanza agentes en paralelo con el único límite físico de la máquina (gate de memoria), en vez de uno solo por proyecto scion

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-19: dispatch start (deskops/dispatch.py:144-147, desde 9daa47b2) responde 'ocupado' si cualquier agente del proyecto scion está running, así que los tres desks (deskops, sldb, IR) comparten un solo ejecutor o tester a la vez. scion no tiene ese límite; vino de una receta del coordinador. Con 20 GB disponibles y agentes de 6 GiB caben dos o tres. El límite serializa todo, y hoy causó fallos 'ocupado' y una cola trabada.

## Goal

_Describe the concrete result this task must produce._

dispatch start lanza un agente si la memoria pasa el gate de la cola (wait_reason de deskops/queue.py: disponible >= queue_min_available_gb y PSI avg60 < queue_max_psi_avg60) y si la misma tarea no tiene ya un agente running (por el prefijo de identidad de scion_child_identity de esa tarea). No hay tope configurable de agentes: el límite es físico. Si no se cumple, sale con EXIT_BUSY (3) e imprime el motivo ('ocupado: memoria ...' o 'ocupado: la tarea ya tiene agente <nombre>'). Con retry_exit_codes [3] la cola lo reintenta.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/dispatch.py (start), tests/test_dispatch.py, docs/operator-manual.md (sección de dispatch) y CHANGELOG. Fuera: un campo de configuración de máximo de agentes (no se agrega), queue.py salvo importar wait_reason, scion y los config.json de los desks.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: tests que fallen antes, con _list_agents y el estado de memoria simulados: con un agente running de otra tarea y memoria suficiente, start lanza; con un agente running de la misma tarea, sale 3 con 'ocupado: la tarea ya tiene agente'; con memoria bajo el gate, sale 3 con el motivo de memoria. p2: reemplazar el bucle de dispatch.py:144-147 ('cualquier agente running => ocupado') por esos dos chequeos, reusando wait_reason. p3: docs y CHANGELOG. p4: commit con rutas nombradas y Task-Id.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

## Done When

_Name the observable condition that makes the task complete._

Los tests nuevos y los de dispatch pasan; la suite completa la corre integrate.

FILE:instruccion
Cold-bundle de la tarea task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de: con el TaskDoc, los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra, reformula el encargo, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

Sección de validación del TaskDoc:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py

