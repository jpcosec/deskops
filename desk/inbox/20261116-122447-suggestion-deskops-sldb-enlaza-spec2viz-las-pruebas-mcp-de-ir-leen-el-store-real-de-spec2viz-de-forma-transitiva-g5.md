---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T12:24:47'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# deskops/.sldb enlaza spec2viz: las pruebas MCP de IR leen el store real de spec2viz de forma transitiva (G5)

_Describe the incoming message with enough evidence to triage._

IR, tarea task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a. El tester deskops-t-79b9a3c32e0f midió con strace (IR/runs/subagents/deskops-t-79b9a3c32e0f/result-summary.md, verificación 4a) lo siguiente. IR ya no enlaza ../spec2viz/.sldb, pero sigue federando el store real de deskops. deskops/.sldb/core/store_index.yaml enlaza spec2viz -> ../spec2viz/.sldb, así que la sesión 'sldb mcp' de las pruebas abre unos 1233 archivos del store real de spec2viz, solo en lectura y sin escribir. Pedido: decidir si deskops quita ese enlace, ahora o como parte del archivo de spec2viz (G5, opción A de JP). Hasta entonces, el Done When de esa tarea de IR no se cumple. Un aparte: la prueba de IR test_reading_through_every_tool_leaves_every_store_untouched digiere el store real de deskops, así que cualquier closeout concurrente en deskops la tumba. Pasó con 4b4ebaa1, a las 12:13:45.
