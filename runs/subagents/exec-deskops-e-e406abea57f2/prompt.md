Task: task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la
Title: los rituales context-review y phase nombran deskops review y la regla de activacion como gate de la tarea
Status: draft
Current node: ritual-execution
Task type: task.docs
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-17T01:36:10Z'
  authority: generated
  via: create_document
id: task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la
status: draft
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/gates-por-tipo/dag.yaml
depends_on: []
pills: []
files:
- desk/rituals/context-review.md
- desk/rituals/phase.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# los rituales context-review y phase nombran deskops review y la regla de activacion como gate de la tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GC08 del plan congelado gates-por-tipo (desk/drawer/plans/gates-por-tipo/dag.yaml), el unico nodo de ese plan que sigue vigente tras el triaje del 2026-11-16. El ritual context-review todavia describe la revision barata con el comando pi a mano (el perfil pi --provider deepseek ... en su linea 18) y guarda la reformulacion en runs/subagents/<run-dir>/preflight.md; el ritual phase describe su gate sin la regla de activacion. Desde CC31-CC33 eso lo hacen deskops review preflight|bundle|dispose con un RuntimeProfileDoc (default runtime-pi-deepseek-flash) y las reglas rule-activation-<tipo> de desk/lifecycle, como ya dicen docs/operator-manual.md y el quickstart.

## Goal

_Describe the concrete result this task must produce._

desk/rituals/context-review.md describe la revision de contexto como deskops review preflight y deskops review bundle (con --engine <perfil> y el default runtime-pi-deepseek-flash), su recibo en desk/reviews/<tarea>/ y su disposicion con deskops review dispose; desk/rituals/phase.md nombra la regla rule-activation-<tipo> como el gate que deja pasar una tarea a ejecucion. Ninguno de los dos instruye correr pi a mano.

## Scope

_State what is in scope and what is out of scope._

Entra: los pasos de context-review que hoy describen el comando pi manual y el archivo preflight.md del run dir, y el gate de phase. Los rituales se cambian con deskops edit ritual <id> <campo> <valor> --root . (nunca a mano). Sale: los otros rituales, las reglas de desk/lifecycle, docs/ (ya estan al dia) y el plan gates-por-tipo (se retira aparte).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) deskops show ritual context-review --root . y deskops show ritual phase --root . para ver campos y pasos. 2) Reescribir los pasos afectados con deskops edit ritual, tomando la redaccion de docs/operator-manual.md sobre deskops review. 3) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops show ritual context-review --root . (sin 'pi --provider' ni 'preflight.md' como instruccion)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && deskops doctor --root . (sin hallazgos nuevos sobre rituales)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py

## Done When

_Name the observable condition that makes the task complete._

context-review y phase nombran deskops review preflight|bundle|dispose y la regla de activacion, no instruyen pi manual, doctor no da hallazgos nuevos y tests/test_skill_cli_drift.py pasa.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-los-rituales-context-review-y-phase-nombran-deskops-review-y-la-regla-de-activacion-como-gate-de-la"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.
