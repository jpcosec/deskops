---
sldb:
  by: agent
  at: '2026-11-25T22:51:38Z'
  authority: generated
  via: create_document
id: task-cada-capacidad-del-cli-de-deskops-tiene-un-test-de-aceptacion-de-caja-negra-antes-de-mover-codigo
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
- ../AGENTS.md
depends_on:
- task-el-ci-de-deskops-vuelve-a-verde-y-baja-de-1h30-a-menos-de-20-minutos
pills: []
files:
- tests/acceptance/
- desk/drawer/plans/deskops-plugin-de-sldb/capacidades.md
- .github/workflows/tests.yml
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Cada capacidad del CLI de deskops tiene un test de aceptación de caja negra antes de mover código

## Rationale

_Explain why this task exists or the business driver behind it._

E1 a E3 mueven y borran cerca del 40 % del código, y la suite actual fija implementación (153 goldens de --help) en vez de capacidades. La regla de paridad del workspace (AGENTS.md) pide la misma capacidad con su test de aceptación, nunca el mismo código ni la salida byte a byte. Sin esta red el refactor no tiene cómo saber que no rompió nada.

## Goal

_Describe the concrete result this task must produce._

tests/acceptance/ tiene un test por capacidad del CLI que corre deskops como subproceso contra un desk temporal con git y comprueba el efecto (documentos en el store, archivos, commits), no el texto de salida; el inventario de capacidades está en desk/drawer/plans/deskops-plugin-de-sldb/capacidades.md con el test de cada una.

## Scope

_State what is in scope and what is out of scope._

Entra: el inventario (crear, editar, avanzar y cerrar una tarea con cada modo de closeout; bind de pill; add, merge, delete y validate de átomos; drawer e inbox; message send, list y ack; review node y dispose; doctor; init y bootstrap; dispatch prompt; integrate; view), la fixture de desk temporal y el paso del CI. Sale: tests de implementación, goldens de salida, atoms split (se retira) y arreglar los bugs que aparezcan (se marcan xfail con su id y los toma la tarea de escenarios o la de E3 que corresponda).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario desde cli/registry.py: verbo, efecto observable y test. 2) Fixture: git init y deskops init en tmp_path. 3) Un test por capacidad que aserta sobre sldb find, los archivos y git log. 4) Paso tests/acceptance en el CI.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/acceptance
- cada fila de desk/drawer/plans/deskops-plugin-de-sldb/capacidades.md nombra un test que existe

## Done When

_Name the observable condition that makes the task complete._

Toda capacidad del inventario tiene su test y pasa en main.
