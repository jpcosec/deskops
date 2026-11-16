---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:36:02'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Namespace de tags host para separar tareas de UI (local) y backend (robocop2)

_Describe the incoming message with enough evidence to triage._

Triaje de drawers e inbox (brief v2 del supervisor, 2026-11-16, /mnt/ssd/proyectos/SLDB_1/triaje-drawers-inbox-brief.md). JP pide que cada tarea diga en qué máquina corre: lo que tiene UI (graph_ui, sldb/surface, UI de deskops, marcado, review-workbench, verificación en navegador sobre un desk real) va a la máquina local; el resto (suites, build --check, benchmarks, migraciones, scion, revisiones) va a robocop2. La vía es TaskDoc.tags con deskops edit task <id> tags '[...]'. El store de deskops (.sldb/store.yaml) no declara tag_namespaces, así que no hay namespace para la máquina. Propuesta: declarar un namespace host (no jerárquico) con los valores host:local y host:robocop2, en la semilla que deskops escribe en cada desk, para que sldb tag check lo valide. Mientras tanto, los informes de triaje anotan el host de cada tarea sin taggearla.
