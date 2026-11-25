REFORMULACION
CC33b es un nodo de entrega (no agregado), hijo de CC33, repo dueño deskops. Propósito: pasar el cierre y las reglas de campo a configuración sldb: RuleDocs semilla por tipo sobre `task_completes` que exigen recibos evidence de CC33a, reglas `on_check/on_write alert` para cinco campos y los 9 chequeos entre documentos del inventario CC38. Resultado: sin recibo `commit` accepted, `task_completes` bloquea con `fact = "commit"`; editar `goal` rebloquea; se borran `_add_closeout_facts`, `closeout_evidence_verified`, `pill_graduation_verified`, `has(closeout_evidence_verified)` y `__closeout_evidence__`; docs, ritual y CHANGELOG. Límites: no escribe en sldb ni implementa evaluadores Python; depende de CC33a y G_GO06/G_GO08, ya satisfechos.

AMBIGUEDADES
1. “CC33b decide si `closeout commit` escribe recibos antes de leerlos con las reglas” (DO6). El scope y la aceptación no fijan esa decisión ni su efecto; obliga a inventar si `closeout commit` escribe recibos o solo lee los de `closeout verify`.
2. “exige los recibos evidence de CC33a (atom|materialization como or de dos)” choca con DO6: “Si el link gate pasa sin documento enlazante ... no se escribe recibo atom ni materialization”. Obliga a inventar la excepción o a contradecir DO6.
3. “las reglas sobre campos pasan a RuleDocs on_check/on_write alert” no tiene aceptación específica; “tests de closeout verdes” no fija disparador, sujeto ni alerta esperada de esas cinco reglas.

DRY-RUN
Un ejecutor leería dag/decisiones, recibos de CC33a, inventario de CC38, `__closeout_evidence__` actuales, semillas de `task_lifecycle` y tests de closeout. Crearía RuleDocs en `deskops/data/rules/`; ajustaría `task_types.py`, `operations.py`, `tasks.py`, `closeout_gates.py`, `lifecycle.py`; actualizaría docs, ritual y CHANGELOG. Verificaría `edges_blocked` con `fact = "commit"`, rebloqueo al editar `goal`, grep vacío, tests verdes, goldens idénticos y `doctor` en los 6 desks. Sin ejecutar.

FUTURO
CC33a entrega los recibos evidence; CC38 su inventario de 9 chequeos; el supervisor corre la suite completa; el operador promueve el TaskDoc. Las gates ya están satisfechas. DO6 no es futuro: asigna una decisión a este nodo.
