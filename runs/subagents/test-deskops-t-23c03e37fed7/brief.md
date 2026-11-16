# Encargo del tester deskops-t-23c03e37fed7 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-verify-anticipa-la-evidencia-de-run-dir-que-exige-closeout-commit` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" del scope son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py, deskops/cli/commands/closeout.py, deskops/cli/registry.py, tests/fixtures/golden/help/deskops_closeout_verify.txt y tests/test_closeout_declared_evidence.py, más su evidencia en runs/subagents/exec-deskops-e-a6a9943b2333/. Hay otros cambios sin commitear en el checkout (otra tarea en curso toca tests/test_command_registry.py; .sldb; Board.md): no son de esta entrega.

1. Lee el diff de esos 5 archivos contra el goal, el scope y el done_when: closeout verify --run-dir reporta la evidencia de run-dir que falta con el mismo texto que closeout commit; sin --run-dir nada cambia; commit sigue igual. Juzga si tocar deskops/cli/registry.py (fuera de files) era necesario.
2. Corre tú, de a un archivo y sin lock, CON PYTHONPATH al checkout (el venv tiene deskops editable desde /mnt/ssd/herramientas/deskops y los tests de subproceso probarían ese otro checkout): `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>` con test_closeout_declared_evidence.py, test_closeout.py, test_output_goldens.py, test_cli_help_examples.py y test_command_registry.py (closeout verify no es un comando nuevo; si test_command_registry falla, mira si es por esta entrega o por la otra tarea en curso, la de atoms citations).
3. Reproducción: los tests nuevos fallan con el código de HEAD (copia en /dev/shm con git archive HEAD más los tests nuevos y PYTHONPATH a esa copia).
4. Comprueba que solo cambió el golden de ayuda de closeout verify.
5. NO corras la suite completa ni stores build --check.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, `--update-golden`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-23c03e37fed7/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-23c03e37fed7/)

- `validation.log`, `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
