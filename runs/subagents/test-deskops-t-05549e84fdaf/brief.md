# Encargo del tester deskops-t-05549e84fdaf (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-desk-update-deja-de-exigir-desk-reviews-vacio-y-en-un-clon-limpio-el-dry-run-da-rc-0` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/cli/commands/desk.py, tests/fixtures/golden/scaffold/update.json, tests/test_cli.py, tests/test_review_doc.py y tests/test_legacy_task_states.py, más su evidencia en runs/subagents/exec-deskops-e-bae0befe2582/ (result-summary.md, validation.log). No confíes en ese resumen: compruébalo.

1. Lee `git diff -- <esos 5 archivos>` contra el goal, scope, implementation_path y done_when. Hay dos archivos de test fuera del campo files (test_review_doc.py, test_legacy_task_states.py): juzga si se rompían legítimamente por el cambio y si el ajuste conserva la intención original de cada test o la debilita.
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_cli.py, test_output_goldens.py, test_review_command.py, test_scaffold_golden.py, test_review_doc.py, test_legacy_task_states.py.
3. Reproducción: confirma que el test nuevo del clon limpio falla con el desk.py de HEAD (en una copia temporal en /dev/shm; no toques el checkout).
4. No corras la suite completa: la corre el integrador.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `--autostash`, worktrees y ramas en el checkout. No escribas fuera de runs/subagents/test-deskops-t-05549e84fdaf/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-05549e84fdaf/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
