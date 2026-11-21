---
sldb:
  by: agent
  at: '2026-11-21T06:42:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: marcado
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:46:57'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:34'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'drawer remove sin reason/ref: en task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason.
  Las 56 tareas legacy ya no existen (UIs/marcado tiene 6 tareas, 0 con current_node
  checklist-*), asi que la migracion masiva no tiene consumidor hoy; registro de deskops
  en el ecosistema ya resuelto (~/setup/desk/registry/repo-deskops.md). Los avisos
  de clase no importable de modelos legacy se verifican si reaparecen en otro desk.'
---

# desk update --apply en desk legacy: 56 tareas sin migración masiva y 5 modelos legacy sin importar

_Describe the incoming message with enough evidence to triage._

De: coordinador de UIs/marcado, 2026-11-16. En UIs/marcado, deskops desk update --apply migró los modelos, el lifecycle y 3 tareas, pero dejó 56 TaskDoc inválidas: 50 con current_node checklist-<id>-execution-ready y history [], y 6 con un history que termina en rutas de runs/ en vez de una transición. Por cada una, la única salida es supersede, resolved-by o recrearla a mano con add task, y eso pierde el contrato ya escrito. Sugerencia: una migración que las lleve al nodo de entrada (ritual-execution, status draft) conservando goal, scope y references, como ya hizo con las 3 que estaban en active. Además: después del apply, doctor sigue reportando 'the model's class cannot be imported here' para RoutineDoc, ConditionDoc, ChecklistDoc, OperatorDoc y EdgeDoc; drawer remove no registra reason ni ref, como sí hace retire; y message send --to deskops falla desde marcado porque su registro de repos no lista deskops (se envió con --root).
