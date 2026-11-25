---
sldb:
  by: agent
  at: '2026-11-25T22:52:11Z'
  authority: generated
  via: save_document_payload
id: task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-el-ci-de-deskops-vuelve-a-verde-y-baja-de-1h30-a-menos-de-20-minutos
pills: []
files:
- pyproject.toml
- .pre-commit-config.yaml
- .git-blame-ignore-revs
- .github/workflows/tests.yml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# ruff configurado, un commit solo de formato, errores arreglados, pre-commit y paso de ruff en el CI

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

deskops tiene lint y formato obligatorios: [tool.ruff] en pyproject.toml, el código formateado, ruff check limpio, pre-commit y un paso en el CI que falla si ruff falla.

## Scope

_State what is in scope and what is out of scope._

Entra: configuración (line-length 120, py312, E F I UP B más complejidad C901 y docstrings D1 en módulos públicos), un commit solo de formato en .git-blame-ignore-revs, arreglos, .pre-commit-config.yaml y el paso del CI. Sale: refactors de lógica.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Configuración. 2) Commit de formato. 3) ruff check --fix y arreglos a mano. 4) pre-commit y CI.

## Validation

_List the checks required before this task can close._

- ruff check deskops tests
- ruff format --check deskops tests
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

ruff check y ruff format --check salen limpios y el CI los corre.
