---
sldb:
  by: agent
  at: '2026-11-23T19:28:52Z'
  authority: generated
  via: save_document_payload
# review-<task>-<kind>-<n>
id: review-task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el-bundle-3
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: bundle
# kind evidence only: tests | commit | atom | materialization | document | external
fact: ''
# kind evidence only: what the producer verified, one item per line
value: ''
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el@sha256:5046ac046e76ce4b82afee1387262c8814ce3d4adc2ff539f05e0f4867d8e5e6
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: runtime-pi-deepseek-flash
actor: deskops
# Run evidence directory under runs/, relative to the project root
run_dir: runs/subagents/20261122-221304/context-review/task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el/bundle/9e494b28024c1b5c1e2d1804223089963e00bc79b74a849a7d3c3af9b9bb7aa0/attempt-2
input_sha256: 9e494b28024c1b5c1e2d1804223089963e00bc79b74a849a7d3c3af9b9bb7aa0
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: 4e4fd3de11ef562fa7df6fc2dd947757d3af123bc7f9f282c432902dd367bf7f
output_sha256: d1f767da2a7ac10a21352d85261a54c59e4acf247a90b2cb1c614aee15ac92ae
# pending | accepted | rejected | incomplete
verdict: accepted
reason: "Aceptado. Resoluciones del coordinador.\n\nP1 y B2) El título del PR es el\
  \ encabezado H1 del archivo de la tarea (la primera línea '# ...' de desk/tasks/<id>.md).\
  \ El cuerpo es fijo:\n\n    Task-Id: <id completo>\n\n    <answer del atom de cierre\
  \ de la tarea>\n\nSi no hay atom, el cuerpo es solo la línea Task-Id.\n\nP2 y B1)\
  \ El closeout es 'deskops closeout commit' (handler deskops/cli/commands/closeout.py:CloseoutCLI),\
  \ que crea el commit de cierre en la rama actual del checkout.\nEn modo pr, el coordinador\
  \ corre el closeout con task/<id> en checkout, y el cierre queda en esa rama. 'Hace\
  \ falta' cambiar closeout solo si hoy asume la rama base: por ejemplo, si rechaza\
  \ commitear fuera de integrate.branch. En ese caso acepta también task/<id> cuando\
  \ mode es 'pr'.\n\nP3 y B3) Detección del PR: 'gh pr list --head task/<id> --base\
  \ <branch> --state open --json url --jq .[0].url'.\n- Si devuelve una URL, el PR\
  \ existe: solo se empuja la rama y se imprime esa URL.\n- Si no, se crea con 'gh\
  \ pr create --base <branch> --head task/<id> --title ... --body ...'.\n- Si hubiera\
  \ varios, se usa el primero y se avisa por stdout.\n\nP4 y B4) <task-id> es el id\
  \ completo de la tarea, así que la rama es 'task/' más ese id.\n- Si la rama ya\
  \ existe localmente, reap la reutiliza: cherry-pick de los commits nuevos del ejecutor\
  \ sobre ella, sin reset ni rebase.\n- Si la base avanzó, no se toca la rama de la\
  \ tarea: el PR resuelve la diferencia.\n- La rama no se borra: la borra el merge\
  \ del PR del lado del remoto.\n\nP5 y B5) Las compuertas son las mismas de integrate._steps\
  \ (deskops/integrate.py:291): memoria, suite, store, graph y fast-forward.\n- En\
  \ modo pr, fast-forward se omite: la rama de la tarea es nueva.\n- Suite, store\
  \ y graph corren igual, sobre la punta de task/<id>.\n- La comparación de graph\
  \ es contra origin/<branch>, como hoy.\n\nP6) Contrato del gh falso: un script en\
  \ un directorio de tmp_path, puesto primero en PATH.\n- Escribe sus argumentos (uno\
  \ por línea) en un archivo del tmp_path.\n- Ante 'pr list' imprime una línea vacía,\
  \ salvo que el test quiera simular un PR existente.\n- Ante 'pr create' imprime\
  \ 'https://github.com/o/r/pull/1' y sale 0.\n- El test comprueba que el archivo\
  \ de argumentos contiene 'pr', 'create', '--base', 'dev', '--head' y 'task/<id>'.\n\
  \nP7 y B6) 'start (simulado)': se usa el fixture env de tests/test_dispatch.py,\
  \ que ya lanza start contra un scion falso y crea la rama deskops/<agente> con su\
  \ worktree. El test commitea en ese worktree, como hace el test existente test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store,\
  \ y sigue con reap, closeout e integrate.\n\nP8) Verificado por el coordinador:\
  \ la línea 11 de .gitignore es 'desk/config.local.json' (git check-ignore lo confirma),\
  \ y DeskConfig.load (deskops/config.py:104) lo mezcla con deep merge sobre config.json.\n\
  \nEl worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id\
  \ de esta tarea>' en el cuerpo.\n\nAgregados para la ronda 3:\n\nP5 y B5) start\
  \ no cambia en modo pr. Sigue creando la rama deskops/<agente> y su worktree desde\
  \ integrate.branch, como hoy. Solo cambian reap (destino task/<id> en lugar de la\
  \ base) e integrate. El seam de simulación es el fixture env de tests/test_dispatch.py,\
  \ con su scion falso, más el gh falso en PATH.\n\nB4) 'Actualizar' el PR significa\
  \ solo empujar más commits a task/<id>: el PR abierto los toma solo. No se usa gh\
  \ pr edit, ni se cambian título ni cuerpo de un PR existente.\n\nP2 y B1) Los artefactos\
  \ del closeout son los que 'deskops closeout commit' ya escribe en un solo commit:\
  \ atom, materializaciones, recibos de evidencia, RunDoc y retiro del archivo de\
  \ la tarea. El orden es:\n1. reap (commits del ejecutor en task/<id>);\n2. closeout\
  \ commit en task/<id>;\n3. integrate (compuertas, push y PR)."
