# Intento 2
Codigo del intento 1 (3db148a0) ya en la rama. Este intento: sldb stores update --store .sldb --pythonpath . en el worktree.
Commit solo de .sldb/core/models/AtomDoc.yaml, InboxNoteDoc.yaml y .sldb/core/store_index.yaml (Task-Id en el cuerpo).
No se commitearon RunDocs/RunDoc.yaml modificados por el update (ajenos a la tarea).
stores check: 213 -> 195 errores, sin contract moved para AtomDoc/InboxNoteDoc. Tests 27 passed. Ver validation.log.
Suite completa -n 4 corrida en intento 1; no repetida aqui.
