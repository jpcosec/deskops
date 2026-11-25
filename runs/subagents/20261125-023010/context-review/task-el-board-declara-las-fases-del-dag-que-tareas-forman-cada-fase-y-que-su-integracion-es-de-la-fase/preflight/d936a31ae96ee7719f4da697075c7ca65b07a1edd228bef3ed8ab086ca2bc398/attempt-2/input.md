FILE:desk/tasks/task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase.md
---
sldb:
  by: agent
  at: '2026-11-25T01:27:04Z'
  authority: generated
  via: save_document_payload
id: task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/inbox/20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El Board declara las fases del DAG: que tareas forman cada fase y que su integracion es de la fase

## Rationale

_Explain why this task exists or the business driver behind it._

Nota 20261123-161332-suggestion-jp-el-lote-de-integraci-n-es-la-fase-del-dag-declarada-en-el-board-falta-en-la-herramienta-y-en-el-skill (JP 2026-11-23): el lote de integracion es la fase del DAG declarada en el Board al descomponer; ritual-phase ya lo dice, pero el Board no registra fases (solo lista rituales y pills).

## Goal

_Describe the concrete result this task must produce._

BoardDoc tiene un campo de fases: cada fase con id, lista de tareas e integracion de la fase (validacion combinada y commit de cierre de fase). El modelo valida que una tarea este en una sola fase. Solo modelo y template; CLI y vista son tareas aparte.

## Scope

_State what is in scope and what is out of scope._

deskops/models/board.py, el template del Board con el marcador de fases y su test de modelo (round-trip extract/render con dos fases). Fuera: comando de CLI (task-deskops-declara-fases-del-board-por-cli), vista (task-deskops-view-board-muestra-las-fases), integrate y skill.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo: /mnt/ssd/proyectos/SLDB_1/deskops. El template del Board NO es un archivo aparte: es el atributo __template__ de BoardDoc en deskops/models/board.py (frontmatter con marcadores rev, como 'tasks: ⸢rev•tasks⸥'). Vocabulario: desk/rituals/phase.md y desk/contexts/pill-007-phase-gated-task-flow.md (solo leer). Esquema fijo: modelo pydantic PhaseIntegration(validation: list[str] = [], closing_commit: str | None = None) y Phase(id: str, tasks: list[str], integration: PhaseIntegration = PhaseIntegration()); en BoardDoc, phases: list[Phase] = [] (default vacio: los Board existentes siguen validos sin la clave). Marcador nuevo en el frontmatter del __template__, despues de rituals: '# DAG phases: id, tasks, integration' y 'phases: ⸢rev•phases⸥'. Validador de BoardDoc: una tarea no puede aparecer dos veces, ni en dos fases ni repetida dentro de la misma fase (ValueError que nombra la tarea). Test nuevo tests/test_board_phases.py, siguiendo como tests/test_board_portable_references.py construye un BoardDoc: (a) un Board con dos fases hace round-trip render -> extract por sldb con los mismos valores; (b) tarea en dos fases falla; (c) tarea repetida en la misma fase falla; (d) un Board sin phases sigue valido. Correr solo tests/test_board_phases.py y tests/test_board_portable_references.py.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases.py tests/test_board_portable_references.py

## Done When

_Name the observable condition that makes the task complete._

tests/test_board_phases.py cubre (a) round-trip de dos fases, (b) tarea en dos fases rechazada, (c) tarea repetida en una fase rechazada y (d) Board sin phases valido; pasa junto con tests/test_board_portable_references.py.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

