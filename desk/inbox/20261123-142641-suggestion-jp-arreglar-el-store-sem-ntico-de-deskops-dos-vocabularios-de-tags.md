---
sldb:
  by: agent
  at: '2026-11-23T17:32:11Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-23T14:26:41'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-23T14:32:02'
# why the note was acknowledged; empty when no reason was given
ack_reason: convertida en task-un-solo-vocabulario-de-tags-semanticos-en-deskops-padres-declarados-en-sldb-add-sin-duplicados-y-mig
  (prioridad 2 de JP); se despacha ya
# conversation thread/message the note came from, e.g. #hilo/1234
---

# JP: arreglar el store semántico de deskops (dos vocabularios de tags)

_Describe the incoming message with enough evidence to triage._

JP (2026-11-23): MUY importante arreglar el store semántico de deskops; lo necesita para explorar deskops con el lector de surface (nota de hoy en el desk de sldb), cuyo índice agrupa por semántica. Diagnóstico del supervisor, por confirmar con JP (él dijo solo 'arreglar la store semántica'): conviven dos vocabularios. (a) Tags de modelo con puntos y jerarquía: workspace.desk.atoms, type.workflow.task, layer.topology. (b) Tags libres con dos puntos en el frontmatter, planos y sin padres en .sldb_cache/semantic_dag.yaml: workspace:desk (792 documentos), system:deskops (537), artifact:task, topic:*, pill-type:*, host:*, runtime:*, layer:cli. Varios duplican a los de (a): workspace:desk y workspace.desk; artifact:task y type.workflow.task; layer:* y layer.*. Además hay nombres de clase usados como tag (TaskDoc, PrimitiveDoc, OperationalArtifactDoc) y tags sueltos (ci/cd, demo). Pedido: un vocabulario único con padres declarados por sldb semantic parent/equivalent, que deskops add deje de escribir los duplicados, y migración de los documentos existentes por CLI. Si a sldb le falta una operación para migrar tags en bloque, va como nota a sldb.
