---
sldb:
  by: agent
  at: '2026-11-20T00:53:05Z'
  authority: generated
  via: create_document
id: materialization-dispatch-paralelo-docs-operator-manual-md
title: dispatch paralelo docs-operator-manual-md
source_atoms:
- atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente
target_kind: docs
target_identity: docs/operator-manual.md
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch paralelo docs-operator-manual-md

## Intent

materializa en docs/operator-manual.md el atom atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente
