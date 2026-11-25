---
sldb:
  by: agent
  at: '2026-11-25T23:06:38Z'
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

El código de deskops/ vive en cinco paquetes (core, ops, runtime, operations, surfaces) según la tabla de desk/drawer/plans/deskops-plugin-de-sldb/capas.md, y import-linter hace cumplir sus tres contratos: core no importa ops, runtime, operations, surfaces ni subprocess; runtime no importa ops, operations ni surfaces, y ops no importa operations ni surfaces; surfaces importa solo operations y modelos de core.

## Scope

_State what is in scope and what is out of scope._

Entra: mover cada módulo al paquete que le asigna la sección 'Asignación por módulo' de desk/drawer/plans/deskops-plugin-de-sldb/capas.md (incluidos __main__.py y about.py, que van a surfaces/cli); partir closure.py, dispatch.py y review.py como dice su sección 'Los tres módulos que se parten'; los contratos de import-linter en pyproject.toml; actualizar el entry point de pyproject.toml y los imports internos; dejar en las rutas viejas que otros repos importan (sección 'Rutas que otros repos importan') un módulo que solo reexporta. No hay otros reexports ni compatibilidad para rutas internas. Sale: cambiar comportamiento o reescribir lógica (E2 y E3).

## Implementation Path

_Outline the expected implementation route or affected surface._

Un commit por paquete, en este orden: core, runtime, ops, operations, surfaces; cada commit deja tests/acceptance en verde. 1) git mv según la tabla. 2) En el commit de core y runtime, partir los tres módulos mixtos. 3) Reexports de las rutas usadas por otros repos. 4) Contratos de import-linter en el último commit.

## Validation

_List the checks required before this task can close._

- lint-imports
- python -m pytest -q tests/acceptance
- todo módulo de deskops/ está en una de las cinco capas

## Done When

_Name the observable condition that makes the task complete._

Todo módulo de deskops/ está en una de las cinco capas y lint-imports pasa.
