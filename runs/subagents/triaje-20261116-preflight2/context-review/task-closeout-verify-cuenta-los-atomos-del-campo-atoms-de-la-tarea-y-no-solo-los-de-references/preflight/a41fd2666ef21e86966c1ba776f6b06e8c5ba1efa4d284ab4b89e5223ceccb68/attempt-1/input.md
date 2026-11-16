FILE:desk/tasks/task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references.md
---
sldb:
  by: agent
  at: '2026-11-16T05:02:04Z'
  authority: generated
  via: save_document_payload
id: task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills:
- desk/contexts/pill-closeout-knowledge-gates-require-traceable-evidence.md
files:
- deskops/services/closeout_gates.py
- deskops/services/closure.py
- tests/test_closeout_gates.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-closeout-verify-ignora-el-campo-atoms-de-la-tarea-y-solo-lee-references.md
---

# closeout verify cuenta los atomos del campo atoms de la tarea y no solo los de references

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (2026-10-29): closeout verify falla con missing_atom_or_materialization_link aunque la tarea tenga atoms: [atom-...] en su frontmatter. Reproduccion: `deskops edit task T atoms '["atom-x"]'` -> verify falla; `deskops edit task T references '[..., "atom-x"]'` -> verify pasa. Sigue igual hoy: deskops/services/closeout_gates.py:100-113 solo recorre references y deskops/services/closure.py:1241 y 1288-1293 usan reference_evidence['atom'].

## Goal

_Describe the concrete result this task must produce._

La compuerta atom|materialization de closeout verify y de closeout commit cuenta como evidencia los ids del campo atoms de la tarea, igual que los atom-* de references.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/closeout_gates.py, deskops/services/closure.py y sus tests. No entra: cambiar otras compuertas ni el formato del reporte. Precisiones del preflight 1: se cuentan todos los valores del campo atoms (es una lista tipada de AtomDoc; no se filtra por prefijo). La compuerta de materialization no cambia. Los tests de Validation que no esten en files pueden editarse solo si el cambio los rompe por una razon legitima. El status draft de la tarea no le toca al ejecutor.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Unir task.atoms a los atom-* de references al armar la evidencia de atomo. 2) Test en tests/test_closeout_gates.py: tarea con atoms y sin atom-* en references pasa la compuerta; tarea sin ninguno sigue fallando.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_gates.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

Los dos casos del test pasan y la reproduccion del item ya no falla.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

