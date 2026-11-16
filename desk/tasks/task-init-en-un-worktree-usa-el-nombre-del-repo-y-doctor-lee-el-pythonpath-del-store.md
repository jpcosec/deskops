---
sldb:
  by: agent
  at: '2026-11-16T06:07:00Z'
  authority: generated
  via: save_document_payload
id: task-init-en-un-worktree-usa-el-nombre-del-repo-y-doctor-lee-el-pythonpath-del-store
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-193759-unclear-init-en-un-worktree-y-modelos-locales-fuera-del-path.md
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# init en un worktree usa el nombre del repo y doctor lee el pythonpath del store

## Rationale

_Explain why this task exists or the business driver behind it._

Origen: nota de MEPU del 15-11 (no llego al inbox de deskops porque --to deskops no resolvia; transcrita en velocidad-hooks-brief.md, Parte D). deskops init dentro de un worktree toma el nombre de la carpeta del worktree como identidad, y doctor no usa el pythonpath declarado en el store, asi que no encuentra los modelos del proyecto.

## Goal

_Describe the concrete result this task must produce._

deskops init en un worktree de git deriva project_identity del repo principal (git common dir o remoto), no de la carpeta; deskops doctor usa el pythonpath que declara el store.

## Scope

_State what is in scope and what is out of scope._

deskops/workspace.py (init), deskops doctor; el pythonpath se lee por la API de sldb, sin parsear store.yaml a mano.

## Implementation Path

_Outline the expected implementation route or affected surface._



## Validation

_List the checks required before this task can close._

- test nuevo de deskops (nombre a fijar al promover) con git worktree add real

## Done When

_Name the observable condition that makes the task complete._

test con git worktree add real: init da el nombre del repo; doctor carga modelos del pythonpath del store.
