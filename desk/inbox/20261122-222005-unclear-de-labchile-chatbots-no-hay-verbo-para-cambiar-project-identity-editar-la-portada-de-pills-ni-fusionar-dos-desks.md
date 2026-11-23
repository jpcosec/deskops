---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: labchile_chatbots
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T22:20:05'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# De labchile_chatbots: no hay verbo para cambiar project_identity, editar la portada de pills ni fusionar dos desks

_Describe the incoming message with enough evidence to triage._

Reenvío de una nota del desk de labchile_chatbots (desk/inbox/20261020-132757-unclear-desk-unificado-de-psp-chatbot-y-grifo-chatbot.md, del 2026-10-20), al triar su inbox el 2026-11-22. El 2026-10-20 se juntaron en un solo desk los de psp_chatbot y grifo_chatbot. Tres cosas no se pudieron hacer con el CLI y siguen igual hoy: (1) desk/contexts/pills.md (id contexts-pills, el documento de portada de los pills que crea el scaffold) todavía dice 'the psp_chatbot desk routine': 'deskops list pills' no lo lista, 'deskops show pill contexts-pills' responde 'No artifact.pill file found' y, según la nota, 'deskops desk replace' lo rechaza por ser un documento modelado; no hay verbo que lo edite. (2) No hay verbo para fusionar dos desks ni para cambiar project_identity: se editó desk/config.json a mano. (3) Al fusionar, los documentos de andamiaje con el mismo id en los dos desks (board-001, rituales, relaciones del ciclo de vida, pills.md, drawer/README.md, tag-namespaces.yaml) y los índices de .sldb chocan; se dejó la versión de un desk y el board del otro quedó solo en la historia de git. Pedido: decidir si deskops debe tener un verbo para cambiar la identidad del desk y otro para editar la portada de pills, y si la fusión de desks merece un comando o una receta en el manual. En labchile_chatbots lo local queda en la tarea task-lab-6-desk-de-labchile-al-día.
