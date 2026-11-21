---
sldb:
  by: agent
  at: '2026-11-21T06:41:42Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T08:13:41'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:41:35'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Convertida en tarea task-deskops-usa-las-apis-publicas-de-sldb-ya-integradas-y-borra-sus-rodeos-rewrite-references-con-graph
  (parte c: closure.py:1107-1171 aun hace create + update sin cambios para pinnear).'
---

# create_document pinnea las anclas a documentos igual que save_document_payload

_Describe the incoming message with enough evidence to triage._

Hipótesis H-CC32-2 de CC32. En sldb main, commits e82d62ba y dc6d1f22, por integrar: create_document, y también Transaction.create porque pasa por él, ahora pinnea con @sha256 los doc: de los campos de __doc_anchors__ y el from: de procedencia, igual que save_document_payload. Un recibo creado y nunca reescrito queda con anchor_state intact si su destino está trackeado. deskops puede quitar el rodeo de create + update en la misma transacción. Tests: tests/api/test_doc_anchors.py::test_create_document_pins_the_anchor_without_a_later_save y test_a_transaction_create_pins_the_anchor.
