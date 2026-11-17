---
sldb:
  by: agent
  at: '2026-11-17T11:16:51Z'
  authority: generated
  via: create_document
id: materialization-tests-de-los-chequeos-del-grafo
title: Tests de los chequeos del grafo
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: test
target_identity: tests/test_graph_checks.py
validation:
- pytest -q tests/test_graph_checks.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md
---

# Tests de los chequeos del grafo

## Intent

verifica los casos de H1 no declarables y que un archivo inexistente se reporta
