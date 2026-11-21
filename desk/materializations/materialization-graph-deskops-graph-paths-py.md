---
sldb:
  by: agent
  at: '2026-11-21T21:55:37Z'
  authority: generated
  via: create_document
id: materialization-graph-deskops-graph-paths-py
title: graph deskops-graph-paths-py
source_atoms:
- atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
target_kind: code
target_identity: deskops/graph/paths.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_snapshot.py
  tests/test_graph_self_reflection.py tests/test_gitignore_policy.py tests/test_graph_cli.py
tags:
- system:deskops
- topic:graph
---

# graph deskops-graph-paths-py

## Intent

materializa en deskops/graph/paths.py el atom atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
