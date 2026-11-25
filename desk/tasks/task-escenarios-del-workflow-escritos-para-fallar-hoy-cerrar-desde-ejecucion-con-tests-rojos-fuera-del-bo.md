---
sldb:
  by: agent
  at: '2026-11-25T23:08:16Z'
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

tests/core/test_escenarios.py documenta cada hallazgo del núcleo de diagnostico.md con un escenario que hoy falla: W3 (closeout commit cierra una tarea que está en ritual-execution sin tomar task_completes), N3 (closeout commit cierra con la evidencia tests aunque la validación de la tarea falle), W4/N10 (una tarea que no está en el Board se activa y cierra sin compuertas), N1 (una tarea sin task_type cierra con commit aunque verify falle) y N9 (review record con engine human cumple el gate de revisión en frío).

## Scope

_State what is in scope and what is out of scope._

Entra: un escenario por hallazgo sobre las fixtures desk y no_subprocess de la suite nueva, cada uno con pytest.mark.xfail(strict=True, reason='<id del hallazgo>'). La variante 'el workflow apaga la compuerta y deja pasar' se escribe con la severidad de la cláusula de RuleDoc del desk, que introduce la tarea de compuertas como reglas; hasta entonces también es xfail estricto con reason='W4: severidad por desk'. Mapa de quién quita cada xfail: W3, tarea del cierre por arista; N3 y N1, tarea de compuertas como reglas; W4/N10, tarea de compuertas como reglas; N9, tarea de compuertas como reglas (motor del recibo como cláusula). Sale: arreglarlos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Un escenario por hallazgo con sus dos variantes. 2) xfail estricto con el id. 3) Comprobar que cada uno falla por la razón del hallazgo y no por la fixture.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/core/test_escenarios.py (todos xfail estrictos)

## Done When

_Name the observable condition that makes the task complete._

Cada hallazgo del núcleo tiene su escenario marcado xfail.
