---
sldb:
  by: agent
  at: '2026-11-21T21:56:08Z'
  authority: generated
  via: create_document
id: materialization-graph-tests-fixtures-golden-self-reflection-findings-json
title: graph tests-fixtures-golden-self_reflection_findings-json
source_atoms:
- atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
target_kind: test
target_identity: tests/fixtures/golden/self_reflection_findings.json
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_snapshot.py
  tests/test_graph_self_reflection.py tests/test_gitignore_policy.py tests/test_graph_cli.py
tags:
- system:deskops
- topic:graph
---

# graph tests-fixtures-golden-self_reflection_findings-json

## Intent

materializa en tests/fixtures/golden/self_reflection_findings.json el atom atom-graph-export-y-self-reflection-escriben-su-salida-derivada-en-sldb-cache
