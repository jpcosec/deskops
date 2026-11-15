---
sldb:
  by: agent
  at: '2026-11-15T15:28:52Z'
  authority: generated
  via: save_document_payload
# board-xxx
id: board-001
# Affected workspace or domain
scope: desk
# List of task-xxx paths
tasks:
- desk/tasks/task-doctor-detecta-rutas-absolutas-en-el-desk-y-repair-las-reescribe-como-direcciones-resolubles-por-los.md
# List of pill-xxx paths
pills:
- pill-001-task-closure-commit
- pill-005-subagent-execution
- pill-007-phase-gated-task-flow
- pill-durable-pill-knowledge-graduates-to-atoms-at-closeout
- pill-phase-closeout-reconciles-pills-and-surfaces-next-work
- pill-ready-phases-prove-dependencies-and-non-overlap
- pill-board-routed-pills-stay-minimal-and-reusable
# List of ritual-xxx paths
rituals:
- ritual-phase
- ritual-execution
- ritual-closeout
- ritual-testing
- context-review
# e.g., system:sldb, workspace:desk
tags:
- system:sldb
- workspace:desk
- topic:routing
---

# Desk Board

## Purpose

_Explain what this board routes and why it exists._

Route the active execution set for deskops.

## Notes

_Add short operational notes about the current routed set._

No active tasks routed.

## Task Details

_Generated from the task references above._

- doctor detecta rutas absolutas en el desk y --repair las reescribe como direcciones resolubles por los links de sldb [draft] - deskops doctor emite una alerta por cada ruta absoluta en un documento del desk (path del registro, files y references de tareas, y cualquier campo de frontmatter). doctor --repair reescribe las que puede resolver: el path del registro como ruta relativa a la raíz del ecosistema y files/references como <repo-id>:<ruta-relativa>, la forma que closeout resolved-by ya acepta.
