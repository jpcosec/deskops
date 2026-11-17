---
sldb:
  by: agent
  at: '2026-11-17T19:13:45Z'
  authority: generated
  via: save_document_payload
id: task-deskops-run-task-recorre-una-pasada-del-ciclo-de-una-tarea-como-comando-sin-coordinador-agente
status: superseded
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history:
- superseded
references: []
depends_on: []
pills: []
files:
- deskops/workflow/run_task.py
- deskops/cli/commands/run.py
- deskops/cli/registry.py
- deskops/runtime/scion.py
- tests/test_run_task.py
- tests/test_scion_runtime.py
- tests/fixtures/scion/README.md
- docs/operator-manual.md
- desk/atoms/workflow-model/atom-scion-coordinator-progresses-authorized-work.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-automatic-routines-vs-llm-tasks
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops run task recorre una pasada del ciclo de una tarea como comando, sin coordinador-agente

## Rationale

_Explain why this task exists or the business driver behind it._

Decision de JP (2026-11-17): el ciclo de una tarea lo recorre deskops como comando y un modelo se llama solo en los pasos de juicio (reformular en la revision, adjudicar un hallazgo, implementar, testear). Hoy quien encadena los pasos es un coordinador-agente de larga vida que lee la prosa del ritual: el procedimiento que _render_coordinator_agents_md (deskops/runtime/scion.py) le escribe en agents.md, seccion "Each cycle", pasos 1 a 7. Casi todos esos pasos son deterministas (reconciliar, elegir identidad, escribir intencion, despachar, esperar, verificar, cerrar). En el piloto de IR (reports/scion-piloto-ir-20261115.md del workspace SLDB_1) el coordinador se desvio justo ahi: despacho con recibos stale y no escribio el RunDoc de intencion. Ademas un coordinador vivo todo el dia ocupa RAM en una maquina que se queda sin ella. Las piezas ya existen y son deterministas: deskops next, deskops review status, deskops advance task, deskops closeout verify, deskops closeout commit, scion_child_identity, scion_start_argv, record_scion_run y materialize_scion_template. Falta lo que las encadena.

## Goal

_Describe the concrete result this task must produce._

Existe el comando `deskops run task <task-id> --root <desk_root> --project <proyecto scion> --workspace <workspace>` con las opciones `--context-file <json>` (el mismo contexto de `deskops runtime template`), `--dry-run` y `--json`. Cada invocacion hace UNA pasada: lee el estado del desk y de scion, decide el paso que sigue, lo ejecuta si es determinista y termina; nunca se queda esperando a un hijo ni guarda estado propio fuera del desk (TaskDoc, recibos ReviewDoc, RunDoc, run_dir) y de scion (agentes por nombre y labels). Volver a invocarlo sin que nada haya cambiado no repite ningun efecto. Imprime un reporte (JSON con --json) con: task_id, state, step (el paso decidido), performed (true/false), child (nombre del agente scion, si aplica), blockers (lista) y next (que evento lo desbloquea). Codigo de salida: 0 si avanzo o si espera a un hijo o no queda nada que hacer; 2 si hace falta juicio o una decision (state needs_adjudication o blocked); 1 ante un error del propio comando.
Tabla de decision, en este orden (la primera que aplica gana). Los nodos y transiciones se leen del grafo de lifecycle del desk con las mismas funciones que usan `deskops next` y `deskops advance task`; no se copian nombres de nodos ni condiciones en el codigo nuevo.
A. La tarea no esta en el Board o ya cerro: state done, sin efecto. B. La regla de activacion bloquea (la tarea aun no se activa):
   B1. Alguna dependencia no esta cerrada: state blocked, blocker con las dependencias abiertas.
   B2. Falta el recibo preflight o bundle, o esta stale: step review; corre la misma revision que
       `deskops review preflight|bundle` (misma funcion de servicio, mismo tope de intentos); una sola revision
       por pasada, preflight antes que bundle. Si el tope de intentos ya se alcanzo: state blocked.
   B3. Hay un recibo preflight o bundle con verdict pending: state needs_adjudication, con los ids de los
       recibos y su run_dir. El comando NO dispone recibos: disponer es juicio y lo hace quien adjudica con
       `deskops review dispose` o corrigiendo la tarea con `deskops edit task`.
   B4. Un recibo rejected o incomplete sin revision nueva posible: state blocked.
   B5. Recibos aceptados e intactos y dependencias cerradas: step advance; hace lo mismo que
       `deskops advance task`.
