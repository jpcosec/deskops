# Encargo del tester deskops-t-69899116f4ae (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos` (task.debug). Contrato: `deskops show task <id> --root .`; precisiones en el motivo del recibo preflight-3 y DECISIONES del coordinador en el motivo del recibo reproduction-1 (desk/reviews/task-valores-con-llaves-rompen-edit-task-message-send-y-closeout-reason-y-closeout-verify-escribe-recibos/): (a) solo texto (verify escribe recibos por diseño; su ayuda lo dice), (b) la línea de éxito no pasa el reason por format y closeout commit incluye desk/reviews/<tarea>/ en su commit de cierre, (c) origen sldb: nota a sldb y xfail(strict=True).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py, deskops/cli/registry.py, tests/test_closeout.py, tests/test_message_cli.py, tests/test_command_registry.py y los goldens de ayuda deskops_closeout.txt y deskops_closeout_verify.txt, más su evidencia en runs/subagents/exec-deskops-e-a9bb6500e6e2/ (result-summary.md con FASE 1 y FASE 2, validation.log) y runs/subagents/repro-llaves-20261117/.

1. Lee el diff contra las decisiones. Juzga en particular: marcar closeout verify como mutates=True en el registro (¿es correcto que verify se declare como comando que escribe?, ¿cambia algún comportamiento más allá de la declaración?); que el cierre commitee todo desk/reviews/<tarea>/ también en supersede/resolved-by/retire.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout (`cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_closeout.py, test_message_cli.py, test_command_registry.py, test_closeout_evidence_receipts.py, test_cli_grammar.py. test_output_goldens.py tarda mucho con la máquina cargada: córrelo solo si la carga lo permite (si no, di que no lo corriste).
3. Reproducción: los tests nuevos de (b) fallan con closure.py de HEAD (copia en /dev/shm).
4. Confirma que la nota a sldb existe en /mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/ (solo lectura) y que el reason del xfail es su nombre.
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-69899116f4ae/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-69899116f4ae/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
