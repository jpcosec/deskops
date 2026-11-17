---
sldb:
  by: agent
  at: '2026-11-17T11:17:15Z'
  authority: generated
  via: create_document
id: materialization-tests-de-aristas-declaradas-del-grafo
title: Tests de aristas declaradas del grafo
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: test
target_identity: tests/test_graph_declared_edges.py
validation:
- pytest -q tests/test_graph_declared_edges.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md
---

# Tests de aristas declaradas del grafo

## Intent

verifica project_graph declarado como datos, con closed: para issues cerrados
