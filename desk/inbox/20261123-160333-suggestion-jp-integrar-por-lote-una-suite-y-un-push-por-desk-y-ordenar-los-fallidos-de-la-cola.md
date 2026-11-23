---
sldb:
  by: agent
  at: '2026-11-23T19:05:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T16:03:33'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T16:05:45'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-integrate-por-lote-una-sola-integracion-por-desk-con-todo-lo-cerrado-pendiente-un-tip-una-suite-un-g
  (prioridad alta, va despues de la de tags semanticos); los 12 fallidos estan todos
  en origin, subidos por integrates posteriores; mientras tanto el coordinador integra
  por lote a mano
# conversation thread/message the note came from, e.g. #hilo/1234
---

# JP: integrar por lote (una suite y un push por desk) y ordenar los fallidos de la cola

_Describe the incoming message with enough evidence to triage._

JP (2026-11-23), al ver los 12 trabajos en runs/queue/failed de deskops: 'creo que puedes mezclar en un solo deployment; por lo que veo son problemas de workflow más que de las tareas en sí'. Pedido: que integrate deje de correr una vez por tarea y junte en una sola integración todo lo cerrado y pendiente de subir de un desk: un tip, una suite completa, una comprobación de grafo y de store, un push. Coherente con la regla del workspace de una suite completa por integración. Evidencia (supervisor local, 23-nov): los 12 fallidos son 10 integrate y 2 dispatch-reap del 21 al 23-nov, y las 11 tareas tienen closeout; ninguno es un defecto de la tarea. Causas: (1) 4 por suite completa con una prueba roja; la última, 1 de 1374 tras 43 min: tests/test_dispatch.py::test_reap_scion_error_continues_and_fails espera una lista y recibe además 'limpieza: /dev/shm/pytest-of-scion' (prueba sensible al entorno). (2) 2 por 'fast-forward: origin/main no es ancestro': otro trabajo empujó durante los 40 min de suite; con una integración por lote no compiten, y si origin se mueve debería rebasar y reintentar en vez de fallar. (3) 2 por 'graph: faltantes N en el tip > M en origin/main'. (4) 4 de entorno: git worktree add sin poder escribir en /dev/shm, 'store: ruta ausente en el commit: runs/subagents/.../run.md', scion list con context deadline exceeded, y un ejecutor con error:1. Además: runs/queue/failed no se limpia ni distingue lo ya resuelto por un reintento, así que el contador solo sube; falta un comando que reintente o archive un fallido con motivo. El diseño (ventana del lote, qué pasa si la suite del lote falla: bisecar o sacar la tarea culpable) lo propone el desk; las decisiones van a JP como task.decision.
