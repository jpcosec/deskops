---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: mepu
# e.g., target_repo
target_project: deskops
# ISO 8601 timestamp
created_at: '2026-11-15T19:37:59'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# init en un worktree y modelos locales fuera del path

_Describe the incoming message with enough evidence to triage._

Dos tropiezos al correr deskops init en un worktree de git (2026-11-15, repo mepu): 1) project_identity y los títulos del Board, los rituales, drawer/README y contexts/pills toman el nombre de la carpeta del worktree (wt-mepu-ontologia) en vez del nombre del repo (mepu); hubo que corregirlo con sldb docs replace archivo por archivo. 2) deskops doctor da el desk por roto ('the model's class cannot be imported here') cuando el store tiene modelos propios en src/ y no se exporta PYTHONPATH=src; doctor no tiene --pythonpath ni lee uno del store.
