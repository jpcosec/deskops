---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T13:23:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# closeout borra una tarea aunque otras hereden de ella (inherits_from) y esas dejan de cargar

_Describe the incoming message with enough evidence to triage._

Caso en Governance (2026-11-22): task-coherencia-de-los-clientes-del-kit-con-el-kit-y-versiones se cerró con closeout el 11-11 (commit 40fc9e2, PR heyantonia/Governance#107) y su archivo se borró. Dos tareas en draft la tenían en inherits_from (task-leer-antonia-cobranza-y-pyme-chatbots… y task-satélites-relockear-uv-lock…). Desde entonces 'deskops list tasks' las saltaba con 'Warning: Failed to load task …: No task file found for selector …', y nadie lo vio en once días porque es solo un aviso. Se arregló a mano con 'deskops edit task <id> inherits_from []' y pasando la tarea cerrada a references (heyantonia/Governance#141).

Lo que falta en deskops, a decidir por quien lo mantiene: (1) closeout no revisa si otras tareas heredan de la que borra; podría negarse, avisar, o reescribir la herencia; (2) una tarea con inherits_from roto deja de cargar entera en vez de cargar sin la herencia; (3) doctor no lo detecta como estado roto.
