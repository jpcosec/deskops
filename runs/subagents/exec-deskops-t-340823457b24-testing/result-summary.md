FALLA

# Veredicto del tester

- task id: `task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase`
- role: tester
- run id: `run-deskops-t-340823457b24`
- session: `scion://agent/deskops-t-340823457b24` (`session_sha256` vacío en `run.md`)
- commit evaluado: `b538850eb5eb21e74311080d271e334aa4553b47` — "BoardDoc declara fases del DAG"
- trailer verificado: `Task-Id: task-el-board-declara-las-fases-del-dag-que-tareas-forman-cada-fase-y-que-su-integracion-es-de-la-fase`
- archivos del commit: `deskops/models/board.py`, `tests/test_board_phases.py`

## Lo que sí cumple

El contrato pedido está implementado en `deskops/models/board.py`:

- `PhaseIntegration(validation: list[str] = [], closing_commit: str | None = None)`.
- `Phase(id: str, tasks: list[str], integration: PhaseIntegration)` con default vacío.
- `BoardDoc.phases: list[Phase]` con default `[]`; un Board existente sin `phases` sigue siendo válido.
- Marcador `phases: ⸢rev•phases⸥` en el frontmatter del `__template__`, justo después de `rituals`.
- Validador que rechaza una tarea repetida, tanto entre fases como dentro de la misma fase, y que nombra la tarea en el `ValueError`.

Verifiqué manualmente el round-trip render -> extract: el YAML renderizado conserva `id`, `tasks`, `integration.validation` y `closing_commit` de las dos fases y el extractor los devuelve con los mismos valores.

Los tests pedidos por la tarea pasan de a uno:

- `tests/test_board_phases.py`: **4 passed** (incluye round-trip de dos fases, tarea en dos fases rechazada, tarea repetida en una fase rechazada y Board sin `phases` válido).
- `tests/test_board_portable_references.py`: **3 passed**.

## Por qué el veredicto es FALLA

El cambio de contrato de `BoardDoc` deja un test relevante del repo en rojo, y el store del desk sin actualizar:

1. `tests/test_model_contract_snapshot.py::test_model_contract_hashes_match_the_snapshot` falla porque `tests/fixtures/model_contract_hashes.json` sigue con el hash viejo de `BoardDoc`:
   - fixture actual: `80862082fe97fe60f36c5bac0d185b8b51d984d99e4c216291210d8ed0246579`
   - hash que calcula el propio test: `333c7d0c3ade74d3b040870e21c33dd9a5403a4c87a67ebaeae685b1860246b0`
   - único modelo cambiado según el test: `BoardDoc`.
2. `sldb stores check --store .sldb` reporta el contrato movido de `BoardDoc`:
   - `contract moved: ... BoardDoc ...`
   - `contract_mutation: BoardDoc:Board: fields differ because the MODEL's contract moved ... [fields: phases]`
   - la corrección que indica la herramienta es reextraer/actualizar el store (`sldb stores update`); `.sldb/core/models/BoardDoc.yaml` sigue con `contract_hash: 80862082...`.

No es una falla preexistente: en el commit padre el fixture coincide con el contrato de `BoardDoc` (el cambio lo introduce este commit). Tampoco es una falla de entorno: los tests pasan con el intérprete 3.12 documentado en `validation.log`.

## Otros tests ejecutados (de a uno, `TMPDIR=/tmp`, `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-340823457b24`)

- `tests/test_model_templates.py`: 14 passed.
- `tests/test_edit_task_refreshes_board.py`: 1 passed.
- `tests/test_model_contract_snapshot.py`: **1 failed, 1 passed**.

No corrí la suite completa; la corre integrate en el host.

## Corrección necesaria antes de closeout/integración

1. Actualizar en `tests/fixtures/model_contract_hashes.json` el hash de `BoardDoc` al valor calculado por el propio test (`333c7d0c...`), no a mano, y commitearlo con el `Task-Id`.
2. Reescribir/reextraer el contrato de `BoardDoc` en el store del desk (por ejemplo `sldb stores update --store .sldb --pythonpath .`, o la operación equivalente que use el repo) y commitear los cambios de `.sldb` si corresponden, de modo que `sldb stores check` deje de reportar `BoardDoc` como contrato movido.
3. Repetir `tests/test_model_contract_snapshot.py`, `tests/test_board_phases.py` y `tests/test_board_portable_references.py`.

## Evidencia

- `validation.log`: comandos, versiones y salidas completas.
- `board.txt`, `task.txt`, `next.txt`, `graph.txt`, `git-status.txt`: recuperación de estado.
