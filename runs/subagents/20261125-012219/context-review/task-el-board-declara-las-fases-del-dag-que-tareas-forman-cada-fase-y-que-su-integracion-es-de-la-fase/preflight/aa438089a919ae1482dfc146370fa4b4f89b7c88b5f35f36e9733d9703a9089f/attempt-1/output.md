## REFORMULACION

Propósito: que el Board declare las fases del DAG, indicando qué tareas componen cada fase y que la integración corresponde a la fase. Resultado: `BoardDoc` con un campo de fases —id, lista de tareas e integración de fase—, validación de que una tarea pertenece a una sola fase, marcador en el template y test de round-trip con dos fases. Repo: `deskops`, con cambios previstos en `deskops/models/board.py`, el template del Board y `tests/test_board_phases.py`. Límites: solo modelo y template; quedan fuera CLI, vista, `integrate` y skill.

## AMBIGUEDADES

1. «el template del Board con el marcador de fases»: no se nombra el archivo exacto del template; obligaría a inventar su ruta.
2. «integracion de la fase (validacion combinada y commit de cierre de fase)»: no se define la forma de representar `integration` en el modelo ni en el marcador; obligaría a inventar su esquema.
3. «El modelo valida que una tarea este en una sola fase.»: no aclara si una tarea repetida dentro de la misma fase también falla; obligaría a inventar ese caso.
4. «Leer ritual-phase y pill-007-phase-gated-task-flow para el vocabulario.»: no se indican rutas ni artefactos concretos; obligaría a inventar dónde leerlos.
5. «round-trip por sldb»: no se especifica el formato de serialización ni el fixture esperado; obligaría a inventar detalles del round-trip.

## DRY-RUN

Lecturas: `deskops/models/board.py`, template del Board, test existente o convenciones de tests, `ritual-phase` y `pill-007-phase-gated-task-flow`. Cambios previstos: añadir `phases` a `BoardDoc`; insertar marcador de fases en el template; validar pertenencia única de tareas; crear `tests/test_board_phases.py` con dos fases y caso de tarea repetida. Dependencias: esquema de `BoardDoc`, parser/render del template y utilidades de round-trip de `sldb`. Validación futura: `TMPDIR=/mnt/ssd/tmp/sldb1 pytest -q tests/test_board_phases.py`. No se ejecuta nada.

## FUTURO

Otros nodos harán el comando CLI, la vista del Board, `integrate` y el skill. Un humano decide la aceptación final del cambio y si el resultado cumple el encargo.
