REFORMULACION
Encargo ejecutable de tipo `task.debug` en el repo `deskops`. Propósito: corregir el fallo de integración en `tests/test_dispatch.py::test_reap_scion_error_continues_and_fails`, donde el subproceso de reap imprime y borra `/dev/shm/pytest-of-scion` real porque `SCION_PYTEST_TMP` no se hereda parcheado. Resultado esperado: `dispatch reap` resuelve la ruta de limpieza con `os.environ.get('DESKOPS_SCION_PYTEST_TMP', SCION_PYTEST_TMP)`; el fixture `Env` apunta esa variable a `tmp_path/'pytest-of-scion'`; ningún test toca el `/dev/shm` real y la salida no depende del host. Límites: solo `deskops/dispatch.py` y `tests/test_dispatch.py`.

AMBIGUEDADES
1. «SCION_PYTEST_TMP es una constante» frente a «por defecto /dev/shm/pytest-of-scion»: no aclara si la constante debe mantenerse, renombrarse o eliminarse; obligaría a inventar la estructura interna de `dispatch.py`.
2. «Ajustar los tests de limpieza para usar esa ruta»: no identifica qué tests ni qué aserciones; obligaría a inventar el alcance exacto de los cambios en la suite.
3. «el fixture Env de tests/test_dispatch.py»: no da su firma ni si comparte entorno con subprocesos; obligaría a inventar cómo se propaga `DESKOPS_SCION_PYTEST_TMP`.
4. «test_reap_scion_error_continues_and_fails no imprime limpieza»: no especifica el mecanismo de comprobación; obligaría a inventar si se asserta salida, fichero o retorno.

DRY-RUN
Lecturas hipotéticas: `dispatch.py` (constante, función de reap/limpieza), fixture `Env`, tests de limpieza y `test_reap_scion_error_continues_and_fails`. Cambios previstos: sustituir la ruta fija por lectura de entorno en el punto de limpieza; fijar `DESKOPS_SCION_PYTEST_TMP` en el fixture; ajustar aserciones afectadas. Dependencias: `pytest`, `tmp_path`, herencia de entorno por `subprocess`. Validaciones futuras, sin ejecutar: `mkdir -p /dev/shm/pytest-of-scion && pytest -q tests/test_dispatch.py && test -d /dev/shm/pytest-of-scion`; además, comprobar que no aparece el borrado del directorio real.

FUTURO
Otro nodo o un humano deberá decidir el commit, aceptar el cambio y rerun del integrate; no son ambigüedades del encargo.
