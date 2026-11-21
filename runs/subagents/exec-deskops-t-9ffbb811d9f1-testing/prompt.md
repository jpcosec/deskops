Task: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime
Title: graph export y self_reflection escriben su salida derivada en .sldb_cache y no en .sldb/runtime
Status: active
Current node: ritual-testing
Task type: task.code
Effective pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T21:35:45Z'
  authority: generated
  via: save_document_payload
id: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime
status: active
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261104-233657-suggestion-sldb-el-store-pasa-a-sldb-versionado-y-sldb-cache-ignorada-journal-retirado.md
depends_on: []
pills:
- desk/contexts/pill-010-graph-runtime-output-policy.md
files:
- deskops/graph/export.py
- deskops/graph/self_reflection.py
- tests/test_graph_snapshot.py
- tests/test_graph_self_reflection.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# graph export y self_reflection escriben su salida derivada en .sldb_cache y no en .sldb/runtime

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de sldb (c420809c, 2026-11-04): el store es .sldb/ versionado y lo derivado vive en .sldb_cache/, ignorada. deskops todavia escribe salidas derivadas en la ruta vieja .sldb/runtime/, que ya no esta ignorada: deskops/graph/export.py:22 y deskops/graph/self_reflection.py:17-18 y 39.

## Goal

_Describe the concrete result this task must produce._

Las salidas de graph export y self_reflection van a .sldb_cache/ (DERIVED_ROOT = Path('.sldb_cache') en un modulo nuevo deskops/graph/paths.py; cada salida conserva la ruta relativa que hoy tiene bajo .sldb/runtime/). Ningun codigo de deskops/ ESCRIBE en .sldb/runtime/; las menciones que solo excluyen o leen esa ruta vieja (p. ej. EXCLUDED_SOURCE_PREFIXES) se conservan. La pill pill-010-graph-runtime-output-policy, que hoy dice que se prefiera .sldb/runtime/, quedo vieja con la decision de sldb c420809c: se actualiza con deskops edit pill para que diga .sldb_cache/ (ignorada por .gitignore). Consumidores: grep -rnF '.sldb/runtime' en /mnt/ssd/proyectos/SLDB_1 excluyendo runs/ y .git; si alguno fuera de deskops lee la ruta vieja, deskops message send --to <repo> con titulo 'deskops mueve sus salidas derivadas a .sldb_cache', las rutas viejas y nuevas y el hash del commit de esta tarea.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/graph/export.py, deskops/graph/self_reflection.py, sus tests (tests/test_graph_snapshot.py, tests/test_graph_self_reflection.py) y tests/test_gitignore_policy.py si hace falta. Consumidores a revisar con `grep -rn '.sldb/runtime' /mnt/ssd/proyectos/SLDB_1/UIs/graph_ui --include=*.py --include=*.js` (excluyendo runs/); si hay, `deskops message send --to graph_ui`. No entra: migrar archivos viejos ya escritos (se borran a mano solo si no estan versionados), tocar sldb. Precisiones del preflight 1: la constante es DERIVED_ROOT = Path('.sldb_cache') en un modulo nuevo deskops/graph/paths.py, importada por export.py y self_reflection.py; cada salida conserva la ruta relativa que hoy tiene bajo .sldb/runtime/ pero bajo .sldb_cache/. tests/test_gitignore_policy.py se toca solo si afirma algo sobre .sldb/runtime. La busqueda es del literal '.sldb/runtime' (grep -rnF). Si hay consumidor en graph_ui, la nota dice: titulo 'deskops mueve sus salidas derivadas a .sldb_cache', cuerpo con las rutas viejas y nuevas y el hash. No se borra ningun archivo existente.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'sldb/runtime\|"runtime"' deskops/graph deskops/services`. 2) Cambiar las rutas a una constante comun que apunte a .sldb_cache. 3) Ajustar los tests. 4) Revisar consumidores en graph_ui.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_snapshot.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_self_reflection.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_gitignore_policy.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_graph_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rnF '.sldb/runtime' deskops/ --include=*.py (solo menciones de exclusion o lectura, ninguna escritura)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Ningun codigo de deskops/ escribe en .sldb/runtime (el grep solo muestra menciones de exclusion o lectura); pill-010 dice .sldb_cache/; los tests listados pasan; consumidores avisados si los hubo.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache-y-no-en-sldb-runtime"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
