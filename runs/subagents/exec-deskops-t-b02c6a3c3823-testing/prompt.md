Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-b02c6a3c3823-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear: deskops/runtime/scion.py y tests/test_scion_runtime.py. Su resumen: runs/subagents/exec-deskops-e-dbce9a3a5f2a/result-summary.md. El ejecutor no pudo correr tests en su contenedor; el coordinador los corrio en el host (40 passed). Tu verificas de forma independiente.
- Entorno: si `python -m pytest` no funciona, prueba `PYTHONPATH=/workspace/deskops:/workspace/sldb/src:$(ls -d /workspace/sldb/.venv/lib/python*/site-packages | head -1) python3 -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py` desde /workspace/deskops (o las mismas rutas bajo /mnt/ssd/proyectos/SLDB_1). Si ningun entorno funciona, verifica leyendo el codigo y generando el template con el CLI, y dilo.
- Comprueba con el CLI, en un directorio temporal bajo /dev/shm que borras despues: `deskops runtime template deskops-tester --root . --harness pi --mode tester --out <dir>` produce en scion-agent.yaml command_args con `--tools` y su valor como dos elementos; y `deskops runtime template deskops-tester --root . --harness claude --mode tester --out <dir2>` conserva la forma `opcion=valor`.
- No implementes ni corrijas nada, no commitees, no edites desk/ ni .sldb/. Hay cambios ajenos sin commitear (message.py, tests de message, inbox y repo identity): ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual.md):
Task: task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual
Title: El template scion de pi pasa tools como opcion y valor separados y no con signo igual
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-el-template-scion-de-pi-pasa-tools-como-opcion-y-valor-separados-y-no-con-signo-igual-bundle-1 {"kind":"bundle"})
