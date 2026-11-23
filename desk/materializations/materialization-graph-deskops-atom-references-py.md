---
sldb:
  by: agent
  at: '2026-11-23T11:32:51Z'
  authority: generated
  via: create_document
id: materialization-graph-deskops-atom-references-py
title: graph deskops-atom_references-py
source_atoms:
- atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
target_kind: code
target_identity: deskops/atom_references.py
validation:
- 'grep LEGACY_FIELDS|scaffold_desk|ensure_lifecycle_graph vacio y pytest -n 4 tests/test_atom_reference_convention.py
  tests/test_graph_*.py tests/test_desk_graph_runs_target.py tests/test_lifecycle_*.py:
  129 passed en worktree limpio de 5fff4cda'
tags:
- system:deskops
- topic:graph
---

# graph deskops-atom_references-py

## Intent

materializa en deskops/atom_references.py el atom atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
