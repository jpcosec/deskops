---
sldb:
  by: agent
  at: '2026-11-22T19:53:58Z'
  authority: generated
  via: create_document
id: materialization-graph-tests-test-graph-checks-py
title: graph tests-test_graph_checks-py
source_atoms:
- atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
target_kind: test
target_identity: tests/test_graph_checks.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_checks.py
  tests/test_graph_cli.py '
tags:
- system:deskops
- topic:graph
---

# graph tests-test_graph_checks-py

## Intent

materializa en tests/test_graph_checks.py el atom atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
