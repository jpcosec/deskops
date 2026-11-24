---
sldb:
  by: agent
  at: '2026-11-24T18:09:21Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de@sha256:aef920a49d7c958864975157461f33b91820f8916ffd21e47bd72b6debd4e764
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261122-212254/context-review/task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de/bundle/66e932e0f10180bb736a93f420152dfcec92fced485cdbd28c0dee231a87e728/attempt-1
input_sha256: 66e932e0f10180bb736a93f420152dfcec92fced485cdbd28c0dee231a87e728
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 3552540fe68f529b4d0f18f8386f8f99ec5d393680b6ca42dc2f2a8df8f6cd5a
output_sha256: 8f54b750ef4b59e122e95d6c16f11e54c66d3a096ed14ceeee03414b493a3ebf
# pending | accepted | rejected | incomplete
verdict: accepted
reason: "Aceptado. Resoluciones del coordinador.\n\nP1, B2 y B5) El comando es exactamente\
  \ este:\n\n    deskops queue job set <trabajo> <campo> <valor> [--json] --root .\n\
  \nVa registrado en deskops/cli/registry.py junto a queue add/run/list (path=(\"\
  queue\", \"job\", \"set\")), con handler en deskops/queue.py.\n- <campo> es un campo\
  \ de QueueJobSpec (deskops/config.py: run, timeout, retry_exit_codes).\n- Con --json,\
  \ <valor> se parsea con json.loads: por ejemplo retry_exit_codes '[3]' da la lista\
  \ [3], y timeout 600 da un entero.\n- Sin --json, <valor> se toma como string.\n\
  - El resultado se valida con el modelo QueueJobSpec antes de escribir; si no valida,\
  \ sale 2 sin tocar el archivo.\n\nP2, B1 y B4) No hay un config por defecto que\
  \ init genere con trabajos de cola: los trabajos dispatch-* se escribieron en cada\
  \ desk/config.json. El punto 'config por defecto de init' se descarta, así como\
  \ su test. Lo que queda es el comando, su test y aplicarlo en este desk.\n\nP3 y\
  \ B6) Preservación: se lee con json.load, se cambia solo queue.jobs.<trabajo>.<campo>\
  \ y se escribe con json.dump(indent=2, ensure_ascii=False) más un salto final, que\
  \ es el formato actual del archivo. Si el archivo tiene otro formato, se acepta\
  \ que se normalice: el test compara el JSON parseado, no el texto.\n\nP4) El worktree\
  \ es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>'\
  \ en el cuerpo.\n\nB3) La regla de solo CLI es del coordinador y no hace falta para\
  \ la tarea: desk/config.json se cambia con el comando nuevo, no a mano.\n\nB4) El\
  \ test va en tests/test_queue.py, que es el archivo existente de la cola. La Validation\
  \ corre ese archivo; tests/test_queue_cli.py no existe.\n\nB7) Las rutas del commit\
  \ son deskops/queue.py, deskops/cli/registry.py, tests/test_queue.py, CHANGELOG.md\
  \ y desk/config.json (este último escrito con el comando)."
# ISO 8601 timestamp
created_at: '2026-11-22T21:23:07.016026+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T21:24:01.254648+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-212254/context-review/task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de/bundle/66e932e0f10180bb736a93f420152dfcec92fced485cdbd28c0dee231a87e728/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1, B2 y B5) El comando es exactamente este:

    deskops queue job set <trabajo> <campo> <valor> [--json] --root .

Va registrado en deskops/cli/registry.py junto a queue add/run/list (path=("queue", "job", "set")), con handler en deskops/queue.py.
- <campo> es un campo de QueueJobSpec (deskops/config.py: run, timeout, retry_exit_codes).
- Con --json, <valor> se parsea con json.loads: por ejemplo retry_exit_codes '[3]' da la lista [3], y timeout 600 da un entero.
- Sin --json, <valor> se toma como string.
- El resultado se valida con el modelo QueueJobSpec antes de escribir; si no valida, sale 2 sin tocar el archivo.

P2, B1 y B4) No hay un config por defecto que init genere con trabajos de cola: los trabajos dispatch-* se escribieron en cada desk/config.json. El punto 'config por defecto de init' se descarta, así como su test. Lo que queda es el comando, su test y aplicarlo en este desk.

P3 y B6) Preservación: se lee con json.load, se cambia solo queue.jobs.<trabajo>.<campo> y se escribe con json.dump(indent=2, ensure_ascii=False) más un salto final, que es el formato actual del archivo. Si el archivo tiene otro formato, se acepta que se normalice: el test compara el JSON parseado, no el texto.

P4) El worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

B3) La regla de solo CLI es del coordinador y no hace falta para la tarea: desk/config.json se cambia con el comando nuevo, no a mano.

B4) El test va en tests/test_queue.py, que es el archivo existente de la cola. La Validation corre ese archivo; tests/test_queue_cli.py no existe.

B7) Las rutas del commit son deskops/queue.py, deskops/cli/registry.py, tests/test_queue.py, CHANGELOG.md y desk/config.json (este último escrito con el comando).
