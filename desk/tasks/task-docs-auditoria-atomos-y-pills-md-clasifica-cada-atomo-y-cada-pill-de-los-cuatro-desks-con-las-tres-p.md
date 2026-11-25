---
sldb:
  by: agent
  at: '2026-11-25T19:13:58Z'
  authority: generated
  via: create_document
id: task-docs-auditoria-atomos-y-pills-md-clasifica-cada-atomo-y-cada-pill-de-los-cuatro-desks-con-las-tres-p
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# docs/auditoria/atomos-y-pills.md clasifica cada átomo y cada pill de los cuatro desks con las tres preguntas de la propuesta

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): "hay muchas pills mal hechas, y muchos átomos también". Hay 647 átomos y 59 pills en los desks de graph_ui, deskops, sldb e IR; 450 átomos responden cómo, qué o dónde, que son los candidatos a estar repitiendo el código o lo que specIR puede extraer. Antes de tipar nada hay que saber cuánto sobra.

## Goal

_Describe the concrete result this task must produce._

Una tabla con un veredicto por documento, para que JP decida qué se retira, qué se mueve y qué se queda.

## Scope

_State what is in scope and what is out of scope._

Dentro: leer los átomos y las pills de los cuatro desks y escribir el informe. Fuera: retirar, mover o editar cualquiera de ellos.

## Implementation Path

_Outline the expected implementation route or affected surface._

Las tres preguntas, en orden: si se puede leer del código o de su docstring; si lo puede extraer specIR; si seguiría valiendo sin el trabajo en curso. Para la primera se abre el código al que el documento se refiere y se cita archivo y línea. No se clasifica por el título.

## Validation

_List the checks required before this task can close._

- test -f docs/auditoria/atomos-y-pills.md

## Done When

_Name the observable condition that makes the task complete._

Cada átomo y cada pill aparece una vez con uno de estos veredictos y su motivo en una línea: ya está en el código (con archivo y línea), falta en el docstring, lo extrae o lo extraería specIR, es una decisión, es un invariante, es contexto de un trabajo abierto, o no se sostiene. El informe trae los totales por desk y por veredicto, y lista aparte los que no se pudieron clasificar.
