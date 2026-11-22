---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: repo-governance
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-22T18:28:10'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# Orden pedido por el concilio (clones primero) y rutas de máquina en desk/config.json

_Describe the incoming message with enough evidence to triage._

Dos cosas del concilio del 22-11 (acta en heyantonia/Governance, docs/diagnostico-vsm-2026-11-19/concilio/acta-2026-11-22-gobierno-por-desks.md). (1) Orden: los tres agentes pusieron primero la puesta al día automática de los clones base y del store en la máquina coordinadora; eso ya es la tarea task-governance-puesta-al-dia-de-los-clones-base-de-la-maquina-coordinadora-y-doctor-que-valida-cada-tare de este desk, en borrador. Governance pide que vaya antes que las otras task-governance-*. Decisión del concilio (falta el recibo de JP): robocop 1 guarda el estado (clones, catálogo, timer) y es de solo lectura; los agentes y el despacho corren en robocop 2. Hoy los clones de robocop 1 se ponen al día a mano. (2) desk/config.json de deskops y sldb guarda en la sección dispatch e integrate rutas de una máquina (/mnt/ssd/…, /home/robocop/.scion/…) y un credential.helper con una cuenta de persona. Para llevar dispatch a otros desks hace falta saber dónde va lo que es de cada máquina sin versionarlo en el repo. Un agente del concilio dijo que desk/config.local.json ya tiene precedencia; no lo comprobé. Pregunta: ¿existe ese mecanismo y cubre dispatch e integrate?
