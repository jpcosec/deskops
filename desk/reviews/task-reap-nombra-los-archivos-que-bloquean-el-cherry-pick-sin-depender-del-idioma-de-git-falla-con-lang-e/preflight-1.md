---
sldb:
  by: agent
  at: '2026-11-24T18:18:51Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e@sha256:277e80f3691eaecd0e734dacaa8f47367cd47ce080e91ef5ac0386e2d594617a
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-114814/context-review/task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e/preflight/5e78198c002fec4090e949d6dcde82e7874d4fee423b3487d7aafaa77d306649/attempt-1
input_sha256: 5e78198c002fec4090e949d6dcde82e7874d4fee423b3487d7aafaa77d306649
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 11c0e9d05cbab9943f276223e4208ab53415fe50f63a1465d6a197d0d2609f8d
output_sha256: 55a406285c46d7829bb7a25d6357f459421e8709a1f3f8076a9ce516544ea072
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador.


  P1, P4 y B1) La estrategia es LC_ALL=C. _git (deskops/dispatch.py:79) pasa env={**os.environ,
  ''LC_ALL'': ''C'', ''LANGUAGE'': ''''} a subprocess.run. _dirty_overwrite_hint (dispatch.py:213)
  deja de buscar ''sobrescrit'' y detecta solo el texto inglés de git (''would be
  overwritten''), que con LC_ALL=C es estable. Los archivos ya se calculan con git
  status --porcelain y git diff --name-only, y eso se queda igual.


  P2 y B2) Solo dispatch.py. git se corre en _git de dispatch.py; deskops/runtime
  no se toca.


  B3) Alcance: solo los subprocess de git de dispatch.py, todos vía _git. No se buscan
  ni corrigen otros sitios fuera de dispatch.py.


  P3) La matriz es exactamente es_ES.UTF-8 (con LC_ALL y LANGUAGE=es) y en_US.UTF-8.
  No hacen falta otros.


  B4) d42ee663 es el commit que agregó _commit_run_docs y _dirty_overwrite_hint a
  dispatch.py y el test test_reap_names_the_files_when_local_changes_block_the_pick.
  Está en main; se ve con git show d42ee663.


  B5) El worktree es el que dispatch le da al ejecutor. El trailer es ''Task-Id: <id
  de esta tarea>'' en el cuerpo.


  B6) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar, en
  el estilo de las vecinas.


  B7) Verificado por el coordinador: locale -a lista es_AR.utf8, es_BO.utf8 y otros
  es_*. Si es_ES.utf8 no está, se usa cualquier es_*.utf8 que liste locale -a. Con
  es_CL.UTF-8 el coordinador ya reprodujo la falla.'
# ISO 8601 timestamp
created_at: '2026-11-21T11:48:26.888585+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T11:49:40.289948+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-114814/context-review/task-reap-nombra-los-archivos-que-bloquean-el-cherry-pick-sin-depender-del-idioma-de-git-falla-con-lang-e/preflight/5e78198c002fec4090e949d6dcde82e7874d4fee423b3487d7aafaa77d306649/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1, P4 y B1) La estrategia es LC_ALL=C. _git (deskops/dispatch.py:79) pasa env={**os.environ, 'LC_ALL': 'C', 'LANGUAGE': ''} a subprocess.run. _dirty_overwrite_hint (dispatch.py:213) deja de buscar 'sobrescrit' y detecta solo el texto inglés de git ('would be overwritten'), que con LC_ALL=C es estable. Los archivos ya se calculan con git status --porcelain y git diff --name-only, y eso se queda igual.

P2 y B2) Solo dispatch.py. git se corre en _git de dispatch.py; deskops/runtime no se toca.

B3) Alcance: solo los subprocess de git de dispatch.py, todos vía _git. No se buscan ni corrigen otros sitios fuera de dispatch.py.

P3) La matriz es exactamente es_ES.UTF-8 (con LC_ALL y LANGUAGE=es) y en_US.UTF-8. No hacen falta otros.

B4) d42ee663 es el commit que agregó _commit_run_docs y _dirty_overwrite_hint a dispatch.py y el test test_reap_names_the_files_when_local_changes_block_the_pick. Está en main; se ve con git show d42ee663.

B5) El worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

B6) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar, en el estilo de las vecinas.

B7) Verificado por el coordinador: locale -a lista es_AR.utf8, es_BO.utf8 y otros es_*. Si es_ES.utf8 no está, se usa cualquier es_*.utf8 que liste locale -a. Con es_CL.UTF-8 el coordinador ya reprodujo la falla.
