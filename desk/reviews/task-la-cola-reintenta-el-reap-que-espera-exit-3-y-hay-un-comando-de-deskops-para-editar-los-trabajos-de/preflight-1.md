---
sldb:
  by: agent
  at: '2026-11-24T18:09:39Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
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
run_dir: runs/subagents/20261122-212231/context-review/task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de/preflight/19c597f119cf02269ed83ea9f30873c4e032ee8989d84c5f13eced9403e6c5ec/attempt-1
input_sha256: 19c597f119cf02269ed83ea9f30873c4e032ee8989d84c5f13eced9403e6c5ec
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 7b773f9dbd1fe831ede10f0d940aa6347f86409c93089d3792764d50e35fa162
output_sha256: e826acd777d0349a433854ba29d2ba08c57c6b16169840dee8fc15fb686a90f9
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
created_at: '2026-11-22T21:22:43.588886+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T21:23:50.012577+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-212231/context-review/task-la-cola-reintenta-el-reap-que-espera-exit-3-y-hay-un-comando-de-deskops-para-editar-los-trabajos-de/preflight/19c597f119cf02269ed83ea9f30873c4e032ee8989d84c5f13eced9403e6c5ec/attempt-1.

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
