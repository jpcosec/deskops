---
sldb:
  by: agent
  at: '2026-11-17T12:07:47Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista@sha256:e178b43368963dd5c93532e0b132192ce2ad846dad92697f05c33922d7a61167
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261117-120023/context-review/task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista/preflight/3895b510ebf6286f70366a831b1ddaf656ae935a8e818ab70eceaa20e3b57619/attempt-1
input_sha256: 3895b510ebf6286f70366a831b1ddaf656ae935a8e818ab70eceaa20e3b57619
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 5e285cd63fba2f4ba02f0cffd19e12c9b397dd610e9bb191c8c3de7603d531c2
output_sha256: 8ab883c5c51456202637909b905c6e7a3d165c53e6679c1b8415256c562527c8
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Precisiones del coordinador (preflight 1 y bundle 1): (1) Orden ascendente
  por created_at, desempate por id. (2) En texto, una linea por recibo: ''receipt
  <id> <kind> <verdict> <anchor_state> <created_at>''. (3) Pertenece a la tarea todo
  ReviewDoc cuyo subject es doc:<ModeloDeTarea>:<id de la tarea>, con o sin el pin
  @sha256:...; los recibos de nodo (subject vacio) no. (4) Las claves son exactamente
  id, kind, verdict, anchor_state y created_at, con los valores del ReviewDoc; anchor_state
  es el de cada recibo, calculado como lo calcula hoy deskops para ese recibo (el
  mismo que ve la regla de activacion). (5) receipts va dentro de task, al mismo nivel
  que gates, en json y en yaml (misma estructura). (6) Los goldens de view (tests/test_view_goldens.py
  y sus fixtures) se pueden regenerar si cambian por este campo, y se dice. (7) El
  fixture usa deskops review record <tarea> --kind reproduction --evidence <archivo>
  --reason x --root <sandbox>. (8) El aviso a graph_ui lo manda el coordinador al
  cerrar, no el ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-17T12:00:34.714224+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T12:07:34.398283+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261117-120023/context-review/task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista/preflight/3895b510ebf6286f70366a831b1ddaf656ae935a8e818ab70eceaa20e3b57619/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Precisiones del coordinador (preflight 1 y bundle 1): (1) Orden ascendente por created_at, desempate por id. (2) En texto, una linea por recibo: 'receipt <id> <kind> <verdict> <anchor_state> <created_at>'. (3) Pertenece a la tarea todo ReviewDoc cuyo subject es doc:<ModeloDeTarea>:<id de la tarea>, con o sin el pin @sha256:...; los recibos de nodo (subject vacio) no. (4) Las claves son exactamente id, kind, verdict, anchor_state y created_at, con los valores del ReviewDoc; anchor_state es el de cada recibo, calculado como lo calcula hoy deskops para ese recibo (el mismo que ve la regla de activacion). (5) receipts va dentro de task, al mismo nivel que gates, en json y en yaml (misma estructura). (6) Los goldens de view (tests/test_view_goldens.py y sus fixtures) se pueden regenerar si cambian por este campo, y se dice. (7) El fixture usa deskops review record <tarea> --kind reproduction --evidence <archivo> --reason x --root <sandbox>. (8) El aviso a graph_ui lo manda el coordinador al cerrar, no el ejecutor.
