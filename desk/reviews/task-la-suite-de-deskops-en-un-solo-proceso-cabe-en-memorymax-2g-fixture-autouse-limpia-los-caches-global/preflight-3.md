---
sldb:
  by: agent
  at: '2026-11-23T19:32:39Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global-preflight-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global@sha256:d86035fa769a548c8bf1f194f2fb259fe8fd8551e7579432958adffb68d67189
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-072814/context-review/task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global/preflight/bdade0da799313f41ee99b23298b75fcedb998d7bcfcb1c5e481dbfe6bdd8e42/attempt-1
input_sha256: bdade0da799313f41ee99b23298b75fcedb998d7bcfcb1c5e481dbfe6bdd8e42
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: d3b5794448b2bcd472f37af695b13eda737ebbb1a037be6eef562f3caad75078
output_sha256: 1d1a7b5ddd5892887a0092636e6b1f116822a6d0c22ac1d9abb952f13ee68e7f
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones: 1) La limpieza va solo en el teardown: la fixture
  hace yield y limpia despues de cada test. 2) Los dicts son _READ_HASHES (deskops/doc_access.py:155)
  e _INDEX_ENTRIES (doc_access.py:158). 3) Verificado hoy con import en el sldb instalado
  (/mnt/ssd/herramientas/sldb, el que usa el venv): sldb.store.runtime_cache.invalidate_runtime_cache,
  sldb.store.io.invalidate_index_cache, sldb.store.built_cache.clear y sldb.cli.alert_sink.forget
  existen y son funciones de modulo invocables; se importan y se llaman sin argumentos.
  4) Baseline: en un worktree limpio (git worktree add /dev/shm/wt-base origin/main)
  se corre TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests desde ahi y
  se anotan las fallas; la corrida de un proceso bajo MemoryMax=2G debe terminar sin
  OOM y con ese mismo conjunto de fallas; se borra el worktree con git worktree remove
  /dev/shm/wt-base. 5) No cabe = el proceso muere por OOM o systemd-run lo mata; resuelto
  = la corrida de un proceso termina con codigo de pytest (pase o falle) sin OOM.
  Si tras limpiar los caches de los 3 archivos de mayor RSS sigue sin caber, la tarea
  se detiene y reporta las mediciones. Commit con ''Task-Id: task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global''
  en el cuerpo, en el worktree que dispatch le da al ejecutor.'
# ISO 8601 timestamp
created_at: '2026-11-21T07:28:26.647617+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T07:31:03.616069+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-072814/context-review/task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global/preflight/bdade0da799313f41ee99b23298b75fcedb998d7bcfcb1c5e481dbfe6bdd8e42/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones: 1) La limpieza va solo en el teardown: la fixture hace yield y limpia despues de cada test. 2) Los dicts son _READ_HASHES (deskops/doc_access.py:155) e _INDEX_ENTRIES (doc_access.py:158). 3) Verificado hoy con import en el sldb instalado (/mnt/ssd/herramientas/sldb, el que usa el venv): sldb.store.runtime_cache.invalidate_runtime_cache, sldb.store.io.invalidate_index_cache, sldb.store.built_cache.clear y sldb.cli.alert_sink.forget existen y son funciones de modulo invocables; se importan y se llaman sin argumentos. 4) Baseline: en un worktree limpio (git worktree add /dev/shm/wt-base origin/main) se corre TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests desde ahi y se anotan las fallas; la corrida de un proceso bajo MemoryMax=2G debe terminar sin OOM y con ese mismo conjunto de fallas; se borra el worktree con git worktree remove /dev/shm/wt-base. 5) No cabe = el proceso muere por OOM o systemd-run lo mata; resuelto = la corrida de un proceso termina con codigo de pytest (pase o falle) sin OOM. Si tras limpiar los caches de los 3 archivos de mayor RSS sigue sin caber, la tarea se detiene y reporta las mediciones. Commit con 'Task-Id: task-la-suite-de-deskops-en-un-solo-proceso-cabe-en-memorymax-2g-fixture-autouse-limpia-los-caches-global' en el cuerpo, en el worktree que dispatch le da al ejecutor.
