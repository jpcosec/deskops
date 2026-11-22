---
sldb:
  by: agent
  at: '2026-11-22T19:53:47Z'
  authority: generated
  via: create_document
id: materialization-graph-deskops-graph-checks-py
title: graph deskops-graph-checks-py
source_atoms:
- atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
target_kind: code
target_identity: deskops/graph/checks.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_checks.py
  tests/test_graph_cli.py '
tags:
- system:deskops
- topic:graph
---

# graph deskops-graph-checks-py

## Intent

materializa en deskops/graph/checks.py el atom atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
