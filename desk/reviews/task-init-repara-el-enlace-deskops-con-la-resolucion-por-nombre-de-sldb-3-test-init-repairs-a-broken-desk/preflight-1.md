---
sldb:
  by: agent
  at: '2026-11-24T18:06:30Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk@sha256:959127cc925c6cc0696e25c406d62979259464b4c9c573998b6cc195e4c69e23
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-091442/context-review/task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk/preflight/d2357f93245f6e8b0626a3346a6359d7fa27d0a94584af5bcc6de82d37e402c8/attempt-1
input_sha256: d2357f93245f6e8b0626a3346a6359d7fa27d0a94584af5bcc6de82d37e402c8
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: cd7b28d1ed40ed1e2e68d9efda0f43acfba4441916834f06d70e500fdc755739
output_sha256: 06fee993bc536fdb01907f5dd00f02f755f4b1c7c9a32fd584160ed1d4a65e42
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador.


  P1) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El trailer
  es ''Task-Id: <id de esta tarea>'' en el cuerpo.


  P2) El store del test es la carpeta de store dentro de root, con root = tmp_path/''repo''.
  Lo inicializa _init_repo(root, capsys) en el propio test (tests/test_doctor_model_registration.py:169).
  La llamada es sldb.api.store_links sobre esa carpeta, después de _point_deskops_link_at
  y shutil.rmtree.


  P3) Tres casos concretos:

  (i) Path borrado pero nombre resoluble al dueño: init devuelve 0, no imprime ''Replaced
  broken'' y el enlace resuelve al dueño.

  (ii) Enlace ''deskops'' a un store sano distinto, creado con sldb stores init en
  tmp_path/''otro'': init imprime el ''Warning: ... already links'' que ya existe.

  (iii) Enlace cuyo status no es ok según store_links (apuntando a un directorio sin
  store y con un nombre que no resuelva): init lo reemplaza e imprime ''Replaced broken''.
  Si (iii) no se puede armar con el sldb actual, se marca con pytest.skip y el motivo,
  y el ejecutor lo informa.


  P4 y B1) Criterio: (a) es la opción por defecto. Se elige (b) solo si el grep del
  punto siguiente encuentra código de deskops, fuera de tests/, que lea el campo path
  de store_index.yaml directamente para abrir el store enlazado sin pasar por sldb.api.store_links.
  Decide el ejecutor y deja el resultado del grep en el run dir.


  B2) El grep es grep -rn store_index deskops/ más una búsqueda del campo path en
  el código de enlaces de stores. Cuenta como lectura usar ese path para abrir el
  store enlazado.


  P5) La línea exacta es deskops/bootstrap.py:271 (''if target == owner.resolve():'',
  dentro del método que enlaza ''deskops'', con store_links importado de sldb.api).


  B3) El run dir es runs/subagents/exec-<tu agente>/, el mismo de result-summary.md.


  B4) La tarea cierra con tests/test_doctor_model_registration.py en verde. En la
  suite completa, las fallas de otros archivos se anotan pero no bloquean; test_dispatch.py::test_reap_names_the_files_when_local_changes_block_the_pick
  es un intermitente conocido.'
# ISO 8601 timestamp
created_at: '2026-11-21T09:14:58.707226+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T09:16:13.629406+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Preflight review of task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-091442/context-review/task-init-repara-el-enlace-deskops-con-la-resolucion-por-nombre-de-sldb-3-test-init-repairs-a-broken-desk/preflight/d2357f93245f6e8b0626a3346a6359d7fa27d0a94584af5bcc6de82d37e402c8/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

P2) El store del test es la carpeta de store dentro de root, con root = tmp_path/'repo'. Lo inicializa _init_repo(root, capsys) en el propio test (tests/test_doctor_model_registration.py:169). La llamada es sldb.api.store_links sobre esa carpeta, después de _point_deskops_link_at y shutil.rmtree.

P3) Tres casos concretos:
(i) Path borrado pero nombre resoluble al dueño: init devuelve 0, no imprime 'Replaced broken' y el enlace resuelve al dueño.
(ii) Enlace 'deskops' a un store sano distinto, creado con sldb stores init en tmp_path/'otro': init imprime el 'Warning: ... already links' que ya existe.
(iii) Enlace cuyo status no es ok según store_links (apuntando a un directorio sin store y con un nombre que no resuelva): init lo reemplaza e imprime 'Replaced broken'. Si (iii) no se puede armar con el sldb actual, se marca con pytest.skip y el motivo, y el ejecutor lo informa.

P4 y B1) Criterio: (a) es la opción por defecto. Se elige (b) solo si el grep del punto siguiente encuentra código de deskops, fuera de tests/, que lea el campo path de store_index.yaml directamente para abrir el store enlazado sin pasar por sldb.api.store_links. Decide el ejecutor y deja el resultado del grep en el run dir.

B2) El grep es grep -rn store_index deskops/ más una búsqueda del campo path en el código de enlaces de stores. Cuenta como lectura usar ese path para abrir el store enlazado.

P5) La línea exacta es deskops/bootstrap.py:271 ('if target == owner.resolve():', dentro del método que enlaza 'deskops', con store_links importado de sldb.api).

B3) El run dir es runs/subagents/exec-<tu agente>/, el mismo de result-summary.md.

B4) La tarea cierra con tests/test_doctor_model_registration.py en verde. En la suite completa, las fallas de otros archivos se anotan pero no bloquean; test_dispatch.py::test_reap_names_the_files_when_local_changes_block_the_pick es un intermitente conocido.
