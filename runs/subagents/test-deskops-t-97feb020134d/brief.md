# Encargo del tester deskops-t-97feb020134d (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu` (contrato: `deskops show task <id> --root .`; precisiones del coordinador en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-closeout-commit-incluye-el-run-md-de-cada-rundoc-que-el-store-trackea-y-git-todavia-no-tiene-para-qu/).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py y tests/test_closeout.py, más su evidencia en runs/subagents/exec-deskops-e-17c5ffaf7b3c/.

1. Lee el diff: el cierre suma el run.md de cada RunDoc de .sldb/store.yaml que existe en disco y git no conoce; uno sin run.md se ignora; nada más cambia. Juzga el riesgo de arrastrar el run.md de una corrida ajena en curso.
2. Corre tú, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py` y lo mismo con tests/test_closeout_declared_evidence.py.
3. Reproducción: el test nuevo falla con closure.py de HEAD (copia en /dev/shm).
4. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-97feb020134d/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-97feb020134d/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
