# Encargo del tester deskops-t-7914d82ef26c (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj` (contrato: `deskops show task <id> --root .`; precisiones en los motivos de los recibos preflight-1 y bundle-1 de desk/reviews/task-closeout-verify-no-trata-como-artefacto-generado-un-golden-json-que-tiene-un-golden-yaml-hermano-baj/).
Entrega: cambios sin commitear en deskops/services/closure.py y tests/test_closeout_declared_evidence.py, más la evidencia en runs/subagents/exec-deskops-e-c153823881a4/.

1. Lee el diff: retorno temprano solo para rutas bajo tests/fixtures/ (comparación por componentes); fuera de ahí el chequeo no cambia.
2. Corre, sin lock y con PYTHONPATH al checkout: test_closeout_declared_evidence.py y test_closeout.py.
3. Reproducción: el test del golden falla con closure.py de HEAD (copia en /dev/shm).
4. Caso real, en una copia del repo en /dev/shm (nunca en el checkout, verify escribe recibos): closeout verify de task-deskops-message-ack-acepta-reason-y-la-nota-guarda-el-porque-en-un-campo-ack-reason con el código nuevo ya no da generated_artifact_missing_declared_sources.
5. NO corras la suite completa.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-7914d82ef26c/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-7914d82ef26c/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
