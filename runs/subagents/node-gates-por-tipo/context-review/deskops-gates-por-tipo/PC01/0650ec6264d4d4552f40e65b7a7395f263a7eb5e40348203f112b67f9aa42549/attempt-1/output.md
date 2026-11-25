## REFORMULACION

Propósito: entregar en deskops, sin esperar a sldb, la base consumidora del plan: tipos de tarea como modelos sldb con jerarquía y evidencia de cierre declarada en el tipo, `ReviewDoc` como recibo anclado al contrato y el comando `deskops review` que los produce y retira los scripts de revisión en frío. Resultado: `G_TYPES` y `G_RECEIPTS` satisfechos, `--task-type` cerrado a tipos registrados, recibos y evidencia en `runs/`, sin `context_review.py` en drawers de deskops. Repo dueño: deskops. Límites: no toca sldb (solo `deskops message send`), no reimplementa el evaluador, no autentica, no convierte la verificación de cierre en recibos; antes de `G_SLDB_ANCHORS` el `subject` se guarda sin hash. PC01 es agregado (`node_role: aggregate`): no se ejecuta; termina cuando cierran sus hijos.

## AMBIGUEDADES

1. «el comando deskops review que produce esos recibos y retira los dos scripts». El brief fija «No toca sldb» y la aceptación solo exige «ningún script context_review.py queda en los drawers de deskops». Obliga a inventar si el segundo script (`sldb/desk/drawer/plans/grafo-operable/context_review.py`) se borra o solo se notifica; borrarlo excedería el límite de no escribir en sldb.

## DRY-RUN

No ejecutable por ser agregado. GC01 entrega tipos registrados (`TaskCodeDoc` y familia, `task_type` cerrado, evidencia leída del tipo, migración idempotente) y transfiere a GC02 el modelo base y `__contract__`. GC02 entrega `ReviewDoc` validado y tracked y transfiere a GC03 el esquema del recibo. GC03 entrega `deskops review` (node, preflight, bundle, status, dispose), borra el script de deskops y produce `G_RECEIPTS`. GC01 y GC02 no tienen arista: no se entregan nada entre sí. Validación conjunta: al cerrar GC01 y GC03, la aceptación de PC01 exige ambos gates satisfechos, rechazo de `--task-type foo`, `ReviewDoc` y evidencia bajo `runs/`, y grep sin `context_review.py` en drawers de deskops.

## FUTURO

Cierre de GC01 y GC03 (revisión en frío aceptada, tests verdes, `closeout commit`) y promoción de los hijos con `deskops add task --from-drawer`. GO07/`G_SLDB_ANCHORS` pinneará el `subject` con hash; hasta entonces sin hash. Nota a sldb sobre su script. Pendientes del dueño: `--evidence`, DC7, `task.external` y plantilla Scion.
