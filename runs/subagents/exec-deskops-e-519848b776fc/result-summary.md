# Resultado (fase 2: arreglo) — deskops-e-519848b776fc

Tarea: task-deskops-view-task-entrega-holds-true-en-un-gate-cuya-regla-de-activacion-da-un-finding-de-error (task.debug)
Fase 1: reproducción aceptada (recibo reproduction-1; evidencia en runs/subagents/repro-holds-20261117/). Atribución: deskops.

## Cambios
- `deskops/services/tasks.py` (`TasksService._lifecycle_gates`): `holds = not blocked and condition_holds(...)`,
  con `blocked = any(finding.level == "error")` sobre los findings on_transition de la tarea. Los findings se
  siguen entregando igual. Coincide con sldb `edges_holding(document=...)`, donde un finding de error frena
  todas las aristas. `view.py` no se tocó: `_gates` copia `show_task`.
- `tests/test_view.py`: test nuevo `test_a_gate_with_an_error_finding_does_not_hold` sobre `lifecycle_desk`
  (tmp_path). Usa una tarea task.code sin recibos y comprueba holds false, el finding de error presente, que en
  `view task --format json` holds coincida con la ausencia de finding de error y `gates_holding == 0`.
  Falla sin el arreglo (`assert True is False`) y pasa con él.
- Fuera de files, pero necesario: `tests/fixtures/golden/output/view_board.json` y `view_task.json`, regenerados
  con `pytest tests/test_view_goldens.py --update-golden`. Los goldens guardaban el bug: solo cambian los gates
  con finding de error (execution y closeout pasan a `holds: false`, `gates_holding` 3 -> 1 en el board, 1 -> 0 en
  la tarea); la tarea de testing, sin errores, sigue `holds: true`. Diff en `golden.diff`.

## Validación (de a un archivo, sin lock; detalle en validation.log y related.log)
- tests/test_view.py: 18 passed (validation de la tarea).
- tests/test_view_goldens.py: 1 passed tras regenerar (antes fallaba solo por el cambio de holds esperado).
- tests/test_activation_rules.py 10 passed; test_lifecycle_graph.py 9 passed; test_lifecycle_end_to_end.py 5 passed;
  test_cli.py 102 passed; test_cli_grammar.py 2 passed; test_inbox_promote_cli_gaps.py 21 passed;
  test_closeout_declared_evidence.py 27 passed.
- Suite completa: no corrida (para el integrador).

## Riesgos
- Cualquier consumidor que leía `holds` como "solo la condición de la arista" ahora ve false si hay un finding
  de error (por ejemplo, graph_ui, que es justo lo que se pidió). `deskops show task` usa los mismos gates: ahí
  el texto "open"/"blocked by" viene de otro lado y no cambió en la salida probada.
- No se corrió test_output_goldens.py: no tiene salidas con holds (grep en fixtures/golden: solo view_*.json).

## Archivos tocados en esta fase
deskops/services/tasks.py, tests/test_view.py, tests/fixtures/golden/output/view_board.json,
tests/fixtures/golden/output/view_task.json, evidencia en runs/subagents/exec-deskops-e-519848b776fc/.
(.sldb/ y desk/reviews/ cambiaron en la fase 1 por `deskops review record`, y por otras sesiones.)
