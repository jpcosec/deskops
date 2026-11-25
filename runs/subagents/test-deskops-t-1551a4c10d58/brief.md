# Encargo del tester deskops-t-1551a4c10d58 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-se-borra-el-camino-legacy-de-deskops-message-y-el-escenario-e2e-inbox-to-task-usa-deskops-message-li`. Contrato: `deskops show task <id> --root .`. Las precisiones están en el motivo de los recibos de desk/reviews/<tarea>/.
Entrega: cambios sin commitear en deskops/cli/commands/message.py, tests/e2e_agent/scenarios/inbox-to-task.yaml, tests/test_inbox_promote_cli_gaps.py, tests/test_message_cli.py y tests/test_repo_identity.py, más la evidencia en runs/subagents/exec-deskops-e-44a082df5dbe/.

1. Lee el diff contra el contrato y las precisiones 1 a 4. Comprueba que no quede ningún camino legacy ni ninguna mención a `deskops inbox` como comando vigente en el código, los tests ni el escenario (grep).
2. Corre sin lock y de a uno, con `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q <archivo>`: tests/test_message_cli.py, tests/test_command_registry.py, tests/test_cli.py, tests/test_repo_identity.py y tests/test_inbox_promote_cli_gaps.py.
3. Reproducción: el test nuevo falla, o no prueba nada, con message.py de HEAD. Usa una copia en /dev/shm y no toques el checkout.
4. A mano: `PYTHONPATH=$PWD ../.venv/bin/python -m deskops message` da rc 2, nombra send/list/read/ack y no imprime la ayuda completa.
5. NO corras la suite completa ni `stores build --check`.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-1551a4c10d58/ y /dev/shm. Limpia SOLO lo tuyo en /dev/shm: no borres nada que empiece por dk-.

## Evidencia (en runs/subagents/test-deskops-t-1551a4c10d58/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
