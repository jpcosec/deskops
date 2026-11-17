# Encargo del tester deskops-t-0d422f0e62e9 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales` (contrato: `deskops show task <id> --root .`; precisiones en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-el-test-de-llaves-de-message-send-deja-de-ser-xfail-porque-sldb-ya-renderiza-los-valores-literales/).
Entrega: cambio sin commitear en tests/test_message_cli.py (quita el xfail estricto, la constante SLDB_JINJA_VALUE_NOTE y su comentario), más la evidencia en runs/subagents/exec-deskops-e-3f4b69d99461/. El ejecutor informa que los tests resuelven sldb desde el checkout hermano ../sldb/src (tests/conftest.py), que incluye d49f6ddc, mientras que /mnt/ssd/herramientas/sldb no lo incluye.

1. Lee el diff: solo quita el xfail, la constante y su comentario; las 4 variantes no cambian.
2. Comprueba tú la procedencia: qué sldb usa la suite (conftest) y si incluye d49f6ddc; qué sldb usa el CLI instalado y si lo incluye.
3. Corre, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q -rxX tests/test_message_cli.py`: sin xfail ni XPASS.
4. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-0d422f0e62e9/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-0d422f0e62e9/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
