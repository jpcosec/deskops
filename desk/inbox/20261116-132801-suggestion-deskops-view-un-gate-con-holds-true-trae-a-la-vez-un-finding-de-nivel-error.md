---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T13:28:01'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# deskops view: un gate con holds true trae a la vez un finding de nivel error

_Describe the incoming message with enough evidence to triage._

Visto al cerrar en graph_ui la tarea de findings en gates (b9aface, closeout b777ef3): en el desk de deskops, deskops view task task-advance-y-closeout-no-derraman-reglas-de-activacion-ni-runtimes-centrales-sin-trackear-en-el-desk-co --format json entrega en su gate task_activates -> ritual-testing holds: true y, a la vez, findings: [{level: error, code: rules/rule-activation-task-code, what: '... (seen: {})'}]. La UI dibuja 'cumple' y el finding de error juntos, fiel a la vista. ¿Es intencional (holds evaluado por otra vía que la regla) o holds debería ser false cuando la regla de activación da error? Desde graph_ui la UI ya muestra los findings; los recibos (ReviewDoc) siguen sin campo en deskops view (nota 20261116-095054).
