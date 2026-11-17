# Encargo del tester deskops-t-91635780a910 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas nada, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista` (contrato: `deskops show task <id> --root .`; precisiones en los motivos de los recibos de desk/reviews/<tarea>/).
Entrega: cambios sin commitear en deskops/cli/commands/view.py, deskops/cli/registry.py (view task pasa a OUTPUT_FORMAT_YAML_ARG), docs/deskops-ui.md, tests/test_view.py, tests/fixtures/golden/help/deskops_view_task.txt y tests/fixtures/golden/output/view_task.json, más la evidencia en runs/subagents/exec-deskops-e-df9455e89049/ (result-summary.md, validation.log).

1. Lee el diff contra el contrato y las precisiones: `task.receipts` al nivel de `gates`, entradas con exactamente id, kind, verdict, anchor_state, created_at; pertenencia por subject sin pin; orden (created_at, id); recibos de nodo fuera; error de índice a `errors` con lista []; json y yaml con la misma estructura; una línea por recibo en texto; board sin receipts.
2. Juzga si los cambios fuera de `files` (registry.py y los dos goldens) son necesarios y mínimos.
3. Corre, sin lock, con `PYTHONPATH=$PWD TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q <archivo>` uno a la vez: tests/test_view.py, tests/test_view_goldens.py, tests/test_command_registry.py, y tests/test_output_goldens.py -k help_goldens.
4. Reproducción: el test nuevo falla con view.py de HEAD (`git show HEAD:deskops/cli/commands/view.py` a una copia en /dev/shm; no toques el checkout).
5. Caso real, solo lectura: `deskops view task <una tarea cerrada con recibos> --root . --format json` (con PYTHONPATH al checkout) trae sus recibos con anchor_state coherente.
6. NO corras la suite completa ni `stores build --check`.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout` en el checkout, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-91635780a910/ y /dev/shm, y limpia lo tuyo.

## Evidencia (en runs/subagents/test-deskops-t-91635780a910/)

`validation.log` y `verdict.md` con una línea `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>` y hallazgos. Tu última línea en la conversación es esa misma.
