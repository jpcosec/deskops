---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:35:33'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Namespace de tags host: para marcar en qué máquina corre cada tarea

_Describe the incoming message with enough evidence to triage._

Triaje de drawers e inbox (brief v2, 2026-11-16, /mnt/ssd/proyectos/SLDB_1/triaje-drawers-inbox-brief.md). JP pide que cada TaskDoc diga en qué máquina corre: lo que tiene UI va a la máquina local; suites, build --check, benchmarks, migraciones, scion y revisiones van a robocop2. La vía es TaskDoc.tags, pero ningún tag_namespaces del ecosistema define un namespace para la máquina (el de IR, desk/atoms/tag-namespaces.yaml, solo tiene domain, layer, system y topic). Propuesta: agregar el namespace host con los valores host:local y host:robocop2. meaning: máquina donde se ejecuta y valida la tarea. use_when: la tarea tiene UI o verificación en navegador (host:local) o es backend, suites, migraciones, scion o revisiones (host:robocop2). do_not_use_when: atoms y pills, que no se ejecutan. Si una tarea tiene las dos partes se separa en dos tareas. Mientras no exista, IR deja la asignación anotada en reports/triaje-IR-20261116.md sin escribir el tag: sus 8 tareas activas son backend y van a host:robocop2.
