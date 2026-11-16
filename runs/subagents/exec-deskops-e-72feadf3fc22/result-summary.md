# result-summary — exec-deskops-e-72feadf3fc22

- run_id: run-deskops-e-72feadf3fc22
- task: task-closeout-verify-cuenta-los-atomos-del-campo-atoms-de-la-tarea-y-no-solo-los-de-references
- session: scion://agent/deskops-e-72feadf3fc22 (agente claude; no hay archivo de sesión local, session_sha256 no disponible)

## Cambios

- `deskops/services/closeout_gates.py` (`CloseoutGatesService.closeout_reference_evidence`): después de recorrer `references`, suma a `evidence["atom"]` cada valor no vacío del campo `atoms` de la tarea, sin filtrar por prefijo y sin duplicados (precisión 1 del preflight). Así la compuerta `atom_or_materialization_link` de `closeout verify` y de `closeout commit` (`closure.py:_closeout_link_gate`, que ya parte de `reference_evidence["atom"]`) cuenta esos átomos. `closure.py` no necesitó cambios. La compuerta de materialization no cambia.
- `tests/test_closeout_gates.py`:
  - test nuevo `test_task_atoms_field_satisfies_the_link_gate[bare_desk|store_desk]`: una tarea con `atoms: [ATOM]` sin átomo en `references` y sin archivos pasa la compuerta (evidencia `[ATOM]`); una tarea sin ninguno sigue fallando con `missing_atom_or_materialization_link`. Con el `closeout_gates.py` de HEAD, el test nuevo falla (`assert False is True`): es la reproducción del item del drawer.
  - aserción ajustada en `test_closeout_reports_cover_each_gate_case`: la tarea fixture `task-skill-guard` ya tenía `atoms: [ATOM]`; ahora su evidencia es `[ATOM, guard-test:...]`. La rompe una razón legítima.
- Corrección del coordinador (ciclo 1): `tests/fixtures/golden/output/view_board.json` y `view_task.json` se regeneraron con `pytest tests/test_view_goldens.py --update-golden` (diff en `golden.diff`). El fixture `tests/view_desk.py` tiene tareas con `atoms`. El diff no es *solo* el átomo en `evidence`; también trae sus consecuencias directas en la misma compuerta y en el resumen:
  - compuerta `atom_or_materialization_link`: `evidence` [] → [átomo], `findings` [missing_atom_or_materialization_link] → [], `state` pending → holds;
  - `found` [] → ["atom|materialization"] y `summary` "encontré nada" → "encontré atom|materialization".
  - `ok` de la tarea sigue en false (faltan tests/commit). No cambia nada más.
  - Afecta a dos tareas en view_board (execution con `atom-atom-for-the-view`, testing con `atom-does-not-exist`) y a una en view_task (execution).

## Validación (detalle en validation.log)

| Comando | Resultado |
|---|---|
| pytest -q tests/test_closeout_gates.py | 5 passed, rc=0 |
| pytest -q tests/test_closeout_declared_evidence.py | 19 passed, rc=0 |
| pytest -q tests/test_closeout.py | 59 passed, rc=0 |
| pytest -q tests/test_view_goldens.py (tras actualizar goldens) | 1 passed, rc=0 |
| suite completa -n 4 (bajo flock; corrió con los goldens ya corregidos) | 3 failed, 1053 passed, 3 skipped, 1 xfailed, rc=1 (26 min) |

Fallas de la suite comparadas con origin/main (worktree limpio en /dev/shm/wt-base, ee9755e3, ya removido): las tres fallan igual ahí, son preexistentes y de entorno (el subproceso no encuentra `python`/`pytest` en el PATH porque el venv no está activado; código 127):
- tests/e2e_agent/test_agent_scenarios.py::test_reference_solutions[first-task-to-closeout] (`reference step failed (127): pytest -q`)
- tests/test_ci_integration.py::test_ci_check_passes_on_a_fresh_desk (`scripts/ci-knowledge-check.sh: line 14: python: command not found`)
- tests/test_ci_integration.py::test_ci_check_fails_on_a_dangling_source_atom (misma causa)

Ninguna falla nueva. Falla causada por el cambio y ya corregida antes de que la suite corriera: `tests/test_view_goldens.py` (goldens de vista, ver arriba; la detectó el coordinador).

## Riesgos

- Como el contrato manda contar *todos* los valores de `atoms` sin filtro, un id que no existe como AtomDoc también satisface la compuerta. El golden lo muestra: la tarea fixture "View golden testing" con `atoms: ["atom-does-not-exist"]` pasa a `holds`. Hoy depende de que SLDB valide el campo tipado `atoms` al escribir la tarea; si eso no se cumple, la compuerta queda más laxa que con `references` (donde `reference_points_to_atom` exige que el archivo exista). Si se quiere exigir existencia, sería una tarea aparte (decisión del supervisor).
- En los receipts de evidencia (`closure._link_documents`), un valor de `atoms` sin prefijo `atom-` o sin archivo no se reconoce como id de átomo; el receipt se emite como `exempt: <ids>`, sin rechazarlo.
