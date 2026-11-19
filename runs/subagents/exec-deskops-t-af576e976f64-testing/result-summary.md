PASA

Commit revisado: ef2ad7533239cfd467ab07c416156f5aebed7727 ("dispatch: quick_gates del desk en los prompts de ejecutor y tester").

Archivos del commit:
- CHANGELOG.md
- deskops/config.py
- deskops/dispatch.py
- docs/operator-manual.md
- tests/test_dispatch.py

Verificación:
- `DispatchConfig.quick_gates` es una lista de argv opcional en el bloque dispatch.
- Con quick_gates declarado, el prompt.md del ejecutor incluye el comando y exige rc 0 antes de commitear; el del tester lo incluye y declara FALLA si el rc es distinto de 0.
- Sin quick_gates el prompt no agrega la sección "Gates rapidos" (la instrucción base queda intacta).
- Documentación y CHANGELOG actualizados.

Tests ejecutados con el python de /tmp/ws-venv, de a uno:
- `TMPDIR=/tmp /tmp/ws-venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py` -> 22 passed (3:47).
- `TMPDIR=/tmp /tmp/ws-venv/bin/python -m pytest -q -p no:cacheprovider tests/test_config.py` -> 5 passed (0.21s).

No se corrió la suite completa: la corre integrate en el host, según el encargo del tester.
