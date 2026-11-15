---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:44:50'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# --to deskops no resuelve desde otro repo

_Describe the incoming message with enough evidence to triage._

Desde MEPU (2026-11-15): `deskops message send --to deskops` falla desde MEPU («Repository id deskops not found in registry at mepu/desk/registry (found: none)»): el registro local de MEPU está vacío y deskops no cae al registro del ecosistema (/home/jp/setup/desk/registry), que tampoco lista deskops (sus repos anidados quedaron fuera). Hubo que mandar con --root a la ruta del repo. Pedido: que --to resuelva contra el registro del ecosistema y que deskops/sldb/spec2viz estén registrados.
