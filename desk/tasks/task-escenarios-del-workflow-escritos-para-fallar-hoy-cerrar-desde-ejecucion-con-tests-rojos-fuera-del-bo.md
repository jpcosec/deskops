---
sldb:
  by: agent
  at: '2026-11-25T23:13:39Z'
  authority: generated
  via: save_document_payload
id: task-escenarios-del-workflow-escritos-para-fallar-hoy-cerrar-desde-ejecucion-con-tests-rojos-fuera-del-bo
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references:
- desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md
depends_on:
- task-suite-de-tests-nueva-por-capa-escenarios-del-nucleo-operacion-con-repos-git-temporales-y-contrato-de
pills: []
files:
- tests/core/
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Escenarios del workflow escritos para fallar hoy: cerrar desde ejecución, con tests rojos, fuera del Board, sin tipo, con recibo humano o autoaprobado

## Rationale

_Explain why this task exists or the business driver behind it._

Sale del diagnóstico de deskops del 25-11 (desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md), ordenado en capas núcleo, operación y uso.

## Goal

_Describe the concrete result this task must produce._

tests/core/test_escenarios.py tiene un escenario por hallazgo del núcleo de diagnostico.md que aserta el comportamiento correcto (el workflow bloquea) y hoy falla: W3 (closeout commit de una tarea en ritual-execution se rechaza), N3 (closeout commit con la validación de la tarea en rojo se rechaza), W4/N10 (una tarea fuera del Board no se activa ni cierra sin compuertas), N1 (una tarea sin task_type no cierra con commit si verify falla) y N9 (review record con engine human no cumple el gate de revisión en frío).

## Scope

_State what is in scope and what is out of scope._

Entra: cinco escenarios sobre las fixtures desk y no_subprocess de tests/conftest.py, cada uno con pytest.mark.xfail(strict=True, reason='<id del hallazgo>'). Quién quita cada xfail: W3, la tarea del cierre por arista; N3, N1, W4/N10 y N9, la tarea de compuertas como reglas. Con xfail estricto, un xpass rompe la suite: la tarea que arregla el hallazgo quita su marca en el mismo commit. Sale: arreglarlos y la variante con la compuerta apagada (la escribe la tarea de compuertas como reglas, que introduce la severidad por desk).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un escenario por hallazgo. 2) xfail estricto con el id. 3) Comprobar que cada uno falla por la razón del hallazgo y no por la fixture.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core/test_escenarios.py (todos xfail estrictos)

## Done When

_Name the observable condition that makes the task complete._

Cada hallazgo del núcleo tiene su escenario marcado xfail.
