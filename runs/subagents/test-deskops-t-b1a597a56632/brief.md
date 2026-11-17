# Encargo del tester deskops-t-b1a597a56632 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit` (contrato: `deskops show task <id> --root .`; precisiones del coordinador en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-closeout-commit-no-amienda-un-commit-que-la-tarea-cita-como-evidencia-de-commit/).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py y tests/test_closeout.py, más su evidencia en runs/subagents/exec-deskops-e-3cd90f55821f/.

1. Lee el diff contra el contrato: el amend se evita solo si el HEAD está citado (references hex de 7+ que son prefijo del sha del HEAD, o value de un recibo evidence-commit accepted de la tarea); lo demás (amend del index.jsonl, trailers, otros modos de cierre) no cambia. Juzga la decisión del ejecutor de comparar el value del recibo línea por línea.
2. Corre tú, de a un archivo, sin lock y con PYTHONPATH al checkout: `cd /mnt/ssd/proyectos/SLDB_1/deskops && PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/test_closeout.py` y lo mismo con tests/test_closeout_declared_evidence.py y tests/test_closeout_resolved_by.py.
3. Reproducción: los tests nuevos de los casos citados fallan con closure.py de HEAD (copia en /dev/shm con git archive HEAD más el test nuevo, PYTHONPATH a la copia).
4. Caso real en sandbox (/dev/shm, git init + deskops init con PYTHONPATH al checkout): commit de código con trailer Task-Id, su sha corto en references, closeout verify y closeout commit; el commit de código sobrevive con su sha.
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout (en tu sandbox de /dev/shm sí puedes commitear), `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-b1a597a56632/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-b1a597a56632/)

`validation.log` y `verdict.md` (APROBADO o RECHAZADO con hallazgos archivo:línea y riesgos). Tu última línea: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
