---
sldb:
  by: agent
  at: '2026-11-24T18:23:51Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar-bundle-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar@sha256:d694d8c173018e60e946b18fce2f06d4363bda7a958d4a7d7dda27d64d02d63e
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261121-114438/context-review/task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar/bundle/704b2d76ff015743b11698c4e1f02e1829083a6c5bcac6eafe0f7792ca60f5ed/attempt-1
input_sha256: 704b2d76ff015743b11698c4e1f02e1829083a6c5bcac6eafe0f7792ca60f5ed
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 7aeca0fdb338a8a99122c6b71c6a66b93feda19436f803e7e60ec8d3f0cebbc9
output_sha256: 8699ba1076767f3bec4a9d3414188f7550c1db3b71a15c6d3be87c19bd4df153
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador.


  P1 y B1) Los stores son las carpetas de store de los dos repos. Los comandos exactos
  son:

  - sldb stores check --store /mnt/ssd/proyectos/SLDB_1/deskops/.sldb

  - sldb stores check --store /mnt/ssd/proyectos/SLDB_1/sldb/.sldb

  Si se corren desde el worktree, la primera puede ir con --store relativo a su raíz.


  P2 y B2) El run dir es runs/subagents/exec-<tu agente>/, el mismo de result-summary.md.


  P3 y B5) El worktree es el que dispatch le da al ejecutor (su prompt lo dice). El
  trailer es ''Task-Id: <id de esta tarea>'' en el cuerpo.


  P4 y B3) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar,
  en el estilo de las vecinas, que diga que el hash de RuleDoc se actualizó por un
  cambio solo de descripción en sldb 22cfafb2, sin migración.


  P5) El camino es el que describe FIXTURE_UPDATE en tests/test_model_contract_snapshot.py
  (línea 12). Si no prevé cambios solo de descripción, se regenera el hash de RuleDoc
  con la misma función del test, se actualiza solo esa entrada y la justificación
  va en el commit y en el CHANGELOG. No se cambia el test.


  P6) No hace falta apuntar a nada: el venv de /mnt/ssd/proyectos/SLDB_1/.venv ya
  importa sldb desde /mnt/ssd/herramientas/sldb/src. Se comprueba con python -c ''import
  sldb; print(sldb.__file__)''. Correr el pytest con ese venv.


  B4) La línea base es la salida de sldb stores check antes de actualizar el fixture.
  Los hallazgos ''nuevos'' son los que mencionan RuleDoc y no estaban en esa base.
  Como el fixture no afecta a los stores, se espera que no haya ninguno.'
# ISO 8601 timestamp
created_at: '2026-11-21T11:44:56.228635+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-21T11:47:58.401046+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261121-114438/context-review/task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar/bundle/704b2d76ff015743b11698c4e1f02e1829083a6c5bcac6eafe0f7792ca60f5ed/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1 y B1) Los stores son las carpetas de store de los dos repos. Los comandos exactos son:
- sldb stores check --store /mnt/ssd/proyectos/SLDB_1/deskops/.sldb
- sldb stores check --store /mnt/ssd/proyectos/SLDB_1/sldb/.sldb
Si se corren desde el worktree, la primera puede ir con --store relativo a su raíz.

P2 y B2) El run dir es runs/subagents/exec-<tu agente>/, el mismo de result-summary.md.

P3 y B5) El worktree es el que dispatch le da al ejecutor (su prompt lo dice). El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

P4 y B3) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar, en el estilo de las vecinas, que diga que el hash de RuleDoc se actualizó por un cambio solo de descripción en sldb 22cfafb2, sin migración.

P5) El camino es el que describe FIXTURE_UPDATE en tests/test_model_contract_snapshot.py (línea 12). Si no prevé cambios solo de descripción, se regenera el hash de RuleDoc con la misma función del test, se actualiza solo esa entrada y la justificación va en el commit y en el CHANGELOG. No se cambia el test.

P6) No hace falta apuntar a nada: el venv de /mnt/ssd/proyectos/SLDB_1/.venv ya importa sldb desde /mnt/ssd/herramientas/sldb/src. Se comprueba con python -c 'import sldb; print(sldb.__file__)'. Correr el pytest con ese venv.

B4) La línea base es la salida de sldb stores check antes de actualizar el fixture. Los hallazgos 'nuevos' son los que mencionan RuleDoc y no estaban en esa base. Como el fixture no afecta a los stores, se espera que no haya ninguno.
