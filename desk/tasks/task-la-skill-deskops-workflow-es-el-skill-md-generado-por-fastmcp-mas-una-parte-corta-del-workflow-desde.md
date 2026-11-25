---
sldb:
  by: agent
  at: '2026-11-25T19:48:54Z'
  authority: generated
  via: create_document
id: task-la-skill-deskops-workflow-es-el-skill-md-generado-por-fastmcp-mas-una-parte-corta-del-workflow-desde
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-cli-de-deskops-sale-de-fastmcp-generate-cli-y-el-cli-escrito-a-mano-queda-solo-para-bootstrap-e-i
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# La skill deskops-workflow es el SKILL.md generado por fastmcp más una parte corta del workflow desde átomos

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

La skill que leen los agentes se arma con el SKILL.md que genera fastmcp generate-cli (no puede divergir del CLI) más una parte escrita sobre los ritos, materializada desde átomos.

## Scope

_State what is in scope and what is out of scope._

Entra: .claude/skills/deskops-workflow y sus references. Sale: el contenido de los ritos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Generar SKILL.md. 2) Parte de workflow desde átomos. 3) Borrar references desactualizadas.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/surfaces

## Done When

_Name the observable condition that makes the task complete._

La skill no nombra comandos inexistentes y se regenera en el build.
