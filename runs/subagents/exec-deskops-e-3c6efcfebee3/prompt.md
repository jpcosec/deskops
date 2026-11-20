Task: task-la-skill-el-ritual-drawer-triage-y-la-ayuda-de-promote-dicen-que-una-nota-del-inbox-que-es-trabajo-s
Title: La skill, el ritual drawer-triage y la ayuda de promote dicen que una nota del inbox que es trabajo se vuelve tarea con references y ack
Status: draft
Current node: ritual-execution
Task type: task.docs
Effective atoms:
- atom-inbox-is-coordination-intake
- atom-drawers-feed-tasks-through-promotion
Lifecycle gates:
- task_activates -> ritual-testing: open [(none)]
  post-hook encola-reap-del-ejecutor: deskops queue add dispatch-reap --root .
  post-hook encola-tester: deskops queue add dispatch-tester --root .

---
sldb:
  by: agent
  at: '2026-11-16T06:06:02Z'
  authority: generated
  via: save_document_payload
id: task-la-skill-el-ritual-drawer-triage-y-la-ayuda-de-promote-dicen-que-una-nota-del-inbox-que-es-trabajo-s
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-003032-unclear-la-skill-y-ritual-drawer-triage-mandan-el-inbox-al-drawer-los-atoms-dicen-que-no.md
- /mnt/ssd/proyectos/SLDB_1/triaje-drawers-inbox-brief.md
depends_on: []
pills: []
files:
- .claude/skills/deskops-workflow/SKILL.md
- .claude/skills/deskops-workflow/references/vocabulary.md
- desk/rituals/ritual-drawer-triage.md
- deskops/cli/registry.py
- docs/operator-manual.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-inbox-is-coordination-intake
- atom-drawers-feed-tasks-through-promotion
---

# La skill, el ritual drawer-triage y la ayuda de promote dicen que una nota del inbox que es trabajo se vuelve tarea con references y ack

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del 2026-11-16. La skill deskops-workflow (.claude/skills/deskops-workflow/SKILL.md, lineas 41, 68 y 100) y el paso 1 de desk/rituals/ritual-drawer-triage.md dicen que las notas del inbox pasan al drawer con `deskops promote inbox-to-drawer-task`. Eso contradice atom-inbox-is-coordination-intake (una nota es un mensaje al proyecto, no un lugar para estacionar trabajo) y atom-drawers-feed-tasks-through-promotion (el drawer se captura directamente); ademas promote borra la nota y la tarea pierde su origen. Camino confirmado por JP: si la nota es trabajo, `deskops add task` con references hacia la nota y despues `deskops message ack`; si no, solo ack y la razon queda en el informe del triaje.

## Goal

_Describe the concrete result this task must produce._

La skill (SKILL.md y references/vocabulary.md), el ritual ritual-drawer-triage (editado con `deskops edit ritual`), el texto de ayuda de `deskops promote inbox-to-drawer-task` y docs/operator-manual.md describen ese camino y ninguno manda una nota del inbox al drawer. La ayuda de promote advierte que borra la nota de origen y que no es el camino para notas que son trabajo.

## Scope

_State what is in scope and what is out of scope._

Entra: .claude/skills/deskops-workflow/SKILL.md, .claude/skills/deskops-workflow/references/vocabulary.md, desk/rituals/ritual-drawer-triage.md (solo via deskops edit ritual), el help de promote en deskops/cli/registry.py y su golden, docs/operator-manual.md. No entra: retirar el comando promote (lo decide JP en otra tarea), cambiar los atoms.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'inbox-to-drawer' .claude docs deskops/cli/registry.py desk/rituals`. 2) Reescribir cada mencion. 3) `deskops edit ritual ritual-drawer-triage steps '[...]' --root .` con el paso 1 nuevo. 4) Regenerar el golden de ayuda. 5) Tests. Precisiones del preflight 1: texto canonico (en el idioma de cada archivo): 'Una nota del inbox que es trabajo se vuelve tarea con deskops add task, con references hacia la nota (en el YAML de --from-yaml o despues con deskops edit task <id> references), y luego deskops message ack <nota>; si no es trabajo, solo ack y la razon queda en el informe. promote inbox-to-drawer-task borra la nota de origen y no es el camino para notas que son trabajo.' Paso 1 nuevo del ritual: '1. Capture repo-local deferred work directly in desk/drawer/tasks/. Inbox notes that are work become tasks with references to the note and then message ack; they do not go to the drawer.' El golden es tests/fixtures/golden/help/deskops_promote_inbox-to-drawer-task.txt, regenerado con pytest --update-golden. Se conservan los ejemplos que sigan siendo correctos.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rn 'inbox-to-drawer' .claude docs desk/rituals (solo menciones que advierten que no es el camino para notas que son trabajo)

## Done When

_Name the observable condition that makes the task complete._

El grep solo muestra advertencias; el ritual tiene el paso 1 nuevo; los tres tests pasan.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-la-skill-el-ritual-drawer-triage-y-la-ayuda-de-promote-dicen-que-una-nota-del-inbox-que-es-trabajo-s"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.