# ISO 8601 timestamp
created_at: '2026-11-22T22:13:26.287372+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-22T22:14:17.417950+00:00'
disposed_by: deskops
# e.g. system:deskops
tags: []
---

# Bundle review of task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el

## Summary

_Summarize what was reviewed and the evidence this receipt records._

bundle review; engine runtime-pi-deepseek-flash; evidence under runs/subagents/20261122-221304/context-review/task-integrate-puede-terminar-en-un-pr-a-la-rama-base-declarada-modo-pr-en-vez-de-un-push-directo-con-el/bundle/9e494b28024c1b5c1e2d1804223089963e00bc79b74a849a7d3c3af9b9bb7aa0/attempt-2.

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: Aceptado. Resoluciones del coordinador.

P1 y B2) El título del PR es el encabezado H1 del archivo de la tarea (la primera línea '# ...' de desk/tasks/<id>.md). El cuerpo es fijo:

    Task-Id: <id completo>

    <answer del atom de cierre de la tarea>

Si no hay atom, el cuerpo es solo la línea Task-Id.

P2 y B1) El closeout es 'deskops closeout commit' (handler deskops/cli/commands/closeout.py:CloseoutCLI), que crea el commit de cierre en la rama actual del checkout.
En modo pr, el coordinador corre el closeout con task/<id> en checkout, y el cierre queda en esa rama. 'Hace falta' cambiar closeout solo si hoy asume la rama base: por ejemplo, si rechaza commitear fuera de integrate.branch. En ese caso acepta también task/<id> cuando mode es 'pr'.

P3 y B3) Detección del PR: 'gh pr list --head task/<id> --base <branch> --state open --json url --jq .[0].url'.
- Si devuelve una URL, el PR existe: solo se empuja la rama y se imprime esa URL.
- Si no, se crea con 'gh pr create --base <branch> --head task/<id> --title ... --body ...'.
- Si hubiera varios, se usa el primero y se avisa por stdout.

P4 y B4) <task-id> es el id completo de la tarea, así que la rama es 'task/' más ese id.
- Si la rama ya existe localmente, reap la reutiliza: cherry-pick de los commits nuevos del ejecutor sobre ella, sin reset ni rebase.
- Si la base avanzó, no se toca la rama de la tarea: el PR resuelve la diferencia.
- La rama no se borra: la borra el merge del PR del lado del remoto.

P5 y B5) Las compuertas son las mismas de integrate._steps (deskops/integrate.py:291): memoria, suite, store, graph y fast-forward.
- En modo pr, fast-forward se omite: la rama de la tarea es nueva.
- Suite, store y graph corren igual, sobre la punta de task/<id>.
- La comparación de graph es contra origin/<branch>, como hoy.

P6) Contrato del gh falso: un script en un directorio de tmp_path, puesto primero en PATH.
- Escribe sus argumentos (uno por línea) en un archivo del tmp_path.
- Ante 'pr list' imprime una línea vacía, salvo que el test quiera simular un PR existente.
- Ante 'pr create' imprime 'https://github.com/o/r/pull/1' y sale 0.
- El test comprueba que el archivo de argumentos contiene 'pr', 'create', '--base', 'dev', '--head' y 'task/<id>'.

P7 y B6) 'start (simulado)': se usa el fixture env de tests/test_dispatch.py, que ya lanza start contra un scion falso y crea la rama deskops/<agente> con su worktree. El test commitea en ese worktree, como hace el test existente test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store, y sigue con reap, closeout e integrate.

P8) Verificado por el coordinador: la línea 11 de .gitignore es 'desk/config.local.json' (git check-ignore lo confirma), y DeskConfig.load (deskops/config.py:104) lo mezcla con deep merge sobre config.json.

El worktree es el que dispatch le da al ejecutor. El trailer es 'Task-Id: <id de esta tarea>' en el cuerpo.

Agregados para la ronda 3:

P5 y B5) start no cambia en modo pr. Sigue creando la rama deskops/<agente> y su worktree desde integrate.branch, como hoy. Solo cambian reap (destino task/<id> en lugar de la base) e integrate. El seam de simulación es el fixture env de tests/test_dispatch.py, con su scion falso, más el gh falso en PATH.

B4) 'Actualizar' el PR significa solo empujar más commits a task/<id>: el PR abierto los toma solo. No se usa gh pr edit, ni se cambian título ni cuerpo de un PR existente.

P2 y B1) Los artefactos del closeout son los que 'deskops closeout commit' ya escribe en un solo commit: atom, materializaciones, recibos de evidencia, RunDoc y retiro del archivo de la tarea. El orden es:
1. reap (commits del ejecutor en task/<id>);
2. closeout commit en task/<id>;
3. integrate (compuertas, push y PR).
