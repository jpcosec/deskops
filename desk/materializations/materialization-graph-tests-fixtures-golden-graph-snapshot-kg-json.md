---
sldb:
  by: agent
  at: '2026-11-21T21:55:58Z'
  authority: generated
  via: create_document
id: materialization-graph-tests-fixtures-golden-graph-snapshot-kg-json
title: graph tests-fixtures-golden-graph_snapshot-kg-json
source_atoms:
- atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
target_kind: test
target_identity: tests/fixtures/golden/graph_snapshot.kg.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_snapshot.py
  tests/test_graph_self_reflection.py tests/test_gitignore_policy.py tests/test_graph_cli.py
tags:
- system:deskops
- topic:graph
---

# graph tests-fixtures-golden-graph_snapshot-kg-json

## Intent

materializa en tests/fixtures/golden/graph_snapshot.kg.json el atom atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
