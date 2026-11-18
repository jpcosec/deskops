FILE:desk/tasks/task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent.md
---
sldb:
  by: agent
  at: '2026-11-18T05:55:15Z'
  authority: generated
  via: create_document
id: task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
pills: []
files:
- deskops/runtime/scion.py
- deskops/config.py
- deskops/cli/registry.py
- docs/operator-manual.md
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

Un grupo de comandos nuevo, deskops dispatch, con dos subcomandos, y su configuracion en el desk. Configuracion: DeskConfig gana un campo dispatch con project (proyecto scion), workspace (ruta), context_file (ruta del JSON de contexto scion), y por cada rol (executor, tester) un objeto con role (id del RoleDoc), harness, model_alias, harness_auth y env_config (ruta opcional que se pasa a scion start con --config). (1) deskops dispatch start <executor|tester> --task <id> --root . : falla con codigo 3 y mensaje si scion list del proyecto muestra un agente en phase running; calcula la identidad con scion_child_identity (intento 1, o 2 si el run_dir del intento 1 ya existe); materializa el template con las mismas funciones que usa deskops runtime template (rol, harness y alias de la configuracion, modo igual al rol, task, agent y run_dir runs/subagents/exec-<nombre> para el ejecutor y con sufijo -testing para el tester) en la carpeta de templates del proyecto scion; corre scion templates sync; escribe el encargo completo (salida de deskops show task mas el texto del TaskDoc) en el archivo prompt.md del run_dir; arma el argv con scion_start_argv usando un prompt corto que nombra la ruta absoluta de prompt.md; ejecuta scion start; imprime nombre y run_dir. (2) deskops dispatch reap --task <id> --root . : busca en scion list del proyecto los agentes cuya etiqueta deskops.task_id es la de la tarea; un agente se considera terminado si su activity es completed, blocked o limits_exceeded, si su phase no es running, o si existe result-summary.md en su run_dir; a cada terminado le corre scion stop y scion delete --yes; imprime por agente nombre, rol y motivo; sale con codigo 0 si no queda ninguno vivo y con codigo 4 si alguno sigue trabajando. Las llamadas a scion pasan por una sola funcion que recibe el argv, para que los tests la reemplacen por un ejecutable scion falso puesto en el PATH que registra sus argumentos y devuelve JSON fijo.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo dispatch.py en el paquete deskops, el campo en deskops/config.py, el registro del grupo en deskops/cli/registry.py, tests nuevos, manual del operador con un ejemplo de queue_jobs que usa estos comandos. Fuera: integrar y pushear (otra tarea); declarar configuracion u hooks en desks reales; cambios en scion. Checkout principal, sin worktree ni rama, sin git add ni git commit.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_scion_runtime.py

## Done When

_Name the observable condition that makes the task complete._

Con un scion falso en el PATH y un desk desechable, dispatch start arma y ejecuta el argv esperado para ejecutor y tester y se niega si hay un agente vivo; dispatch reap detiene y borra los terminados y deja los vivos.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

