## REFORMULACION

Propósito: eliminar la serialización por proyecto scion en `dispatch start`. Resultado: lanzar un agente si pasa el gate de memoria (`disponible >= queue_min_available_gb` y `PSI avg60 < queue_max_psi_avg60`) y no hay agente running de la misma tarea; si no, salir con `EXIT_BUSY (3)` y motivo. Repo: `deskops`. Límites: dentro `deskops/dispatch.py` (start), `tests/test_dispatch.py`, `docs/operator-manual.md` y `CHANGELOG`; fuera tope configurable, `queue.py` salvo importar `wait_reason`, scion y `config.json` de desks. Es una tarea `task.code` ejecutable por un futuro ejecutor; esta revisión no ejecuta nada.

## AMBIGUEDADES

1. Título: “hasta max-agents” frente a Goal: “No hay tope configurable de agentes: el límite es físico.” Obliga a decidir si `max-agents` es residual/ignorado o si se conserva como tope existente; el Scope solo excluye agregarlo.
2. “por el prefijo de identidad de scion_child_identity de esa tarea” no define cómo se construye ni compara el prefijo. Obliga a inventar formato y función.
3. “reusando wait_reason” y “queue.py salvo importar wait_reason” no fijan firma ni retorno. Obliga a inventar si devuelve motivo, booleano o tupla.
4. “con _list_agents y el estado de memoria simulados” no da contrato de `_list_agents` ni punto de mock. Obliga a inventar dobles si no se lee el código.

## DRY-RUN

Lecturas: TaskDoc, `dispatch.py:144-147`, `wait_reason` en `queue.py`, `tests/test_dispatch.py`, documentación, CHANGELOG y helper de identidad. Cambios previstos: p1 tests rojos para los tres casos; p2 sustituir el bucle por gate de memoria y exclusión de misma tarea, con `EXIT_BUSY` y mensajes; p3 docs/CHANGELOG; p4 commit con rutas y `Task-Id`. Dependencias: `wait_reason`, `_list_agents`, `scion_child_identity`, `EXIT_BUSY`, pytest/TMPDIR. Validación futura: ejecutar `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py`; la suite completa la corre `integrate`.

## FUTURO

`integrate` ejecuta la suite completa; revisión humana/merge resuelve el título `max-agents` y acepta el commit; operación observa la cola real.
