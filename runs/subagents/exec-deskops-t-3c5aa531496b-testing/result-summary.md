PASA

# Resultado de testing — task-build-neighbours-de-absolute-paths...

## Entrega verificada

- Commit del ejecutor: `342b22e9cb92838ad8fd8c0332af5732d47b221d` (`build_neighbours resuelve el registro con resolve_registered_root`, Task-Id correcto).
- Archivos: `deskops/absolute_paths.py`, `tests/test_doctor_absolute_paths.py` (2 archivos, +21/-5).
- `build_neighbours` ahora resuelve cada `path` del registro con `resolve_registered_root(root, value)`: expande `~` y resuelve relativas contra la raíz del repo, igual que `doc_access.repository_root`. El guard de `near.roots` usa `Path(value).expanduser().is_absolute()` para no tratar una entrada con `~` como relativa.

## Tests corridos (de a uno, TMPDIR=/tmp, sin PYTHONPATH)

El `.venv` del proyecto está roto en este host (`bin/python` apunta a Python 3.11 pero su `site-packages` es de 3.12 y no tiene pytest). Usé el intérprete con pytest disponible: `/dev/shm/t311/bin/python` (Python 3.11.2, pytest 9.2.0).

    cd /mnt/ssd/proyectos/SLDB_1/deskops
    TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_doctor_absolute_paths.py
    -> 14 passed, 1 warning (172.44s)

    TMPDIR=/tmp /dev/shm/t311/bin/python -m pytest -q tests/test_registry_robustness.py
    -> 8 passed, 1 warning (33.06s)

No existe `tests/test_absolute_paths.py`; el único test del módulo tocado es `tests/test_doctor_absolute_paths.py`.

Nota de entorno: con `PYTHONPATH=$PWD` los 8 tests de doctor que invocan `python -m sldb` fallan porque el directorio local `deskops/sldb` (namespace sin `__main__`) tapa al checkout hermano; sin `PYTHONPATH` —la forma indicada por el brief— pasan los 14. No es un defecto del commit.

## Discriminación del test nuevo

Ejecuté el test nuevo contra el commit padre (`a1d8fda6`) en un worktree temporal: falla porque `<root>/~/tilde-repo` no es `$HOME/tilde-repo` (`1 failed`). Con `342b22e9` pasa. El test nuevo cubre la regresión.

## Conclusión

PASA: el test nuevo pasa, los dos archivos de la Validation pasan completos, y la entrada con `~` y la relativa resuelven al mismo directorio por `build_neighbours` y por `doc_access.repository_root`.
