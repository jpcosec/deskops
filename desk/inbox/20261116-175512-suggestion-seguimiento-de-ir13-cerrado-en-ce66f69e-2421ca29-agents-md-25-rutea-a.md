---
sldb:
  by: agent
  at: '2026-11-17T01:27:30Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T17:55:12'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: deskops
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:27:22'
---

# Seguimiento de IR13 (cerrado en ce66f69e/2421ca29): AGENTS.md:25 rutea a

_Describe the incoming message with enough evidence to triage._

Seguimiento de IR13 (cerrado en ce66f69e/2421ca29): AGENTS.md:25 rutea a la skill use-spec2viz y README.md:54 cita references/spec2viz-cli.md; quedaron fuera de files de la tarea. Pasarlos a use-specir (skill del repo IR). Además la carpeta .opencode/skills/use-spec2viz tiene name: use-specir en el frontmatter (lo exige specir retirement check) y opencode pide que name coincida con la carpeta: renombrar la carpeta a use-specir. Y el comando de Validation de la tarea (specir retirement check --path deskops=...) sale rc 2: hay que pasar todas las rutas del inventario.
