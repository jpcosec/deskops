---
sldb:
  by: agent
  at: '2026-11-16T04:13:14Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: pron-repair
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:45'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T01:13:11'
---

# Namespace de tags host: para rutear tareas por máquina (triaje 2026-11-16)

_Describe the incoming message with enough evidence to triage._

El brief de triaje del 2026-11-16 (SLDB_1/triaje-drawers-inbox-brief.md, sección 'Dónde corre cada tarea') pide marcar en TaskDoc.tags la máquina donde corre cada tarea: lo que tiene UI va a la máquina local y el resto (suites, build --check, benchmarks, migraciones, scion, revisiones) a robocop2. Ningún tag_namespaces.yaml define un namespace para eso (pron/desk/atoms/tag-namespaces.yaml solo tiene domain, layer, system, topic). Propuesta: namespace 'host' con meaning 'máquina donde se ejecuta y valida la tarea', use_when 'la tarea debe correr en una máquina concreta', ejemplos host:local y host:robocop2; una tarea con partes de UI y de backend se separa en dos. Mientras no exista, pron anota el host en reports/triaje-pron-20261116.md: sus dos tareas nuevas (IR13 specir y la decisión de .sldb/) van a host:robocop2.
