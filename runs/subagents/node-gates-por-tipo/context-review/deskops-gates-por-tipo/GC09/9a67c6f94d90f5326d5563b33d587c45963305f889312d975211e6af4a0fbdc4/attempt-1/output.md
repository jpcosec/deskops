## REFORMULACION
GC09 es un nodo de entrega (`kind: code`, `delivery`) del plan gates-por-tipo, repo deskops, hijo de PC03. Propósito: composición real de tareas. Resultado: `parent_id`/`children` en TaskDoc, `add task --parent` transaccional que exige padre `task.aggregate`, alerta de `doctor`, regla de activación del agregado, evidencia de cierre `children` verificada por `closeout verify`, y `show`/`next` con relaciones. Límites: no reimplementa el evaluador, no escribe en sldb salvo `message send`, no cambia la autoridad de cierre. Depende de GC01 y GC05; requiere G_SLDB_LANG.

## AMBIGUEDADES
1. "nonempty(children) and count(children: status != "closed") = 0 (DC6: los hijos cerrados fueron borrados y no cuentan; uno abierto cuenta)". Si los hijos cerrados se borran y sldb los omite, `nonempty` sería falso al cerrar todos, contra la acceptance; obliga a inventar si lee la lista cruda o los documentos resueltos.
2. "o está en desk/tasks con status closed". DC6 y alcance dicen que el cierre borra el archivo: la alternativa es inalcanzable; obliga a decidir si se implementa, se ignora o contradice DC6.
3. "el ritual de testing para un agregado es la validación conjunta de la fase (phase.md)". `phase.md` no está en el input y "validación conjunta" no se define; obliga a inventar el ritual y su criterio.
4. "doctor alerta cuando parent_id y children no se corresponden". La acceptance solo prueba una dirección (hijo con parent_id ausente de children); obliga a inventar si se comprueba también la inversa.

## DRY-RUN
Lecturas: task.py, task_types.py, tasks.py, closeout_gates.py/closure.py, rules.py, doctor_findings.py, CLI y fixtures. Cambios: campos y referencias en TaskDoc; transacción `--parent`; validación de padre agregado; chequeo de doctor; RuleDoc del agregado; commits `closeout: <id>` en closeout; salida de show/next; tests, hashes de contrato, CHANGELOG y docs. Dependencias: GC01 y GC05; gate G_SLDB_LANG. Validaciones: `pytest tests`, escenarios de acceptance en desk temporal, idempotencia, caso de doctor y fallo de closeout nombrando hijo.

## FUTURO
GC10 usará `parent_id`/`children` al promover nodos; GC11 los leerá como aristas del grafo. El plan de sldb (GO05) fija la semántica de `nonempty`/`count` sobre referencias borradas; el dueño decide el contenido de `phase.md` y si el fallback `status closed` se retira.
