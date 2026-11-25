---
sldb:
  by: agent
  at: '2026-11-25T21:13:02Z'
  authority: generated
  via: save_document_payload
id: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un
status: active
summary: ''
tags: []
current_node: ritual-testing
history:
- task_activates
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# átomos, pills y tareas guardan el dónde como punteros a un documento del store, a una categoría o a un ancla de código

## Rationale

_Explain why this task exists or the business driver behind it._

Propuesta deskops/desk/drawer/plans/que-es-un-atomo-y-que-es-una-pill/README.md (JP, 2026-11-25): "dónde debe apuntar al código, pero también a categorías como aplica a toda la UI". Hoy el dónde es texto libre en la pill (where) y una lista de rutas en la tarea (files); las categorías existen como tags en los átomos pero nada las usa para decir a qué aplica algo. deskops solo guarda los punteros: los resuelve sldb, y lo que hay que resolver lo pone specIR.

## Goal

_Describe the concrete result this task must produce._

Un mismo campo de punteros en los tres modelos, que distingue las tres clases de puntero y rechaza uno mal formado.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/models/ (atom, pill, task), deskops add y deskops edit, y la lectura de los documentos existentes sin romperlos. Fuera: resolver los punteros (tarea de sldb), migrar el contenido de los where y files actuales.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer sldb/docs/architecture/code-anchoring.md, tags.md y selectors.md para usar la forma de dirección que sldb ya tiene para cada clase de puntero; no se inventa una sintaxis. El texto libre actual se conserva como está hasta que una tarea aparte lo migre.

Aclaraciones de la revisión: Campo nuevo, opcional, por defecto [], llamado pointers, igual en AtomDoc, PillDoc y TaskDoc: lista de strings con prefijo de clase: 'doc:<Modelo>:<id>', 'tag:<tag>' y 'code:<ruta>[::<símbolo>]'. Después del prefijo, usar la forma que sldb ya tiene (leer /mnt/ssd/proyectos/SLDB_1/sldb/docs/architecture/code-anchoring.md, tags.md y selectors.md) y adaptar los prefijos a esa forma si difiere, explicándolo en result-summary. Convive con los campos de texto libre actuales (where, files), que no cambian. Uno mal formado lo rechaza la validación del modelo con un mensaje que nombra la clase esperada, y la CLI (deskops edit ... pointers) lo muestra con rc != 0. deskops show <tipo> <id> lo muestra. 'Desk sano' = deskops doctor --root . sin errores nuevos respecto de main. Va antes de la tarea de la pill (mismo models/pill.py). No poner Task-Id en el commit de código.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_where_pointers.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Un átomo, una pill y una tarea se crean con un puntero de cada clase y deskops los guarda y los muestra. Un puntero con forma inválida se rechaza nombrando la clase esperada. Los documentos existentes siguen leyéndose y el desk queda sano según deskops doctor.
