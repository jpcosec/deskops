FILE:desk/tasks/task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13.md
---
sldb:
  by: agent
  at: '2026-11-16T04:02:58Z'
  authority: generated
  via: create_document
id: task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-224757-suggestion-ir13-pide-migrar-las-habilidades-y-el-script-de-deskops-de-spec2viz-a-specir.md
depends_on: []
pills: []
files:
- .claude/skills/deskops-workflow/SKILL.md
- .claude/skills/deskops-workflow/references/spec2viz-cli.md
- .opencode/skills/use-spec2viz/SKILL.md
- .opencode/skills/use-deskops/SKILL.md
- desk/drawer/plans/workspace-documental/render_diagram.py
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Las skills y el script de diagramas de deskops dejan de invocar spec2viz y usan specir (IR13)

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR (2026-11-15): el gate de retiro de spec2viz (IR13, G4) exige migrar las dependencias de deskops. `specir retirement check` (repo IR, solo lectura) lista en deskops la skill deskops-workflow, su referencia del CLI de spec2viz, la skill use-spec2viz de opencode y el script render_diagram.py del plan workspace-documental. El punto 3 de la nota (FileRule de specs en deskops/graph/desk_graph.py:75) lo cubre otra tarea: task-la-regla-de-desk-graph-sobre-specs-deja-de-nombrar-spec2viz-...

## Goal

_Describe the concrete result this task must produce._

Nada versionado en deskops instruye a invocar spec2viz salvo la regla de desk_graph.py que cubre la otra tarea. Correspondencia (IR/docs/spec2viz/correspondencia-cli.md): spec2viz diagram render -> specir diagram render; spec2viz diagram validate -> specir diagram validate; spec2viz catalog build -> specir catalog build; catalog sync/validate -> sldb notations sync --catalog [--check]; catalog serve -> sldb serve; diagram generate/from-graph -> sldb notations from-graph. Al cerrar se responde a IR con el hash del commit.

## Scope

_State what is in scope and what is out of scope._

Entra: .claude/skills/deskops-workflow/SKILL.md (menciones de spec2viz), .claude/skills/deskops-workflow/references/spec2viz-cli.md (se reemplaza por una remision a la skill skills/use-specir/SKILL.md del repo IR), .opencode/skills/use-spec2viz/SKILL.md (se borra o queda como remision a use-specir), .opencode/skills/use-deskops/SKILL.md, y desk/drawer/plans/workspace-documental/render_diagram.py lineas 7 y 9 si el plan sigue existiendo (si JP lo retiro, no hay nada que hacer ahi). No entra: deskops/graph/desk_graph.py, los .pi/skills (no versionados), el repo IR.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) `grep -rn spec2viz .claude .opencode desk/drawer/plans/workspace-documental/render_diagram.py`. 2) Reescribir cada mencion con la tabla del goal. 3) Correr el comprobador de IR. 4) Correr los tests de skills. 5) `deskops message send --to IR --title 'IR13: deskops migrado' "commit <hash>" --root .`

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/IR && .venv/bin/specir retirement check --path deskops=/mnt/ssd/proyectos/SLDB_1/deskops (no lista nada de deskops salvo deskops/graph/desk_graph.py:75)
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_skill_cli_drift.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_skill_links.py

## Done When

_Name the observable condition that makes the task complete._

El comprobador de IR solo lista desk_graph.py:75; los dos tests pasan; la nota de respuesta a IR esta enviada con el hash.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-las-skills-y-el-script-de-diagramas-de-deskops-dejan-de-invocar-spec2viz-y-usan-specir-ir13: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

