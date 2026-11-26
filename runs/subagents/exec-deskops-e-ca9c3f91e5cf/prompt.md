Task: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un
Title: átomos, pills y tareas guardan el dónde como punteros a un documento del store, a una categoría o a un ancla de código
Status: active
Current node: ritual-testing
Task type: task.code
Lifecycle gates:
- task_hands_to_closeout -> ritual-closeout: open [nonempty(validation)]
  post-hook evento-para-el-coordinador: sh -c mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID" "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
  post-hook encola-reap-del-tester: deskops queue add dispatch-reap --root .

---
sldb:
  by: agent
  at: '2026-11-25T22:14:32Z'
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

Intento 2 (el tester deskops-t-19aa7b8d6d39 dio FALLA sobre 7a9d0be0e, que ya está en main). Parte de main y agrega solo esto: (a) actualizar tests/fixtures/model_contract_hashes.json con los hashes nuevos de AtomDoc, PillDoc y TaskDoc (es el cambio deliberado de contrato que el test pide) hasta que pase tests/test_model_contract_snapshot.py; (b) regenerar los goldens con python -m pytest -q tests/test_output_goldens.py --update-golden, revisar que el diff solo agregue --pointers en la ayuda y "pointers" en las salidas, y que después pase sin la opción; (c) agregar --pointers a deskops add task, igual que en add atom y add pill; (d) en deskops/models/pointers.py aceptar el valor de un tag con ':' (tag:area:ui:graph) y el sufijo ~N de code-anchoring.md (code:src/a.py::foo~2, code:src/a.py::Clase.metodo~2), con un caso de test para cada uno en tests/test_where_pointers.py. Fuera: tests/test_scaffold_golden.py, que ya falla en el padre 6fb2245. Correr tests/test_where_pointers.py, tests/test_model_contract_snapshot.py y tests/test_output_goldens.py. Commit sin trailer Task-Id.

## Validation

_List the checks required before this task can close._

- python -m pytest -q tests/test_where_pointers.py
- python -m pytest -q

## Done When

_Name the observable condition that makes the task complete._

Un átomo, una pill y una tarea se crean con un puntero de cada clase y deskops los guarda y los muestra. Un puntero con forma inválida se rechaza nombrando la clase esperada. Los documentos existentes siguen leyéndose y el desk queda sano según deskops doctor.

## Entrega del ejecutor

Al terminar, commitea solo los archivos que cambiaste para la tarea, nombrados uno por uno (los mismos que listas en result-summary.md):

    git add <ruta> <ruta> ...
    git commit -m "<resumen>" -m "Task-Id: task-atomos-pills-y-tareas-guardan-el-donde-como-punteros-a-un-documento-del-store-a-una-categoria-o-a-un"

Nunca uses `git add -A`, `git add -u` sobre todo el arbol ni `git stash`: puede haber trabajo ajeno sin commitear. No hagas push. Recien despues ejecuta `deskops advance task`.

## Temporales de pytest

Antes de cualquier pytest exporta, para que sus temporales caigan en el /tmp del contenedor (muere con el agente) y no en el /dev/shm del host:

    export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-e-ca9c3f91e5cf"

## Tu worktree

Tu codigo vive en un worktree propio, en la rama `deskops/deskops-e-ca9c3f91e5cf`:

    /mnt/ssd/proyectos/SLDB_1/deskops/.worktrees/deskops-e-ca9c3f91e5cf

Haz `cd` ahi: edita, corre los tests y commitea ahi (git add / git commit), no en el checkout principal /mnt/ssd/proyectos/SLDB_1/deskops. Las operaciones de desk (`deskops ... --root /mnt/ssd/proyectos/SLDB_1/deskops`, evidencia en runs/subagents/..., `deskops advance task`) siguen usando el checkout principal. Al terminar, reap trae tus commits a la rama principal y borra el worktree.
