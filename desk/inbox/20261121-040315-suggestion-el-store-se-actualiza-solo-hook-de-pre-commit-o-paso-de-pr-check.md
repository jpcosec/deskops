---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-21T04:03:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# El store se actualiza solo: hook de pre-commit o paso de pr check

_Describe the incoming message with enough evidence to triage._

Hoy nada actualiza el store cuando cambia un documento del desk o de docs: depende de que alguien corra 'sldb stores update' y 'deskops desk update --apply'. En Governance el store quedó atrasado varios días y hubo que repararlo a mano (heyantonia/Governance#130); JP: 'no veo por qué esto no es algo automático'. Pedido: que deskops instale un hook de pre-commit que registre lo editado (o, si no se quiere tocar el commit, que 'pr check' falle cuando el store no corresponde al árbol y diga el comando que lo arregla). Relacionado: en shared_llm-gateway, cada comando de deskops sembraba 11 reglas de desk/lifecycle sin registrar hasta que entraron por heyantonia/shared_llm-gateway#40; la siembra de reglas nuevas debería quedar registrada por el mismo mecanismo.
