---
sldb:
  by: agent
  at: '2026-11-21T08:40:58Z'
  authority: generated
  via: save_document_payload
id: task-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete-y-reserva-technical-failur
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- deskops/services/review.py
- docs/operator-manual.md
- tests/test_review_command.py
- f32c12b213f58fb2e4697218f5546327fc22336f
depends_on: []
pills: []
files:
- deskops/services/review.py
- docs/operator-manual.md
- tests/test_review_command.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-review-status-muestra-incomplete-para-un-recibo-dispuesto-como-incomplete
---

# review status muestra incomplete para un recibo dispuesto como incomplete y reserva technical_failure para la falla tecnica

## Rationale

_Explain why this task exists or the business driver behind it._

Nota del coordinador de UIs/sldb-ui (20261116-013120): 16 recibos bundle dispuestos con deskops review dispose --verdict incomplete muestran technical_failure en deskops review status, que en el ritual context-review significa falla de transporte o cuota. En deskops/services/review.py (~898-912) el estado cae en technical_failure para todo verdict que no sea accepted, rejected ni pending; la falla tecnica real se escribe con verdict incomplete y reason technical (~lineas 641-647).

## Goal

_Describe the concrete result this task must produce._

deskops review status muestra el estado incomplete para un recibo vigente con verdict incomplete cuya reason no es technical, y sigue mostrando technical_failure solo para verdict incomplete con reason technical (la corrida que fallo por transporte o cuota). accepted, rejected, reviewed, stale y missing no cambian. La ayuda o doc que enumere los estados incluye incomplete.

## Scope

_State what is in scope and what is out of scope._

Entra: deskops/services/review.py (calculo del estado, ~lineas 880-912), la lista de estados en la ayuda de review status si la hay (deskops/cli/registry.py) y su golden de ayuda si cambia, y un test nuevo. No entra: cambiar como se escriben los recibos.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer review.py alrededor de 640-670 y 880-912. 2) Distinguir incomplete humano de incomplete technical por el campo reason. 3) Test: un recibo dispuesto incomplete con reason "re-fundar" muestra incomplete; uno escrito por falla tecnica muestra technical_failure.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests -k review
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se corre igual en un worktree limpio de origin/main y solo se acepta si falla igual ahi, listada en la entrega)

## Done When

_Name the observable condition that makes the task complete._

Test nuevo: review status de un recibo dispuesto incomplete muestra incomplete y el de una corrida con falla tecnica muestra technical_failure.
