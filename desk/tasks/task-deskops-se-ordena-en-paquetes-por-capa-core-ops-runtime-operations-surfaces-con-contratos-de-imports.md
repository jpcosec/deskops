---
sldb:
  by: agent
  at: '2026-11-25T22:53:31Z'
  authority: generated
  via: save_document_payload
id: task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- desk/drawer/plans/deskops-plugin-de-sldb/capas.md
depends_on:
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
- task-se-borra-el-codigo-muerto-y-cada-modulo-publico-dice-su-proposito
- task-se-retira-deskops-atoms-split
- task-cada-capacidad-del-cli-de-deskops-tiene-un-test-de-aceptacion-de-caja-negra-antes-de-mover-codigo
pills: []
files:
- deskops/
- pyproject.toml
task_type: task.refactor
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops se ordena en paquetes por capa (core, ops, runtime, operations, surfaces) con contratos de imports

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

El código de deskops/ vive en cinco paquetes por capa y import-linter impide que core importe git, scion o superficies, y que surfaces llame a otra cosa que operations.

## Scope

_State what is in scope and what is out of scope._

Entra: mover módulos a deskops/core, ops, runtime, operations y surfaces según desk/drawer/plans/deskops-plugin-de-sldb/capas.md, partir closure.py, dispatch.py y review.py por funciones como dice ese mapa, configuración de import-linter con los tres contratos y ajustar imports. Sale: cambiar comportamiento o reescribir lógica (eso es de E2 y E3).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Mover por paquete con git mv según capas.md, un commit por paquete. 2) Partir los tres módulos mixtos. 3) Contratos de import-linter en pyproject.toml. 4) tests/acceptance en verde después de cada commit.

## Validation

_List the checks required before this task can close._

- lint-imports
- python -m pytest -q tests/acceptance
- todo módulo de deskops/ está en una de las cinco capas

## Done When

_Name the observable condition that makes the task complete._

Todo módulo de deskops/ está en una de las cinco capas y lint-imports pasa.
