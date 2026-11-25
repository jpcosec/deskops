## REFORMULACION

Propósito: evitar que pytest escriba su basetemp en `/dev/shm` (ENOSPC) y que carpetas `deskops-integrate-*` de corridas muertas queden para siempre. Resultado: en `deskops/integrate.py`, `_run_suite` añade `--basetemp=<work>/pytest` a `PYTEST_ADDOPTS` conservando lo previo; cada carpeta de trabajo lleva `owner.pid`; con `_suite_lock` tomado se borran carpetas `deskops-integrate-*` de pids muertos (`os.kill(pid,0)` → `ProcessLookupError`) o sin `owner.pid` y mtime mayor que `cfg.suite_timeout`, nunca la propia ni la de un pid vivo, imprimiendo `limpieza: <ruta>`. Repo `/mnt/ssd/proyectos/SLDB_1/deskops`; toca `deskops/integrate.py` y `tests/test_integrate.py`. Fuera: `desk/config.json`, limpieza de `/dev/shm/pytest-of-scion`, `deskops/queue.py`.

## AMBIGUEDADES

1. "ya con el lock de la suite tomado (_suite_lock(cfg.tests_lock))" — `_run_suite` no recibe `work`; obliga a inventar si la limpieza va dentro de `_run_suite`, con qué firma, o en `_steps`.
2. "Cada carpeta de trabajo deja un archivo owner.pid" — no dice cuándo se escribe, formato (¿texto decimal?) ni si aplica en `--dry-run`.
3. "las que tienen owner.pid con un pid que no vive" — no cubre `owner.pid` ilegible, vacío o no numérico; habría que inventar el criterio.
4. "conservando lo que ya traiga PYTEST_ADDOPTS, separado por un espacio" — no fija el orden (basetemp antes o después).
5. "Al empezar la suite" — `_run_suite` solo corre si el rango toca código; no dice si la limpieza ocurre también en rangos solo-desk, en dry-run o al fallar antes.
6. "test_stale_integrate_dirs_are_removed_under_the_lock" — no define cómo el test invoca la limpieza (¿`_run_suite` con cfg/copy?, ¿función nueva?), obligando a inventar API.

## DRY-RUN

Lecturas: `deskops/integrate.py` (`_run_suite` ~195, `finally` ~283, `_steps` ~303, `_suite_lock`) y `tests/test_integrate.py`. Cambios previstos: helper de limpieza con `tempfile.gettempdir()` + glob, lectura de `owner.pid` y `os.kill`; escritura de `owner.pid` tras `mkdtemp`; paso de `<work>/pytest` a `_run_suite` para `PYTEST_ADDOPTS`; dos tests nuevos. Dependencias: `cfg.suite` (`sh -c ... pytest`), `cfg.tests_lock`, `cfg.suite_timeout`. Validaciones futuras: los dos comandos pytest del TaskDoc y una corrida real que deje temporales dentro de la carpeta.

## FUTURO

Otro nodo implementa en el worktree de dispatch y crea el commit con `Task-Id`; un humano revisa y mergea.
