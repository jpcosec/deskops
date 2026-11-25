---
sldb:
  by: agent
  at: '2026-11-25T16:53:08Z'
  authority: generated
  via: create_document
id: task-el-skill-deskops-workflow-pasa-a-un-nucleo-corto-que-delega-en-deskops-next-y-dispatch-start-gana-on
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261125-015557-suggestion-mejorar-el-skill-deskops-workflow-sin-meterle-deskops-entero-sesi-n-de.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El skill deskops-workflow pasa a un núcleo corto que delega en deskops next y dispatch start gana --only-prompt

## Rationale

_Explain why this task exists or the business driver behind it._

En la sesión de MEPU del 24/25-11, con el skill cargado igual se despachó con briefs a mano, se editó el repo de deskops desde MEPU (PR #12) y no se usó --to <repo> para las faltas de otra herramienta (nota 20261125-015557).

## Goal

_Describe the concrete result this task must produce._

Un skill núcleo de unas 30 líneas que manda a correr deskops next en cada paso, más references/ por situación (dispatch, varias sesiones, falta en otra herramienta, gates y reviews), y el comando deskops dispatch start <rol> --task <id> --only-prompt, que escribe prompt.md sin lanzar scion.

## Scope

_State what is in scope and what is out of scope._

Entra: .claude/skills/deskops-workflow (núcleo + references), un test que compara el mapa de comandos del skill con --help, y --only-prompt en dispatch start. Sale: evals automáticas del skill (quedan anotadas como siguiente paso).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) --only-prompt en deskops/dispatch.py reutiliza la escritura de prompt.md y termina antes de scion templates sync. 2) Reescribir SKILL.md como núcleo y mover el detalle a references/. 3) Corregir lo desactualizado: status es alias de doctor y el repo es jpcosec/deskops. 4) Agregar la regla de no editar el repo de otra herramienta y de usar message send --to <repo>.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_dispatch.py tests/test_skill_cli_drift.py

## Done When

_Name the observable condition that makes the task complete._

dispatch start --only-prompt escribe prompt.md sin llamar a scion (lo prueba un test), y el skill núcleo pasa el test de drift contra el CLI.
