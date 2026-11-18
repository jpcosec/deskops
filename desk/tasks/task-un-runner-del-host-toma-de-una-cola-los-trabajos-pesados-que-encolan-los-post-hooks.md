---
sldb:
  by: agent
  at: '2026-11-18T04:47:13Z'
  authority: generated
  via: save_document_payload
id: task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
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
- deskops/config.py
- deskops/cli/registry.py
- docs/operator-manual.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-automatic-routines-vs-llm-tasks
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# Un runner del host toma de una cola los trabajos pesados que encolan los post-hooks

## Rationale

_Explain why this task exists or the business driver behind it._

Los post-hooks de una transicion corren donde corre `deskops advance task`. Cuando lo corre un ejecutor dentro de un contenedor scion, ahi no estan el cerrojo de tests de la maquina, el control de memoria ni las credenciales de push. La suite completa, la integracion y el push tienen que correr en el host, de a uno.

## Goal

_Describe the concrete result this task must produce._

Un grupo de comandos nuevo, `deskops queue`, con tres subcomandos, y su configuracion en el desk.

Configuracion. `DeskConfig` (archivo `deskops/config.py`, se lee de `desk/config.json`) gana tres campos: `queue_jobs`, un mapa de tipo de trabajo a `{"run": [lista argv], "timeout": segundos enteros mayores que cero, por defecto 3600}`; `queue_min_available_gb` (entero, por defecto 8); `queue_max_psi_avg60` (numero, por defecto 10). Por defecto `queue_jobs` es un mapa vacio.

Cola. Vive en la carpeta `runs/queue` del repo, con las subcarpetas `pending`, `running`, `done`, `failed` y `logs`, que los comandos crean si faltan. Un trabajo es un archivo JSON llamado `<AAAAMMDDTHHMMSSZ>-<tipo>-<id de tarea>.json` con las claves `id` (el nombre sin extension), `kind`, `task_id`, `transition`, `enqueued_at`. Cambiar de estado es mover el archivo de carpeta con `os.replace`.

1. `deskops queue add <tipo> --task <id> --transition <relacion> --root .` escribe el trabajo en `pending` e imprime su `id`. Si `--task` o `--transition` no vienen, se leen de las variables `DESKOPS_TASK_ID` y `DESKOPS_TRANSITION` (las que reciben los post-hooks). Un tipo que no esta en `queue_jobs` sale con codigo 2 y un mensaje que lista los tipos declarados; sin id de tarea sale con codigo 2.

2. `deskops queue run --root .` ejecuta como maximo un trabajo y sale. Pasos, en orden: (a) toma un cerrojo exclusivo no bloqueante (`fcntl.flock`) sobre el archivo `run.lock` de la carpeta de la cola; si otro proceso lo tiene, imprime `ocupado: otro queue run en curso` y sale con codigo 0 sin tocar nada; (b) si no hay pendientes imprime `sin trabajos` y sale con codigo 0; (c) lee `MemAvailable` de `/proc/meminfo` y el `avg60` de la linea `some` de `/proc/pressure/memory`; si la memoria disponible en GB es menor que `queue_min_available_gb` o el avg60 es mayor o igual que `queue_max_psi_avg60`, imprime `en espera: <motivo con los valores>` y sale con codigo 0 dejando el trabajo en `pending`; (d) toma el pendiente mas antiguo (orden por nombre), lo mueve a `running` y ejecuta el argv de su tipo con `subprocess.run`, sin shell, con la raiz del repo como directorio de trabajo y con las variables `DESKOPS_ROOT`, `DESKOPS_TASK_ID`, `DESKOPS_TRANSITION`, `DESKOPS_JOB_ID`, `DESKOPS_JOB_KIND`; la salida estandar y de error van al archivo `<id>.log` de la carpeta `logs`; (e) agrega al JSON `started_at`, `ended_at`, `exit_code` (o `timeout: true` si paso el tope) y `log`, y lo mueve a `done` si el codigo fue 0 y a `failed` en otro caso; (f) si fallo, deja una nota en el inbox del mismo desk con la misma funcion que usa `deskops message send`, tipo `unclear`, titulo `queue: <id>` y cuerpo con el tipo, la tarea, el codigo de salida y la ruta del log; `queue run` sale con codigo 1. Con `--all` repite los pasos (b) a (f) hasta que no queden pendientes o uno falle.
   Un trabajo que quedo en `running` de una corrida que murio (el cerrojo esta libre y hay archivos en `running`) se mueve a `failed` con `exit_code: null` y `interrupted: true` antes del paso (b), con su nota.

