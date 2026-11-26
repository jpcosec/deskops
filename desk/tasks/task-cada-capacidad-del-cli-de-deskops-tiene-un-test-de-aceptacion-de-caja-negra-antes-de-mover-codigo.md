---
sldb:
  by: agent
  at: '2026-11-25T23:12:56Z'
  authority: generated
  via: save_document_payload
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

tests/acceptance/ tiene un test por capacidad del CLI que corre deskops como subproceso contra un desk temporal con git y comprueba el efecto (documentos en el store, archivos, commits), no el texto de salida; esta tarea crea desk/drawer/plans/deskops-plugin-de-sldb/capacidades.md con una fila por capacidad: verbo, efecto observable y test.

## Scope

_State what is in scope and what is out of scope._

Entra: una fila por verbo de cli/registry.py salvo atoms split; la lista mínima es add, edit, advance y next de una tarea; closeout en sus cinco modos, una fila y un test por modo (commit, verify, supersede, resolved-by, retire); bind de pill; add, merge, delete y validate de átomos; drawer e inbox; message send, list y ack; review preflight, node y dispose; doctor; init y bootstrap; dispatch prompt; integrate; view. Los tests llaman a [sys.executable, '-m', 'deskops'] con cwd en el desk temporal y HOME en tmp_path, y asertan sobre sldb find --format json, los archivos y git log --format=%B. Sale: tests de implementación, goldens de salida, atoms split (se retira). Un bug que aparezca no se arregla aquí: su test lleva pytest.mark.xfail(strict=True, reason='<id>: <qué falla>'), con el id del hallazgo de diagnostico.md (W3, N1...) o uno nuevo CAP-n anotado en la fila de capacidades.md; un xfail estricto cuenta como pasar.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Inventario desde cli/registry.py en capacidades.md. 2) Fixture en tests/acceptance/conftest.py: git init con usuario y commit inicial, y deskops init en tmp_path. 3) Un test por fila. 4) Un paso separado pytest -q tests/acceptance en el job de tests de .github/workflows/tests.yml, antes del paso de la suite completa (que excluye tests/acceptance con --ignore).

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/acceptance
- cada fila de desk/drawer/plans/deskops-plugin-de-sldb/capacidades.md nombra un test que existe

## Done When

_Name the observable condition that makes the task complete._

Toda capacidad del inventario tiene su test y pasa en main.
