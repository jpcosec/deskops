REFORMULACION
Propósito: que `deskops init` deje `.deskops.log` ignorado en repos git, evitando que `OperationsService._setup_logging` lo exponga como no trackeado en cada comando. Resultado observable: tras init, el `.gitignore` raíz contiene `.deskops.log` exactamente una vez y `git status` no lo lista. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops` (Python, pytest). Límites: tocar `deskops/bootstrap.py` (`_init_store`) y `tests/test_gitignore_policy.py`; no mover el log fuera de la raíz ni cambiar sldb; reutilizar la idea idempotente de `ensure_cache_ignored`.

AMBIGUEDADES
1. "los rituales enrutados por el Board, las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra": el bundle solo trae el TaskDoc; faltan rituales, pills, átomos y contenido de archivos. Obligaría a inventar su contenido y requisitos.
2. "alrededor de la linea 348": no se aporta el código. Obligaría a inventar el punto exacto de inserción y la firma de `_init_store`.
3. "con la misma idea idempotente": no se define el criterio (línea exacta, salto final, orden). Obligaría a inventar la normalización.
4. "un .gitignore previo con la linea queda igual": no aclara si "igual" es byte a byte o solo sin duplicado. Obligaría a inventar la aserción.
5. "git status no muestra .deskops.log como no trackeado": no cubre el caso de archivo ya trackeado. Obligaría a inventar el comportamiento esperado.

DRY-RUN (hipotético, sin ejecutar)
Lecturas: `deskops/bootstrap.py`, `tests/test_gitignore_policy.py`, `tests/test_runtime_initializer.py`, referencia `desk/inbox/20261119-220154-suggestion-init-no-ignora-deskops-log.md`. Cambios previstos: helper idempotente que crea/lee el `.gitignore` raíz y añade `.deskops.log` si falta, invocado tras `sldb.api.init_store` en `_init_store`; test nuevo con repo temporal (una vez, segundo init sin duplicar, preexistente intacto). Dependencias: `../.venv` con sldb, git disponible, `TMPDIR=/dev/shm`. Validaciones futuras: los tres comandos pytest del TaskDoc, incluida la suite completa y comparación de fallas en worktree limpio de `origin/main`.

FUTURO
Un ejecutor implementa y corre los pytest; el Board/ritual decide aceptación; un humano interpreta fallas de la suite completa y valida la entrega. Los rituales, pills y átomos ausentes deben aportarlos el nodo que los enruta.