3. `deskops queue list --root . --format text|json` muestra los trabajos agrupados por estado, con id, tipo, tarea y, en los terminados, codigo de salida.

El manual del operador gana una seccion `Host queue` que explica el formato de `queue_jobs`, los tres subcomandos, los gates, y un ejemplo de post-hook que encola: `run: [deskops, queue, add, <tipo>, --root, .]`.

## Scope

_State what is in scope and what is out of scope._

Dentro: `deskops/config.py`, un modulo nuevo llamado queue.py dentro del paquete deskops, el registro del grupo `queue` en `deskops/cli/registry.py` siguiendo el patron de los grupos vecinos, un archivo de tests nuevo llamado test_queue.py en la carpeta tests, `docs/operator-manual.md`. Fuera: un servicio o timer permanente; cualquier comando que lance agentes scion, corra suites o haga push (eso es otra tarea que usa esta cola); declarar `queue_jobs` u hooks en desks reales; cambios en el repo sldb. Se trabaja en el checkout principal de deskops, sin worktree ni rama, sin `git add` ni `git commit`. Si el cambio deja codigo o tests sin ninguna referencia, se borran en la misma tarea. No se tocan archivos ya modificados por otros en el checkout (`deskops/cli/commands/message.py`, `tests/e2e_agent/scenarios/inbox-to-task.yaml`, `tests/test_inbox_promote_cli_gaps.py`, `tests/test_message_cli.py`, `tests/test_repo_identity.py`). La carpeta de la cola es salida de ejecucion: no se registra en el store.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Campos nuevos en `DeskConfig`. 2. Modulo queue.py con las funciones de encolar, correr y listar. 3. Grupo `queue` en `deskops/cli/registry.py`. 4. Tests. 5. Manual. 6. `deskops advance task` de esta tarea y aviso de termino.

## Validation

_List the checks required before this task can close._

- El archivo de tests nuevo pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Los tests usan un desk desechable bajo `tmp_path`, creado como lo hacen los tests vecinos que prueban comandos del CLI, y comandos reales en `queue_jobs` (por ejemplo `[sh, -c, ...]`), sin mocks. Cubren: (a) `queue add` de un tipo declarado crea el archivo en pending y uno no declarado sale con codigo 2; (b) `queue add` toma tarea y transicion de las variables de entorno; (c) `queue run` ejecuta el trabajo, lo deja en done con `exit_code` 0 y escribe el log con la salida del comando y las cinco variables; (d) un comando que sale con codigo distinto de 0 queda en failed, `queue run` sale con 1 y aparece una nota nueva en el inbox del desk que nombra el log; (e) un comando que supera su `timeout` queda en failed con `timeout: true`; (f) con `queue_min_available_gb` fijado en un valor imposible de cumplir, `queue run` imprime `en espera`, sale con 0 y el trabajo sigue en pending; (g) dos procesos `queue run` lanzados a la vez sobre un trabajo que duerme dos segundos: uno lo ejecuta y el otro imprime `ocupado`, y el comando corrio una sola vez; (h) `queue run --all` vacia dos pendientes en orden; (i) un archivo dejado en running sin cerrojo tomado pasa a failed con `interrupted: true`; (j) `queue list --format json` devuelve los cuatro estados.
- `TMPDIR=/dev/shm pytest -q tests/test_lifecycle_graph.py` sigue pasando.
- `deskops queue --help` y la ayuda de cada subcomando terminan con codigo 0.
- `deskops graph missing --root .` no informa ninguna referencia nueva que nombre esta tarea.

## Done When

_Name the observable condition that makes the task complete._

Las cuatro validaciones pasan, el manual tiene la seccion `Host queue` y `git status --short` no muestra archivos nuevos fuera de los nombrados en Scope.
