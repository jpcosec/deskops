---
sldb:
  by: agent
  at: '2026-11-25T23:12:32Z'
  authority: generated
  via: save_document_payload
id: task-se-borra-el-codigo-muerto-y-cada-modulo-publico-dice-su-proposito
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-ruff-configurado-un-commit-solo-de-formato-errores-arreglados-pre-commit-y-paso-de-ruff-en-el-ci
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

# Se borra el código muerto y cada módulo público dice su propósito

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

ClosureService.close_auto (services/closure.py:720), graph/atom_trace.py y las funciones sin llamadores se borran antes de la mudanza por capas; cada módulo de deskops/ tiene un docstring de módulo que dice qué hace y quién lo usa.

## Scope

_State what is in scope and what is out of scope._

Entra: borrar lo de arriba y escribir los docstrings de módulo y de paquete, borrando de per-file-ignores en pyproject.toml las entradas D100 y D104 de deskops/ (tests/** = D se queda). Una función no tiene llamadores si vulture deskops --min-confidence 80 la marca y un grep de su nombre (como identificador o como cadena) en deskops/, tests/, pyproject.toml y en sldb, IR, UIs/graph_ui, scion y legos no encuentra usos. Módulo público: todo módulo bajo deskops/ cuyo nombre no empieza con guion bajo, más los __init__.py (D104). El docstring dice en una o dos frases qué hace y qué capa o comando lo usa. Sale: testing/foreign_suites.py (lo importan 5 tests de scion) y refactors.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) vulture y grep para la lista. 2) Borrar y correr tests/acceptance. 3) Docstrings y vaciar los per-file-ignores.

## Validation

_List the checks required before this task can close._

- ruff check deskops (D100 y D104 sin per-file-ignores)
- vulture deskops --min-confidence 80 no lista funciones sin llamadores
- python -m pytest -q tests/acceptance

## Done When

_Name the observable condition that makes the task complete._

No hay per-file-ignores de D100 ni D104 y vulture no marca funciones sin llamadores.