C. La tarea esta activa y espera implementacion (carril executor):
   C1. Otro agente deskops-e-* o deskops-t-* de OTRA tarea del mismo desk esta vivo en el proyecto scion:
       state waiting, blocker "desk ocupado por <agente>". Un ejecutor o tester por repositorio a la vez.
   C2. No hay RunDoc ni agente para la identidad scion_child_identity(tarea, "executor", intento): step dispatch;
       en este orden escribe el RunDoc de intencion (record_scion_run), materializa el template con
       materialize_scion_template en <run_dir>/scion-template y lanza `scion start` con scion_start_argv.
       El prompt del hijo se arma solo con `deskops show task` y las rutas de run_dir; sin texto libre.
       Si `scion start` falla, el RunDoc de intencion queda y el fallo se reporta como blocker.
   C3. El agente existe y su activity no es completed: state waiting_child con la activity leida. Activity
       blocked, limits_exceeded, error o stalled: state blocked con ese dato (salida 2).
   C4. activity completed (activity manda; phase solo como respaldo): exige en el run_dir del ejecutor
       result-summary.md y validation.log. Si faltan: state blocked "handoff incompleto". Si estan: detiene
       al hijo (`scion stop`) y hace la transicion de lifecycle que entrega a testing.
D. La tarea espera prueba independiente (carril tester): igual que C2 a C4 con rol tester, identidad
   deskops-t-*, template de modo tester y run_dir terminado en -testing. Al completar, el veredicto se lee de
   <run_dir>-testing/result.json (ver abajo). No se interpreta prosa.
   D1. verdict fail en el intento 1: step dispatch del ejecutor intento 2 (identidad con -a2, run_dir nuevo);
       su prompt nombra la ruta del result.json y del validation.log del tester que fallo. Despues, tester -a2.
   D2. verdict fail en el intento 2: state blocked (salida 2). No existe intento 3.
   D3. verdict pass: sigue en E.
E. Cierre:
   E1. Los archivos cambiados (git status --porcelain del repo del desk) que no estan en `files` de la tarea,
       ni bajo sus run_dir, ni bajo desk/reviews/<tarea>/, ni son escrituras del propio cierre: state blocked
       con la lista (es la version mecanica de "revisar el diff"). Lo que ya estaba sucio antes del despacho
       del ejecutor (se guarda la lista en el run_dir al despachar) no cuenta.
   E2. Corre la misma verificacion que `deskops closeout verify --task <id> --run-dir <run>`. Si no esta ok o
       reporta alertas: state needs_adjudication con los hallazgos y alertas; no commitea.
   E3. Si esta ok y sin alertas: step closeout; hace lo mismo que
       `deskops closeout commit --task <id> --run-dir <run> --paths <files de la tarea + run_dirs + desk/reviews/<tarea>>`.
F. Estado de scion desconocido o no disponible (binario ausente, hub caido, JSON ilegible) cuando el paso lo
   necesita: state blocked "estado de scion no disponible"; nunca se asume ni se duplica un hijo.

`--dry-run` decide e imprime el paso sin ejecutar ningun efecto (ni revision, ni escritura, ni scion start).
Veredicto legible por maquina: _render_tester_agents_md pasa a exigir, ademas de result-summary.md, un archivo result.json en el run_dir del tester con las claves task_id, role ("tester"), verdict ("pass" o "fail") y validations (lista de objetos con command y exit_code). Un result.json ausente o invalido es state blocked.
El atom atom-scion-coordinator-progresses-authorized-work se reescribe con el CLI para decir: el ciclo de una tarea lo recorre `deskops run task` como comando determinista y sin estado propio; un modelo interviene solo en la revision de contexto, la adjudicacion de hallazgos, la implementacion y la prueba; el coordinador-agente deja de ser quien encadena los pasos. Conserva lo que sigue valiendo (identidad por contrato, RunDoc de intencion antes del start, activity antes que phase, un ejecutor por repositorio, dos intentos, nunca git add -A).

