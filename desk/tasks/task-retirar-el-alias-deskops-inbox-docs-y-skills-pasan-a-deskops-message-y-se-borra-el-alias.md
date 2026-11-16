---
sldb:
  by: agent
  at: '2026-11-16T06:05:15Z'
  authority: generated
  via: save_document_payload
id: task-retirar-el-alias-deskops-inbox-docs-y-skills-pasan-a-deskops-message-y-se-borra-el-alias
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/cli/registry.py
- docs/operator-manual.md
- docs/faq.md
- .claude/skills/deskops-workflow/SKILL.md
- .claude/skills/deskops-workflow/references/deskops-cli.md
- .claude/skills/deskops-workflow/references/vocabulary.md
- tests/test_message_cli.py
- tests/test_message_delivery.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
from_drawer: desk/drawer/tasks/task-retirar-caminos-legacy-migrar-los-datos-y-borrar-el-c-digo-de-compatibilidad.md
---

# Retirar el alias deskops inbox: docs y skills pasan a deskops message y se borra el alias

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (punto 4). El alias `deskops inbox` esta deprecado a favor de `deskops message` (deskops/cli/registry.py:651, deprecated_for=('message',)). Aun lo nombran docs/operator-manual.md:421 y 425, docs/faq.md:52 y 230 y la skill .claude/skills/deskops-workflow (SKILL.md, references/deskops-cli.md y references/vocabulary.md), que es la skill global por symlink.

## Goal

_Describe the concrete result this task must produce._

Ningun doc ni skill versionado usa `deskops inbox`; el alias, sus goldens de ayuda y sus tests desaparecen.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/cli/registry.py, docs/operator-manual.md, docs/faq.md, deskops/data/faq.md si lo nombra, .claude/skills/deskops-workflow/SKILL.md y references/, goldens de ayuda, tests/test_message_cli.py y tests/test_message_delivery.py (casos de alias). No entra: .pi/skills (no versionado). Precisiones del preflight 1: el reemplazo es deskops message send: 'deskops inbox "<texto>" --kind K --root .' pasa a 'deskops message send "<texto>" --kind K --root .' (sin --to escribe en el propio desk; con --to <repo> en otro). Entra tambien deskops/data/faq.md, .opencode/ y README.md si el grep los muestra. Goldens: los de tests/fixtures/golden/help que nombran el alias (deskops_inbox.txt y los que lo listen como comando), regenerados con pytest --update-golden. Casos de test a borrar = los que invocan 'deskops inbox' o comprueban el aviso de deprecado. El patron de busqueda es grep -rnw 'deskops inbox'.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn 'deskops inbox' docs .claude .opencode deskops/data README.md`. 2) Reescribir con deskops message send. 3) Borrar el alias y sus tests. 4) Regenerar goldens.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && ! grep -rnw 'deskops inbox' docs .claude .opencode deskops/data README.md
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_cli.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_message_delivery.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_output_goldens.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_cli_grammar.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar). Sin fallas nuevas: cada test que falle se corre con el mismo comando en un worktree limpio de origin/main (git worktree add /dev/shm/wt-base origin/main; luego git worktree remove /dev/shm/wt-base) y solo se acepta si falla igual ahí; la lista de esas fallas va en el informe de la tarea

## Done When

_Name the observable condition that makes the task complete._

El grep queda vacio, `deskops inbox` da error de comando desconocido y los tests pasan.
