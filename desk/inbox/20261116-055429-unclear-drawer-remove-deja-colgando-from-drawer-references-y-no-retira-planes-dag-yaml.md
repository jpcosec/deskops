---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T05:54:29'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# drawer remove deja colgando from_drawer/references y no retira planes (dag.yaml)

_Describe the incoming message with enough evidence to triage._

Triaje del desk de sldb (2026-11-16). Dos huecos del CLI. (1) El flujo add task --from-drawer y después drawer remove deja from_drawer (y references) apuntando a un archivo que ya no existe, y deskops graph missing lo marca como missing_declared_target. Así, el flujo que manda el ritual impide entregar un desk con graph missing en cero. En sldb lo resolví reescribiendo esos campos como texto ('drawer <id> (retirado en el triaje 2026-11-16; contenido en git antes del commit del triaje)'). Propuesta: que drawer remove reescriba from_drawer con el commit y la ruta (por ejemplo git:<sha>:<ruta>), o que graph missing no trate from_drawer como destino declarado. (2) drawer remove no acepta un plan de desk/drawer/plans/<plan>/ (dag.yaml): responde 'No drawer file matches'. Los tres planes entregados de sldb se retiraron con git rm, a mano, como dice el ritual. Propuesta: drawer remove para planes con status delivered, o un verbo plan retire.
