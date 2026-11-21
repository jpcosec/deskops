PASA

# Verificación

Commit del ejecutor: `f5b017755746a11b8798d3a003c43899e0997afa` — "deskops init agrega .deskops.log al .gitignore" (trailer `Task-Id: task-deskops-init-agrega-deskops-log-al-gitignore-del-repo`).

Archivos del commit:
- `deskops/bootstrap.py`
- `tests/test_gitignore_policy.py`

# Tests

Corridos en un worktree limpio de `f5b01775` (`/tmp/deskops-test-f5b01775`), uno por archivo, con `PYTHONPATH=$PWD TMPDIR=/tmp`.

- `python -m pytest -q -p no:cacheprovider tests/test_gitignore_policy.py` → **2 passed** (rc 0)
- `python -m pytest -q -p no:cacheprovider tests/test_runtime_initializer.py` → **3 passed** (rc 0)

No existe `tests/test_bootstrap.py`; por eso el otro archivo relevante es `test_runtime_initializer.py`, que ejercita el bootstrap. No corrí la suite completa, según la instrucción del rol tester.

Nota de entorno: el `.venv` de `/mnt/ssd/proyectos/SLDB_1` está roto en este contenedor (sus binarios apuntan a un Python 3.12 ausente y no importan pytest). Usé el venv funcional `/dev/shm/t311/bin/python` (3.11, pytest 9.2.0), que ya tiene `deskops` y `sldb` instalados en modo editable.

# Done When

El test nuevo `test_init_local_store_ignores_deskops_log_once` pasa y cubre el Done When:

1. Primer init en repo temporal: `.gitignore` contiene `.deskops.log` una sola vez.
2. Segundo init: no la duplica.
3. `.gitignore` previo con `node_modules` + `.deskops.log`: queda intacto.
4. `.gitignore` previo sin salto final (`node_modules`): se agrega `.deskops.log` con el salto correcto.

Verificación manual adicional sobre un `git init` real:

- `ensure_log_ignored` escribe una vez y en la segunda llamada devuelve `False`.
- Con `.deskops.log` presente en la raíz, `git status --porcelain` solo muestra `?? .gitignore` (no muestra `.deskops.log`) y `git check-ignore --quiet .deskops.log` devuelve 0.

# Implementación

`SLDBBootstrap.init_local_store` llama a `ensure_log_ignored(target_path)` tras `_init_store` y antes de `ensure_merge_driver`. La función:

- no hace nada si `target_path` no es un repo git (no existe `.git`);
- crea `.gitignore` si falta;
- reconoce `.deskops.log` y `/.deskops.log` (con strip) y no duplica;
- preserva el contenido previo y agrega el salto final si faltaba.

Sin hallazgos bloqueantes.
