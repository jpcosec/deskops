PASA

# Resultado del tester

Tarea: task-deskops-desk-update-apply-sobre-el-repo-de-deskops-no-vacía-el-path-de-los-modelos-en-sldb-core-mode
Tester: deskops-t-ed585d19a144

## Pruebas

- `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_desk_sync.py` -> **9 passed**, 0 failed (366.68 s), exit 0.
  Log: `pytest-test_desk_sync.log`.
- Extra: `TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_federated_models.py` -> **2 passed** (76.05 s), exit 0
  (cubre la herencia/registro de modelos que toca `deskops/bootstrap.py`).
- No se corrió la suite completa (la corre integrate en el host).

## Falla antes / pasa después

- El test nuevo `test_desk_update_apply_keeps_the_local_path_of_a_declared_model`, aplicado solo sobre un clon limpio de
  HEAD, falla: `AssertionError: assert '' == 'deskops/models/role.py'` (`pytest-before-fix.log`).
- Con el arreglo del árbol de trabajo, ese test y los 8 restantes de `tests/test_desk_sync.py` pasan.

## Reproducción en clon limpio después del arreglo

- `deskops desk update --apply --root <clon>` sale 0.
- `git diff -- .sldb/core/models sldb/relation_types` no muestra ningún cambio de `path:` ni toca `sldb/relation_types`;
  no se agrega `links_to`. Solo cambian hashes/`documents_count` de `RelationDoc`/`RelationTypeDoc` por los documentos
  de ciclo de vida nuevos, además de `store.yaml`/`store_index.yaml` normales de `desk update`.
- Evidencia en `repro-after-fix-*.txt|log|diff`.

## Observaciones

- No existe commit del ejecutor con `Task-Id`; el trabajo está sin commitear en el árbol (el ejecutor lo explica en su
  `result-summary.md`: el commit lo hace closeout). Se testeó el diff de sus archivos, no archivos ajenos.
- El arreglo preserva entradas cuyo `path` no vacío existe dentro del repo; eso cubre el caso real de los 30 modelos de
  deskops y mantiene la conversión de copias externas que exige `tests/test_federated_models.py`.
- No se modificó código, tests, desk ni `.sldb`; no se creó commit.
