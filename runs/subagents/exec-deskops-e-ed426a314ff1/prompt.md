Task: task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar
Title: Snapshot de contratos de modelo: RuleDoc cambió solo la descripción de where (sldb 22cfafb2); actualizar el hash sin migración
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
  at: '2026-11-21T11:43:49Z'
  authority: generated
  via: create_document
id: task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Snapshot de contratos de modelo: RuleDoc cambió solo la descripción de where (sldb 22cfafb2); actualizar el hash sin migración

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-21: el integrate del arreglo de init falló en la suite por tests/test_model_contract_snapshot.py::test_model_contract_hashes_match_the_snapshot ('Model contract changed for: RuleDoc'). Falla igual en origin/main de deskops. La causa es sldb 22cfafb2 (retiro de incomplete del lenguaje de predicados, ya en sldb origin eab79da6), que solo cambió la description del campo where de src/sldb/models/rule_doc.py: de '...false or incomplete means the rule does not apply...' a '...false means the rule does not apply...'. No cambió el tipo, el default ni los campos. El snapshot incluye la description en el hash, y el test pide actualizar tests/fixtures/model_contract_hashes.json solo como parte de una migración deliberada. Bloquea todos los integrate de deskops.

## Goal

_Describe the concrete result this task must produce._

tests/fixtures/model_contract_hashes.json tiene el hash nuevo de RuleDoc, recalculado con la función del propio test (no a mano), y el commit explica que es un cambio solo de descripción, sin migración de stores. Antes de actualizarlo, verificar con evidencia que no hace falta migrar: sldb stores check sobre el store de deskops y el de sldb no da hallazgos nuevos de RuleDoc (anotar la salida en el run dir). Si el test permite marcar cambios solo de descripción sin migración (ver FIXTURE_UPDATE en el test), seguir ese camino.

## Scope

_State what is in scope and what is out of scope._

Dentro: tests/fixtures/model_contract_hashes.json (solo la entrada RuleDoc) y CHANGELOG. Fuera: el test, otros hashes y sldb.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: leer FIXTURE_UPDATE en tests/test_model_contract_snapshot.py y seguir el procedimiento que indica para regenerar el hash. p2: comprobar que solo cambió RuleDoc y que la diferencia es la description de where (git -C /mnt/ssd/herramientas/sldb show 22cfafb2 -- src/sldb/models/rule_doc.py). p3: sldb stores check en los dos stores, salida en el run dir. p4: actualizar solo la entrada RuleDoc y correr el test. p5: CHANGELOG; commit desde el worktree que dispatch te da con 'git commit -- <rutas>' y el trailer 'Task-Id: <id de esta tarea>' en el cuerpo.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_model_contract_snapshot.py pasa contra el sldb de /mnt/ssd/herramientas/sldb y solo cambió la entrada RuleDoc del fixture.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-ed426a314ff1`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-ed426a314ff1

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
