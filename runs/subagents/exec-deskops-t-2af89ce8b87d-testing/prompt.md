Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-2af89ce8b87d-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear; resumen en runs/subagents/exec-deskops-e-cd2f053c032d/result-summary.md. Archivos: deskops/dispatch.py (nuevo), deskops/config.py, deskops/cli/registry.py, tests/test_dispatch.py (nuevo), declaraciones del grupo en tests/test_cli.py, tests/test_cli_grammar.py y tests/test_command_registry.py, goldens de ayuda y docs/operator-manual.md.
- Aclaraciones aceptadas: el nombre del agente es el `name` de scion_child_identity y el run_dir es `runs/subagents/exec-<name>` (con `-testing` solo para el tester); el rol de cada agente en reap sale de su etiqueta `deskops.role`; sin campo dispatch el mensaje es `falta el campo dispatch en desk/config.json` y el codigo 2; el prompt de arranque es la frase que nombra la ruta absoluta de prompt.md.
- Verifica cada punto de Validation y Done When. Ademas de correr los tests, prueba tu mismo los dos subcomandos en un desk desechable bajo /dev/shm (creado con `deskops init`, con roles y una tarea creados por el CLI y un campo dispatch en su desk/config.json) usando un scion DE PRUEBA escrito por ti (un script que guarda sus argumentos y contesta `list` con JSON) puesto primero en el PATH. NUNCA ejecutes el scion real ni lances agentes. Borra el desk al terminar.
- Revisa que los tests no usen mocks ni monkeypatch sobre funciones del modulo y que no afirmen contra literales que solo duplican la salida.
- Corre tambien los tests guardianes del CLI (tests/test_cli_grammar.py, tests/test_command_registry.py, tests/test_cli.py -k help_uses_deskops_name), tests/test_output_goldens.py -k help, tests/test_queue.py y tests/test_scion_runtime.py, y busca otras regresiones en tests que enumeren comandos, campos de DeskConfig o archivos del paquete (por ejemplo tests/test_packaging.py).
- Entorno: el .venv del workspace deberia funcionar en /mnt/ssd/proyectos/SLDB_1/.venv/bin/python; si no, usa `PYTHONPATH=/workspace/deskops:/workspace/sldb/src:/workspace/sldb/.venv/lib/python3.13/site-packages /home/scion/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13 -m pytest -q -p no:cacheprovider <archivos>`. TMPDIR=/dev/shm.
- No implementes ni corrijas nada, no commitees, no edites desk/ ni .sldb/ del repo. Cambios ajenos sin commitear (message.py, tests de message, inbox y repo identity): ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent.md):
Task: task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent
Title: deskops dispatch lanza y recoge por scion al ejecutor y al tester de una tarea sin coordinador agente
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-deskops-dispatch-lanza-y-recoge-por-scion-al-ejecutor-y-al-tester-de-una-tarea-sin-coordinador-agent-bundle-1 {"kind":"bundle"})
