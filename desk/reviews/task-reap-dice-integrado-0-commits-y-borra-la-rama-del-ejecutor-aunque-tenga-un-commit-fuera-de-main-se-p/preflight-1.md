---
sldb:
  by: agent
  at: '2026-11-22T12:19:24Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p-preflight-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: preflight
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDebugDoc:task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p@sha256:787d27f29ebab1b6d83f42fb2a289d1c7230620cf216ace708b241cdec7f8749
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261122-121627/context-review/task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p/preflight/9ca2d1ab56fa03f8880ea5fdbcd010f2c22bdff27689ef2ccae405ea0bf3983f/attempt-1
input_sha256: 9ca2d1ab56fa03f8880ea5fdbcd010f2c22bdff27689ef2ccae405ea0bf3983f
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: d923424526ea15855e205c58d5b14c8059d75bbc0128e057bfe906ffb1637c94
output_sha256: 91a165a1bdf072f3620986ddbc0b532b353c58f9847355adff0984714fbf0000
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'Aceptado. Resoluciones del coordinador, con la causa ya identificada en el
  código.


  B4 (la causa) y P2) No es el rango. Es una carrera:

  - el reap corrió a las 12:05:46 (log 20261122T120546Z en el desk de sldb);

  - el commit b424ce65 del ejecutor es de las 12:05:52, seis segundos después.


  Cuando el reap calculó git rev-list --right-only <base>...<rama> (deskops/dispatch.py:157),
  la rama todavía no tenía el commit: dio 0, que era correcto en ese instante. Después
  llamó a _remove_worktree (dispatch.py:133), que hace ''git worktree remove --force''
  y ''git branch -D'', y borró el worktree con los cambios sin commitear. El commit
  quedó colgante.


  El arreglo:

  1. Antes de borrar, _remove_worktree (o su llamador en la línea 172) corre ''git
  -C <worktree> status --porcelain''. Si hay cambios, no borra nada.

  2. Antes de borrar, si el agente sigue vivo en scion (phase running y activity distinta
  de completed, stopped o exited, la misma consulta que ya usa reap para leer el estado),
  tampoco borra.

  3. En esos dos casos sale con EXIT_BUSY (3, para que la cola reintente) y por stdout:
  ''en espera: el worktree de <nombre> tiene cambios sin commitear'' o ''en espera:
  <nombre> sigue vivo''.

  4. Se quita --force de ''git worktree remove'': un worktree sucio no se borra nunca.

  El orden y los conflictos del cherry-pick no cambian; ya hace --abort y devuelve
  EXIT_WORKTREE.


  B1) <base> es la que ya usa reap: _base_branch(root), la rama local principal. No
  es origin/main.


  P3 y B2) Contrato del error: código 3 (EXIT_BUSY), mensajes en español por stdout
  como los demás de reap, con estos textos exactos:

  - ''en espera: el worktree de <nombre> tiene cambios sin commitear''

  - ''en espera: <nombre> sigue vivo''


  P1) El test reproduce la carrera con el fixture env de tests/test_dispatch.py: después
  de start, escribir un archivo en el worktree sin commitear y correr reap. Tiene
  que salir 3, conservar el worktree y la rama, y no borrar el archivo. Un segundo
  test: con el archivo commiteado, reap lo integra.


  P4 y B3) Los locales se fijan en el entorno del comando:

  - LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es python -m pytest -n 4 -q -p no:cacheprovider
  tests/test_dispatch.py

  - y lo mismo con en_US.UTF-8.


  P5 y B5) La reproducción va en runs/subagents/exec-<tu agente>/reproduction.log,
  con la salida del test nuevo antes del arreglo (falla) y después (pasa).


  P6) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El trailer
  es ''Task-Id: <id de esta tarea>'' en el cuerpo.


  B6) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar.'
# ISO 8601 timestamp
created_at: '2026-11-22T12:16:38.633394+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T12:19:16.897569+00:00'
disposed_by: deskops
# e.g. workspace:desk
tags:
- workspace:desk
---

# Preflight review of task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p

## Summary

_Summarize what was reviewed and the evidence this receipt records._

preflight review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-121627/context-review/task-reap-dice-integrado-0-commits-y-borra-la-rama-del-ejecutor-aunque-tenga-un-commit-fuera-de-main-se-p/preflight/9ca2d1ab56fa03f8880ea5fdbcd010f2c22bdff27689ef2ccae405ea0bf3983f/attempt-1.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador, con la causa ya identificada en el código.

B4 (la causa) y P2) No es el rango. Es una carrera:
- el reap corrió a las 12:05:46 (log 20261122T120546Z en el desk de sldb);
- el commit b424ce65 del ejecutor es de las 12:05:52, seis segundos después.

Cuando el reap calculó git rev-list --right-only <base>...<rama> (deskops/dispatch.py:157), la rama todavía no tenía el commit: dio 0, que era correcto en ese instante. Después llamó a _remove_worktree (dispatch.py:133), que hace 'git worktree remove --force' y 'git branch -D', y borró el worktree con los cambios sin commitear. El commit quedó colgante.

El arreglo:
1. Antes de borrar, _remove_worktree (o su llamador en la línea 172) corre 'git -C <worktree> status --porcelain'. Si hay cambios, no borra nada.
2. Antes de borrar, si el agente sigue vivo en scion (phase running y activity distinta de completed, stopped o exited, la misma consulta que ya usa reap para leer el estado), tampoco borra.
3. En esos dos casos sale con EXIT_BUSY (3, para que la cola reintente) y por stdout: 'en espera: el worktree de <nombre> tiene cambios sin commitear' o 'en espera: <nombre> sigue vivo'.
4. Se quita --force de 'git worktree remove': un worktree sucio no se borra nunca.
El orden y los conflictos del cherry-pick no cambian; ya hace --abort y devuelve EXIT_WORKTREE.

B1) <base> es la que ya usa reap: _base_branch(root), la rama local principal. No es origin/main.

P3 y B2) Contrato del error: código 3 (EXIT_BUSY), mensajes en español por stdout como los demás de reap, con estos textos exactos:
- 'en espera: el worktree de <nombre> tiene cambios sin commitear'
- 'en espera: <nombre> sigue vivo'

P1) El test reproduce la carrera con el fixture env de tests/test_dispatch.py: después de start, escribir un archivo en el worktree sin commitear y correr reap. Tiene que salir 3, conservar el worktree y la rama, y no borrar el archivo. Un segundo test: con el archivo commiteado, reap lo integra.

P4 y B3) Los locales se fijan en el entorno del comando:
- LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 LANGUAGE=es python -m pytest -n 4 -q -p no:cacheprovider tests/test_dispatch.py
- y lo mismo con en_US.UTF-8.

P5 y B5) La reproducción va en runs/subagents/exec-<tu agente>/reproduction.log, con la salida del test nuevo antes del arreglo (falla) y después (pasa).

P6) El worktree es el que dispatch le da al ejecutor (lo dice su prompt). El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

B6) CHANGELOG.md en la raíz: una viñeta en la sección superior sin publicar.
