---
sldb:
  by: agent
  at: '2026-11-21T21:56:19Z'
  authority: generated
  via: create_document
id: materialization-graph-tests-test-graph-self-reflection-py
title: graph tests-test_graph_self_reflection-py
source_atoms:
- atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
target_kind: test
target_identity: tests/test_graph_self_reflection.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_snapshot.py
  tests/test_graph_self_reflection.py tests/test_gitignore_policy.py tests/test_graph_cli.py
tags:
- system:deskops
- topic:graph
---

# graph tests-test_graph_self_reflection-py

## Intent

materializa en tests/test_graph_self_reflection.py el atom atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
