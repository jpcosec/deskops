Eres el tester independiente de UNA tarea del desk /mnt/ssd/proyectos/SLDB_1/deskops. Tu run_dir asignado es runs/subagents/exec-deskops-t-701c64bccb46-testing (si ya existe con su run.md, no lo reemplaces).
Notas del coordinador:
- El ejecutor dejo sus cambios SIN commitear; resumen y decisiones en runs/subagents/exec-deskops-e-7b5f40795a7e/result-summary.md. Archivos: deskops/integrate.py (nuevo), deskops/config.py, deskops/cli/registry.py, deskops/queue.py (solo el renombre de _wait_reason a wait_reason), tests/test_integrate.py (nuevo), declaraciones en tests/test_cli.py, tests/test_cli_grammar.py y tests/test_command_registry.py, goldens de ayuda y docs/operator-manual.md.
- Decisiones del ejecutor que el coordinador ACEPTA y que debes tomar como contrato: (1) como `closeout commit` borra el TaskDoc, una tarea ausente de HEAD esta cerrada si existe en HEAD un commit de asunto exacto `closeout: <id>`; (2) el commit de codigo sale de la primera entrada de 40 hexadecimales de `references` y, si no hay, del recibo aceptado `evidence-commit` de la tarea en desk/reviews; (3) la cuenta de graph missing se hace en proceso; (4) con --dry-run la linea de events.log dice `dry-run` y el comando imprime `simulado`; (5) el tope de la suite no cuenta la espera del cerrojo. Tambien: --task y --task-from-env son excluyentes y uno es obligatorio; el timeout de la suite sale como `fallo: suite: timeout tras <N> s`.
- Verifica cada punto de Validation y Done When. Ademas de correr los tests, arma tu mismo bajo /dev/shm un repo git con un desk (deskops init), un remoto bare local y una tarea cerrada con los comandos reales, y prueba: integracion en verde, --dry-run, suite que falla, y no fast-forward. Comprueba que el remoto bare queda como corresponde y que no quedan copias temporales. Borra todo al terminar.
- SEGURIDAD: nunca hagas git push ni git fetch contra un remoto real (github) ni ejecutes `deskops integrate` sobre /mnt/ssd/proyectos/SLDB_1/deskops o /workspace/deskops. Solo repos de prueba con remoto bare local.
- Revisa que los tests no usen mocks y que el comando nunca use force en el push (busca `--force` y `-f` en deskops/integrate.py).
- Corre tambien tests/test_queue.py, tests/test_dispatch.py, tests/test_config.py, tests/test_packaging.py, los guardianes del CLI y tests/test_output_goldens.py -k help.
- Entorno: /mnt/ssd/proyectos/SLDB_1/.venv/bin/python deberia funcionar; si no, `PYTHONPATH=/workspace/deskops:/workspace/sldb/src:/workspace/sldb/.venv/lib/python3.13/site-packages /home/scion/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13 -m pytest -q -p no:cacheprovider <archivos>`. TMPDIR=/dev/shm.
- No implementes ni corrijas nada, no commitees, no edites desk/ ni .sldb/ del repo. Cambios ajenos sin commitear (message.py, tests de message, inbox y repo identity): ignoralos.
- Escribe validation.log y result-summary.md en tu run_dir con veredicto PASS o FAIL por punto y termina con `sciontool status task_completed "<veredicto>"`.

Tarea (lee el TaskDoc completo en desk/tasks/task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip.md):
Task: task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip
Title: deskops integrate corre los gates de una tarea cerrada en copia limpia y pushea codigo y tip
Status: ready_for_testing
Current node: ritual-closeout
Task type: task.code
Effective atoms:
- atom-code-changes-close-with-tests-and-commit
- atom-cli-mutation-testing-uses-sandbox-desk-roots
Lifecycle gates:
- task_completes -> complete: closed [status = "ready_for_testing"]
  blocked by: error: [rules/rule-closeout-task-code] TaskCodeDoc:task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip: Una tarea task.code se cierra con recibos evidence aceptados e intactos de tests, commit y atom o materialization (los escribe deskops closeout verify). | any(^subject: kind = "evidence" and fact = "tests" and anchor_state = "intact" and verdict = "accepted") (seen: {}) (witness: ReviewDoc:review-task-deskops-integrate-corre-los-gates-de-una-tarea-cerrada-en-copia-limpia-y-pushea-codigo-y-tip-bundle-1 {"kind":"bundle"})
