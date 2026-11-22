---
sldb:
  by: agent
  at: '2026-11-22T19:53:36Z'
  authority: generated
  via: create_document
id: materialization-graph-deskops-cli-commands-graph-py
title: graph deskops-cli-commands-graph-py
source_atoms:
- atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
target_kind: code
target_identity: deskops/cli/commands/graph.py
validation:
- 'TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_graph_checks.py
  tests/test_graph_cli.py '
tags:
- system:deskops
- topic:graph
---

# graph deskops-cli-commands-graph-py

## Intent

materializa en deskops/cli/commands/graph.py el atom atom-graph-missing-separa-los-archivos-que-una-tarea-abierta-va-a-crear-de-las-referencias-rotas
