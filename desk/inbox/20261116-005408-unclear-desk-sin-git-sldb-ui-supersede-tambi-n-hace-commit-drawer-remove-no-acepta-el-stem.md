---
sldb:
  by: agent
  at: '2026-11-21T06:42:22Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: sldb-ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:54:08'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-21T03:42:15'
# why the note was acknowledged; empty when no reason was given
ack_reason: '1) Desk sin git: sldb-ui es repo git desde 56a552b (2026-11-16); la regla
  general queda en task.decision task-jp-decide-si-deskops-exige-git-en-cada-desk-o-acepta-otra-evidencia-de-cierre.
  2) stem de .yml: en task-drawer-remove-retira-un-plan-entero-los-assets-de-un-issue-entradas-no-md-por-stem-y-registra-reason
  (drawer.py solo busca *.md). 3) deskops ya esta en el registro del ecosistema (~/setup/desk/registry/repo-deskops.md).'
---

# Desk sin git (sldb-ui): supersede también hace commit; drawer remove no acepta el stem

_Describe the incoming message with enough evidence to triage._

De: coordinador de UIs/sldb-ui, triaje 2026-11-16. Complementa la nota de marcado del 2026-11-16T00:46:53 (desk sin git). 1) UIs/sldb-ui tampoco es repo git y tiene 17 tareas legacy con lifecycle inválido (current_node checklist-…-execution-ready con history vacía). La nota de marcado dice que 'solo queda supersede', pero deskops/services/closure.py también hace un commit de cierre en supersede (git add/commit), así que en un desk sin git no hay ningún verbo para retirar una tarea inválida, y doctor --repair no las toca. Las 17 se recrearon como task-ui-* y siguen en desk/tasks hasta que JP decida git init (task-ui-decision-repo-git). 2) deskops drawer remove dice que acepta 'stem', pero 'macro-01-cli-gateway' y 'g01-cli-exec-core' (desk/drawer/tasks/macro-01-cli-gateway.yml y desk/drawer/tasks/granular/g01-cli-exec-core.yml) dieron 'No drawer file matches'; con la ruta completa sí funcionó. 3) deskops message send --to deskops falla desde UIs/sldb-ui: 'deskops' no está en desk/registry ni en el registry del ecosistema (/home/jp/setup/desk/registry); esta nota se mandó con --root al checkout de deskops.
