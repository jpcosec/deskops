Task: task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason
Title: drawer remove retira un plan entero, los assets de un issue, entradas no .md por stem, y registra reason y ref
Status: draft
Current node: ritual-execution
Task type: task.code
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-21T13:25:45Z'
  authority: generated
  via: save_document_payload
id: task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-055429-unclear-drawer-remove-deja-colgando-from-drawer-references-y-no-retira-planes-dag-yaml.md
- desk/inbox/20261116-004719-unclear-drawer-remove-de-un-issue-deja-sus-assets-y-retire-los-rechaza-no-hay-verbo-para-darlos-de-baja.md
- desk/inbox/20261116-005408-unclear-desk-sin-git-sldb-ui-supersede-tambi-n-hace-commit-drawer-remove-no-acepta-el-stem.md
- desk/inbox/20261116-004657-unclear-desk-update-apply-en-desk-legacy-56-tareas-sin-migraci-n-masiva-y-5-modelos-legacy-sin-importar.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# drawer remove retira un plan entero, los assets de un issue, entradas no .md por stem, y registra reason y ref

## Rationale

_Explain why this task exists or the business driver behind it._

Cuatro notas del 2026-11-16: sldb (20261116-055429, punto 2): drawer remove no acepta un plan de desk/drawer/plans/<plan>/ (dag.yaml) y responde No drawer file matches, los planes se retiraron con git rm a mano (tambien en deskops, commit 1530e576); graph_ui (20261116-004719): drawer remove de un issue deja sus capturas en desk/drawer/issues/assets/<issue>/ y deskops retire las rechaza con has its own retirement verb aunque el issue ya no existe; sldb-ui (20261116-005408, punto 2): el stem de la entrada macro-01-cli-gateway del drawer (yml, ya retirada) no matchea porque resolve_drawer_source solo busca *.md (deskops/services/drawer.py ~linea 74); marcado (20261116-004657): drawer remove no registra reason ni ref como si hace retire.

## Goal

_Describe the concrete result this task must produce._

deskops drawer remove: (1) acepta un directorio de plan bajo desk/drawer/plans/ (por ruta o por nombre del plan) y lo retira entero, con su tracking y sus bullets del Board del drawer; (2) al retirar un issue retira tambien su carpeta de assets si nadie mas la referencia (y deskops retire acepta un asset huerfano de un issue que ya no existe); (3) resuelve por stem o fragmento tambien entradas .yml/.yaml del drawer; (4) acepta --reason y --ref y los deja registrados igual que deskops retire. Lo que hoy funciona sigue igual, incluido el bloqueo por from_drawer sin --force.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/drawer.py (resolve_drawer_source ~52-80, remove_entry ~148), deskops/services/retire.py (_DEDICATED_VERBS ~19 y el chequeo ~70-75), deskops/cli/registry.py (argumentos de drawer remove) y su golden de ayuda tests/fixtures/golden/help/deskops_drawer_remove.txt, tests nuevos. No entra: from_drawer colgante (ya resuelto: PROVENANCE_FIELDS en deskops/graph/desk_graph.py:44 lo deja como texto y graph missing no lo cuenta).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer drawer.py y retire.py completos y como retire registra reason/ref. 2) Extender la resolucion a directorios de plan y a .yml/.yaml. 3) Retiro de assets del issue. 4) --reason/--ref. 5) Tests por cada punto en un desk temporal.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_inbox_promote_cli_gaps.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests -k "drawer or retire"
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_help_examples.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

Tests nuevos: drawer remove retira un plan con dag.yaml, retira los assets de un issue, resuelve un .yml por stem y deja reason y ref registrados; retire acepta un asset huerfano de un issue inexistente.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-0f70399e3d10`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-0f70399e3d10

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
