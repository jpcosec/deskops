# Encargo del tester deskops-t-a96b503b0505 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" son parte del contrato).
Entrega del ejecutor: cambios sin commitear en el checkout (deskops/services/closeout_gates.py, tests/test_closeout_gates.py, tests/fixtures/golden/output/view_board.json, tests/fixtures/golden/output/view_task.json) y su evidencia en runs/subagents/exec-deskops-e-72feadf3fc22/ (result-summary.md, validation.log, golden.diff). No confíes en ese resumen: compruébalo.

1. Lee el diff (`git diff -- <esos 4 archivos>`) contra el goal, scope y done_when. ¿Toca algo fuera del scope? ¿El cambio de goldens es solo consecuencia directa de contar `atoms`?
2. Corre tú, de a un archivo y sin lock: `cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>` para test_closeout_gates.py, test_closeout_declared_evidence.py, test_closeout.py y test_view_goldens.py.
3. Reproducción: confirma que el test nuevo falla con el closeout_gates.py de HEAD (p. ej. `git show HEAD:deskops/services/closeout_gates.py > /dev/shm/cg_head.py` y compararlo/ejecutarlo en una copia temporal en /dev/shm; no toques el checkout).
4. No corras la suite completa (ya corrió bajo lock en esta integración; revisa su resultado en validation.log y la comparación con origin/main).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `--autostash`, worktrees y ramas. No escribas fuera de runs/subagents/test-deskops-t-a96b503b0505/ y /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-a96b503b0505/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
