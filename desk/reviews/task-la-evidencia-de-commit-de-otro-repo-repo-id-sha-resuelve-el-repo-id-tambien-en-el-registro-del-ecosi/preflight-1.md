---
sldb:
  by: agent
  at: '2026-11-24T18:10:00Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi@sha256:baa183b529250eac2ee4507ee2ea2198f61d2938e77775238d25055d4d86da17
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261116-170649/context-review/task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi/preflight/be4ebaa6d61a0dc9b85e929ec791afb9f1d0685fdc445f5fe33e2b58eabc2a42/attempt-1
input_sha256: be4ebaa6d61a0dc9b85e929ec791afb9f1d0685fdc445f5fe33e2b58eabc2a42
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: b80ee3d145db6bbd40f220b9ebf9daa837797ce8e915d4645404855a8ffe8234
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Precisiones del coordinador (preflight 1):

  (1) Aislamiento del registro en tests: la variable de entorno DESKOPS_ECOSYSTEM_REGISTRY
  (ECOSYSTEM_REGISTRY_ENV de deskops/identity.py, leída por ecosystem_registry_dir)
  apuntando a un directorio registry dentro de tmp_path; en tests en proceso con monkeypatch.setenv,
  en subprocesos con env (patrón de tests/test_message_ecosystem_registry.py). Nunca
  ~/setup/desk/registry.

  (2) "El registro del desk" es desk/registry/repo-*.md del desk bajo --root (las
  entries que ya recibe RepositoryReferences). Si el repo-id no está ahí, se busca
  en el registro del ecosistema (load_ecosystem_registry / find_registered_desk).
  El registro local gana si están en ambos.

  (3) "Alcanzable" es exactamente el criterio de reference_points_to_commit: id hex
  en minúsculas, git rev-parse --verify <sha>^{commit} en el repo de ese repo-id,
  y ancestro de su HEAD. Reutiliza esa función (CloseoutGatesService sobre la raíz
  de ese repo), no la dupliques.

  (4) Doc: subsección nueva "Commit evidence from another repository" dentro de "Closeout
  rules" de docs/workflow-policy-reference.md, justo después de "Tests evidence from
  a suite in another language". Contenido: la forma <repo-id>:<sha>, el orden de resolución
  (registro local y luego ecosistema), el criterio de (3) y que una referencia que
  no resuelve no cuenta y no lanza excepción.

  (5) La nota a scion la manda el coordinador después del closeout, con deskops message
  send --to scion, porque el hash solo existe entonces. El ejecutor no la manda; deja
  en result-summary.md un texto de 3 a 5 líneas para esa nota (qué cambió y cómo referenciar
  <repo-id>:<sha>).'
# ISO 8601 timestamp
created_at: '2026-11-16T17:07:00.085538+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-16T17:08:10.053470+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261116-170649/context-review/task-la-evidencia-de-commit-de-otro-repo-repo-id-sha-resuelve-el-repo-id-tambien-en-el-registro-del-ecosi/preflight/be4ebaa6d61a0dc9b85e929ec791afb9f1d0685fdc445f5fe33e2b58eabc2a42/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Precisiones del coordinador (preflight 1):
(1) Aislamiento del registro en tests: la variable de entorno DESKOPS_ECOSYSTEM_REGISTRY (ECOSYSTEM_REGISTRY_ENV de deskops/identity.py, leída por ecosystem_registry_dir) apuntando a un directorio registry dentro de tmp_path; en tests en proceso con monkeypatch.setenv, en subprocesos con env (patrón de tests/test_message_ecosystem_registry.py). Nunca ~/setup/desk/registry.
(2) "El registro del desk" es desk/registry/repo-*.md del desk bajo --root (las entries que ya recibe RepositoryReferences). Si el repo-id no está ahí, se busca en el registro del ecosistema (load_ecosystem_registry / find_registered_desk). El registro local gana si están en ambos.
(3) "Alcanzable" es exactamente el criterio de reference_points_to_commit: id hex en minúsculas, git rev-parse --verify <sha>^{commit} en el repo de ese repo-id, y ancestro de su HEAD. Reutiliza esa función (CloseoutGatesService sobre la raíz de ese repo), no la dupliques.
(4) Doc: subsección nueva "Commit evidence from another repository" dentro de "Closeout rules" de docs/workflow-policy-reference.md, justo después de "Tests evidence from a suite in another language". Contenido: la forma <repo-id>:<sha>, el orden de resolución (registro local y luego ecosistema), el criterio de (3) y que una referencia que no resuelve no cuenta y no lanza excepción.
(5) La nota a scion la manda el coordinador después del closeout, con deskops message send --to scion, porque el hash solo existe entonces. El ejecutor no la manda; deja en result-summary.md un texto de 3 a 5 líneas para esa nota (qué cambió y cómo referenciar <repo-id>:<sha>).
