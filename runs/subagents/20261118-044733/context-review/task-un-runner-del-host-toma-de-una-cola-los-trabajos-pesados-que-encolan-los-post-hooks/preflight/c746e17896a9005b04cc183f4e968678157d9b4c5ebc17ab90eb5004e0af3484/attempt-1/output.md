REFORMULACION
Nodo ejecutable (`task.code`). Propósito: que los trabajos pesados que encolan los post-hooks —suite completa, integración, push— corran en el host y de a uno, porque dentro del contenedor scion no están el cerrojo de tests, el control de memoria ni las credenciales de push. Resultado: grupo `deskops queue` con `add`, `run` y `list`; tres campos nuevos en `DeskConfig`; cola de archivos JSON en `runs/queue`; `deskops/queue.py`; registro en `deskops/cli/registry.py`; `tests/test_queue.py`; sección `Host queue` en el manual. Repo: checkout principal de deskops, sin worktree, rama, `git add` ni `git commit`. Límites: solo los archivos del Scope; no tocar los cinco archivos ya modificados por otros; fuera servicio o timer permanente, comandos que lancen agentes o hagan push, declarar `queue_jobs` en desks reales y cambios en sldb.

AMBIGUEDADES
1. «sin id de tarea sale con codigo 2»: no dice qué ocurre si falta solo `--transition`; obliga a inventar si es error, cadena vacía u otro código.
2. «con la misma funcion que usa `deskops message send`»: no nombra la función ni el formato exacto; obliga a inferirlo del código.
3. «no se registra en el store»: «store» no está definido; obliga a inventar a qué almacén se refiere.
4. «hasta que no queden pendientes o uno falle»: no fija el código de salida de `--all` al fallar; obliga a decidir válvula.
5. «Si el cambio deja codigo o tests sin ninguna referencia, se borran»: no define «referencia»; obliga a inventar el criterio.
6. «aviso de termino»: no describe mecanismo; obliga a inventarlo.

DRY-RUN
Lecturas: `deskops/config.py`, `deskops/cli/registry.py`, la función de inbox usada por `message send`, tests vecinos y `docs/operator-manual.md`. Cambios previstos: añadir los tres campos a `DeskConfig`; crear `deskops/queue.py` con encolar, correr y listar, usando `fcntl.flock`, gates de `/proc`, `subprocess.run` sin shell, logs y notas de fallo; registrar el grupo en `registry.py`; crear `tests/test_queue.py`; añadir la sección al manual. Dependencias: patrón de grupos vecinos, función de inbox de message, disponibilidad de `/proc/meminfo` y `/proc/pressure/memory`, `flock`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q` sobre el archivo nuevo; `pytest -q tests/test_lifecycle_graph.py`; `deskops queue --help` y ayudas de subcomandos; `deskops graph missing --root .`.

FUTURO
Otra tarea consumirá la cola para lanzar suites e integración y hacer push. Un humano declarará `queue_jobs` y hooks en desks reales, revisará el cambio y decidirá el commit, que está fuera de alcance. `deskops advance task` de esta tarea emitirá el aviso de término.
