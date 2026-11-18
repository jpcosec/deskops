FILE:desk/tasks/task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip.md
---
sldb:
  by: agent
  at: '2026-11-18T11:07:01Z'
  authority: generated
  via: save_document_payload
id: task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip
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
- deskops/config.py
- deskops/cli/registry.py
- deskops/queue.py
- docs/operator-manual.md
- tests/test_cli.py
- tests/test_cli_grammar.py
- tests/test_command_registry.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
---

# deskops integrate corre los gates de una tarea cerrada en copia limpia y pushea codigo y tip

## Rationale

_Explain why this task exists or the business driver behind it._

La integracion (copia limpia, suite completa, checks del desk, push del commit de codigo y luego del tip, actualizar la instalacion de herramientas) la hace hoy a mano el integrador siguiendo la receta escrita en el archivo integrate-recipe.md de la carpeta .bootstrap del workspace. JP quiere que corra sola como trabajo de la cola del host.

## Goal

_Describe the concrete result this task must produce._

Un comando nuevo, `deskops integrate --task <id> --root .` (con `--dry-run` opcional), y su configuracion en el desk.

Configuracion. `DeskConfig` (`deskops/config.py`) gana un campo `integrate` con: `remote_url` (URL o ruta del remoto), `branch` (rama remota), `suite` (lista argv de la suite completa), `suite_timeout` (segundos, por defecto 5400), `tests_lock` (ruta de un archivo de cerrojo; opcional), `tools_checkout` (ruta de un checkout de herramientas; opcional) y `push_env` (mapa de variables de entorno para los comandos git de push; opcional). Sin campo `integrate` el comando sale con codigo 2 y el mensaje `falta el campo integrate en desk/config.json`.

Entrada. La tarea debe estar cerrada: su ultima entrada de history es el registro de cierre. El tip es el commit de cierre de la tarea, que se busca con `git log` por el asunto exacto `closeout: <id de la tarea>`; el commit de codigo es el sha de 40 caracteres que aparece en `references` de la tarea. Si la tarea no esta cerrada o falta alguno de los dos commits, sale con codigo 2 y dice cual falta.

Pasos, en orden; el primero que falla detiene todo, no se pushea nada, se borra la copia y el comando sale con codigo 1 imprimiendo `fallo: <paso>: <detalle>`:
1. `memoria`: los mismos dos gates de `deskops queue run` (campos `queue_min_available_gb` y `queue_max_psi_avg60`), reutilizando la funcion que ya los calcula en el modulo de la cola.
2. `copia`: `git clone --no-hardlinks <root> <dir temporal bajo TMPDIR>`, `git checkout --detach <tip>`, `git remote set-url origin <remote_url>`, `git fetch origin <branch>`.
3. `fast-forward`: `git merge-base --is-ancestor origin/<branch> HEAD` debe salir con 0.
4. `suite`: solo si `git diff --name-only origin/<branch> HEAD` trae alguna ruta que no empieza con `desk/`, `.sldb/` ni `runs/`. Corre el argv `suite` en la copia, con `PYTHONPATH` igual a la copia, tomando antes el cerrojo exclusivo de `tests_lock` (bloqueante, `fcntl.flock`) si esta declarado, con tope `suite_timeout`; la salida va a un log. Falla si el codigo no es 0.
5. `store`: cada ruta `path:` de `.sldb/store.yaml` del tip que no empieza con `../` debe existir en el commit (`git cat-file -e HEAD:<ruta>`).
6. `graph`: la cuenta de faltantes de `deskops graph missing --root <copia>` en el tip no puede ser mayor que la misma cuenta en `origin/<branch>` (se mide en un segundo checkout temporal de esa rama).
7. `push`: `git push origin <sha de codigo>:<branch>` y despues `git push origin <tip>:<branch>`, nunca con force, con las variables de `push_env` agregadas al entorno. Con `--dry-run` no se ejecuta e imprime los dos comandos.
8. `herramientas`: si `tools_checkout` esta declarado, `git -C <tools_checkout> fetch origin` y `git -C <tools_checkout> checkout --detach origin/<branch>`. Con `--dry-run` no se ejecuta.
9. Siempre, al final: borra las copias temporales y agrega a `runs/hooks/events.log` del root la linea `<fecha UTC ISO> <id de tarea> integrate <ok|fallo:<paso>> <tip corto>`. El log de la suite queda en `runs/queue/logs/integrate-<id de tarea>.log` del root.
En exito imprime `integrado <sha de codigo corto> <tip corto> en <branch>` y sale con 0.

El manual del operador gana una seccion `Integrate` con la configuracion, los pasos y el ejemplo de `queue_jobs` `integrate: {run: [deskops, integrate, --task-from-env, --root, .]}`; para eso el comando acepta `--task-from-env`, que toma el id de `DESKOPS_TASK_ID`.

## Scope

_State what is in scope and what is out of scope._

Dentro: un modulo nuevo llamado integrate.py en el paquete deskops, el campo en `deskops/config.py`, el registro del comando en `deskops/cli/registry.py`, un archivo de tests nuevo, las declaraciones del comando en `tests/test_cli.py`, `tests/test_cli_grammar.py` y `tests/test_command_registry.py`, los goldens de ayuda, y `docs/operator-manual.md`. Fuera: declarar la configuracion en desks reales; el timer del host; reintentos o rebase automatico cuando no es fast-forward; cambios en sldb. Checkout principal, sin worktree ni rama, sin git add ni git commit. Los tests jamas tocan un remoto real: el remoto es un repositorio bare creado en `tmp_path`.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- Un archivo de tests nuevo, test_integrate.py en la carpeta tests, pasa con `TMPDIR=/dev/shm pytest -q` sobre ese archivo. Cada test arma en `tmp_path` un repo git real con un desk creado por el CLI, una tarea llevada hasta su cierre con los comandos reales (como lo hacen los tests de closeout vecinos) y un remoto bare local, y comprueba: (a) con gates en verde, el remoto queda con el commit de codigo y el tip en la rama, events.log gana la linea `ok` y el comando imprime `integrado`; (b) `--dry-run` no cambia el remoto e imprime los dos comandos de push; (c) una `suite` que sale con 1 produce `fallo: suite`, codigo 1 y remoto intacto; (d) un rango que solo toca `desk/` no corre la suite (la suite configurada es un comando que fallaria); (e) un tip que no es fast-forward de la rama remota produce `fallo: fast-forward`; (f) una ruta de `.sldb/store.yaml` ausente en el commit produce `fallo: store`; (g) tarea sin cerrar y falta del campo `integrate` salen con codigo 2; (h) tras cualquier corrida no queda ninguna copia temporal bajo TMPDIR.
- Los tests guardianes del CLI pasan con el comando nuevo declarado (`pytest -q tests/test_cli_grammar.py tests/test_command_registry.py` y `pytest -q tests/test_cli.py -k help_uses_deskops_name`) y los goldens de ayuda se regeneran conservando solo los que cambian por el comando nuevo.
- `TMPDIR=/dev/shm pytest -q tests/test_queue.py` sigue pasando.

## Done When

_Name the observable condition that makes the task complete._

Las tres validaciones pasan y el manual tiene la seccion `Integrate`.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

