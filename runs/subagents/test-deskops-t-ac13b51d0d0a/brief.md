# Encargo del tester deskops-t-ac13b51d0d0a (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea (task.debug): `task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error`. Contrato: `deskops show task <id> --root .`. Precisiones en los motivos de los recibos de desk/reviews/<tarea>/: preflight-1, bundle-1 y reproduction-1, este último aceptado por el coordinador con la decisión de arreglar en `_lifecycle_gates`.
Entrega: cambios sin commitear en deskops/services/tasks.py, tests/test_view.py, tests/fixtures/golden/output/view_board.json y view_task.json. Reproducción en runs/subagents/repro-holds-20261117/; evidencia en runs/subagents/exec-deskops-e-519848b776fc/ (result-summary.md, validation.log, related.log, golden.diff).

1. Lee el diff. Comprueba que holds sea false si el gate tiene al menos un finding de nivel error, que los findings se sigan entregando igual y que el resto de la semántica no cambie. Juzga si el bloqueo de TODAS las transiciones del nodo por un finding de error coincide con sldb (`edges_holding`/`edges_blocked`) y con la regla en desk/lifecycle/.
2. Juzga si el cambio de los goldens es solo el de holds/gates_holding (golden.diff) y si es correcto.
3. Corre, sin lock, con `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q <archivo>` y uno a la vez: tests/test_view.py, tests/test_view_goldens.py, tests/test_activation_rules.py, tests/test_lifecycle_graph.py, tests/test_lifecycle_end_to_end.py y tests/test_cli.py.
4. Reproducción: el test nuevo falla con tasks.py de HEAD. Copia el repo en /dev/shm y no toques el checkout. Corre también runs/subagents/repro-holds-20261117/repro.py con el código nuevo y comprueba que holds sale false.
5. NO corras la suite completa ni `stores build --check`.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-ac13b51d0d0a/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-ac13b51d0d0a/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
