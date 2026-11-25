## REFORMULACION

PF2 es un nodo **agregado** (`node_role: aggregate`): no se ejecuta; termina cuando cierran sus hijos CC38, CC31, CC32, CC33 (a su vez agregado) y CC37. Su propósito es que las reglas del desk —invariantes de documento, ciclo de vida, activación por tipo, cierre y vías de escape— dejen de vivir en Python de deskops y pasen a validadores pydantic y a `RuleDoc`/`RelationDoc` evaluados por sldb. Resultado conjunto: `task_lifecycle.yaml` sin `sets_status` ni `terminal` por transición, activación por reglas con `edges_blocked` visible en `advance`, cierre por recibos `ReviewDoc kind: evidence` sin inyectar hechos en el payload, y consistencia del ciclo de vida rechazada por el modelo `TaskDoc` en toda escritura. Repo dueño: deskops. Límites: no escribe en sldb (pide por `message send`), no suple reglas con Python, no cambia formato del desk ni gramática del CLI, no altera la autoridad de `closeout commit`, y cada superficie borra su código viejo en el mismo paso.

## AMBIGUEDADES

1. «grep de closeout_evidence_verified y TASK_TYPE_EVIDENCE en deskops/ vacío». `TASK_TYPE_EVIDENCE` no aparece en ninguna otra fuente suministrada ni en el `scope` de ningún hijo (CC32 nombra `__activation_receipts__`; CC33, `__closeout_evidence__`). Obligaría a inventar qué símbolo es y a qué hijo asignar su borrado.

## DRY-RUN

Un ejecutor futuro no corre PF2: promueve y verifica hijos. CC38 entrega validadores de documento y borra chequeos sueltos; CC31 entrega `RelationDoc` con `attributes.sets/terminal` y `advance` por `edges_holding`; CC32 entrega `RuleDoc` de activación y `G_CONSUMER`; CC33 cierra sus hijos (a/b/c) y entrega recibos de evidencia y reglas de cierre; CC37 entrega el validador de `TaskDoc`. Cada uno transfiere estado cerrado, no código. La validación conjunta aplica la aceptación de PF2 sobre main integrado (greps, tarea `task.code` sin recibos bloqueada, cierre sin `closeout_evidence_verified`), más suite completa por el supervisor, `doctor` en los 6 desks y goldens.

## FUTURO

Gates de sldb (`G_GO06/08/09`, `G_GD21`, `G_GD26`) los cierra sldb; `G_CONSUMER` ya consta satisfecho. Las decisiones DO2–DO6 y el contenido de CC33a/b/c vienen de otros nodos o del coordinador; la suite integrada la corre el supervisor.
