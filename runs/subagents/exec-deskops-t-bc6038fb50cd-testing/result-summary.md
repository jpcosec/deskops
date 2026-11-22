PASA

# result-summary

Task: task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason
Rol: tester (pi), run run-deskops-t-bc6038fb50cd, directorio runs/subagents/exec-deskops-t-bc6038fb50cd-testing
Commit revisado: 89a0ea98cf6f8d1f6938fdfac2cd05b8aae5b65c ("drawer remove: planes, assets de issues, .yml por stem, --reason/--ref", Task-Id en el mensaje)
Archivos del commit: deskops/services/drawer.py, deskops/services/retire.py, deskops/cli/commands/drawer.py, deskops/cli/registry.py, tests/fixtures/golden/help/deskops_drawer_remove.txt, tests/test_inbox_promote_cli_gaps.py

## Veredicto

PASA. Los 5 criterios de "Done When" tienen test y pasan; no hubo regresiones en los tests de drawer/retire ni en el golden de ayuda. Evidencia cruda en validation.log (este mismo directorio).

## Tests corridos (de a uno, TMPDIR=/tmp)

- `python -m pytest -q tests/test_inbox_promote_cli_gaps.py` -> 26 passed (incluye los 5 tests nuevos: plan por nombre y por ruta, assets del issue con guarda de referencias, .yml por stem, reason/ref, y retire de asset huerfano).
- `python -m pytest -q tests/test_retire_cli.py` -> 13 passed (modulo retire.py tocado).
- `python -m pytest -q tests/test_add_task_from_drawer.py` -> 3 passed (modulo drawer.py tocado).
- `python -m pytest -q tests/test_cli_help_examples.py` -> 13 passed (golden deskops_drawer_remove.txt actualizado).
- `python -m pytest -q tests -k "drawer or retire"` -> 84 passed, 1217 deselected (incluye los tests de regresion de from_drawer/--force).
- `python -m pytest -q tests/test_command_registry.py` -> 3 passed (registry.py tocado).
- `python -m pytest -q tests/test_skill_cli_drift.py` -> 2 passed (drift CLI respecto del registry).
- `python -m pytest -q tests/test_closeout.py` -> 73 passed (usa retire_document; sin regresiones).

No corrí la suite completa: el encargo del tester lo prohibe expresamente y la corre el integrador en el host.

## Comprobaciones funcionales independientes

- `.yml` anidado (`desk/drawer/tasks/granular/g01-cli-exec-core.yml`) se resuelve por stem y se retira; imprime `Reason: done` / `Refs: abc123`.
- Plan por ruta (`desk/drawer/plans/plan-x`) se retira entero (dag.yaml + nodes/), borra su bullet del Board y deja las demas lineas intactas; `--reason` con espacios se normaliza y `--ref` repetible se junta (`Refs: abc, def`).
- El bloqueo existente por task con from_drawer sin `--force` sigue vigente para entradas normales (tests existentes pasan).

## Revisión de alcance

- El commit toca solo los 6 archivos del scope declarado; no hay cambios ajenos ni a from_drawer/grafo.
- La rama main contiene 89a0ea98 (por delante de origin/main 0a514d6d); el worktree tenia ademas el commit de run 8c0df1e7.

## Riesgos / notas (no bloquean)

- El `.venv` indicado en el encargo (`/mnt/ssd/proyectos/SLDB_1/.venv`) esta roto en este contenedor: su `python` es 3.11 y no tiene pytest. Use `/workspace/sldb/.venv/bin/python` (3.13, pytest 9.1.1), que resuelve `sldb` a `/mnt/ssd/proyectos/SLDB_1/sldb/src` y `deskops` al arbol de trabajo del commit.
- `drawer remove <plan>` no aplica el bloqueo por `from_drawer` sin `--force`: si una task apunta a un archivo dentro del plan, el plan se retira igual. No lo considero blocker porque los planes no eran retirables antes de este commit (no es regresion de "lo que hoy funciona") y el Done When no lo pide; queda como mejora de seguimiento si se quiere uniformar.
- No se corrio la suite completa (ver arriba).
