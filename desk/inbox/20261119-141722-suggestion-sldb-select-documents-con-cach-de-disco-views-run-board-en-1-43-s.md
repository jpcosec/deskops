---
sldb:
  by: agent
  at: '2026-11-21T06:42:59Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-19T14:17:22'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:53'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'Informativa: deskops solo nombra .sldb_cache como prefijo excluido del
  grafo (deskops/graph/desk_graph.py:91), que cubre document_rows/; no lee su contenido.
  Nada que hacer.'
---

# sldb: select_documents con caché de disco; views run board en 1,43 s

_Describe the incoming message with enough evidence to triage._

sldb main 40bff94e (código d3568eea), en herramientas. select_documents guarda en .sldb_cache/document_rows/ las filas de documentos, como JSON con clave de stats, y vuelve a los shards ante cualquier cambio o caché corrupta. networkx se importa perezoso y store.yaml se carga con libyaml. sldb views run board bajó de 2,48 s a 1,43 s con caché caliente; la meta de 1 s sigue pendiente. La suite completa de deskops main pasó con este sldb (1252 passed). Si algo de deskops lee .sldb_cache, la carpeta nueva es document_rows/.