## Scope

_State what is in scope and what is out of scope._

Entra: el modulo nuevo de decision y efectos bajo deskops/workflow/, el comando nuevo bajo deskops/cli/commands/ y su registro en el CLI, el cambio de _render_tester_agents_md en deskops/runtime/scion.py, los tests nuevos, la seccion del manual de operador y la reescritura del atom. La decision es una funcion pura sobre una foto del estado (tarea, recibos, RunDocs, lista de agentes scion ya leida, archivos cambiados); los efectos van en una capa aparte y delgada que llama a las funciones existentes. No entra: recorrer el Board entero ni elegir tarea (es la tarea siguiente), el disparador (schedule de scion o timer), un agente adjudicador, llevar `pi` a la imagen del contenedor, borrar el template o el agents.md del coordinador, ni cambiar reglas de lifecycle, modelos de documento o el formato de los recibos. No se reimplementa nada que ya haga deskops o sldb: se llaman las funciones de servicio que hoy usan los comandos nombrados arriba. Si una de esas funciones no se puede llamar sin pasar por el parser del CLI, se extrae lo minimo y se deja el comando viejo llamando a lo extraido.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer deskops/runtime/scion.py completo (identidad, argv, RunDoc, templates y el procedimiento del coordinador), deskops/lifecycle.py, deskops/workflow/next_actions.py, deskops/services/review.py, deskops/services/closure.py y como deskops/cli/commands/runtime.py y deskops/cli/registry.py registran un comando. 2) Foto del estado: una estructura con lo que la decision necesita; la lectura de scion es `scion list --project <p> --format json` (campos name, labels, phase, activity) y entra a la decision ya parseada. 3) Funcion pura decide(foto) -> paso, que implementa la tabla A a F. 4) Capa de efectos, un efecto por paso, llamando a lo existente. 5) Comando `deskops run task` con --dry-run y --json. 6) result.json en el agents.md del tester. 7) Tests sobre desks sandbox reales creados con el CLI (como exige atom-cli-mutation-testing-uses-sandbox-desk-roots): una prueba por fila de la tabla que no necesita un hijo real (A, B1 a B5, E1, F) llevando el desk real a ese estado con los comandos de deskops; para las filas C y D la decision se prueba con listas de agentes capturadas del hub real de robocop2 con `scion list --format json` y guardadas como fixture con la fecha y el comando de captura en un README junto a ellas, no escritas a mano; y la fila F se prueba de verdad invocando el comando sin scion en el PATH. Sin mocks ni dobles del binario scion. 8) Manual de operador. 9) Atom con `deskops edit`.

## Validation

_List the checks required before this task can close._

- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_run_task.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_scion_runtime.py
- cd /mnt/ssd/proyectos/SLDB_1/deskops && ../.venv/bin/python -m deskops run task --help
- cd /mnt/ssd/proyectos/SLDB_1/IR && git status --porcelain > /dev/shm/run-task-ir-antes.txt && ../.venv/bin/python -m deskops run task task-ir09 --root . --project sldb-1 --workspace /mnt/ssd/proyectos/SLDB_1 --dry-run --json && git status --porcelain | diff - /dev/shm/run-task-ir-antes.txt && rm /dev/shm/run-task-ir-antes.txt
- cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm flock /dev/shm/sldb1-tests.lock ../.venv/bin/python -m pytest -n 4 -q tests (suite completa una vez antes de entregar; cada falla se compara con el mismo comando sobre origin/main y solo se acepta si falla igual ahi; la lista va en el informe)

## Done When

_Name the observable condition that makes the task complete._

`deskops run task --help` documenta estados, pasos y codigos de salida; los tests nuevos pasan y cubren cada fila de la tabla; `deskops run task <tarea real de otro desk> --dry-run --json` sobre el desk de IR (/mnt/ssd/proyectos/SLDB_1/IR, proyecto scion sldb-1) imprime el paso que corresponde al estado real de esa tarea sin modificar nada (git status de IR identico antes y despues, evidencia en el run_dir); el atom dice que el ciclo lo recorre el comando; y ninguna prueba existente de deskops cambia de resultado.
