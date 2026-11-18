---
sldb:
  by: agent
  at: '2026-11-18T10:39:48Z'
  authority: generated
  via: save_document_payload
id: task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references: []
depends_on:
- task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
pills: []
files:
- deskops/runtime/scion.py
- deskops/config.py
- deskops/cli/registry.py
- docs/operator-manual.md
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops dispatch lanza y recoge por scion al ejecutor y al tester de una tarea sin coordinador agente

## Rationale

_Explain why this task exists or the business driver behind it._

JP quiere que los agentes se lancen solos. Hoy un coordinador agente arma a mano la identidad, el template, el prompt y el scion start de cada ejecutor y tester, y despues detiene y borra el agente. Todo eso es determinista y ya existe como funciones en deskops/runtime/scion.py; falta el comando que las encadena para que la cola del host (deskops queue) lo invoque como trabajo.

## Goal

_Describe the concrete result this task must produce._

Un grupo de comandos nuevo, `deskops dispatch`, con dos subcomandos, y su configuracion en el desk.

Configuracion. `DeskConfig` (`deskops/config.py`) gana un campo `dispatch` con: `project` (proyecto scion), `workspace` (ruta absoluta), `templates_dir` (carpeta de templates del proyecto scion), `context_file` (ruta del JSON de contexto scion) y un mapa `roles` con las claves `executor` y `tester`, cada una con `role` (id o nombre del RoleDoc), `harness`, `model_alias`, `harness_auth` (opcional) y `env_config` (ruta opcional que se pasa a scion start con `--config`). Sin campo `dispatch` los dos subcomandos salen con codigo 2 y un mensaje.

(1) `deskops dispatch start <executor|tester> --task <id> --root .` hace, en orden:
  a. Corre `scion list --project <project> --format json`; si algun agente tiene `phase` igual a `running`, imprime `ocupado: <nombre>` y sale con codigo 3.
  b. Calcula la identidad con `scion_child_identity(<ruta del TaskDoc>, <rol>, 1)`. El run_dir es `runs/subagents/exec-<nombre del agente>` para el ejecutor y `runs/subagents/exec-<nombre del agente>-testing` para el tester (el sufijo va solo en el run_dir, no en el nombre). Si ese run_dir ya existe usa el intento 2; si el del intento 2 tambien existe, sale con codigo 5 y el mensaje `sin intentos: <tarea> <rol>`.
  c. Escribe el template con `materialize_scion_template` (la funcion de `deskops/runtime/scion.py` que usa `deskops runtime template`) con el rol, el harness, el alias y el harness_auth de la configuracion, `mode` igual a `executor` o `tester` segun el subcomando, el context_file, la tarea, el nombre del agente y el run_dir, en la carpeta `<templates_dir>/<nombre del rol>`. Esa llamada tambien escribe el RunDoc.
  d. Corre `scion templates sync <nombre del rol> --project <project>`.
  e. Escribe en `<run_dir>/prompt.md` la salida de `deskops show task <id>` seguida del archivo Markdown completo del TaskDoc.
  f. Arma el argv con `scion_start_argv` (prompt: una linea que nombra la ruta absoluta de prompt.md y pide leerlo completo y cumplirlo; project, workspace, template igual al nombre del rol, harness_auth de la configuracion) y agrega `--config <env_config>` si esta declarado. Lo ejecuta.
  g. Imprime `agente <nombre> run_dir <run_dir>` y sale con el codigo de scion start.

(2) `deskops dispatch reap --task <id> --root .`: de `scion list --project <project> --format json` toma los agentes cuyo `labels["deskops.task_id"]` es igual al valor que `scion_child_identity` pone en esa etiqueta para la tarea. Para cada uno decide, en este orden de prioridad, el motivo de termino: `phase` distinta de `running` (motivo `phase:<valor>`); `activity` igual a `completed`, `blocked` o `limits_exceeded` (motivo `activity:<valor>`); existe `result-summary.md` en su run_dir, que se deduce del nombre y del rol como en (1)b (motivo `result-summary`). A cada terminado le corre `scion stop <nombre> --project <project>` y `scion delete <nombre> --project <project> --yes`. Imprime una linea por agente: `<nombre> <rol> <motivo>` o `<nombre> <rol> vivo`. Sale con codigo 0 si no queda ninguno vivo y con codigo 4 si alguno sigue vivo.

Todas las llamadas a scion pasan por una sola funcion del modulo que recibe el argv y usa `subprocess.run`. Los tests no la reemplazan en Python: ponen primero en el PATH un ejecutable llamado scion, escrito por el test, que guarda cada argv recibido en un archivo y contesta `scion list` con un JSON que el test controla.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo llamado dispatch.py en el paquete deskops, el campo en `deskops/config.py`, el registro del grupo en `deskops/cli/registry.py`, el archivo de tests nuevo, las declaraciones del grupo en `tests/test_cli.py`, `tests/test_cli_grammar.py` y `tests/test_command_registry.py`, los goldens de ayuda, y `docs/operator-manual.md` con un ejemplo de `queue_jobs` que usa estos comandos. Fuera: integrar y pushear (otra tarea); declarar configuracion u hooks en desks reales; cambios en scion. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Un archivo de tests nuevo, test_dispatch.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Con el scion de prueba en el PATH y un desk desechable de `tmp_path` con roles y una tarea creados por el CLI, comprueba: (a) `dispatch start executor` ejecuta `templates sync` y `start` con el argv esperado (nombre, tipo, proyecto, workspace, etiquetas, `--config`), deja el template, el RunDoc y prompt.md; (b) lo mismo para tester con su run_dir terminado en `-testing`; (c) con un agente en phase running sale con 3 y no ejecuta start; (d) el segundo start de la misma tarea y rol usa el intento 2 y el tercero sale con 5; (e) `dispatch reap` detiene y borra por cada uno de los tres motivos, deja vivo al que sigue trabajando y sale con 4; (f) sin campo `dispatch` en la configuracion los dos subcomandos salen con 2.
- `TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py` sigue pasando.
- Los tests guardianes del CLI pasan con el grupo nuevo declarado: `pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`; los goldens de ayuda se regeneran con `pytest -n 4 tests/test_output_goldens.py -k help --update-golden` conservando solo los que cambian por el grupo nuevo.

## Done When

_Name the observable condition that makes the task complete._

Con un scion falso en el PATH y un desk desechable, dispatch start arma y ejecuta el argv esperado para ejecutor y tester y se niega si hay un agente vivo; dispatch reap detiene y borra los terminados y deja los vivos.
