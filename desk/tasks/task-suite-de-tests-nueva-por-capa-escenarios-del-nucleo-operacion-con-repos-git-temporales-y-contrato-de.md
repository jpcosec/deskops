---
sldb:
  by: agent
  at: '2026-11-25T23:13:46Z'
  authority: generated
  via: save_document_payload
id: task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-deskops-se-ordena-en-paquetes-por-capa-core-ops-runtime-operations-surfaces-con-contratos-de-imports
pills: []
files:
- tests/README.md
- tests/conftest.py
- tests/core/
- tests/ops/
- tests/surfaces/
- tests/fixtures/golden/help/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Suite de tests nueva por capa: escenarios del núcleo, operación con repos git temporales y contrato de superficies

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

Existe la estructura tests/core, tests/ops y tests/surfaces con sus fixtures y su convención: el núcleo se prueba con escenarios contra las reglas sin subprocesos, la operación contra repos git temporales; tests/surfaces queda con su README y se llena en E2 (CLI y MCP llegan a la misma operación).

## Scope

_State what is in scope and what is out of scope._

Entra: tests/conftest.py con tres fixtures: desk (deskops init en tmp_path y una tarea creada con deskops add task --task-type code con título, goal, scope y validation mínimos), git_repo (git init, usuario de prueba y un commit inicial en main) y no_subprocess (monkeypatch de subprocess.run, Popen y check_output que falla; autouse en tests/core/conftest.py); un test de ejemplo en core (una tarea avanza por sus aristas y la regla rechaza el salto a cierre) y en ops (init deja un store que sldb stores check acepta); tests/surfaces solo con su README (se llena en E2); la convención en tests/README.md; borrar tests/fixtures/golden/help/ y test_help_goldens de tests/test_output_goldens.py (los otros goldens del archivo se quedan hasta el retiro de la suite vieja). Sale: el servidor MCP en proceso y los tests de superficies (E2), y escribir los tests de cada tarea (E2 y E3 traen los suyos).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Fixtures. 2) Ejemplo por capa. 3) README. 4) Borrar los goldens de help.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core tests/ops
- tests/fixtures/golden/help no existe

## Done When

_Name the observable condition that makes the task complete._

La estructura y las fixtures existen, hay un test de ejemplo por capa y no quedan goldens de --help.
