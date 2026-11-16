---
sldb:
  by: agent
  at: '2026-11-16T20:39:55Z'
  authority: generated
  via: create_document
id: materialization-tests-de-la-migracion-de-estados-y-claves-legacy-de-taskdoc
title: Tests de la migracion de estados y claves legacy de TaskDoc
source_atoms:
- atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc
target_kind: test
target_identity: tests/test_legacy_task_states.py
validation:
- pytest -q tests/test_legacy_task_states.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-la-consistencia-del-ciclo-de-vida-de-una-tarea-es-un-validador-de-taskdoc.md
---

# Tests de la migracion de estados y claves legacy de TaskDoc

## Intent

verifica que desk update migra estados legacy y quita las claves legacy checklists y routine del frontmatter de las tareas, en desks sandbox
