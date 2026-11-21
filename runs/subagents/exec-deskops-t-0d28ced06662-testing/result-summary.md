PASA

Commit del ejecutor: 3a8df5ac43103578c7eb8da69ff6deae22adf289
Mensaje: Snapshot: RuleDoc hash updated, description-only change in where (sldb 22cfafb2), no store migration
Trailer: Task-Id: task-snapshot-de-contratos-de-modelo-ruledoc-cambio-solo-la-descripcion-de-where-sldb-22cfafb2-actualizar

Archivos del commit:
- CHANGELOG.md (+1 línea)
- tests/fixtures/model_contract_hashes.json (solo la entrada RuleDoc)

Verificación:
- El commit no toca tests/*.py ni módulos de código, así que el test aplicable es el de validación de la tarea.
- En un worktree limpio del commit (`/tmp/deskops-test-3a8df5ac`, detached y sin cambios locales): `TMPDIR=/tmp PYTHONPATH=/tmp/deskops-test-3a8df5ac python -m pytest -q -p no:cacheprovider tests/test_model_contract_snapshot.py` -> 2 passed, 1 warning (warning preexistente por `asyncio_default_fixture_loop_scope`). Ver validation.log.
- También pasó en el checkout principal; el worktree limpio se usó para descartar que el estado local del store influyera en el resultado.
- Recalculé los hashes con `_contract_hashes()` del propio test: la única diferencia contra el fixture anterior es RuleDoc, de f2d2b1e396ed... a 411e41fc4ed0..., y coincide exactamente con el valor del fixture actualizado.
- `git diff --check` del commit: OK.

El objetivo observable se cumple: el snapshot pasa contra el sldb con el cambio 22cfafb2 y solo cambió la entrada RuleDoc.
