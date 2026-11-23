---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T23:12:20'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# desk update --apply activa la validación de tags de TaskDoc y deja tareas sin poder editarse (namespaces del roadmap sin declarar)

_Describe the incoming message with enough evidence to triage._

Visto el 22-11 en cinco desks (ftcourier, mepu, labchile_chatbots, shared_llm-gateway, Chatbot_Infra) al triar sus inbox. 'deskops desk update --apply' declara los namespaces de tags en .sldb/store.yaml y mete TaskDoc en tag_models; desde ese momento el store valida los tags de las tareas. Las tareas del roadmap de noviembre traen tags de namespaces que ningún desk declaró (certeza, roadmap, pr, capa, categoria, nodo, responsable, semana). Efecto: en ftcourier 'deskops edit task' empezó a fallar con SLDBRuleViolationError: tag_namespace y doctor sumó 55 errores; en mepu falló con tag_namespace:capa en las 12 tareas MEPU-N; en labchile quedaron 16 errores en 15 tareas y en el gateway 4. ftcourier y mepu lo resolvieron declarando los namespaces a mano (heyantonia/ftcourier#68, heyantonia/mepu#459); labchile y el gateway quedaron sin declarar porque el significado no está escrito en esos repos. Governance tiene 35 tareas con certeza, categoria y nodo y todavía no valida TaskDoc. Pedidos: (1) que 'desk update' en seco liste los tags de tareas cuyo namespace no está declarado, y que --apply no active la validación de TaskDoc dejando tareas que ya no se pueden editar (negarse, o avisar y pedir los namespaces antes); (2) decidir si un desk puede tomar namespaces declarados en el desk que coordina (por el store enlazado) en vez de copiarlos en cada repo: los del roadmap nacen en Governance (docs/roadmap/roadmap-2026-11.md) y hoy habría que copiarlos en cada desk. No comprobé si (2) ya existe.
