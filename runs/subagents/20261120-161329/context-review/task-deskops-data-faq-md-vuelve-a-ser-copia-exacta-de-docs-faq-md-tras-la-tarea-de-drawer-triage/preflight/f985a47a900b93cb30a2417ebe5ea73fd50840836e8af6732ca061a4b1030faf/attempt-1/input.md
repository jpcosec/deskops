FILE:desk/tasks/task-deskops-data-faq-md-vuelve-a-ser-copia-exacta-de-docs-faq-md-tras-la-tarea-de-drawer-triage.md
---
sldb:
  by: agent
  at: '2026-11-20T16:13:23Z'
  authority: generated
  via: create_document
id: task-deskops-data-faq-md-vuelve-a-ser-copia-exacta-de-docs-faq-md-tras-la-tarea-de-drawer-triage
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.docs
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# deskops/data/faq.md vuelve a ser copia exacta de docs/faq.md tras la tarea de drawer-triage

## Rationale

_Explain why this task exists or the business driver behind it._

2026-11-20: integrate de la tarea drawer-triage (código 812f6115 y 2b5f68da, cerrada) falló en la suite de deskops: tests/test_packaging.py::test_packaged_faq_matches_the_human_copy y tests/test_large_doc_materialization.py::test_packaged_faq_is_a_projection_of_the_docs_faq. El intento 2 agregó una advertencia en docs/faq.md:53 pero no en su copia empaquetada deskops/data/faq.md, que tiene que ser idéntica byte a byte. No hay comando que la regenere.

## Goal

_Describe the concrete result this task must produce._

deskops/data/faq.md queda idéntica a docs/faq.md y los dos tests pasan. No cambia ningún otro archivo.

## Scope

_State what is in scope and what is out of scope._

Dentro: deskops/data/faq.md. Fuera: docs/faq.md (ya está bien) y cualquier otro archivo.

## Implementation Path

_Outline the expected implementation route or affected surface._

p1: copiar docs/faq.md sobre deskops/data/faq.md ('cp docs/faq.md deskops/data/faq.md') y verificar con 'cmp docs/faq.md deskops/data/faq.md'. p2: correr 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_packaging.py tests/test_large_doc_materialization.py'. p3: commit solo de deskops/data/faq.md con 'git commit -- deskops/data/faq.md' y el trailer 'Task-Id: <id de esta tarea>', y deskops advance.

## Validation

_List the checks required before this task can close._

- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_packaging.py tests/test_large_doc_materialization.py

## Done When

_Name the observable condition that makes the task complete._

cmp no muestra diferencias y los dos archivos de tests pasan.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-deskops-data-faq-md-vuelve-a-ser-copia-exacta-de-docs-faq-md-tras-la-tarea-de-drawer-triage: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

