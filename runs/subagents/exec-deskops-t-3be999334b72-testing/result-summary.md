PASA

# Resultado del tester

Tarea: task-deskops-init-y-desk-update-apply-instalan-el-merge-driver-de-sldb-en-el-repo-del-desk
Commit probado: d944d0e3d02d99b301102e489452a0cddffd1225

## Verificación

- `tests/test_desk_merge_driver.py`: 3 passed. Cubre init en repo git (`.gitattributes` con las tres líneas `merge=sldb` y `merge.sldb.driver` en la config), init fuera de git (no escribe nada) y `desk update --apply` que instala el driver faltante y es idempotente.
- `tests/test_lifecycle_seed_drift.py`: 8 passed, con sldb 9007f78a (el que trae el alert del merge driver). El golden `doctor_lifecycle_seed_out_of_date.text` no cambia.
- Tests de los módulos tocados: `tests/test_desk_paths.py` (16), `tests/test_desk_replace.py` (10), `tests/test_desk_sync.py` (9), `tests/test_desk_graph_runs_target.py` (2), todos passed.
- Extra por el cambio en `tests/conftest.py`: `tests/test_task_lifecycle_validator.py` (39) y `tests/test_doctor_model_registration.py` (8), todos passed.
- Comprobación manual: `deskops init` en un repo git temporal deja el driver y `deskops doctor` responde `Desk is healthy. No issues found.` sin `merge-driver-missing`.

Todos los comandos se corrieron de a un archivo con `TMPDIR=/tmp`, usando el Python del entorno de pruebas `/dev/shm/t311/bin/python` (el `python` del PATH apunta a un venv cuyo intérprete 3.12 no está disponible) y el `PYTHONPATH` del workspace.

## Veredicto

PASA: el trabajo del commit cumple el encargo y sus tests pasan.
