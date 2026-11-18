## REFORMULACION

El nodo debe implementar en el repo `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`): (a) corregir `dispatch.reap` para calcular la etiqueta del agente con `_scion_task_label(task_id)` en vez de leer el TaskDoc, manteniendo stop/delete y códigos de retorno; (b) ajustar el `prompt.md` del rol executor para commitear rutas nombradas con trailer `Task-Id` y sin push; (c) ajustar el `prompt.md` del rol tester para localizar el commit por `Task-Id`, correr solo los tests tocados, de a uno y con `TMPDIR=/tmp`, y dejar veredicto `PASA`/`FALLA`. Resultado esperado: reap funciona tras el cierre, el ejecutor entrega un commit trazable y el tester entrega informe dentro del límite. Límites: no cambiar la cola ni `integrate`; este preflight solo usa el TaskDoc y no ejecuta nada.

## AMBIGUEDADES

1. Cita: “mismo criterio de terminado (phase, activity, result-summary.md)”. Obligaría a inventar los valores exactos de `phase`/`activity` y el contenido mínimo de `result-summary.md`.
2. Cita: “‘vivo’ y rc 4 si queda alguno vivo” y “ese caso también da rc distinto de 0”. Obligaría a inventar la precedencia entre rc 4 y el rc de error de stop/delete, y el código exacto para este último.
3. Cita: “los mismos que lista en result-summary.md”. Obligaría a inventar el formato/sección de esa lista y cómo derivarla para el commit.
4. Cita: “entrega su informe dentro del límite”. Obligaría a inventar la duración máxima concreta del tester.
5. Cita: “El tester escribe result-summary.md”. Obligaría a inventar la ruta exacta y si sobrescribe un archivo existente.

## DRY-RUN

Lecturas previstas: TaskDoc; `deskops/dispatch.py` (`def reap`); `deskops/runtime/scion.py:224`; generadores de `prompt.md` de `dispatch start`; `tests/test_dispatch.py`; `docs/operator-manual.md`; `CHANGELOG`. Cambios previstos: test rojo de reap con TaskDoc borrado y scion simulado; sustitución de la etiqueta; tests de los textos de prompt por rol e implementación; docs/changelog. Dependencias: `_scion_task_label`, convenciones existentes de stop/delete y rc, plantillas de prompt y fixtures de scion. Validaciones futuras: `TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py`; suite completa por `integrate`.

## FUTURO

Otro nodo implementador producirá código, tests y documentación; `integrate` ejecutará la suite completa en el host y cerrará la tarea. La cola y `dispatch` no se modifican.
