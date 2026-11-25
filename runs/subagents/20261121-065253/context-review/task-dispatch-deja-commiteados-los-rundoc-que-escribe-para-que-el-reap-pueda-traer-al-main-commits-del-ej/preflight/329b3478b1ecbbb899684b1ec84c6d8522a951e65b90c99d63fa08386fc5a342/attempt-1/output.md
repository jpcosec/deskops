## REFORMULACION

Encargo ejecutable (task.code, no agregado): hacer que `dispatch start` deje commiteados en el checkout principal los archivos del store que escribe `record_scion_run` (store.yaml, store_index.yaml, models/RunDoc.yaml y el shard), con pathspec, para que el reap pueda cherry-pickear commits del ejecutor que también tocan el store. Además, `reap` debe commitear, antes del cherry-pick, cualquier RunDoc pendiente de sus agentes; si otro cambio local choca, el error debe nombrar los archivos y sugerir commitearlos. Resultado observable: el test nuevo y `tests/test_dispatch.py` pasan. Repo: deskops (`deskops/dispatch.py`, `deskops/runtime/scion.py`, tests, CHANGELOG). Límites: fuera el resto.

## AMBIGUEDADES

1. "deskops/dispatch.py (start y reap) o deskops/runtime/scion.py (record_scion_run)" — el "o" no decide ubicación; obligaría a inventar en qué archivo implementar.
2. "commitea en la rama principal" — no define si es `main` o la rama actualmente chequeada; obligaría a inventar la rama destino.
3. "mensaje 'run: <agente>' y [skip ci]" — no indica si `[skip ci]` va en el asunto o como trailer; obligaría a inventar el formato exacto.
4. "reap, antes del cherry-pick, commitea igual" — "igual" no aclara pathspec, mensaje ni comportamiento si no hay cambios pendientes; obligaría a inventar el no-op.
5. "Si queda otro cambio local que choca, el mensaje de error nombra los archivos" — no dice quién emite el mensaje ni su formato; obligaría a inventar el texto y el punto de captura.
6. "y trailer Task-Id" — no da el valor ni el formato del trailer; obligaría a inventar `Task-Id: <id>`.
7. "el ejecutor (simulado) commitea en su rama" — no describe la simulación; obligaría a inventar el harness del test.

## DRY-RUN

Lecturas: `deskops/dispatch.py` (start, reap), `deskops/runtime/scion.py` (record_scion_run), `tests/test_dispatch.py`, CHANGELOG, esquema del store. Cambios previstos: p1 test de repo temporal que falla; p2 commit con pathspec en start y en reap pre-cherry-pick; p3 CHANGELOG. Dependencias: git, store y shard existentes, rama del ejecutor. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`. Sin ejecutar nada.

## FUTURO

Deciden humanos/otros nodos: ubicación final (dispatch.py vs scion.py), rama destino y formato exacto de mensajes/trailers, y la aceptación tras el pytest.
