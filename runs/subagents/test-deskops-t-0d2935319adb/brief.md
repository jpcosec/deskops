# Encargo del tester deskops-t-0d2935319adb (independiente)

Rol: `desk/roles/deskops-tester.md` del repo /mnt/ssd/proyectos/SLDB_1/deskops (léelo primero). Verificas una entrega ajena y das un veredicto con evidencia. NO implementas, no editas código ni tests, no commiteas, no ruteas.

## Qué verificar

Tarea: `task-closeout-una-materialization-cuyo-target-identity-es-un-directorio-cubre-los-archivos-bajo-ese-direc` (contrato: `deskops show task <id> --root .`; las "Precisiones del preflight 1" son parte del contrato).
Entrega del ejecutor: cambios sin commitear en deskops/services/closure.py y tests/test_materialization_targets_outside_package.py, más su evidencia en runs/subagents/exec-deskops-e-312954356a7f/ (result-summary.md con la sección "Corrección 1", validation.log, graph-missing-sandbox.log, message-send.log). No confíes en ese resumen: compruébalo.

1. Lee `git diff -- deskops/services/closure.py tests/test_materialization_targets_outside_package.py` contra el goal, scope, implementation_path y done_when. ¿Toca algo fuera del scope? ¿target_covers cumple la normalización de la precisión? ¿Quedó resuelto el bug de la nota desk/inbox/20261116-070913-* (prefijo <kind>: de target_id, directorio dentro de tests/)? ¿Se mantiene inválida una materialization a la que le falta algo más que su target directorio?
2. Corre tú, de a un archivo y sin lock (`cd /mnt/ssd/proyectos/SLDB_1/deskops && TMPDIR=/dev/shm ../.venv/bin/python -m pytest -q tests/<archivo>`): test_materialization_targets_outside_package.py, test_closeout_gates.py, test_closeout.py, test_closeout_declared_evidence.py, test_view_goldens.py.
3. Reproducción: confirma que los tests nuevos fallan con el closure.py de HEAD (en una copia temporal en /dev/shm; no toques el checkout).
4. Paso 4 del contrato: confirma que la nota a sldb existe en /mnt/ssd/proyectos/SLDB_1/sldb/desk/inbox/20261116-054845-suggestion-declared-target-nodes-aceptar-un-directorio-como-target-declarado.md, con el título y el cuerpo que pide la precisión.
5. No corras la suite completa: la corre el integrador.

## Reglas

`export TMPDIR=/dev/shm`. Prohibido `pkill`, `pgrep`, `git add`, `git commit`, `git push`, `git stash`, `--autostash`, worktrees y ramas. No escribas fuera de runs/subagents/test-deskops-t-0d2935319adb/ y /dev/shm, y limpia lo tuyo en /dev/shm.

## Evidencia (en runs/subagents/test-deskops-t-0d2935319adb/)

- `validation.log`: cada comando con su salida y rc.
- `verdict.md`: veredicto `APROBADO` o `RECHAZADO`, con hallazgos (archivo:línea) y riesgos.
- Tu última línea en la conversación: `VEREDICTO: APROBADO` o `VEREDICTO: RECHAZADO: <motivo>`.
