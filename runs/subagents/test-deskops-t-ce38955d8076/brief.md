# Encargo del tester deskops-t-ce38955d8076 (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe` (contrato: `deskops show task <id> --root .`). Las "Precisiones del preflight 1" del scope y las precisiones del coordinador del motivo del recibo preflight-2 (desk/reviews/task-desk-update-migra-las-claves-legacy-checklists-y-routine-del-frontmatter-de-las-tareas-para-que-supe/preflight-2.md) son parte del contrato.
Entrega del ejecutor: cambios sin commitear en deskops/workspace.py, deskops/cli/commands/desk.py y tests/test_legacy_task_states.py, más su evidencia en runs/subagents/exec-deskops-e-79646a51295e/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee `git diff -- <esos 3 archivos>` contra el goal, el scope, el implementation_path y el done_when. Revisa:
   - lista cerrada: solo checklists y routine; otra clave no declarada no se toca y supersede la sigue rechazando;
   - formato del dry-run ('<ruta>: legacy frontmatter key <clave>'), orden (ruta; checklists antes que routine), rc 1 con migración pendiente;
   - --apply: una línea por clave quitada con el valor en json.dumps(..., ensure_ascii=False, default=str, separators=(',',':')); el resto del archivo intacto; idempotente;
   - frontmatter ilegible: no se toca, se reporta como invalid task y no aborta el resto. Juzga si el cambio en _task_type_migration_plan (salta una tarea ilegible en vez de abortar desk update) es necesario y no rompe nada;
   - que no haya cambios fuera de scope.
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_legacy_task_states.py, test_cli.py, test_review_doc.py, y cualquier otro test de desk update que encuentres (grep "desk update" o "migrate_task_types" en tests/).
3. Reproducción: confirma que los tests nuevos fallan con el código de HEAD, en una copia temporal en /dev/shm (git archive HEAD más los tests nuevos); no toques el checkout.
4. Caso real, solo lectura: copia a /dev/shm un desk mínimo con las 3 tareas legacy de /mnt/ssd/proyectos/SLDB_1/UIs/marcado/desk/tasks/ que tienen checklists o routine y corre ahí desk update (dry-run y --apply) con el código del checkout. No escribas en UIs/marcado.
5. NO corras la suite completa ni stores build --check (orden del integrador wA:p1: el lock /dev/shm/sldb1-tests.lock es el cuello de botella).

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `git checkout`, `--autostash`, y worktrees o ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-ce38955d8076/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-ce38955d8076/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
