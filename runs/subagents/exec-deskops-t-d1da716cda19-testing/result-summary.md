PASA

# Veredicto del tester

- task id: `task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin`
- role: tester
- run id: `run-deskops-t-d1da716cda19`
- session: `scion://agent/deskops-t-d1da716cda19` (`session_sha256` vacío en `run.md`)
- commit evaluado: `58ce512897651a6bce9e7169bca0d42a1b481466` — `integrate: mover a done los integrate fallidos ya en origin`
- trailer verificado: `Task-Id: task-un-integrate-exitoso-pasa-a-done-los-integrate-fallidos-del-desk-ya-presentes-en-origin`
- archivos del commit: `deskops/integrate.py`, `tests/test_integrate.py` (solo esos dos; 42 y 44 líneas agregadas)

El commit `58ce5128` es el del ejecutor y no hay cambios posteriores en esos dos archivos
(`git diff --stat 58ce5128 HEAD -- deskops/integrate.py tests/test_integrate.py` sale vacío).

## Tests ejecutados

Con `PYTEST_ADDOPTS="--basetemp=/tmp/pytest-deskops-t-d1da716cda19"` y `TMPDIR=/tmp`, desde el
checkout del repo:

```text
TMPDIR=/tmp /dev/shm/tester-venv/bin/python -m pytest -q tests/test_integrate.py -k failed
2 passed, 30 deselected, 1 warning in 195.29s (0:03:15)

TMPDIR=/tmp /dev/shm/tester-venv/bin/python -m pytest -q tests/test_integrate.py
32 passed, 1 warning in 308.21s (0:05:08)
```

El warning es el `PytestConfigWarning: Unknown config option: asyncio_default_fixture_loop_scope`,
ajeno al cambio. Los dos tests nuevos son:

- `test_integrate_moves_failed_already_in_origin_to_done`
- `test_integrate_keeps_failed_not_in_origin`

Ambos usan el repo git temporal y el origin bare del propio archivo. El primero crea un commit con
`Task-Id: task-old` que el integrate termina empujando (queda ancestro de origin) y comprueba el
movimiento a `done`, el contenido final del log y que otro job (`task-other`, sin commit de cierre)
sigue en `failed`. El segundo crea un commit con código que no se empuja y comprueba que el job
correspondiente sigue en `failed` con el log intacto. Son tests significativos, no verdes triviales.

## Revisión funcional

`deskops/integrate.py` agrega `_resolve_failed(root, cfg, current)` y la invoca:

- en el camino `AlreadyIntegrated` (integrate que reporta «ya integrado»), cuando no es `--dry-run`;
- al final de un integrate con push exitoso, cuando no es `--dry-run` ni modo `pr`.

El barrido cumple el Implementation Path:

- lee `queue_dir(root)/failed/*.json` con `queue._read_job` y filtra `kind == "integrate"` con
  `task_id` no vacío;
- hace `git fetch` de `cfg.remote_url`/`cfg.branch` y toma `FETCH_HEAD` como tip remoto;
- busca el commit de cierre con `git log -1 --format=%H --grep=^Task-Id: <task_id>$ <cfg.branch>`;
- verifica `git merge-base --is-ancestor <sha> <FETCH_HEAD>`;
- solo si es ancestro mueve el JSON a `queue_dir(root)/done` y agrega al final de `job["log"]` la
  línea `resuelto por integrate <task actual>: <sha> ya en origin/<branch>`;
- si no hay commit de cierre o no es ancestro, deja el job en `failed`.

## Observación no bloqueante

En `mode: "pr"` el barrido no se dispara tras abrir el PR (solo en el camino «ya integrado»), por el
guard `cfg.mode != "pr"`. El desk real no declara `mode` y usa el default `push`, y la Validation y el
Done When describen un integrate que publica en la rama; no afecta la aceptación de esta tarea.

## Entorno

El `.venv` de `/mnt/ssd/proyectos/SLDB_1` está roto en este contenedor (apunta a un Python 3.12
ausente y su `python` resuelve a 3.11 sin pytest). Usé `/dev/shm/tester-venv/bin/python`
(Python 3.12.16, pytest 9.2.0) con `deskops` y `sldb` instalados en modo editable. No modifiqué el
repositorio ni los archivos del commit para la validación.
