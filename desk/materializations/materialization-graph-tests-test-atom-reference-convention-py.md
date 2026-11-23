---
sldb:
  by: agent
  at: '2026-11-23T11:33:46Z'
  authority: generated
  via: create_document
id: materialization-graph-tests-test-atom-reference-convention-py
title: graph tests-test_atom_reference_convention-py
source_atoms:
- atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
target_kind: test
target_identity: tests/test_atom_reference_convention.py
validation:
- 'grep LEGACY_FIELDS|scaffold_desk|ensure_lifecycle_graph vacio y pytest -n 4 tests/test_atom_reference_convention.py
  tests/test_graph_*.py tests/test_desk_graph_runs_target.py tests/test_lifecycle_*.py:
  129 passed en worktree limpio de 5fff4cda'
tags:
- system:deskops
- topic:graph
---

# graph tests-test_atom_reference_convention-py

## Intent

materializa en tests/test_atom_reference_convention.py el atom atom-se-borra-el-detector-legacy-de-related-atoms-y-los-alias-scaffold-desk-y-ensure-lifecycle-graph
