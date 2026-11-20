PASA

# Resultado del tester

Tarea: task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de
Tester: deskops-t-674f356814bf

## Commit del ejecutor

`bdf06f810e1c045a139c17dc9e72f9a7904bb9e1` — "dispatch start: gate de memoria y limite por tarea en vez de uno por proyecto".
Trailer verificado: `Task-Id: task-dispatch-start-lanza-varios-agentes-en-paralelo-hasta-max-agents-y-con-el-gate-de-memoria-en-vez-de`.

Archivos del commit:
- `deskops/dispatch.py`: `start` consulta `wait_reason` de `deskops.queue` antes de lanzar y solo rechaza si el agente running pertenece a la identidad (`scion_child_identity`) de la misma tarea/rol; elimina el bloqueo por cualquier agente running del proyecto.
- `tests/test_dispatch.py`: reemplaza el test viejo por tres casos (otra tarea running permite lanzar, misma tarea running devuelve 3 con `ocupado: la tarea ya tiene agente`, memoria bajo el gate devuelve 3 con `ocupado: memoria ...`), y fija el gate de memoria en la config del fixture.
- `docs/operator-manual.md`: documenta el límite físico, los dos motivos de `ocupado` y el reintento de la cola con `retry_exit_codes: [3]`.
- `CHANGELOG.md`: entrada en Fixed.

## Pruebas ejecutadas

- `TMPDIR=/tmp /mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`
  -> **24 passed**, 1 warning, exit 0 (219.14 s).
- `TMPDIR=/tmp /mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_queue.py`
  -> **16 passed**, 1 warning, exit 0 (44.18 s). Se corrió además porque `dispatch.start` importa `wait_reason` de `deskops.queue`; `queue.py` no fue modificado por el commit.

No existe otro `tests/test_<modulo>.py` para módulos de código tocados: el único módulo de código del commit es `deskops/dispatch.py`, cubierto por `tests/test_dispatch.py`. No se corrió la suite completa (la corre integrate en el host).

## Falla antes / pasa después

En un worktree temporal sobre `bdf06f81^` (`e6081707`), con el `tests/test_dispatch.py` nuevo, los tres casos objetivos fallan:
- lanzar con otra tarea running -> `ocupado: other-agent` (returncode 3 en vez de 0),
- misma tarea running -> mensaje viejo `ocupado: <name>` sin `la tarea ya tiene agente`,
- memoria bajo el gate -> lanza igualmente (returncode 0 en vez de 3).

`3 failed` en 37.18 s. Con el commit actual esos mismos casos pasan dentro de los 24 tests. El worktree temporal se eliminó; no se modificó el repo.

## Entorno

`python` no está en PATH y el `.venv` de `/mnt/ssd/proyectos/SLDB_1` apunta a un Python 3.12 ausente; se usó `/mnt/ssd/proyectos/SLDB_1/sldb/.venv/bin/python` (3.13.18, pytest 9.1.1), equivalente a `/workspace/sldb/.venv/bin/python`.

## Observaciones no bloqueantes

- El gate de memoria se consulta antes de listar agentes, de modo que una máquina bajo presión devuelve `ocupado: memoria ...` incluso si la tarea ya tuviera un agente; es coherente con el orden pedido y con los tests.
- El chequeo por prefijo cubre también el intento `-a2` de la misma identidad, que es el comportamiento esperado.
