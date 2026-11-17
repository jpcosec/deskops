# Resultado: ejecutor deskops-e-df9455e89049 (intento 1)

- run_id: run-deskops-e-df9455e89049
- task: task-deskops-view-task-entrega-los-recibos-de-la-tarea-en-un-campo-receipts-del-contrato-de-la-vista
- session: scion://agent/deskops-e-df9455e89049 (agente claude); session_sha256: no disponible desde dentro de la sesión

## Qué cambió

- `deskops/cli/commands/view.py` (en files): nuevo `_Projection._receipts`. Lee los nodos `ReviewDoc` del índice compuesto del store (`sldb.api.load_edge_index(store, include_linked=False)`), que es el mismo índice desde donde la regla de activación (`edges_holding` → `any(^subject: anchor_state = ...)`) toma el `subject__anchor_state` que sldb deriva. Pertenece a la tarea todo recibo cuyo subject, sin el pin `@sha256:…`, es `doc:<modelo de la tarea>:<id>`. El modelo sale del `export_id` de la fila de la vista (p. ej. `TaskCodeDoc`). Los recibos de nodo (subject vacío) quedan fuera. Cada entrada tiene exactamente `id, kind, verdict, anchor_state, created_at`, ordenadas por (`created_at`, `id`). `task.receipts` va dentro de `task`, al mismo nivel que `gates`. Si el índice no se puede leer, el error queda en `errors` y la lista sale `[]`. En texto: una línea `receipt <id> <kind> <verdict> <anchor_state> <created_at>` por recibo. También actualicé el docstring del módulo.
- `docs/deskops-ui.md` (en files): `receipts` en el ejemplo de la vista task, la viñeta que define el campo (pertenencia, claves, orden, anchor_state, yaml y texto), una fila en la tabla de fuentes y la fila del mapeo de Stitch, que antes decía "no se dibuja hasta que existan" y ahora apunta a `task.receipts`.
- `tests/test_view.py` (en files): nuevo `test_task_receipts_are_the_reviewdocs_of_the_task_with_their_anchor_state`. Trabaja sobre un desk sandbox (tmp_path). Primero comprueba que la tarea sin recibos da `[]`. Luego registra 2 recibos con `deskops review record <tarea> --kind reproduction --evidence notes/repro.txt --reason x --root <sandbox>` y verifica en json las 5 claves exactas, `pending` e `intact`, y el orden. Verifica también que los recibos de otra tarea no se mezclan, que yaml trae la misma estructura y que el texto trae una línea por recibo. Al final edita el goal de la tarea y comprueba que `anchor_state` pasa a `changed`.
- **Fuera de files** `deskops/cli/registry.py`: `view task` usaba `OUTPUT_FORMAT_ARG` (text/json) y no tenía yaml. El implementation_path y la precisión (5) del coordinador piden json y yaml con la misma estructura, así que lo cambié a `OUTPUT_FORMAT_YAML_ARG`, la constante que ya existía (text/json/yaml). Es una sola línea, sin comando nuevo, y el comando sigue siendo read-only (mutates=False).
- **Fuera de files** `tests/fixtures/golden/help/deskops_view_task.txt`: es el golden de `--help` de `view task`, que cambia porque `--format` ahora acepta yaml. Regeneré solo ese archivo con `_collect_help()` de tests/test_output_goldens.py.
- **Fuera de files** `tests/fixtures/golden/output/view_task.json`: la precisión (6) permite regenerar los goldens de view. Lo regeneré con `--update-golden`. El único cambio es `"receipts": []`, porque la tarea golden está en ejecución sin recibos.

## Validación (validation.log)

- `pytest -q tests/test_view.py`: 17 passed, rc=0
- `pytest -q tests/test_view_goldens.py`: 1 passed, rc=0 (después de regenerar view_task.json; antes de regenerarlo fallaba solo por el campo nuevo)
- `pytest -q tests/test_command_registry.py`: 3 passed, rc=0 (lo pide el integrador porque cambió el registro)
- `pytest -q tests/test_output_goldens.py -k help_goldens`: 1 passed, rc=0 (por el golden de ayuda)
- Prueba manual contra el desk real, solo lectura: `deskops view task <una tarea> --root .` en texto, sin errores.
- No corrí la suite completa ni `stores build --check` (orden del integrador): **quedan para el integrador**.

## Riesgos

- Para leer `anchor_state` uso el índice compuesto con el `model_type_of` por defecto de sldb, el mismo de `load_edge_index` y `edges_holding`. No es el resolver con `package_pythonpath` que usa `check_doc_anchors` en closure. Si alguna vez difieren, la vista sigue a la regla de activación, que es lo que pide la precisión (4).
- Cada `view task` compone el índice una vez más. Está cacheado mientras los shards no se mueven.
- La vista board no lleva receipts, como pide el scope.
- No envié el aviso a graph_ui: lo manda el coordinador al cerrar (precisión 8).
