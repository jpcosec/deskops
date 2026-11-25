## REFORMULACION
Nodo ejecutable de depuración: corregir `reap(root, task_id)` en `deskops/dispatch.py` para que, tras integrar correctamente el commit de un ejecutor, se encole `dispatch-tester` si no existe tester vivo ni trabajo pendiente/en ejecución de ese tipo para la tarea, sin depender del número de intento. Repo: `/mnt/ssd/proyectos/SLDB_1/deskops`. Límite: solo `dispatch.py` y `tests/test_dispatch.py`; no tocar la máquina de estados de rituales. Resultado: cambio en reap, deduplicación por `task_id` y `kind`, mensaje `encolado: dispatch-tester`, y tests (a), (b), (c).

## AMBIGUEDADES
1. “si no hay un tester vivo ni pendiente” y “agente con labels deskops.role == 'tester' que quedo como 'vivo'”: no define cómo determinar “vivo” ni si incluye agentes en ejecución. Obligaría a inventar el criterio exacto.
2. “Al final de reap, antes de los return”: no especifica cuántos `return` existen ni qué rutas de salida deben cubrirse. Obligaría a inventar la ubicación y el flujo exactos.
3. “reutilizar queue._jobs y queue._read_job”: no da firmas, parámetros ni forma de retorno. Obligaría a inventar o asumir la API interna.
4. “siguiendo los fakes de scion que ya usa ese archivo”: no describe las fixtures ni su comportamiento. Obligaría a inventar el setup de pruebas.

## DRY-RUN
Nodo ejecutable, no agregado. Lecturas previstas: `dispatch.py` (`reap`, `_integrate_branch`), módulo `queue` (`enqueue`, `_jobs`, `_read_job`), hook de lifecycle citado y `tests/test_dispatch.py` con sus fakes. Cambios previstos: marcar `integrated = True` cuando un ejecutor se integre con código 0; tras el bucle, comprobar ausencia de tester vivo y de `dispatch-tester` pendiente/en ejecución por `task_id`; llamar `queue.enqueue(root, 'dispatch-tester', task_id, 'reap')` e imprimir `encolado: dispatch-tester`. Dependencias: semántica real de `_integrate_branch`, helpers de cola y fixtures existentes. Validación futura: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_dispatch.py`, verificando los casos (a), (b) y (c).

## FUTURO
Un nodo ejecutor producirá el parche y los tests. Un nodo de validación ejecutará la prueba indicada. Un humano decidirá la aceptación final o resolverá el criterio de “tester vivo” si sigue sin estar definido.
