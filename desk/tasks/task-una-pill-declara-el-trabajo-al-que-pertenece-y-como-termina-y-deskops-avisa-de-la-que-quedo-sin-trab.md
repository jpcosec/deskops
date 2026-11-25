---
sldb:
  by: agent
  at: '2026-11-25T19:27:50Z'
  authority: generated
  via: save_document_payload
id: task-una-pill-declara-el-trabajo-al-que-pertenece-y-como-termina-y-deskops-avisa-de-la-que-quedo-sin-trab
status: draft
summary: ''
tags: []
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# una pill declara el trabajo al que pertenece y cómo termina, y deskops avisa de la que quedó sin trabajo abierto

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): una pill es el contexto de un trabajo concreto y termina con él: pasa al código o a su docstring, se destila a un átomo, o se borra. Hoy una pill carga las seis preguntas como secciones, su estado solo conoce active, y nada avisa cuando el trabajo cerró y la pill sigue ahí. Hay pills permanentes y globales, que por definición no son pills.

## Goal

_Describe the concrete result this task must produce._

Que el modelo de pill lleve el trabajo al que pertenece y su salida, con los cuatro tipos de la propuesta (pointer, question, constraint, finding) como subclases, y que la revisión del desk señale las huérfanas.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/models/pill.py y los subtipos, deskops add pill, deskops doctor, el ritual de cierre. Fuera: retirar o reescribir las pills existentes (lo decide JP con el informe de clasificación), generar pills desde specIR.

## Implementation Path

_Outline the expected implementation route or affected surface._

Mismo mecanismo que los tipos de tarea (deskops/models/task_types.py): un tipo es una subclase que solo agrega y sus compuertas son RuleDoc sembradas. La pill base no pierde campos en esta tarea, para que las existentes sigan leyéndose.

Aclaraciones de la revisión: Va después de la tarea de punteros (mismo models/pill.py): parte de main cuando esa esté integrada. Trabajo: campo work = id de la tarea abierta (task-...) o ruta del plan de drawer, uno solo. Salida: campo exit con valores code, atom, delete. Tipos: PillPointerDoc, PillQuestionDoc, PillConstraintDoc, PillFindingDoc como subclases de PillDoc, modelados como los tipos de tarea (deskops/models/task_types.py); pointer exige pointers no vacío y nada de texto de regla; question exige una pregunta (termina en ?); constraint exige un enunciado y su porqué; finding exige evidencia archivo:línea. CLI: deskops add pill --type <pointer|question|constraint|finding> --work <id> ...; sin --work, rc != 0. Cierre: 'deskops closeout verify' emite un aviso (no bloquea) por cada pill cuyo work es la tarea que cierra. Revisión del desk = deskops doctor: lista las pills cuyo work no es una tarea abierta (sin tarea o todas cerradas). No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_pill_types.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

deskops add pill acepta el tipo y exige el trabajo al que pertenece. Cerrar la última tarea de una pill sin haber declarado su salida lo informa el cierre. deskops doctor lista las pills sin ninguna tarea abierta. Cada tipo rechaza lo que no le corresponde (una pointer con razonamiento propio, una question sin quién decide).
