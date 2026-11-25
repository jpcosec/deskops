PASA

# Result summary

Commit revisado: `3b9d6f5ed73c6556c34c2801a3f4c8da01f955b5` ("dispatch reap: encola dispatch-tester tras integrar un ejecutor"), con trailer `Task-Id: task-el-reap-del-intento-n-de-un-ejecutor-encola-el-tester-aunque-la-tarea-ya-este-en-ritual-testing`. Toca solo `deskops/dispatch.py` (+27) y `tests/test_dispatch.py` (+51).

## Verificación de la implementación

- `reap()` marca `integrated = True` únicamente cuando se reapea un ejecutor y `_integrate_branch(...)` devuelve `code == 0`; si la integración falla no se marca.
- Dentro del bucle solo marca `tester_alive = True` para agentes con `labels.deskops.role == "tester"` que quedan vivos (`sin reason`, el caso que imprime `vivo`). Un tester terminado y reapeado no bloquea el encolado.
- Al final, antes de los `return`, si `integrated and not tester_alive` y no existe ya un job `dispatch-tester` del mismo `task_id` en `runs/queue/{pending,running}`, llama a `queue.enqueue(root, "dispatch-tester", task_id, "reap")` e imprime `encolado: dispatch-tester`.
- `_tester_queued()` reutiliza `queue.queue_dir`, `queue._jobs` y `queue._read_job` y deduplica por `kind == "dispatch-tester"` + `task_id`, sin importar el intento. También comprueba que el kind esté declarado en `queue_jobs`, evitando el `UsageError` de `enqueue`.
- No se tocó la máquina de estados de rituales ni otros módulos.

## Tests ejecutados

Entorno: el `pytest` del host no estaba instalado. Se usó el Python 3.13 de la tool venv de deskops (`/home/scion/.local/share/uv/tools/deskops/bin/python`) con pytest instalado en `/tmp/pytest-deskops-deps` y `PYTHONPATH` apuntando al repo y a `/workspace/sldb/src`.

- `tests/test_dispatch.py` completo: **52 passed** (499.91 s).
- Casos nuevos aislados (`-k 'enqueues_the_tester or does_not_duplicate_a_pending_tester or does_not_enqueue_the_tester'`): **3 passed** (41.37 s).

La validación pedía `TMPDIR=/mnt/ssd/tmp/sldb1`, pero `/mnt/ssd/tmp` no existe y `/mnt/ssd` no es escribible por el usuario `scion`; se usó `TMPDIR=/tmp` junto con `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-8e7688cc843a`, sin afectar el resultado de los tests.

## Cobertura de los casos exigidos

- (a) ejecutor reapeado e integrado sin tester pendiente -> queda exactamente un JSON `dispatch-tester` en `runs/queue/pending` con el `task_id`.
- (b) tester ya pendiente -> no se duplica (sigue habiendo uno y no aparece `encolado`).
- (c) `_integrate_branch` falla (conflicto) -> `reap` devuelve 8 y no se encola ningún tester.

## Pendiente para integración

No se ejecutó la suite completa: la corre el host, según la instrucción del tester.
