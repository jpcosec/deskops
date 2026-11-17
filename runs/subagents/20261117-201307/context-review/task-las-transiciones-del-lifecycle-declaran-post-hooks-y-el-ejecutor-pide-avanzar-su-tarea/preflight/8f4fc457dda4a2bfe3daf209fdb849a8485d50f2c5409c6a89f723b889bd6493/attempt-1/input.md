FILE:desk/tasks/task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea.md
---
sldb:
  by: agent
  at: '2026-11-17T20:13:00Z'
  authority: generated
  via: save_document_payload
id: task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- deskops/lifecycle.py
- deskops/services/tasks.py
- deskops/workflow/next_actions.py
- deskops/doctor_findings.py
- deskops/runtime/scion.py
- tests/test_lifecycle_graph.py
- tests/test_lifecycle_end_to_end.py
- tests/test_lifecycle_seed_drift.py
- tests/test_scion_runtime.py
- docs/operator-manual.md
- desk/atoms/workflow-model/atom-automatic-routines-vs-llm-tasks.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-automatic-routines-vs-llm-tasks
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Las transiciones del lifecycle declaran post-hooks y el ejecutor pide avanzar su tarea

## Rationale

_Explain why this task exists or the business driver behind it._

Hoy un coordinador que no vive dentro de scion (el de mepu) se entera de que su ejecutor termino con un bucle de shell que espera un archivo de informe, y el paso de entrega a prueba lo mueve el a mano. deskops ya tiene el lifecycle como grafo (RelationDoc con `condition` y `attributes.sets/terminal`), las reglas de transicion y `deskops advance task`. Falta que una transicion pueda disparar comandos despues de ocurrir, y que el ejecutor sea quien pide la transicion al terminar. Los coordinadores siguen existiendo y nada de lo que ya hay se reimplementa: esto solo agrega el aviso y el encadenamiento que hoy se hacen a mano.

## Goal

_Describe the concrete result this task must produce._

1. Post-hooks declarados en la transicion. Un RelationDoc del lifecycle puede llevar `attributes.hooks`: una lista ordenada de entradas con `name` (texto) y `run` (lista de argumentos, sin shell). `deskops advance task` los corre despues de persistir la transicion que tomo, en orden, con el directorio de trabajo en la raiz del desk y las variables de entorno DESKOPS_ROOT, DESKOPS_TASK_ID, DESKOPS_TRANSITION (el relation_type), DESKOPS_FROM_NODE y DESKOPS_TO_NODE. Cada hook tiene un tope de tiempo. La salida de cada hook se guarda en un log por tarea y transicion bajo el directorio de runs del desk.
2. Fallo de un hook. Si un hook sale distinto de cero o agota el tope, no se corren los siguientes, la tarea vuelve al estado exacto que tenia antes de la transicion (status, current_node e history) y `deskops advance task` termina con codigo distinto de cero imprimiendo un hallazgo de nivel error que nombra el hook, su codigo de salida y la ruta del log. Sin hooks declarados el comportamiento de `advance` no cambia en nada.
3. Los hooks son del desk. Los RelationDoc del lifecycle son semillas gestionadas del paquete; `attributes.hooks` es la unica parte que pertenece al desk: `deskops desk update --apply` la conserva al reescribir la semilla y `deskops doctor` no la reporta como deriva. Las semillas del paquete no traen hooks.
4. `deskops next` y `deskops show task` muestran los hooks de la transicion que sigue, para que quien avanza sepa que se va a ejecutar.
5. El ejecutor pide avanzar. El texto que genera `_render_agents_md` para el ejecutor pasa a indicar que, con la evidencia escrita, corre `deskops advance task` sobre su tarea antes de `sciontool status task_completed`; si `advance` queda bloqueado o un hook falla, deja el hallazgo en su resumen y senala `sciontool status blocked` con ese texto. Sigue prohibido que el ejecutor cierre la tarea, commitee o toque otras tareas. El texto del coordinador (`_render_coordinator_agents_md`) deja de avanzar el esa transicion y pasa a verificar que ocurrio.
6. El atom atom-automatic-routines-vs-llm-tasks se actualiza con el CLI: las rutinas y los hooks de la capa de primitivas siguen retirados; lo que existe ahora son post-hooks declarados en las transiciones del lifecycle, que son comandos deterministas y no tareas de un modelo.

