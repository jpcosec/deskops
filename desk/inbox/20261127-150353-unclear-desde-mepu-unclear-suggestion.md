---
sldb:
  by: agent
  at: '2026-11-27T18:06:20Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-27T15:03:53'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Desde mepu: piloto UI-122 (6) context_file exige clonar deskops y sldb; el closeout solo acepta tests .py (no vitest)

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (triage del 27-11; nota original desk/inbox/20261124-220606-unclear-para-deskops-piloto-ui-122-en-johanes-6-el-context-file-exige-sourc.md en heyantonia/mepu). # PARA DESKOPS (piloto UI-122 en johanes): (6) El context_file exige sourc


PARA DESKOPS (piloto UI-122 en johanes): (6) El context_file exige source_root (deskops) y sldb_root dentro de workspace_root; para un repo de producto (MEPU) obliga a clonar deskops y sldb dentro del checkout (quedaron en .worktrees/deskops-src y .worktrees/sldb-src). (7) La imagen ghcr.io/jpruizantonia/scion-claude:latest de johanes no trae uv ni pip ni pydantic: el paso 'Python environment' del agents.md (uv venv /tmp/ws-venv) no corre y el ejecutor no puede usar deskops (advance task) dentro del contenedor. (8) closeout: la evidencia tests solo acepta .py bajo tests/; una tarea de UI probada con vitest (*.test.tsx) tiene que citar un test de Python ajeno. (9) El bundle pi de scion solo configura DeepSeek (sin saldo) y johanes no tiene harness-config pi ni imagen scion-pi: el tester pi no es posible hoy; en johanes el tester quedó con harness claude.
