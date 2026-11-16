---
sldb:
  by: agent
  at: '2026-11-16T04:02:14Z'
  authority: generated
  via: create_document
id: task-jp-decide-el-release-0-2-0-de-deskops-y-que-hacer-con-el-tag-v0-2-0-prematuro
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- CHANGELOG.md
- pyproject.toml
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-release-deskops-0-2-0-pendiente-hasta-que-la-suite-completa-funcione-junta.md
---

# JP decide el release 0.2.0 de deskops y que hacer con el tag v0.2.0 prematuro

## Rationale

_Explain why this task exists or the business driver behind it._

Item del drawer (2026-10-18). Regla del dueno: no hay tags, releases ni PyPI hasta que sldb, deskops, spec2viz y graph_ui funcionen juntos (d2ac42bf). Hallazgo del 2026-11-16: el tag v0.2.0 ya existe en origin y apunta a 9832bb12 (2026-10-19), mientras CHANGELOG.md sigue con '## [0.2.0] - Unreleased' (linea 90) y una seccion [Unreleased] arriba; pyproject.toml dice 0.2.0.

## Goal

_Describe the concrete result this task must produce._

JP decide: (1) si la suite ya funciona junta y se hace el release (fecha en CHANGELOG, tag apuntando a un commit verde); (2) que hacer con el tag v0.2.0 existente: dejarlo, moverlo (exige borrar el tag remoto, irreversible para quien ya lo bajo) o saltar a 0.2.1/0.3.0. Con la decision se crea la tarea de release.

## Scope

_State what is in scope and what is out of scope._

Entra: la decision. No entra: tocar tags, CHANGELOG ni pyproject.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Presentar a JP el estado del tag y del CHANGELOG. 2) Registrar el recibo owner. 3) Crear la tarea de release si corresponde.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && git ls-remote --tags origin v0.2.0

## Done When

_Name the observable condition that makes the task complete._

La decision de JP sobre el release y el tag esta registrada y, si corresponde, existe la tarea de release.
