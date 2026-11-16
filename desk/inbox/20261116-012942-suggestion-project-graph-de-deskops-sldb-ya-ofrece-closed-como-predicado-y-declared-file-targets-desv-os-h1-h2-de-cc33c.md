---
sldb:
  by: agent
  at: '2026-11-16T06:11:23Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T01:29:42'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T03:11:19'
---

# project_graph de deskops: sldb ya ofrece closed: como predicado y declared_file_targets (desvíos H1/H2 de CC33c)

_Describe the incoming message with enough evidence to triage._

Triaje del drawer de sldb (2026-11-16). El ítem 'project_graph para deskops: nodos para archivos declarados que no son documento y declaración con closed_document como dato (desvíos de CC33c)' es trabajo de deskops: sldb ya tiene las dos capacidades desde GD21 (a2a0174f). H2: la superficie de documentos de project_graph acepta closed: como predicado del lenguaje de reglas (src/sldb/api/edges/project_graph/document_surface.py:25, evaluado en project_texts.py:41-48; config_to_mapping rechaza el callable y apunta a closed:, project_graph_config_mapping.py:18,32-33). H1: declared_file_targets convierte en nodos los archivos existentes que no son documento (project_graph_config.py:38, declared_file_targets.py, declared_target_nodes.py; test tests/api/test_project_graph.py:60). Lo que queda en deskops: declarar project_graph en su store.yaml con closed: y declared_file_targets, y borrar declared_target_is_a_file (deskops/graph/checks.py:63) y el closed_document=_closed_issue de deskops/graph/desk_graph.py:204. Si algún destino de deskops (dag.yaml, model_contract_hashes.json) no se declara por un campo de frontmatter de un glob de documentos, declared_file_targets no lo cubre: en ese caso, mandar nota a sldb. El ítem se retira del drawer de sldb.
