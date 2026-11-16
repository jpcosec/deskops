---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T13:02:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# G5, opción b (decisión de JP): deskops quita su enlace al store de spec2viz; IR espera con un espejo

_Describe the incoming message with enough evidence to triage._

Sigue a la nota 20261116-122447. JP decidió la opción b el 2026-11-16: el Done When de la tarea de IR no se ajusta, y deskops quita de su store (deskops/.sldb/core/store_index.yaml) el enlace spec2viz -> ../spec2viz/.sldb. En IR, la tarea task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a depende ahora del espejo task.external task-espejo-deskops-deskops-sldb-deja-de-enlazar-el-store-de-spec2viz-g5-opción-b, que se cierra cuando deskops cierre su tarea y el store_index ya no enlace spec2viz. Cuando lo integren, avisen a IR con el id de su tarea y el commit. Precaución: las pruebas de IR digieren el store real de deskops, así que eviten escribir en él mientras corre una suite de IR bajo /dev/shm/sldb1-tests.lock.
