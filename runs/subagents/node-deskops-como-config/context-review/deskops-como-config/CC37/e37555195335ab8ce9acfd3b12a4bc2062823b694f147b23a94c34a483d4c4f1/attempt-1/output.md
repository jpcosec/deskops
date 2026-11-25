REFORMULACION
CC37 (delivery, repo deskops) cierra las vías de escape que quedan tras GC06: inventariar en el TaskDoc toda vía que escribe un TaskDoc y si pasa por transición; convertir la consistencia del ciclo de vida en validador del modelo TaskDoc (status = sets.status de la última arista hacia current_node, history nombra current_node, task_type coincide con el modelo); y comprobar por grep que las escrituras internas que cambian el ciclo de vida pasan solo por advance/apply_effects y closeout commit, de modo que sldb fields/docs update y /save rechacen estados inconsistentes. Límite: no se pide a sldb un campo "solo por transición"; lo que solo se ve entre documentos queda como RuleDoc.

AMBIGUEDADES
1. "status es el sets.status de la última arista que llevó a current_node": no cubre el estado inicial (sin arista entrante) ni el que deja closeout commit; el ejecutor debe inventar la tabla para esos casos.
2. "pasa las reglas tras desk update --apply (o el desk update reporta las inconsistentes sin escribirlas)": dos resultados admisibles dejan vivo si `desk update` debe modificarse para reportar; obliga a inventar cuándo aplica cada rama.
3. "si la tabla depende de RelationDocs, el validador la lee del paquete deskops": no dice cómo se reconcilia con los RelationDoc que `desk update --apply` escribe en el desk; obliga a inventar qué configuración manda cuando difieren.

DRY-RUN
Sin ejecutar: lecturas de RelationDocs de CC31, reglas de CC32, mecanismo de CC38, modelos, `tests/test_cli_escape_hatches.py` y `payload_save_steps.py:62`. Cambios previstos: validador pydantic, inventario en el TaskDoc, grep de status/current_node fuera de lifecycle.advance y closure, tests y CHANGELOG. Dependencias: CC31, CC32, CC38 y G_GO08 (satisfecho). Validaciones futuras: fields/docs update y /save rechazan el payload inconsistente; advance y closeout verdes; tarea migrada de los 6 desks; goldens.

FUTURO
La promoción fija el patrón de grep y recibe el inventario (operador); CC38 entrega el mecanismo, CC31 la tabla de sets y CC32 las RuleDoc; CC35 retira escrituras de graph_ui; DO5 admite closeout resolved-by para CC38.