7. Precisiones. Tope de tiempo: 300 segundos por hook; una entrada puede traer `timeout` (entero, segundos) que lo reemplaza. Log: un archivo por avance en `runs/hooks/<id de la tarea>/<relation_type>-<fecha y hora UTC compacta>.log`, con el nombre, los argumentos, el resultado y la salida estandar y de error de cada hook corrido. Vuelta atras: solo se restauran los campos de la tarea (status, current_node, history); lo que un hook haya escrito fuera de la tarea no se deshace, y el manual del operador dice que los hooks deben poder repetirse sin dano. Conservacion: al reescribir una semilla se copia la lista `attributes.hooks` completa y en el mismo orden desde la copia del desk; no hay mezcla por nombre, porque el paquete no declara hooks. Presentacion: `next` y `show task` listan los hooks de cada transicion que sale del nodo actual, bajo su relation_type; hoy sale una sola de cada ritual. Agotado el tope, el hallazgo dice `timeout tras <n> s` en el lugar del codigo de salida. Una entrada de hooks mal formada (sin `name`, sin `run`, o `run` que no es lista de textos) hace que `advance` falle antes de persistir la transicion, con un hallazgo que nombra el RelationDoc.

## Scope

_State what is in scope and what is out of scope._

Dentro: lectura de `attributes.hooks`, ejecucion y vuelta atras en el camino de `deskops advance task`; conservacion de los hooks en la actualizacion de semillas y en doctor; salida de `next` y `show task`; texto de los templates de ejecutor y coordinador; el atom; documentacion del operador. Fuera: una cola o runner en el host para hooks pesados (suite, integracion, push); un rol especialista de sldb; cambios en sldb; hooks en comandos que no sean `advance task` (closeout commit no corre hooks en esta tarea); declarar hooks concretos en el desk de deskops o de otro repositorio.

## Implementation Path

_Outline the expected implementation route or affected surface._

`deskops/lifecycle.py` ya arma cada Transition desde `edge.metadata["attributes"]`: agregar ahi el campo de hooks. La ejecucion va en el servicio que persiste el avance (`advance_task` en `deskops/services/tasks.py`), no en la funcion pura `advance`, porque necesita el estado previo para volver atras y escribir el log. La comparacion de semillas esta en `deskops/doctor_findings.py` y la reescritura en el camino de `deskops desk update --apply`. Los textos de los agentes estan en `deskops/runtime/scion.py`. Las pruebas usan un desk desechable creado con `deskops init`, con hooks que son comandos reales del sistema (uno que termina bien y escribe un archivo, uno que falla); nada de dobles ni de salidas fabricadas.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py tests/test_lifecycle_end_to_end.py tests/test_lifecycle_seed_drift.py tests/test_scion_runtime.py
- TMPDIR=/dev/shm pytest -q
- deskops graph missing --root .

## Done When

_Name the observable condition that makes the task complete._

En un desk desechable: una transicion con dos hooks los corre en orden y deja su log; con un hook que falla la tarea queda en el estado previo, `advance` sale distinto de cero y nombra hook, codigo y log; sin hooks la salida y el estado son los de hoy; `desk update --apply` conserva los hooks y doctor no alerta por ellos; `next` lista los hooks; el template del ejecutor contiene el paso de `advance` antes de `task_completed`. La suite completa de deskops pasa.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-las-transiciones-del-lifecycle-declaran-post-hooks-y-el-ejecutor-pide-avanzar-su-tarea: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

