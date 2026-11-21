PASA

# Resultado del tester

Tarea: task-dispatch-deja-commiteados-los-rundoc-que-escribe-para-que-el-reap-pueda-traer-al-main-commits-del-ej

## Trabajo verificado

- Commit del ejecutor: `1253422f452392baa4d9a7d2cdc072c759d31bbc` («dispatch commitea los RunDoc que escribe (start y reap) para que el reap no choque con el store»), rama `deskops/deskops-e-e5f89cdffe35`.
- Archivos del commit: `CHANGELOG.md`, `deskops/dispatch.py`, `tests/test_dispatch.py`.
- El commit incluye `Task-Id` correcto.

## Tests corridos

Comando de validación sobre el commit del ejecutor (`1253422f`), desde un worktree temporal:

    TMPDIR=/tmp <python> -m pytest -q -p no:cacheprovider tests/test_dispatch.py

Resultado: **35 passed**, 1 warning (opción de asyncio desconocida), 422.92 s.

Los dos tests nuevos, corridos aparte, también pasan:

- `test_start_commits_the_rundoc_so_reap_brings_an_executor_commit_touching_the_store`
- `test_reap_names_the_files_when_local_changes_block_the_pick`

## Verificación en rojo

Copié el `tests/test_dispatch.py` del commit sobre su padre (`712b8dc3`) y corrí los dos tests nuevos: **ambos fallan**, como corresponde al comportamiento previo (el store del RunDoc queda sin commitear y reap no nombra los archivos que bloquean el pick).

## Nota de entorno

En este sandbox el intérprete del venv (`python3.12`) no está disponible (symlink roto). Corrí los mismos tests con `/usr/bin/python3.11` y dependencias compatibles instaladas en `/tmp/py311deps`, más el fuente de SLDB en `/mnt/ssd/proyectos/SLDB_1/sldb/src`. No cambié código ni tests del commit.
