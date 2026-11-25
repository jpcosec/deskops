## REFORMULACION
Encargo: en el repo `/mnt/ssd/proyectos/SLDB_1/deskops`, ampliar `SUBJECT_REF_PATTERN` en `deskops/models/review.py` para que el id de nodo admita punto (`dag.yaml#node:WS13.1`), replicarlo en el modelo `ReviewDoc` del store si declara el mismo patrón, y añadir tests en `tests/test_review_doc.py` y `tests/test_review_command.py` que prueben: validación con punto, rechazo con espacio o `#` extra, y que `deskops review node` escribe recibo en sandbox con un dag de prueba y el pi falso. Resultado: recibos de nodos con punto; ids inválidos siguen rechazados. Límites: no cambia formato de ids ni de `review_id`; si el punto colisiona en `review_id`, solo se informa.

## AMBIGUEDADES
1. «el modelo ReviewDoc del store si declara el mismo patron» — no se indica archivo ni módulo del store; obligaría a inventar la ruta y el nombre del modelo.
2. «si el punto choca en el review_id, se informa en el resultado sin cambiar su formato» — no define dónde ni cómo se informa (mensaje, campo, warning); obligaría a inventar el canal.
3. «con el pi falso que ya usan los tests» — no identifica fixture ni helper; obligaría a inventar cuál es y cómo se invoca.
4. «un dag.yaml de prueba que tenga un nodo con punto» — no se especifica ruta del sandbox ni estructura mínima; obligaría a inventar el layout.

## DRY-RUN
Lecturas: `deskops/models/review.py`, modelo `ReviewDoc` del store, `tests/test_review_doc.py`, `tests/test_review_command.py`, fixtures del pi falso. Cambios previstos: ampliar clase de caracteres del id de nodo para incluir `.` (manteniendo rechazo de espacio y `#`), espejo en store, tests de modelo y de comando. Dependencias: helpers de sandbox de tests existentes (`atom-cli-mutation-testing-uses-sandbox-desk-roots`) y commit con tests (`atom-code-changes-close-with-tests-and-commit`). Validaciones futuras: los dos comandos pytest de la Validation.

## FUTURO
Un ejecutor futuro inspecciona el store para localizar el patrón duplicado; un humano decide el canal de aviso de colisión de `review_id`; la validación final la ejecutan los pytest indicados.
