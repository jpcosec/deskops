---
sldb:
  by: agent
  at: '2026-11-23T19:16:09Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph@sha256:345beca62f38bd237742a77fe2b93ae5cff342ec9cec78124797344ebe3d13ef
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-070333/context-review/task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph/preflight/ad310cae9d4fece5df366808b74ea4210fd7ca80317343904a66ee20a7f8de3a/attempt-1
input_sha256: ad310cae9d4fece5df366808b74ea4210fd7ca80317343904a66ee20a7f8de3a
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 4b8b46c096d7bf58d42fb92abb93348e5b43de830ea6febaea8fe066422adaf6
output_sha256: 2aad3ea55998c76bcd3ad75b8a086e837158ff319f291a5e10900b068075ebdd
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) Erratum de redaccion: se elimina el rodeo. Hoy
  closure.py:1168-1173 hace tx.create(''ReviewDoc'', ...) y despues tx.update(review_id,
  payload) sin cambios solo para pinnear subject; queda solo tx.create, que en el
  sldb instalado ya pinnea. 2) Se permite tocar tests en imports, monkeypatches y
  helpers; no se cambian las aserciones existentes; se agregan tests nuevos si hace
  falta. 3) g es el ProjectGraph que _Lookup ya arma (deskops/services/references.py:62,
  self.graph = desk_graph(self.root)); se pasa como graph=lookup.graph. 4) excluded_sources
  es el conjunto que hoy calcula _skipped(root, path, excluded) (references.py, el
  propio path mas los excluded del llamador), en rutas relativas al repo. 5) La comprobacion
  es: tras closeout verify en un desk temporal, el ReviewDoc de evidencia tiene subject
  con ''@sha256:'' y sldb le da anchor_state ''intact''. 6) La nota es ''deskops message
  send --root . --to sldb --kind suggestion --title "..." "<cuerpo>"'', la manda el
  ejecutor si una API no se comporta como dice su nota. 7) Worktree base: ''git worktree
  add /dev/shm/wt-base origin/main'', correr ahi el mismo comando de pytest del test
  fallido, y ''git worktree remove /dev/shm/wt-base'' al terminar; se acepta solo
  si falla igual (mismo test, mismo error). Commit con ''Task-Id: task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph''
  en el cuerpo, en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T07:03:46.480694+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:07:28.177191+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-070333/context-review/task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph/preflight/ad310cae9d4fece5df366808b74ea4210fd7ca80317343904a66ee20a7f8de3a/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) Erratum de redaccion: se elimina el rodeo. Hoy closure.py:1168-1173 hace tx.create('ReviewDoc', ...) y despues tx.update(review_id, payload) sin cambios solo para pinnear subject; queda solo tx.create, que en el sldb instalado ya pinnea. 2) Se permite tocar tests en imports, monkeypatches y helpers; no se cambian las aserciones existentes; se agregan tests nuevos si hace falta. 3) g es el ProjectGraph que _Lookup ya arma (deskops/services/references.py:62, self.graph = desk_graph(self.root)); se pasa como graph=lookup.graph. 4) excluded_sources es el conjunto que hoy calcula _skipped(root, path, excluded) (references.py, el propio path mas los excluded del llamador), en rutas relativas al repo. 5) La comprobacion es: tras closeout verify en un desk temporal, el ReviewDoc de evidencia tiene subject con '@sha256:' y sldb le da anchor_state 'intact'. 6) La nota es 'deskops message send --root . --to sldb --kind suggestion --title "..." "<cuerpo>"', la manda el ejecutor si una API no se comporta como dice su nota. 7) Worktree base: 'git worktree add /dev/shm/wt-base origin/main', correr ahi el mismo comando de pytest del test fallido, y 'git worktree remove /dev/shm/wt-base' al terminar; se acepta solo si falla igual (mismo test, mismo error). Commit con 'Task-Id: task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph' en el cuerpo, en el worktree que dispatch le da al ejecutor.
