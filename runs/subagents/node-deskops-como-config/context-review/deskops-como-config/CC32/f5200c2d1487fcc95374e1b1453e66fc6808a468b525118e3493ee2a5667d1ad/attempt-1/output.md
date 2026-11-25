## REFORMULACION
CC32 es un nodo `delivery` de código, repo dueño deskops. Propósito: rehacer GC05 como gates de activación por tipo de tarea declarados en `RuleDoc` semilla, borrar `__activation_receipts__` y hacer que `advance`, `next` y `show` expliquen bloqueos con findings de `edges_blocked`. Resultado: reglas por tipo, prueba de integración G_CONSUMER en tres pasos, nota a sldb y documentación. Límites: no escribe en sldb, no suple reglas con Python, no cambia formato del desk ni gramática del CLI, y borra el chequeo viejo en el mismo paso.

## AMBIGUEDADES
1. «task.aggregate: all(children: status = "closed") si GC09 de gates-por-tipo no existe, hipótesis en el TaskDoc…»: obliga a inventar si GC09 existe y si debe escribir o no la regla de hijos; el alcance no da criterio de comprobación.
2. «una tarea task.debug exige reproduction y no bundle; una tarea task.refactor exige además goldens» contradice DO2: «task.debug, task.refactor y task.decision no se pueden activar» hasta una tarea de seguimiento posterior. Obliga a inventar si la aceptación se ejecuta, se omite o se fuerza.
3. «el mensaje de bloqueo lista los findings… en lugar de las condiciones crudas; next y show los muestran también» contradice `alcance.md`: «goldens de salida… quedan iguales». Obliga a inventar si el cambio de salida es la excepción no declarada o si debe preservarse el golden.
4. «tabla normativa de gates-por-tipo brief.md §Tipos»: el input no la incluye y de ella dependen los recibos exigidos por cada tipo (incluidos `task.decision` y `task.aggregate`); obliga a inventar kinds y cláusulas.

## DRY-RUN
Lecturas: `models/task_types.py`, `models/review.py`, `lifecycle.py`, `services/tasks.py`, `workflow/next_actions.py`, `cli/commands/desk.py`, inventario de CC38 y semillas de reglas. Cambios previstos: crear `deskops/data/rules/`, ajustar modelos y anclas, mensaje de bloqueo por findings, borrar `__activation_receipts__`, actualizar docs, rituales vía deskops y CHANGELOG. Dependencias: CC31, CC38; gates GO06, GO08 y GATES_FROZEN ya satisfechos. Validaciones futuras: test de activación en tres pasos, `task.debug`/`task.refactor`, herencia de subtipo, `depends_on`, greps, goldens de ayuda, `rules check/explain` sobre copia, `doctor` en 6 desks. Sin ejecutar nada.

## FUTURO
CC33 consume los recibos y reglas de cierre; CC37 consume la consistencia; sldb recibe la nota G_CONSUMER; DO2 y la existencia de GC09 los decide el dueño/coordinador; el supervisor corre la suite integrada.
