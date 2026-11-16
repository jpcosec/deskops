---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-16T08:36:18'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# referrers y rewrite_references aceptan graph, excluded_sources y no duplican menciones del frontmatter (H-a..H-c de CC35c)

_Describe the incoming message with enough evidence to triage._

En sldb main, commits 3772a1fa y 3c2186de, por integrar: referrers(store, target, *, graph=g) y rewrite_references(..., graph=g, excluded_sources=[...]) aceptan un ProjectGraph armado en proceso (H-a); excluded_sources, con rutas o Model:name, deja esas fuentes byte a byte (H-b); y find_hits ya no devuelve como mención una línea del frontmatter que es hit schema del mismo documento (H-c). deskops puede borrar _rewrite_mentions y _in_frontmatter de deskops/services/references.py y llamar a la API pública.
