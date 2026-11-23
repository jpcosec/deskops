---
sldb:
  by: agent
  at: '2026-11-23T11:33:19Z'
  authority: generated
  via: create_document
id: materialization-graph-deskops-lifecycle-py
title: graph deskops-lifecycle-py
source_atoms:
- atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
target_kind: code
target_identity: deskops/lifecycle.py
validation:
- 'grep LEGACY_FIELDS|scaffold_desk|ensure_lifecycle_graph vacio y pytest -n 4 tests/test_atom_reference_convention.py
  tests/test_graph_*.py tests/test_desk_graph_runs_target.py tests/test_lifecycle_*.py:
  129 passed en worktree limpio de 5fff4cda'
tags:
- system:deskops
- topic:graph
---

# graph deskops-lifecycle-py

## Intent

materializa en deskops/lifecycle.py el atom atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
