# Encargo del tester deskops-t-a963945f7a8c (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo` (contrato: `deskops show task <id> --root .`; precisiones en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-deskops-review-node-acepta-ids-de-nodo-con-punto-como-ws13-1-en-el-subject-ref-del-recibo/).
Entrega del ejecutor: cambios sin commitear en deskops/models/review.py, tests/test_review_doc.py y tests/test_review_command.py, más su evidencia en runs/subagents/exec-deskops-e-3d60a97676f5/.

1. Lee el diff: el id de nodo admite el punto; espacio y segundo '#' siguen rechazados; nada más cambia.
2. Corre tú, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_review_doc.py` y lo mismo con tests/test_review_command.py.
3. Reproducción: los tests nuevos de punto fallan con review.py de HEAD (copia en /dev/shm).
4. NO corras review node sobre los planes reales del drawer ni la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-a963945f7a8c/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-a963945f7a8c/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
