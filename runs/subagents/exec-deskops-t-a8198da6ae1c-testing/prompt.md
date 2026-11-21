Task: task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor
Title: La guia versionada de deskops dice que los cambios solo de desk van en el checkout principal, sin worktree
Status: active
Current node: ritual-testing
Task type: task.docs
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-21T20:16:21Z'
  authority: generated
  via: save_document_payload
id: task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor
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
- desk/inbox/20261104-180658-suggestion-cambios-solo-de-desk-van-directo-en-el-checkout-principal-nunca-en-un-worktree.md
depends_on: []
pills: []
files:
- .opencode/skills/use-deskops/SKILL.md
- docs/operator-manual.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La guia versionada de deskops dice que los cambios solo de desk van en el checkout principal, sin worktree

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de JP (2026-11-04, desde MEPU): crear una tarea, mandar notas, editar un campo o hacer un closeout se hace con deskops en el checkout principal del repo, sobre su rama de integracion: ponerse al dia con el remoto, git add solo de los archivos de desk/ y .sldb que toco deskops (nunca git add -A), commit con [skip ci] y push; los worktrees son para cambios de codigo que pasan por PR. Ya esta en .claude/skills/deskops-workflow/SKILL.md (lineas 80-85); falta en la guia de opencode y en el manual.

## Goal

_Describe the concrete result this task must produce._

La regla aparece en ingles, igual en ambos archivos: en .opencode/skills/use-deskops/SKILL.md y en docs/operator-manual.md (subseccion nueva '### Desk-only changes' al final de la seccion '## Desk scaffold, migration, and repair'). Texto: 'Desk-only changes go straight on the main checkout, never in a worktree. Creating a task, sending inbox notes, editing a field or committing a closeout is done with deskops in the repo main checkout on its integration branch: sync with the remote first, git add only the desk/ and .sldb files deskops touched (never git add -A: other sessions may have uncommitted work there), commit with [skip ci] and push. Worktrees are for code changes that go through a PR.'

## Scope

_State what is in scope and what is out of scope._

Entra: .opencode/skills/use-deskops/SKILL.md y docs/operator-manual.md. No entra: un aviso de deskops al correr dentro de un worktree secundario (la nota lo pide 'si aplica'; se descarta en este triaje), .pi/skills (no versionado).

## Implementation Path

_Outline the expected implementation route or affected surface._

Copiar el parrafo de .claude/skills/deskops-workflow/SKILL.md:80-85 adaptado a cada archivo y correr los tests.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_operator_manual.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -n 'Desk-only changes go straight on the main checkout' .opencode/skills/use-deskops/SKILL.md docs/operator-manual.md (una linea por archivo)

## Done When

_Name the observable condition that makes the task complete._

El grep encuentra la regla en ambos archivos y los dos tests pasan.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-la-guia-versionada-de-deskops-dice-que-los-cambios-solo-de-desk-van-en-el-checkout-principal-sin-wor"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
