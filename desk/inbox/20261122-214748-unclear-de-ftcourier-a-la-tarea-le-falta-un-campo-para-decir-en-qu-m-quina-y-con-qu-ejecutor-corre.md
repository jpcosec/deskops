---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: ftcourier
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T21:47:48'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# De ftcourier: a la tarea le falta un campo para decir en qué máquina y con qué ejecutor corre

_Describe the incoming message with enough evidence to triage._

Reenviada desde el desk de ftcourier (nota 20261119-233140, triaje del 2026-11-22). TaskCodeDoc no tiene campo de host, ejecutor ni asignación, RuntimeProfileDoc tampoco tiene host, y deskops runtime workers solo lista agentes de esta máquina. En ftcourier se marca con tags (host:robocop2, host:local) y en el título: sirve para leer, pero deskops next, el Board y deskops list tasks no lo usan ni lo filtran. Ejemplo: desk/tasks/task-ftc-30b-*.md de heyantonia/ftcourier. Relacionadas en este inbox: las notas del 16-11 sobre el namespace de tags host y la del 21-11 sobre clones base de una máquina coordinadora. La nota original no se pudo mandar el 19-11 porque el registro de esa máquina no tenía a deskops.
