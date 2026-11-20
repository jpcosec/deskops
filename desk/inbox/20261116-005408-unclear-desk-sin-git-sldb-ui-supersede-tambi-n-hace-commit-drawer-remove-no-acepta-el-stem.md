---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:54:08'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# Desk sin git (sldb-ui): supersede también hace commit; drawer remove no acepta el stem

_Describe the incoming message with enough evidence to triage._

De: coordinador de UIs/sldb-ui, triaje 2026-11-16. Complementa la nota de marcado del 2026-11-16T00:46:53 (desk sin git). 1) UIs/sldb-ui tampoco es repo git y tiene 17 tareas legacy con lifecycle inválido (current_node checklist-…-execution-ready con history vacía). La nota de marcado dice que 'solo queda supersede', pero deskops/services/closure.py también hace un commit de cierre en supersede (git add/commit), así que en un desk sin git no hay ningún verbo para retirar una tarea inválida, y doctor --repair no las toca. Las 17 se recrearon como task-ui-* y siguen en desk/tasks hasta que JP decida git init (task-ui-decision-repo-git). 2) deskops drawer remove dice que acepta 'stem', pero 'macro-01-cli-gateway' y 'g01-cli-exec-core' (desk/drawer/tasks/macro-01-cli-gateway.yml y desk/drawer/tasks/granular/g01-cli-exec-core.yml) dieron 'No drawer file matches'; con la ruta completa sí funcionó. 3) deskops message send --to deskops falla desde UIs/sldb-ui: 'deskops' no está en desk/registry ni en el registry del ecosistema (/home/jp/setup/desk/registry); esta nota se mandó con --root al checkout de deskops.
