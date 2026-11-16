---
sldb:
  by: agent
  at: '2026-11-16T15:08:25Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: marcado
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T10:32:16'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T12:08:20'
---

# closeout supersede rechaza 3 TaskDocs de marcado con claves checklists/routine

_Describe the incoming message with enough evidence to triage._

En UIs/marcado (robocop2, 2026-11-16), deskops closeout supersede --root UIs/marcado --task <id> --reason ... --ref 39e1ca7600e0cf5a7dfacd5ceaa726c50c3250e5 --ref 8e283c387d13a29d1dadef26ab82e15be7fdab80 rechaza estas tareas: task-close-the-runtime-pipeline-baseline, task-close-the-source-and-marker-model-baseline y task-design-the-runtime-architecture-and-extension-model. El error exacto es: Refusing to rewrite <id>.md: it has content its model (TaskDoc) does not declare, and rewriting would erase it: frontmatter key 'checklists'; frontmatter key 'routine'. Son TaskDocs heredados de antes de la migración. Ni la migración (desk update --apply) ni deskops edit pueden quitar esas claves, y supersede no puede cerrarlas. Hace falta una vía con el CLI, por ejemplo supersede --drop-undeclared, una migración que mueva o descarte checklists y routine, o un retire. Bloquea la tarea task-cerrar-con-supersede-las-53-tareas-de-spec-y-diseño-de-marcado-b3 de marcado (50/53 cerradas). Aparte: deskops message send corrido desde /mnt/ssd/proyectos/SLDB_1 (sin --root) falla con 'Unable to resolve sender identity'.
