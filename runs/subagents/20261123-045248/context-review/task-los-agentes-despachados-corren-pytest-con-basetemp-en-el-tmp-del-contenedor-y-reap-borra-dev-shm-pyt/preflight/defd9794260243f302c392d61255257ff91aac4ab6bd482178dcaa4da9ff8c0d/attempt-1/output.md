## REFORMULACION

Propósito: evitar que los pytest de agentes despachados dejen temporales en `/dev/shm` del host y que `reap` los limpie cuando no queden agentes vivos. Resultado: en el repo `deskops`, `deskops/dispatch.py` debe generar para executor y tester una sección “Temporales de pytest” que ordene `export PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<nombre real del agente>"` antes de cualquier pytest; y `dispatch reap`, tras borrar agentes, si `_list_agents` no muestra ningún agente con phase running en el proyecto, debe borrar `SCION_PYTEST_TMP=/dev/shm/pytest-of-scion` —constante parcheable— e imprimir `limpieza: <ruta>`; si queda uno vivo, no tocarlo. Añadir tres tests en `tests/test_dispatch.py`. Límites: solo `dispatch.py` y `test_dispatch.py`; fuera RoleDoc, templates de scion, validaciones existentes y el basetemp de integrate, que es tarea hermana. Cierre: los tres tests nuevos y los existentes de `test_dispatch.py` en verde.

## AMBIGUEDADES

1. “con el nombre real del agente”: no se define de dónde se obtiene ni si se sanea para una ruta `/tmp`. Obligaría a inventar fuente y política de saneamiento.
2. “si _list_agents no muestra ningún agente con phase running en el proyecto”: no se define qué proyecto ni el esquema de `_list_agents`. Obligaría a inventar filtro y campos.
3. “después de borrar agentes”: no aclara si se comprueba tras cada borrado o al final de `reap`. Obligaría a inventar la secuencia.
4. “imprime ‘limpieza: <ruta>’”: no indica stdout/stderr, logger ni formato exacto. Obligaría a inventar canal y formato.
5. “exportar PYTEST_ADDOPTS=...”: no aclara si sobrescribe o concatena un valor previo. Obligaría a inventar esa semántica.

## DRY-RUN

Lecturas: `deskops/dispatch.py` (`_role_instructions`/`_base_instructions`, `reap`, `_list_agents`) y `tests/test_dispatch.py`. Cambios previstos: tests primero con scion falso; sección de prompt para executor y tester; constante, borrado condicional e impresión en `reap`. Dependencias: pytest y fixtures existentes; sin librerías nuevas. Validaciones futuras, sin ejecutar: pytest de `tests/test_dispatch.py` con `TMPDIR=/dev/shm`; suite completa con `-n 4`; commit con `Task-Id`.

## FUTURO

El ejecutor futuro implementará, ejecutará las validaciones y commiteará desde el worktree. Un humano u otro nodo aprobará el TaskDoc y decidirá las ambigüedades. La tarea hermana de integrate cubrirá `pytest-of-robocop`; el integrador validará el resultado conjunto.
