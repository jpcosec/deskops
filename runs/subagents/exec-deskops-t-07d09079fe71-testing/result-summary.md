PASA

# Resultado del tester

Tarea: task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb
Tester: deskops-t-07d09079fe71

## Commit del ejecutor

`f680196999dacc787f87850c2bf296fb87bee86f` — "closeout verify covers files under a directory target that is a graph node".
Trailer verificado: `Task-Id: task-closeout-verify-cubre-los-archivos-bajo-un-directorio-target-que-ahora-es-nodo-del-grafo-de-sldb`.

Archivos del commit:
- `deskops/services/closure.py`: `_directory_materialization_targets` incluye ahora las materializations válidas cuya arista apunta a un target declarado que es un directorio existente (`_materialization_edges_to` + `(root / declared).is_dir()`), además de las inválidas que ya cubría.
- `CHANGELOG.md`: entrada en Fixed.

## Pruebas ejecutadas

- `TMPDIR=/tmp /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_materialization_targets_outside_package.py`
  -> **18 passed**, 1 warning, exit 0 (93.44 s).
- Caso objetivo, ambos parámetros:
  `... tests/test_materialization_targets_outside_package.py::test_closeout_verify_covers_files_under_a_directory_target -v`
  -> **2 passed**, exit 0 (32.18 s).

No existe `tests/test_closure.py` para el módulo tocado; el test relevante es el archivo anterior. No se corrió la suite completa (la corre integrate en el host).

## Falla antes / pasa después

Sobre un worktree temporal en `f6801969^` (código sin el arreglo), el mismo test objetivo falla en ambos casos:
- `pkg/sub/a.py` y `tests/notations/test_a.py` aparecen en `missing_changed_file_link`.
- `pkg/subzero.py` y `tests/notationszero.py` siguen (correctamente) en missing.
Con el commit actual: 2 passed. El worktree temporal se eliminó; no se modificó el repo.

## Entorno

El `.venv` del workspace apunta a un Python 3.12 ausente y `python` no está en PATH; se usó `/workspace/sldb/.venv/bin/python` (3.13.18), cuyo `sldb` resuelve a `/workspace/sldb/src` con HEAD `524a2c06` (incluye `6f14a3b5`, el cambio que convierte un directorio existente en nodo del grafo).

## Observación no bloqueante

El docstring de `_directory_materialization_targets` todavía describe el caso viejo ("The graph only makes a node of a declared target that is a file..."), que ya no es cierto con el sldb actual. No afecta el comportamiento ni los tests.
