---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T07:09:13'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# closeout: una materialization cuyo target es un directorio dentro de tests/ no cubre nada (prefijo test_file: sin normalizar)

_Describe the incoming message with enough evidence to triage._

Visto al cerrar task-portar-a-sldb-las-pruebas-de-spec2viz en sldb (2026-11-16). El campo files de la tarea tenía 'tests/notations/'. Hice una materialization con target_identity tests/notations y el grafo la reporta como missing_declared_target -> test_file:tests/notations. En deskops/services/closure.py, _directory_materialization_targets compara _normalize_target_path(entry.target_id) con el target declarado, pero entry.target_id trae el prefijo de tipo ('test_file:') y no coincide. Por eso la cobertura de directorio que promete target_covers nunca aplica dentro de tests/, y closeout verify falla con missing_changed_file_link para 'tests/notations'. Workaround en sldb: retiré la materialization de directorio y dejé files con los archivos reales. Propuesta: quitar el prefijo de tipo (<kind>:) antes de comparar, con un test para un directorio dentro de tests/.
