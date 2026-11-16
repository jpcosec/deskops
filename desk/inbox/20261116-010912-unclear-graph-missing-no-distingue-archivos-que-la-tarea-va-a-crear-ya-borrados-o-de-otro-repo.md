---
sldb:
  by: agent
  at: '2026-11-16T06:11:51Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T01:09:12'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T03:11:46'
---

# graph missing no distingue archivos que la tarea va a crear, ya borrados o de otro repo

_Describe the incoming message with enough evidence to triage._

Triaje del 2026-11-16 en deskops. SOURCE_PATH (deskops/graph/desk_graph.py:122-125) convierte en arista toda mención de deskops|desk|tests|spec|docs/<ruta>.<ext> en el texto de un TaskDoc, y graph missing la reporta como missing_declared_target si el archivo no existe. Tres casos legítimos quedan como falsos faltantes: (1) archivos que la tarea va a crear (tests/test_ascii_ids.py, docs/configuration.md, docs/config-vs-code.md, tests/test_docs_recipes.py, tests/test_atom_citations.py, tests/test_config_vs_code_doc.py); (2) archivos que el texto cita como ya borrados (deskops/specs/loader.py y mermaid.py, borrados en CC30); (3) rutas de otro repo (docs/spec/spec-procesos-modelables.md de Governance). Hoy hay 11 faltantes de este tipo en desk/tasks, y graph missing da rc 0 igual. Reescribir la ruta (p. ej. ./ruta) para esquivar el detector engaña a la evidencia, así que quedan tal cual. Pedido: una forma declarada de distinguirlos (p. ej. un campo o marca para archivos a crear en TaskDoc.files, ignorar menciones en Rationale/Why, o un nivel informational para targets inexistentes en tareas en draft), sin que oculte referencias rotas reales.
