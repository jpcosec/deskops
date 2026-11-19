---
sldb:
  by: agent
  at: '2026-11-19T08:15:02Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T05:14:34'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-19T05:14:56'
# why the note was acknowledged; empty when no reason was given
ack_reason: Informativo. deskops escribe sus documentos del desk con save_document_payload;
  con sldb 94c4b4bb un documento del desk con ruido estructural o frontmatter no declarado
  falla en vez de perder contenido, que es lo buscado. La suite de deskops pasó contra
  este sldb en el integrate de hoy.
---

# sldb: una escritura por campos ya no borra ruido estructural ni frontmatter no declarado, falla antes de escribir

_Describe the incoming message with enough evidence to triage._

sldb main 94c4b4bb (código 6a4e5ec5). save_document_payload y el update de apply_batch, que pasa por él, aplican ahora al texto actual del archivo las mismas guardas que al crear o trackear (refuse_structural_noise y refuse_undeclared_frontmatter) antes de re-renderizar. Si el archivo tiene encabezados o frontmatter que el modelo no declara, la escritura por campos falla con el error de esas guardas, que nombra lo que se perdería, y el archivo queda intacto. Antes se borraba en silencio. Los documentos limpios se escriben igual. Un documento trackeado con force que arrastre ruido deja de poder escribirse por campos hasta limpiarlo: hay que tenerlo en cuenta en los clientes que escriben por apply_batch update.
