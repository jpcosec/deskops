---
sldb:
  by: agent
  at: '2026-11-25T23:12:15Z'
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

Entra: [tool.ruff] en pyproject.toml (line-length 120, target py312, select E F I UP B C901 D100 D104; per-file-ignores con tests/** = D y con los módulos de deskops/ que hoy no tienen docstring para D100 y D104, lista que vacía la tarea de código muerto), ruff agregado a [project.optional-dependencies] dev con la versión fijada (==, la última estable al ejecutar), un commit solo de ruff format y un segundo commit que agrega su SHA a .git-blame-ignore-revs, ruff check --fix y arreglos a mano que no cambian comportamiento (E402 moviendo imports; si un arreglo cambiaría lógica, '# noqa: <código>  <motivo>'), .pre-commit-config.yaml con los hooks ruff y ruff-format de astral-sh/ruff-pre-commit con rev igual a la versión fijada, y un paso en el job de tests de .github/workflows/tests.yml antes de pytest: ruff check deskops tests && ruff format --check deskops tests. Sale: refactors de lógica.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Configuración y versión fijada. 2) Commit de formato. 3) Commit con su SHA en .git-blame-ignore-revs. 4) ruff check --fix y arreglos a mano. 5) pre-commit y paso del CI.

## Validation

_List the checks required before this task can close._

- ruff check deskops tests
- ruff format --check deskops tests
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

ruff check y ruff format --check salen limpios y el CI los corre.
