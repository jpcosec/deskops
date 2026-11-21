---
sldb:
  by: agent
  at: '2026-11-21T06:41:32Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T08:22:30'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:41:24'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph
  (parte b: doc_access.py:550 aun usa AST_Handler+TemplateExtractor; sldb.api.template_anchors
  existe en el sldb instalado).'
---

# sldb.api.template_anchors: los párrafos ancla literales de la plantilla de un modelo (H1 de placeholder)

_Describe the incoming message with enough evidence to triage._

Pedido H1 de placeholder, del task.debug de deskops 'edit no guarda el párrafo placeholder'. En sldb main, commits 5ccf720f y 7cd8a5e3, por integrar. sldb.api.template_anchors(model_type) -> dict[str, str] devuelve, para cada campo cuyo marcador va inmediatamente después de un párrafo ancla literal en __template__, el texto de ese párrafo tal como está en la plantilla, cursivas incluidas (por ejemplo '_Outline the expected implementation route or affected surface._' para implementation_path). Usa las mismas recetas que Validator.extract. deskops puede dejar de usar AST_Handler().split_nodes y TemplateExtractor().extract_nodes.
