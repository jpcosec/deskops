---
sldb:
  by: agent
  at: '2026-11-20T00:53:13Z'
  authority: generated
  via: create_document
id: materialization-dispatch-paralelo-tests-test-dispatch-py
title: dispatch paralelo tests-test_dispatch-py
source_atoms:
- atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente
target_kind: test
target_identity: tests/test_dispatch.py
validation:
- TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/test_dispatch.py
tags:
- system:deskops
- topic:dispatch
---

# dispatch paralelo tests-test_dispatch-py

## Intent

materializa en tests/test_dispatch.py el atom atom-dispatch-start-solo-se-frena-por-la-memoria-de-la-maquina-o-porque-la-tarea-ya-tiene-agente
