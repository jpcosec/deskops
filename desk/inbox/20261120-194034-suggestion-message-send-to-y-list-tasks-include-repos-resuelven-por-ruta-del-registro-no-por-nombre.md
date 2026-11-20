---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-20T19:40:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# message send --to y list tasks --include-repos resuelven por ruta del registro, no por nombre

_Describe the incoming message with enough evidence to triage._

Al despachar desde Governance: --to y --include-repos ubican el repo destino por el campo path de la ficha en desk/registry, que es una ruta relativa propia de cada máquina. Una ficha sin path (repo-votaciones) hace fallar list tasks --include-repos con «Missing required field: 'path'». JP (20-11): la identidad de un store es su nombre y es igual en todas las máquinas; la ruta es de cada una. sldb ya resuelve los enlaces por nombre contra el catálogo de la máquina (jpcosec/sldb#3, sldb.store.link_path.resolve_link). Pedido: que el registro de deskops resuelva igual, y que una ficha sin ruta se salte con aviso en vez de botar la consulta. Estos mensajes se entregaron con --desk-root a un worktree por ese motivo.
