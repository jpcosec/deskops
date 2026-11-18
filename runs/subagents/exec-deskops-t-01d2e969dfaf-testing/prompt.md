Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-01d2e969dfaf-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear en el checkout principal; su resumen esta en runs/subagents/exec-deskops-e-86e44ee7cd8a/result-summary.md. Archivos de la tarea: deskops/config.py, deskops/queue.py (nuevo), deskops/cli/registry.py, docs/operator-manual.md, tests/test_queue.py (nuevo) y los goldens de ayuda tests/fixtures/golden/help/deskops.txt y deskops_queue*.txt.
- Aclaraciones aceptadas en la revision: --root es la raiz del repositorio; sin transicion el trabajo se encola con transition vacia; `queue run --all` sale con 1 al fallar un trabajo; la nota de un trabajo interrumpido no trae codigo ni log.
- Verifica cada punto de Validation y de Done When del TaskDoc de forma independiente. Ademas de correr los tests, prueba tu mismo el comando en un desk desechable bajo /dev/shm (creado con `deskops init`), con un `queue_jobs` real en su desk/config.json: encola, corre, falla, lista; y lanza dos `queue run` a la vez para comprobar el cerrojo. Borra ese desk al terminar.
- Revisa que los tests no usan mocks ni afirman contra literales que duplican la respuesta: deben ejecutar comandos reales.
- Si en tu entorno no existe /mnt/ssd/proyectos/SLDB_1/.venv, usa el python que tenga pytest con PYTHONPATH apuntando al repo deskops y a sldb/src, y dilo en el resumen.
- `deskops graph missing --root .` ya daba 47 faltantes de otras tareas: el criterio es que ninguno nombre esta tarea ni sus archivos.
- No implementes ni corrijas nada, no commitees, no edites archivos de desk/ ni .sldb/. Hay cambios ajenos sin commitear (deskops/cli/commands/message.py, tests de message, inbox y repo identity) y tareas nuevas en desk/tasks: ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto, borra tus temporales de /dev/shm y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks.md):
Task: task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks
Title: Un runner del host toma de una cola los trabajos pesados que encolan los post-hooks
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-automatic-routines-vs-llm-tasks
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-un-runner-del-host-toma-de-una-cola-los-trabajos-pesados-que-encolan-los-post-hooks-bundle-1 {"kind":"bundle"})
