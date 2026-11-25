Task: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use
Title: AGENTS.md, README.md y la carpeta de la skill de opencode dejan de nombrar use-spec2viz y pasan a use-specir
Status: active
Current node: ritual-testing
Task type: task.docs
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-19T18:34:53Z'
  authority: generated
  via: save_document_payload
id: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use
status: active
summary: ''
tags:
- host:robocop2
current_node: ritual-testing
history:
- task_activates
references:
- desk/inbox/20261116-175512-suggestion-seguimiento-de-ir13-cerrado-en-ce66f69e-2421ca29-agents-md-25-rutea-a.md
depends_on: []
pills: []
files:
- AGENTS.md
- README.md
- .opencode/skills/use-spec2viz/SKILL.md
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
---

# AGENTS.md, README.md y la carpeta de la skill de opencode dejan de nombrar use-spec2viz y pasan a use-specir

## Rationale

_Explain why this task exists or the business driver behind it._

Seguimiento de la tarea de skills de IR13 (ce66f69e, closeout 2421ca29; nota 20261116-175512). Quedaron fuera de sus files: AGENTS.md rutea a la skill use-spec2viz y README.md cita references/spec2viz-cli.md. Ademas la carpeta .opencode/skills/use-spec2viz tiene name: use-specir en su frontmatter (lo exige specir retirement check), y opencode pide que name coincida con el nombre de la carpeta.

## Goal

_Describe the concrete result this task must produce._

AGENTS.md y README.md nombran la skill use-specir del repo IR en vez de use-spec2viz y de references/spec2viz-cli.md, y la carpeta .opencode/skills/use-spec2viz pasa a .opencode/skills/use-specir (git mv) con su SKILL.md sin cambios de contenido.

## Scope

_State what is in scope and what is out of scope._

Entra: AGENTS.md, README.md y el git mv de la carpeta de la skill de opencode. Sale: .claude/skills/deskops-workflow (ya migrada), el repo IR y menciones historicas de spec2viz (por ejemplo 'spec2viz se archiva'), que se quedan.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) grep -n spec2viz AGENTS.md README.md. 2) Cambiar cada mencion que instruye a usar use-spec2viz o references/spec2viz-cli.md por use-specir (skills/use-specir/SKILL.md del repo IR). 3) git mv .opencode/skills/use-spec2viz .opencode/skills/use-specir. 4) Correr la Validation.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && grep -rn use-spec2viz AGENTS.md README.md .opencode (sin coincidencias, rc 1)

## Done When

_Name the observable condition that makes the task complete._

grep de use-spec2viz en AGENTS.md, README.md y .opencode no da nada, la carpeta se llama use-specir y tests/test_skill_cli_drift.py pasa.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.
