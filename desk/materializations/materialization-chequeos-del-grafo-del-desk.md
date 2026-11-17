---
sldb:
  by: agent
  at: '2026-11-17T11:16:39Z'
  authority: generated
  via: create_document
id: materialization-chequeos-del-grafo-del-desk
title: Chequeos del grafo del desk
source_atoms:
- atom-declared-materialization-targets-are-graph-nodes
target_kind: code
target_identity: deskops/graph/checks.py
validation:
- pytest -q tests/test_graph_checks.py
tags:
- system:deskops
- topic:materialization
provenance: desk/atoms/atom-declared-materialization-targets-are-graph-nodes.md
---

# Chequeos del grafo del desk

## Intent

graph missing filtra los destinos que existen como archivo y no son declarables en project_graph (H1)
