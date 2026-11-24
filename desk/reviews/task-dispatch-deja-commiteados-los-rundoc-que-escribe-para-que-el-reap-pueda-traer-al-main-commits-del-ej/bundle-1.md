---
sldb:
  by: agent
  at: '2026-11-23T19:17:50Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej@sha256:5399fedcf1feae303755e0a402b8bcd2b137639ddf9acd6b75700746861b1a87
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-065421/context-review/task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej/bundle/0f0e006a2a2b03d10e1730f9b4df51dbea962c8de396400a2e760ef27912ce69/attempt-1
input_sha256: 0f0e006a2a2b03d10e1730f9b4df51dbea962c8de396400a2e760ef27912ce69
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ba2002f2699fef2cf46b05758a09ff08924c1f633b72c064750773ea1c45a462
output_sha256: b4eeaecc10bc5c838b078a073ee3e4bd83028ccfa677f649a8ac1b30b751a2a7
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) Un helper en deskops/dispatch.py (p. ej. _commit_run_docs(root,
  paths, agent, task_id)) llamado desde start despues de record_scion_run (~linea
  309) y desde _integrate_branch (linea 141) antes del rev-list; scion.py no cambia.
  2) Rama: _base_branch(root) (dispatch.py:90); _check_on_base ya rechaza si el checkout
  principal no esta en ella (detached HEAD incluido), y en ese caso no se commitea
  y se informa igual que hoy. Los worktrees de ejecutores no se tocan. 3) Pathspec:
  las rutas que git status --porcelain -z -- .sldb <run_dir> lista como modificadas
  o sin trackear justo despues de record_scion_run (store.yaml, core/store_index.yaml,
  core/models/RunDoc.yaml, el shard core/documents/RunDoc/run-<agente>.yaml y <run_dir>/run.md).
  4) <agente> es el nombre del agente de scion que start ya calcula (variable name,
  p. ej. deskops-e-8eb91b4956b3). 5) Mensaje: asunto ''run: <agente> [skip ci]'' y
  cuerpo ''Task-Id: <id de la tarea>''. 6) Pendientes en reap: los run.md bajo runs/subagents/exec-<agente>*
  de los agentes de la tarea mas los archivos modificados/sin trackear bajo .sldb/;
  solo esos; sin pendientes es no-op. 7) El mensaje lo arma _integrate_branch cuando
  el cherry-pick falla: agrega a ''conflicto al traer <rama> a <base>'' la lista de
  archivos que git reporta y ''commitealos con git commit -- <rutas> y re-encola el
  reap''. 8) El trailer ''Task-Id: <id de la tarea despachada>'' va en los commits
  run: y tambien en el commit de codigo del ejecutor, que lleva ''Task-Id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej''
  y se hace en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T06:54:38.543075+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T06:55:04.906458+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-065421/context-review/task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej/bundle/0f0e006a2a2b03d10e1730f9b4df51dbea962c8de396400a2e760ef27912ce69/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) Un helper en deskops/dispatch.py (p. ej. _commit_run_docs(root, paths, agent, task_id)) llamado desde start despues de record_scion_run (~linea 309) y desde _integrate_branch (linea 141) antes del rev-list; scion.py no cambia. 2) Rama: _base_branch(root) (dispatch.py:90); _check_on_base ya rechaza si el checkout principal no esta en ella (detached HEAD incluido), y en ese caso no se commitea y se informa igual que hoy. Los worktrees de ejecutores no se tocan. 3) Pathspec: las rutas que git status --porcelain -z -- .sldb <run_dir> lista como modificadas o sin trackear justo despues de record_scion_run (store.yaml, core/store_index.yaml, core/models/RunDoc.yaml, el shard core/documents/RunDoc/run-<agente>.yaml y <run_dir>/run.md). 4) <agente> es el nombre del agente de scion que start ya calcula (variable name, p. ej. deskops-e-8eb91b4956b3). 5) Mensaje: asunto 'run: <agente> [skip ci]' y cuerpo 'Task-Id: <id de la tarea>'. 6) Pendientes en reap: los run.md bajo runs/subagents/exec-<agente>* de los agentes de la tarea mas los archivos modificados/sin trackear bajo .sldb/; solo esos; sin pendientes es no-op. 7) El mensaje lo arma _integrate_branch cuando el cherry-pick falla: agrega a 'conflicto al traer <rama> a <base>' la lista de archivos que git reporta y 'commitealos con git commit -- <rutas> y re-encola el reap'. 8) El trailer 'Task-Id: <id de la tarea despachada>' va en los commits run: y tambien en el commit de codigo del ejecutor, que lleva 'Task-Id: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej' y se hace en el worktree que dispatch le da al ejecutor.
