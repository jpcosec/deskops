# Encargo del tester deskops-t-59a02e2fac60 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo` (contrato: `deskops show task <id> --root .`; precisiones del coordinador en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-closeout-verify-escribe-un-recibo-nuevo-cuando-el-veredicto-cambia-aunque-el-input-sea-el-mismo/).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py y tests/test_closeout_declared_evidence.py, más su evidencia en runs/subagents/exec-deskops-e-7fbb23ba5137/.

1. Lee el diff contra el contrato: se salta un recibo solo si hay uno intacto con el mismo fact, input_sha256 y verdict; cualquier cambio de verdict con el mismo input escribe uno nuevo; dos verify iguales no duplican; input_sha256, nombres y la regla no cambian.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout_declared_evidence.py` y lo mismo con tests/test_closeout.py.
3. Reproducción: el test nuevo falla con closure.py de HEAD (copia en /dev/shm).
4. Juzga si el test usa bien el método privado para simular el gate en rojo y si cubre el caso real de la nota (sldb-ui, desk/inbox/20261116-151745-*.md).
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-59a02e2fac60/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-59a02e2fac60/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
