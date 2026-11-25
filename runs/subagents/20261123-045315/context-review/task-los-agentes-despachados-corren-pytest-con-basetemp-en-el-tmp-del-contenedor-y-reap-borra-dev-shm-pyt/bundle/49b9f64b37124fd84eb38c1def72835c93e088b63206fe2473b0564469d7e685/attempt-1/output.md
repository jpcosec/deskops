REFORMULACION

Nodo ejecutable, no agregado. Propósito: evitar que los pytest de agentes despachados dejen `/dev/shm/pytest-of-scion`. Resultado: en `/mnt/ssd/proyectos/SLDB_1/deskops`, modificar `deskops/dispatch.py` y `tests/test_dispatch.py` para que el prompt de executor y tester incluya “Temporales de pytest” con `PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<nombre-real>"`; y que `dispatch reap`, tras borrar agentes, si `_list_agents` no muestra ningún `phase: running` en el proyecto, borre `SCION_PYTEST_TMP = /dev/shm/pytest-of-scion` —parcheable en tests— e imprima `limpieza: <ruta>`, sin tocarlo si queda alguno. Límites: fuera RoleDoc, templates de scion, validaciones existentes y basetemp de integrate; commit con `Task-Id`.

AMBIGUEDADES

1. “después de borrar agentes, si _list_agents no muestra ningún agente con phase running en el proyecto”: no define si limpia cuando no borró nada, cuando hubo conflicto/busy/error, ni si requiere rc 0. Obligaría a inventar la condición exacta.
2. “SCION_PYTEST_TMP = /dev/shm/pytest-of-scion, parcheable en tests”: no dice qué hacer si la ruta no existe o falla el borrado, ni si imprime siempre. Obligaría a inventar manejo de errores.
3. “exportar PYTEST_ADDOPTS="--basetemp=/tmp/pytest-<nombre del agente>"”: no aclara si reemplaza o preserva un `PYTEST_ADDOPTS` previo. Obligaría a inventar concatenación.
4. “antes de cualquier pytest”: ¿solo en el prompt o también en validaciones/comandos? El alcance excluye validaciones existentes; obligaría a inventar el alcance.
5. “el nombre real del agente”: no precisa si la sección se genera dinámicamente por agente o queda estática. Obligaría a inventar el punto de inyección.

DRY-RUN

Lecturas: TaskDoc, `deskops/dispatch.py`, `tests/test_dispatch.py`. Cambios previstos: añadir constante; texto de temporales con el nombre del agente; ajustar llamada a `_role_instructions`; en `reap`, segunda consulta a `_list_agents`, comprobación de `phase == "running"`, borrado e impresión `limpieza: <ruta>`; tres tests con scion falso y ruta parcheada. Dependencias: pytest, suite con `-n 4`, fake scion existente. Validaciones futuras: los dos comandos del TaskDoc y commit con trailer.

FUTURO

Otro nodo o humano ejecutará la implementación, correrá tests, revisará el diff y hará commit/integración; no es ambigüedad.
