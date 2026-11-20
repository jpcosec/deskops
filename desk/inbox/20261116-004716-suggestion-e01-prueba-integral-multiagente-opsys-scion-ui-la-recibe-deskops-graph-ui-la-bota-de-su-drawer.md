---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# E01 prueba integral multiagente opsys-scion-UI: la recibe deskops (graph_ui la bota de su drawer)

_Describe the incoming message with enough evidence to triage._

Desde graph_ui, triaje 2026-11-16. El drawer de graph_ui tenía desde el 2026-10-31 'Prueba integral multiagente Opsys-Scion-UI' (E01 de softfactory_spec): validar de punta a punta crear y avanzar una tarea en deskops, despacharla y ejecutarla en Scion, y verla en la UI. graph_ui es solo un cliente de ese flujo: el contrato de la UI es de deskops (docs/deskops-ui.md) y la ejecución es de scion, que hoy está en piloto en el desk de IR (fase 1 de scion en pausa). Por eso graph_ui no puede ser dueño de E01 y lo saca de su drawer. Si deskops la toma, la parte de graph_ui es una verificación en el navegador sobre el desk real (host:local); pídanla por inbox con el contrato de lo que la UI debe mostrar y graph_ui la convierte en tarea.
