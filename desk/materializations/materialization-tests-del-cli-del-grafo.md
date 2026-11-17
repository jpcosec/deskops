---
sldb:
  by: agent
  at: '2026-11-17T11:17:04Z'
  authority: generated
  via: create_document
id: materialization-tests-del-cli-del-grafo
title: Tests del CLI del grafo
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: test
target_identity: tests/test_graph_cli.py
validation:
- pytest -q tests/test_graph_cli.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md
---

# Tests del CLI del grafo

## Intent

verifica deskops graph missing, incluido un issue cerrado como registro
