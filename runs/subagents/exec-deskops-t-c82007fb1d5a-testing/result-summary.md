PASA

# Resultado del tester

Tarea: `task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt`
Tester: `deskops-t-c82007fb1d5a` (role-deskops-tester)

## Commit del ejecutor

`0a40890cdfe7e7aa12af07ba6e17036a7cf2f796` — *dispatch: basetemp de pytest en /tmp del contenedor y limpieza de pytest-of-scion en reap*.
Trailer verificado: `Task-Id: task-los-agentes-despachados-corren-pytest-con-basetemp-en-el-tmp-del-contenedor-y-reap-borra-dev-shm-pyt`.

Archivos del commit:
- `deskops/dispatch.py`
- `tests/test_dispatch.py`

## Verificación contra el Goal

1. **Prompt con temporales de pytest en /tmp (executor y tester).**
   `start()` pasa el nombre real del agente a `_role_instructions` y este añade la sección
   `## Temporales de pytest` con `export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<agente>"`.
   Cubierto por `test_prompt_sets_pytest_basetemp_in_container_tmp` para ambos roles.

2. **Reap limpia /dev/shm/pytest-of-scion solo si no queda ningún agente vivo.**
   `SCION_PYTEST_TMP` es una constante de módulo (parcheable) con el valor
   `/dev/shm/pytest-of-scion`. Tras borrar los agentes, `_clean_scion_pytest_tmp` recorre
   `_list_agents` y solo elimina el directorio (e imprime `limpieza: <ruta>`) cuando ningún
   agente del proyecto sigue en phase `running` (ignorando los recién reapeados, que pueden
   aparecer aún en el listado). Si queda otro agente vivo, no toca el directorio.
   Cubierto por `test_reap_cleans_scion_pytest_tmp_when_no_agent_is_alive` y
   `test_reap_keeps_scion_pytest_tmp_while_an_agent_runs`.

## Tests ejecutados

- `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`
  → **49 passed**, 1 warning, exit 0 (incluye los 4 casos nuevos: 2 parametrizados + 2 de reap).
- `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py -k 'pytest_basetemp or scion_pytest_tmp'`
  → **4 passed**, 45 deselected, exit 0.

No se corrió la suite completa, según la instrucción del encargo para el tester.

Nota de entorno: la línea `../.venv/bin/python` del TaskDoc no es ejecutable en este contenedor
(`.venv/bin/python` resuelve a Python 3.11 y el venv está construido para 3.12, sin intérprete
3.12 disponible). Los tests se corrieron con `/dev/shm/t311/bin/python` (3.11, pytest 9.2.0,
con las dependencias del proyecto disponibles vía `PYTHONPATH` ya configurado). No se modificó
el repositorio para esto.

## Veredicto

Los tres tests nuevos (4 casos con parametrización) pasan y los 45 tests existentes de
`tests/test_dispatch.py` siguen verdes. **PASA.**
