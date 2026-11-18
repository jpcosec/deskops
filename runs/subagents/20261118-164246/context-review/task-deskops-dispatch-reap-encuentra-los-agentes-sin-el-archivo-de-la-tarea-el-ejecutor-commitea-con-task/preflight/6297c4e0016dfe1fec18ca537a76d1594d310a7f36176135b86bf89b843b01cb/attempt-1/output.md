## REFORMULACION

Propósito: corregir tres fallos de la primera corrida real del despacho automático en el repo `deskops` (`/mnt/ssd/proyectos/SLDB_1/deskops`). Resultado: (a) `dispatch.reap` encuentra y borra agentes aunque el TaskDoc ya no exista; (b) el prompt del ejecutor ordena commit con rutas nombradas y trailer `Task-Id`, sin push, antes de `deskops advance`; (c) el prompt del tester limita los tests a los archivos tocados y exige `result-summary.md` con PASA/FALLA. Límites: no cambiar la cola ni `integrate`; incluye tests, `docs/operator-manual.md` y CHANGELOG. Validación: `TMPDIR=/dev/shm python -m pytest -q tests/test_dispatch.py`; la suite completa la corre `integrate`.

## AMBIGUEDADES

1. «usa el id de la tarea (hash de deskops.task_id calculado del id)»: no define algoritmo ni formato del hash; obligaría a inventar la función y la representación exacta de la etiqueta.
2. «solo los tests de los archivos del diff del commit del ejecutor»: no indica cómo obtiene el tester el commit/diff ni el criterio archivo→test; obligaría a inventar el mecanismo de selección.
3. «commit de código con rutas nombradas»: no aclara si deben enumerarse todas las rutas modificadas o solo las del cambio; obligaría a fijar una política.
4. «detiene y borra los agentes de la tarea igual»: no precisa orden ni comportamiento si `stop` falla; obligaría a inventar manejo de errores.

## DRY-RUN

Lecturas: TaskDoc, `tests/test_dispatch.py`, código de `dispatch.reap` y del generador de prompts, `docs/operator-manual.md` y CHANGELOG. Cambios previstos: p1 test que falla con TaskDoc ausente; p2 fallback por `deskops.task_id`; p3 tests e implementación de textos de prompt para executor/tester; p4 documentación y CHANGELOG. Dependencias: simulación de scion, APIs existentes de dispatch, sin tocar cola ni `integrate`. Validaciones futuras: el pytest indicado y, después, suite completa por `integrate`. Sin ejecutar nada.

## FUTURO

El nodo integrador ejecuta la suite completa y confirma el Done When; el operador valida la primera corrida real y revisa docs/CHANGELOG. El ejecutor futuro produce el commit con `Task-Id` antes de `deskops advance`.
