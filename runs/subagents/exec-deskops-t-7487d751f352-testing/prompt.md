Task: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un
Title: átomos, pills y tareas guardan el dónde como punteros a un documento del store, a una categoría o a un ancla de código
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un-bundle-1 {"kind":"bundle"})

---
sldb:
  by: agent
  at: '2026-11-25T23:30:15Z'
  authority: generated
  via: save_document_payload
id: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un
status: ready_for_testing
summary: ''
tags: []
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references: []
depends_on: []
pills: []
files: []
pointers: []
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
Intento 2 (el tester deskops-t-19aa7b8d6d39 dio FALLA sobre 7a9d0be0e, que ya está en main). Parte de main y agrega solo esto: (a) actualizar tests/fixtures/model_contract_hashes.json con los hashes nuevos de AtomDoc, PillDoc y TaskDoc (es el cambio deliberado de contrato que el test pide) hasta que pase tests/test_model_contract_snapshot.py; (b) regenerar los goldens con python -m pytest -q tests/test_output_goldens.py --update-golden, revisar que el diff solo agregue --pointers en la ayuda y "pointers" en las salidas, y que después pase sin la opción; (c) agregar --pointers a deskops add task, igual que en add atom y add pill; (d) en deskops/models/pointers.py aceptar el valor de un tag con ':' (tag:area:ui:graph) y el sufijo ~N de code-anchoring.md (code:src/a.py::foo~2, code:src/a.py::Clase.metodo~2), con un caso de test para cada uno en tests/test_where_pointers.py. Fuera: tests/test_scaffold_golden.py, que ya falla en el padre 6fb2245. Correr tests/test_where_pointers.py, tests/test_model_contract_snapshot.py y tests/test_output_goldens.py. Commit sin trailer Task-Id.

Intento 3 (el tester deskops-t-6f073db3f764 dio FALLA sobre 871f5f4b1, que ya está en main con 7a9d0be0e; la funcionalidad pasa). Parte de main y agrega solo esto: (a) regenerar el golden de vistas con python -m pytest -q tests/test_view_goldens.py --update-golden; el único cambio esperado es la línea pointers: [] en view_drawer, y después tiene que pasar sin la opción. (b) Actualizar el sample de tests/test_atom_materialization.py::test_atom_doc_roundtrips para que incluya pointers: [], hasta que pase. (c) Agregar pointers al __template__ de AtomAdrDoc en deskops/models/adr.py, para que deskops add atom --atom-type atom.adr --pointers guarde los punteros, con un caso en tests/test_where_pointers.py. Si eso cambia el hash de AtomAdrDoc, actualizarlo en tests/fixtures/model_contract_hashes.json. Correr tests/test_view_goldens.py, tests/test_atom_materialization.py, tests/test_where_pointers.py y tests/test_model_contract_snapshot.py. Commit sin trailer Task-Id.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_where_pointers.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Un átomo, una pill y una tarea se crean con un puntero de cada clase y deskops los guarda y los muestra. Un puntero con forma inválida se rechaza nombrando la clase esperada. Los documentos existentes siguen leyéndose y el desk queda sano según deskops doctor.

## Como probar (tester)

Ubica el trabajo del ejecutor:

    git log -1 --format=%H --grep "Task-Id: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un"   # commit del ejecutor
    git show --name-only <commit>                           # sus archivos

Los tests a correr son los archivos tests/*.py de ese commit, mas tests/test_<modulo>.py cuando exista para cada modulo de codigo tocado; de a uno, con `TMPDIR=/tmp python -m pytest -q <archivo>`. No corras la suite completa: la corre integrate en el host.

Escribe result-summary.md con el veredicto PASA o FALLA en la primera linea.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-7487d751f352"
