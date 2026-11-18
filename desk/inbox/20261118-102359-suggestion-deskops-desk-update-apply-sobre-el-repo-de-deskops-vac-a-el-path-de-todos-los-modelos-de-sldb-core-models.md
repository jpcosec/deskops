---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-18T10:23:59'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# deskops desk update --apply sobre el repo de deskops vacía el path de todos los modelos de .sldb/core/models

_Describe the incoming message with enough evidence to triage._

Visto por el integrador el 2026-11-18 con herramientas en 31460a48. En /mnt/ssd/proyectos/SLDB_1/deskops, 'deskops desk update --apply' reescribió los 30 archivos de .sldb/core/models/*.yaml con path: '' en lugar de la ruta del modelo (ej. RoleDoc: 'path: deskops/models/role.py' -> "path: ''"). También tocó sldb/relation_types/has_model.md y agregó reltype-links_to. Lo revertí entero sin commitear. En sldb e IR el mismo comando no tocó los modelos: solo agregó las semillas de testing->execution y refrescó hashes. Hipótesis: en el repo de deskops los modelos son del propio paquete y el update los re-registra como modelos instalados, sin ruta local. Repro: copia limpia de deskops en 31460a48, desk update --apply y git diff -- .sldb/core/models.
