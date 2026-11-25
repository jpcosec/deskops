## REFORMULACION

Encargo ejecutable de tipo `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`. Propósito: adaptar los tests de review al subject pinneado (`doc:TaskCodeDoc:<id>@sha256:<hash>`) que `create_document` de sldb escribe ahora al registrar recibos. Resultado: los tres tests citados pasan contra el sldb instalado y el diff solo toca `tests/test_review_record.py` y `tests/test_review_command.py`. Límites: no se modifica código de `deskops/`, ni sldb, ni otros tests, ni aserciones ajenas a `subject`; si un test falla por otra causa, se detiene y se informa.

## AMBIGUEDADES

1. «la misma forma que ya usa la aserción de la línea 266 de tests/test_review_record.py» — la línea puede haberse desplazado; obliga a inventar cuál aserción sirve de modelo si no coincide.
2. «donde el test ya compara con el id completo de la tarea, usar re.escape del valor esperado» — en `test_a_short_selector_keys_and_anchors_receipts_on_the_full_task_id` no se aclara si el `<id>` del ancla es el completo o el selector corto; obliga a inventar el valor esperado.
3. «Cada asercción de igualdad exacta con 'doc:TaskCodeDoc:<id>'» — no especifica si en `test_review_command.py` hay subjects con otro modelo o id; obliga a inventar el alcance exacto.
4. «El docstring ... se corrige: sldb pinnea al crear y al guardar» — no da el texto ni dice si otros docstrings mencionan pinning; obliga a inventar redacción.

## DRY-RUN

Hipotético, sin ejecutar: (1) lectura de ambos tests, del docstring y de la aserción de la línea 266; (2) ejecución de los dos archivos para guardar fallos esperados por subject sin pin; (3) sustitución de igualdades exactas por `re.fullmatch(r'doc:TaskCodeDoc:<id>@sha256:[0-9a-f]{64}', subject)`, con `re.escape` si aplica; (4) corrección del docstring. Dependencias: sldb de `origin/main` en `477d1bc0`, intérprete `../.venv/bin/python`, `TMPDIR=/dev/shm`. Validaciones futuras: los dos `pytest -q` y `git diff --stat` limitado a los dos archivos.

## FUTURO

Un nodo de cierre/revisión verifica el diff y decide el commit (átomo `atom-code-changes-close-with-tests-and-commit`), que esta tarea no ordena explícitamente. La corrección en sldb ya está hecha y no se transfiere aquí.
