## REFORMULACION
CC33 es un agregado de PF2 (`node_role: aggregate`): no se ejecuta; termina cuando cierran sus hijos. Encargo: que el cierre de deskops sea regla sobre recibos de evidencia y que en código solo queden productores de hechos de git y archivos, en el repo deskops. Resultado: (1) `closeout verify` escribe `ReviewDoc kind: evidence` por kind, con idempotencia; (2) `RuleDoc` semilla de cierre por tipo y de campos; (3) se borran la inyección de hechos y `verify` como evaluador; (4) el grafo lee `sldb graph project` (GD21). Límites: no escribe en sldb, no suple reglas con Python, no cambia formato ni CLI, borra el código viejo en el mismo paso. Depende de CC32 y CC38; gates GO06/GO08/GD21 satisfechos; aceptación por escenarios, greps, goldens, doctor en 6 desks y paridad con el oráculo v1.

## AMBIGUEDADES
1. «una verificación repetida sin cambios no crea un recibo nuevo (mismo input_sha256)»: no se define qué se hashea (¿payload de la tarea, valor del hecho, ambos?); obliga a inventar el dominio del hash y cuándo dos verificaciones son «sin cambios».
2. Aceptación: «dan lo mismo que el oráculo v1 … y después tests/graph_oracle_v1/ se borra» frente a DO8: «declared_target_is_a_file y su test quedan (b15) … Ambos esperan a sldb H1-H2». Obliga a inventar si la paridad excluye esos casos o si el borrado se difiere.
3. «por cada kind de evidencia verificado … fact = <kind> (tests | commit | atom | materialization | document | external)»: no empareja explícitamente productores y kinds; obliga a inventar de qué productor salen `document` y `external`.

## DRY-RUN
Agregado: no se ejecuta; termina con CC33a/b/c. Un ejecutor futuro leería `closeout_gates.py`, `operations.py`, `task_types.py`, `desk_graph.py` y los tests de closeout y grafo; escribiría recibos, reglas y borrados; validaría con escenarios, greps, goldens, doctor en 6 desks y paridad con el oráculo v1. Dependencias: CC32 (reglas de activación), CC38 (inventario de chequeos entre documentos), gates satisfechos. Los hijos no están en el input (solo ids): no puedo trazar qué transfiere cada uno; CC33 declara cuatro frentes (1)-(4) y su aceptación valida el conjunto.

## FUTURO
CC33b decide si `closeout commit` escribe recibos antes de leerlos (DO6); los TaskDoc de CC33a/b/c fijan el reparto; sldb H1-H2 cubre los casos del grafo (DO8); CC34 consume los recibos evidence (DA1).
