---
sldb:
  by: agent
  at: '2026-11-19T19:12:58Z'
  authority: generated
  via: save_document_payload
id: task-agents-md-readme-md-y-la-carpeta-de-la-skill-de-opencode-dejan-de-nombrar-use-spec2viz-y-pasan-a-use
status: active
summary: ''
tags:
- host:robocop2
current_node: ritual-execution
history:
- task_activates
- 'task_returns_to_execution: Tester deskops-t-a7703272a0b7 FALLA sobre eee49b89 (informe
  en runs/subagents/exec-deskops-t-a7703272a0b7-testing/). Según las resoluciones
  aceptadas, el token use-spec2viz no puede quedar en AGENTS.md, README.md ni .opencode;
  quedan tres: el título y el cuerpo de .opencode/skills/use-specir/SKILL.md y .opencode/skills/use-deskops/SKILL.md:159.
  Intento 2: quitarlos manteniendo el sentido histórico (p. ej. ''# use-specir (antes
  la skill de spec2viz de opencode)'', ''la ruta anterior de spec2viz'', ''replaces
  the retired spec2viz''), sin cambiar el resto, y verificar que ''grep -rn use-spec2viz
  AGENTS.md README.md .opencode'' sale vacío.'
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
