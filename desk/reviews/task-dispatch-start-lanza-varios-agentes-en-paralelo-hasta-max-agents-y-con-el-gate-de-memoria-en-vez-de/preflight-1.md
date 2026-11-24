---
sldb:
  by: agent
  at: '2026-11-24T17:58:39Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de@sha256:122d77a303986507f9e055439eae619e64eb8527868a895b5ae4133f3bcaa24c
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261119-214249/context-review/task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de/preflight/e6e50ca62bcf4f7bdf8bc61cf6626c71e1a811ff06313a7a9ddc15357db25361/attempt-1
input_sha256: e6e50ca62bcf4f7bdf8bc61cf6626c71e1a811ff06313a7a9ddc15357db25361
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 5ea5681f9d00ba6dbdf212f050e68d267fff1500ae37eb7b74915b0b092c40cd
output_sha256: 644ee76b6c40d27e2345ff1ee28704dfc36f85a3c702bf04c8e84ac256f0a16a
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador: 1) Mensajes exactos, por stdout y
  con exit 3: ''ocupado: memoria: <motivo>'', donde <motivo> es el string que devuelve
  wait_reason, y ''ocupado: la tarea ya tiene agente <name>'', con el name de scion.
  2) Un agente pertenece a la tarea si su label ''deskops.task_id'' (que pone scion_child_identity
  con _scion_task_label en deskops/runtime/scion.py) es igual a _scion_task_label(task_id)
  y su phase es running. Si scion list no trae labels, se usa el nombre: el de cualquier
  intento de cualquier rol de esa tarea, calculado con scion_child_identity sobre
  el TaskDoc para executor, tester y specialist y attempt 1 y 2. 3) wait_reason(config:
  DeskConfig) -> str | None está en deskops/queue.py:119: None si la memoria alcanza
  y, si no, el motivo; se importa y se le pasa la config del desk. 4) En los tests
  se mockea _list_agents (deskops/dispatch.py:64, devuelve list[dict] con name, phase
  y labels) y deskops.queue._memory_state (devuelve (available_gb, avg60)). 5) El
  título viejo menciona max-agents, pero el Goal manda: no hay tope configurable,
  ni existente ni nuevo. El commit lleva el trailer ''Task-Id: <id de la tarea>'',
  es decir el id de este TaskDoc, con git add de rutas nombradas.'
# ISO 8601 timestamp
created_at: '2026-11-19T21:42:59.042051+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-19T21:44:34.787240+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261119-214249/context-review/task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de/preflight/e6e50ca62bcf4f7bdf8bc61cf6626c71e1a811ff06313a7a9ddc15357db25361/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador: 1) Mensajes exactos, por stdout y con exit 3: 'ocupado: memoria: <motivo>', donde <motivo> es el string que devuelve wait_reason, y 'ocupado: la tarea ya tiene agente <name>', con el name de scion. 2) Un agente pertenece a la tarea si su label 'deskops.task_id' (que pone scion_child_identity con _scion_task_label en deskops/runtime/scion.py) es igual a _scion_task_label(task_id) y su phase es running. Si scion list no trae labels, se usa el nombre: el de cualquier intento de cualquier rol de esa tarea, calculado con scion_child_identity sobre el TaskDoc para executor, tester y specialist y attempt 1 y 2. 3) wait_reason(config: DeskConfig) -> str | None está en deskops/queue.py:119: None si la memoria alcanza y, si no, el motivo; se importa y se le pasa la config del desk. 4) En los tests se mockea _list_agents (deskops/dispatch.py:64, devuelve list[dict] con name, phase y labels) y deskops.queue._memory_state (devuelve (available_gb, avg60)). 5) El título viejo menciona max-agents, pero el Goal manda: no hay tope configurable, ni existente ni nuevo. El commit lleva el trailer 'Task-Id: <id de la tarea>', es decir el id de este TaskDoc, con git add de rutas nombradas.
