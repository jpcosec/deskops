Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-873e90b300b4-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear; su resumen: runs/subagents/exec-deskops-e-e54423baf717/result-summary.md (lista de archivos y decisiones). Verifica de forma independiente cada punto de Validation y Done When del TaskDoc.
- Aclaraciones aceptadas: history sigue siendo lista de cadenas y la entrada de la vuelta es `task_returns_to_execution: <texto>`; `--back` sin transicion manual sale como un avance bloqueado con el mensaje `no hay transicion de vuelta desde <nodo>`; los tres casos de uso incorrecto salen con codigo 2.
- Ademas de los tests, prueba tu mismo en un desk desechable bajo /dev/shm creado con `deskops init`: crea una tarea con el CLI, llevala a ritual-testing, devuelvela con `deskops advance task <id> --back --reason "prueba"`, mira `deskops show task` (status, nodo, history), comprueba que el avance normal desde ritual-testing sigue yendo a ritual-closeout, y corre `deskops doctor --root .` (sin deriva). Borra el desk al terminar. Si activar la tarea exige recibos de revision, dilo y usa lo que los tests del repo usan para llegar a ritual-testing.
- Busca regresiones: corre tambien tests/test_desk_sync.py y cualquier test que liste las transiciones sembradas.
- Entorno: si `python -m pytest` no funciona, usa `PYTHONPATH=/workspace/deskops:/workspace/sldb/src:$(ls -d /workspace/sldb/.venv/lib/python*/site-packages | head -1) python3 -m pytest -q -p no:cacheprovider <archivos>` desde /workspace/deskops.
- No implementes ni corrijas nada, no commitees, no edites desk/ ni .sldb/ del repo. Cambios ajenos sin commitear (message.py, tests de message, inbox y repo identity): ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution.md):
Task: task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution
Title: Un ejecutor bloqueado no puede dejar su tarea en testing y existe la vuelta de testing a execution
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-un-ejecutor-bloqueado-no-puede-dejar-su-tarea-en-testing-y-existe-la-vuelta-de-testing-a-execution-bundle-1 {"kind":"bundle"})
