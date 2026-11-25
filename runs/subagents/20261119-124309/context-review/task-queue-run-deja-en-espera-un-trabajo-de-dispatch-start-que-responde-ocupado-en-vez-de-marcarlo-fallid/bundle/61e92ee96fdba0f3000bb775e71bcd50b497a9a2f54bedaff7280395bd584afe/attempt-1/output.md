## REFORMULACION
Nodo ejecutable (`task.code`) del repo **deskops**. Propósito: corregir `queue run` para que un trabajo cuyo comando sale con el código 3 —interpretado por `dispatch start` como “ocupado”— quede en `pending` para la próxima corrida, imprima `en espera: <id> ocupado` y continúe o se detenga sin fallar; cualquier otro código distinto de 0 sigue siendo fallo. Resultado esperado: cambio en `deskops/queue.py`, test en `tests/test_queue.py`, campo opcional `retry_exit_codes` por tipo de trabajo en `queue_jobs` (lista de enteros, default vacío), documentación en `docs/operator-manual.md` y `CHANGELOG`, y commit con rutas y `Task-Id`. Límites: no cambiar los códigos de dispatch; la incorporación de `[3]` a configuraciones y la suite completa quedan fuera de este nodo.

## AMBIGUEDADES
1. “sigue con el resto (o se detiene sin fallar)”: obliga a inventar la política de control del bucle; ambas conductas son válidas y afectan el test.
2. “igual que con los gates de memoria”: obliga a inferir un comportamiento existente no descrito en el bundle; no se especifica salida ni flujo exacto.
3. “un campo opcional por tipo de trabajo en queue_jobs”: obliga a inventar la forma exacta del esquema, su clave de búsqueda y si requiere migración.
4. “en la configuración de los desks dispatch-executor y dispatch-tester con [3]” frente a “el integrador agrega retry_exit_codes a los config.json de deskops, sldb e IR”: obliga a decidir qué archivos y claves concretas corresponden, y si este nodo los toca.

## DRY-RUN
Sin ejecutar: leer el TaskDoc, `queue.py`, `tests/test_queue.py`, el esquema/configuración de `queue_jobs`, la implementación de gates de memoria, `docs/operator-manual.md` y `CHANGELOG`. Añadir primero un test que falle: código 3 con `retry_exit_codes: [3]` deja el trabajo en `pending` sin nota `unclear`; otro código no listado va a `failed`. Implementar la consulta del campo con default vacío y el tratamiento del código en `queue run`. Actualizar docs y CHANGELOG. Dependencias: semántica del código 3, esquema de `queue_jobs` y comportamiento de gates. Validación futura: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_queue.py`; después, suite completa de deskops.

## FUTURO
El integrador añadirá `retry_exit_codes` a los `config.json` de deskops, sldb e IR tras integrar, y ejecutará la suite completa. El commit deberá incluir rutas nombradas y `Task-Id`.
