Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-5ea818e706bb-a2-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear en el checkout principal; su resumen esta en runs/subagents/exec-deskops-e-9fc95085d5a3/result-summary.md. Los archivos de la tarea son deskops/runtime/scion.py, deskops/cli/registry.py, tests/test_scion_runtime.py, docs/operator-manual.md y desk/roles/role-sldb-store-specialist.md.
- Verifica cada punto de Validation y de Done When del TaskDoc de forma independiente. Para pytest usa: PATH=/mnt/ssd/proyectos/SLDB_1/.venv/bin:$PATH TMPDIR=/dev/shm python -m pytest -q -p no:cacheprovider tests/test_scion_runtime.py
- Comprueba ademas que el agents.md generado por `deskops runtime template sldb-store-specialist --root . --out <dir temporal bajo /dev/shm>` contiene los apartados a-f del Goal, y borra ese directorio.
- `deskops graph missing --root .` ya daba 47 faltantes de otras tareas antes de este cambio: el criterio es que ninguno nombre esta tarea ni sus archivos.
- No implementes ni corrijas nada, no commitees, no edites archivos de desk/ ni .sldb/. Hay cambios ajenos sin commitear (deskops/cli/commands/message.py, tests de message, inbox y repo identity): ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto, borra tus temporales de /dev/shm y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook.md):
Task: task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook
Title: Rol especialista de sldb que deja el store limpio, disparado por un post-hook
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-scion-coordinator-progresses-authorized-work
- atom-automatic-routines-vs-llm-tasks
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-rol-especialista-de-sldb-que-deja-el-store-limpio-disparado-por-un-post-hook-bundle-1 {"kind":"bundle"})
