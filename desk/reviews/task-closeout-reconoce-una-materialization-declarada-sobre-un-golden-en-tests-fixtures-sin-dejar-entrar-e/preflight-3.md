---
sldb:
  by: agent
  at: '2026-11-23T19:04:20Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e-preflight-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e@sha256:76825e15bbbaf4f511d974dd056d2df55895b2d8e158187f6311cb13d894238e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-074357/context-review/task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e/preflight/2f96aca615e7c2353c60e1f05efde1550585ca1456c955c6c9764b2a7db066cf/attempt-1
input_sha256: 2f96aca615e7c2353c60e1f05efde1550585ca1456c955c6c9764b2a7db066cf
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 515bb537a151056dca71a261cd7a79b7b8940ffe925acbb17556284f3e627e15
output_sha256: 10e3e67d8c3d62234d9d5e7a57edd4d8c76505f096682edb72a55e9ecfd3239c
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) ''Respaldado por un atomo'' = la MaterializationContractDoc
  en desk/materializations/ declara source_atoms con el id del atomo y target_identity
  con la ruta del golden; para el corte solo importa target_identity, y el test de
  regresion puede escribir la materialization sin atomo como el helper _materialization
  de tests/test_desk_graph_runs_target.py:15. 2) MATERIALIZATION_TARGETS (deskops/graph/desk_graph.py:96-99)
  declara de donde salen los targets y no se espera cambiarlo; el sospechoso es EXCLUSIONS.path_prefixes
  (desk_graph.py:89-94, que incluye ''tests/fixtures''): el arreglo en deskops, si
  el corte es de deskops, es que esa exclusion no aplique a un target declarado. 3)
  Sandbox: para el nodo, tmp_path como en tests/test_desk_graph_runs_target.py:29
  (escribir tests/fixtures/golden.txt y la materialization, y llamar desk_graph(tmp_path));
  para closeout verify, el fixture lifecycle_desk de tests/conftest.py:113 (desk con
  git como lo deja deskops init). 4) Invocaciones: deskops graph missing --root RUTA_SANDBOX
  y deskops closeout verify --task ID_TAREA --root RUTA_SANDBOX. 5) Orden: primero
  se manda la nota a sldb (deskops message send --root . --to sldb --kind suggestion
  ...), que imprime la ruta de la nota creada; ese nombre de archivo va en xfail(reason=...).
  Commit con ''Task-Id: task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e''
  en el cuerpo, en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T07:44:07.445350+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:46:38.050333+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-074357/context-review/task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e/preflight/2f96aca615e7c2353c60e1f05efde1550585ca1456c955c6c9764b2a7db066cf/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) 'Respaldado por un atomo' = la MaterializationContractDoc en desk/materializations/ declara source_atoms con el id del atomo y target_identity con la ruta del golden; para el corte solo importa target_identity, y el test de regresion puede escribir la materialization sin atomo como el helper _materialization de tests/test_desk_graph_runs_target.py:15. 2) MATERIALIZATION_TARGETS (deskops/graph/desk_graph.py:96-99) declara de donde salen los targets y no se espera cambiarlo; el sospechoso es EXCLUSIONS.path_prefixes (desk_graph.py:89-94, que incluye 'tests/fixtures'): el arreglo en deskops, si el corte es de deskops, es que esa exclusion no aplique a un target declarado. 3) Sandbox: para el nodo, tmp_path como en tests/test_desk_graph_runs_target.py:29 (escribir tests/fixtures/golden.txt y la materialization, y llamar desk_graph(tmp_path)); para closeout verify, el fixture lifecycle_desk de tests/conftest.py:113 (desk con git como lo deja deskops init). 4) Invocaciones: deskops graph missing --root RUTA_SANDBOX y deskops closeout verify --task ID_TAREA --root RUTA_SANDBOX. 5) Orden: primero se manda la nota a sldb (deskops message send --root . --to sldb --kind suggestion ...), que imprime la ruta de la nota creada; ese nombre de archivo va en xfail(reason=...). Commit con 'Task-Id: task-closeout-reconoce-una-materialization-declarada-sobre-un-golden-en-tests-fixtures-sin-dejar-entrar-e' en el cuerpo, en el worktree que dispatch le da al ejecutor.
