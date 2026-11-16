---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: scion
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T21:59:33'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# runtime template: el coordinador lanza hijos con --harness-auth api-key fijo

_Describe the incoming message with enough evidence to triage._

Piloto scion en IR, fase 0 (reports/scion-piloto-ir-20261115.md). scion_start_argv y el agents.md del coordinador (_render_coordinator_agents_md) escriben 'scion start ... --harness-auth api-key' para executor y tester. Un hijo claude con la suscripción (secret de archivo CLAUDE_AUTH, auth-file) o con CLAUDE_CODE_OAUTH_TOKEN (oauth-token) no arranca así: pide ANTHROPIC_API_KEY. Desde 4b74cdcd el template del hijo ya elige su auth_selectedType con --harness-auth; falta que el argv de start y el texto del coordinador usen el auth del template del hijo (o no pasen --harness-auth y dejen que mande el template). Hace falta antes de la fase 1 (coordinador scion en IR con ejecutores claude).
